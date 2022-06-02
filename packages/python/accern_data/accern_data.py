import io
import os
import time
import traceback
import warnings
from collections import deque
from copy import deepcopy
from typing import (
    Any,
    Callable,
    Deque,
    Dict,
    Generic,
    get_args,
    Iterator,
    List,
    Literal,
    Optional,
    Set,
    Tuple,
    TypedDict,
    TypeVar,
    Union,
)

import pandas as pd
import requests

from .util import (
    BarIndicator,
    field_transformation,
    generate_file_response,
    get_overall_total_from_dummy,
    is_example_url,
    MessageIndicator,
    ProgressIndicator,
    SilentIndicator,
    write_json,
)

ExcludedFilterField = Literal[
    "crawled_at",
    "date",
    "format",
    "harvested_at",
    "published_at",
    "size",
    "token",
]

FilterField = Literal[
    "doc_cluster_id",
    "doc_id",
    "doc_source",
    "doc_title",
    "doc_type",
    "doc_url",
    "entity_accern_id",
    "entity_country",
    "entity_exchcode",
    "entity_figi",
    "entity_hits",
    "entity_indices",
    "entity_name",
    "entity_region",
    "entity_relevance",
    "entity_sector",
    "entity_share_class",
    "entity_text",
    "entity_ticker",
    "entity_type",
    "event",
    "event_accern_id",
    "event_group",
    "event_hits",
    "event_text",
    "primary_signal",
    "provider_id",
    "signal_id",
    "signal_tag",
]
FiltersType = TypedDict(
    "FiltersType",
    {
        "doc_cluster_id": Optional[str],
        "doc_id": Optional[str],
        "doc_source": Optional[str],
        "doc_title": Optional[str],
        "doc_type": Optional[str],
        "doc_url": Optional[str],
        "entity_accern_id": Optional[str],
        "entity_country": Optional[str],
        "entity_exchcode": Optional[str],
        "entity_figi": Optional[str],
        "entity_hits": Optional[str],
        "entity_indices": Optional[str],
        "entity_name": Optional[str],
        "entity_region": Optional[str],
        "entity_relevance": Optional[int],
        "entity_sector": Optional[str],
        "entity_share_class": Optional[str],
        "entity_text": Optional[str],
        "entity_ticker": Optional[str],
        "entity_type": Optional[str],
        "event": Optional[str],
        "event_accern_id": Optional[int],
        "event_group": Optional[str],
        "event_hits": Optional[str],
        "event_text": Optional[str],
        "primary_signal": Optional[Union[str, bool]],
        "provider_id": Optional[int],
        "signal_id": Optional[str],
        "signal_tag": Optional[str],
    },
    total=False)

ModeType = Literal["csv", "df", "json"]
Indicators = Literal["pbar", "silent", "message"]
INDICATORS = get_args(Indicators)
FILTER_FIELD = get_args(FilterField)
EXCLUDED_FILTER_FIELD = get_args(ExcludedFilterField)
ALL_MODES: Set[ModeType] = {"csv", "df", "json"}
DT_FORMAT = r"%Y-%m-%dT%H:%M:%S.%fZ"

T = TypeVar('T')


class Mode(Generic[T]):
    def __init__(self) -> None:
        self._cur_date: Optional[str] = None
        self._cur_path: Optional[str] = None
        self._cur_pattern: Optional[str] = None

    def get_format(self) -> str:
        raise NotImplementedError()

    def split_dates(self) -> bool:
        raise NotImplementedError

    def clean_buffer(self) -> None:
        raise NotImplementedError

    def get_buffer(self) -> Optional[T]:
        raise NotImplementedError

    def get_instance(self) -> 'Mode':
        return deepcopy(self)

    def parse_result(self, resp: requests.Response) -> List[T]:
        raise NotImplementedError()

    def size(self, batch: List[T]) -> int:
        raise NotImplementedError()

    def max_date(self, batch: List[T]) -> str:
        raise NotImplementedError()

    def init_day(
            self,
            cur_date: str,
            path: str,
            pattern: Optional[str],
            indicator: ProgressIndicator) -> None:
        self._cur_date = cur_date
        self._cur_path = path
        self._cur_pattern = pattern
        self.do_init(indicator)

    def do_init(self, indicator: ProgressIndicator) -> None:
        raise NotImplementedError()

    def add_result(self, signal: T) -> None:
        raise NotImplementedError()

    def finish_day(self, indicator: ProgressIndicator) -> None:
        raise NotImplementedError()

    def iterate_data(
            self,
            data: Optional[List[T]],
            indicator: ProgressIndicator) -> Iterator[T]:
        raise NotImplementedError()

    def split(self, batch: List[T], value: pd.Timestamp) -> List[T]:
        raise NotImplementedError()

    def get_path(self, is_by_day: bool) -> str:
        # NOTE: pattern can be None or "" only for csv_date & json.
        # In case of None, filenames would be <date>.csv or <date>.json.
        # In case of empty string (""), filenames would be -<date>.csv or
        # -<date>.json.
        day_str = f"{self._cur_date}" if is_by_day else None
        assert self._cur_path is not None
        pattern = self._cur_pattern
        if pattern is None:
            pattern = ""
        assert pattern.strip() or day_str is not None, \
            "csv mode with split_dates=False should have an output pattern."
        if self._cur_pattern is None:
            fname = f"{day_str}.{self.get_format()}"
        elif day_str is None:
            fname = f"{self._cur_pattern}.{self.get_format()}"
        else:
            fname = f"{self._cur_pattern}-{day_str}.{self.get_format()}"
        return os.path.join(self._cur_path, fname)


class CSVMode(Mode[pd.DataFrame]):
    def __init__(
            self, is_by_day: bool, chunk_size: Optional[int] = None) -> None:
        super().__init__()
        self._cols = None
        self._is_by_day = is_by_day
        self._chunk_size = chunk_size
        self._buffer: List[pd.DataFrame] = []
        self._buffer_size = 0

    def get_format(self) -> str:
        return "csv"

    def split_dates(self) -> bool:
        return self._is_by_day

    def clean_buffer(self) -> None:
        self._buffer = []
        self._buffer_size = 0

    def get_buffer(self) -> Optional[pd.DataFrame]:
        if len(self._buffer) > 0:
            buffer = pd.concat(self._buffer)
            if not buffer.empty:
                return buffer
        return None

    def parse_result(self, resp: requests.Response) -> List[pd.DataFrame]:
        res = pd.read_csv(io.StringIO(resp.text))
        if res.empty:
            return []
        if "harvested_at" not in res:
            return []
        res["harvested_at"] = pd.to_datetime(res["harvested_at"])
        if "published_at" in res:
            res["published_at"] = pd.to_datetime(res["published_at"])
        if "crawled_at" in res:
            res["crawled_at"] = pd.to_datetime(res["crawled_at"])
        return [res]

    def size(self, batch: List[pd.DataFrame]) -> int:
        return sum(cur.shape[0] for cur in batch)

    def max_date(self, batch: List[pd.DataFrame]) -> str:
        temp = set()
        for cur in batch:
            harvested_at_list = cur["harvested_at"].to_list()
            for harvested_at in harvested_at_list:
                assert isinstance(harvested_at, pd.Timestamp)
                temp.add(harvested_at)
        dates: List[pd.Timestamp] = sorted(temp)
        if len(dates) <= 1:
            return dates[0].strftime(DT_FORMAT)
        # Second last date.
        return max(dates[:-1]).strftime(DT_FORMAT)

    def do_init(self, indicator: ProgressIndicator) -> None:
        fname = self.get_path(self._is_by_day)
        indicator.log(f"current file is {fname}")

    def add_result(self, signal: pd.DataFrame) -> None:
        fname = self.get_path(is_by_day=self._is_by_day)
        if self._cols is None:
            signal.to_csv(fname, index=False, header=True, mode="w")
            self._cols = signal.columns
        else:
            signal[self._cols].to_csv(
                fname, index=False, header=False, mode="a")

    def finish_day(self, indicator: ProgressIndicator) -> None:
        # csv files are saved by add_result
        if self._is_by_day:
            self._cols = None

    def split(
            self,
            batch: List[pd.DataFrame],
            value: pd.Timestamp) -> List[pd.DataFrame]:
        df = batch[0]
        return [df[df["harvested_at"] <= value]]

    def iterate_data(
            self,
            data: Optional[List[pd.DataFrame]],
            indicator: ProgressIndicator) -> Iterator[pd.DataFrame]:
        assert self._chunk_size is None or self._chunk_size > 0
        if self._chunk_size is None:
            if data is not None:
                df = data[0]
                indicator.update(df.shape[0])
                if not df.empty:
                    yield df
        else:
            if data is not None:
                self._buffer.append(data[0])
                self._buffer_size += data[0].shape[0]
            while self._buffer_size >= self._chunk_size:
                res_df = pd.concat(self._buffer)
                result: pd.DataFrame = res_df.iloc[:self._chunk_size]
                remainder: pd.DataFrame = res_df.iloc[self._chunk_size:]
                if remainder.empty:
                    self._buffer = []
                else:
                    self._buffer = [remainder]
                self._buffer_size = remainder.shape[0]
                indicator.update(result.shape[0])
                yield result.reset_index(drop=True)

            if self.split_dates() and data is None:
                if len(self._buffer) > 0:
                    buffer = pd.concat(self._buffer)
                    if not buffer.empty:
                        indicator.update(buffer.shape[0])
                        yield buffer.reset_index(drop=True)
                self._buffer = []
                self._buffer_size = 0


class JSONMode(Mode[Dict[str, Any]]):
    def __init__(self, debug_json: bool = False) -> None:
        super().__init__()
        self._res: List[Dict[str, Any]] = []
        self._debug_json = debug_json
        self._debug_ix = 0

    def get_format(self) -> str:
        return "json"

    def split_dates(self) -> bool:
        return True

    def clean_buffer(self) -> None:
        # json mode has no buffer
        pass

    def get_buffer(self) -> Optional[Dict[str, Any]]:
        return None

    def parse_result(self, resp: requests.Response) -> List[Dict[str, Any]]:
        res_json = resp.json()
        if self._debug_json:
            with open(f"tmp{self._debug_ix}.json", "w") as out:
                print(resp.text, file=out)
                self._debug_ix += 1

        def parse_dates(obj: Dict[str, Any]) -> Dict[str, Any]:
            obj["harvested_at"] = pd.to_datetime(obj["harvested_at"])
            if "published_at" in obj:
                obj["published_at"] = pd.to_datetime(obj["published_at"])
            if "crawled_at" in obj:
                obj["crawled_at"] = pd.to_datetime(obj["crawled_at"])
            return obj

        return [
            parse_dates(signal)
            for signal in res_json["signals"]
        ]

    def size(self, batch: List[Dict[str, Any]]) -> int:
        return len(batch)

    def max_date(self, batch: List[Dict[str, Any]]) -> str:
        temp = set()
        for cur in batch:
            harvested_at = cur["harvested_at"]
            assert isinstance(harvested_at, pd.Timestamp)
            temp.add(harvested_at)
        dates: List[pd.Timestamp] = sorted(temp)
        if len(dates) <= 1:
            return dates[0].strftime(DT_FORMAT)
        return max(dates[:-1]).strftime(DT_FORMAT)

    def do_init(self, indicator: ProgressIndicator) -> None:
        self._res = []

    def add_result(self, signal: Dict[str, Any]) -> None:
        self._res.append(signal)

    def finish_day(self, indicator: ProgressIndicator) -> None:
        fname = self.get_path(is_by_day=True)
        indicator.log(f"writing results to {fname}")

        def stringify_dates(obj: Dict[str, Any]) -> Dict[str, Any]:
            if "harvested_at" in obj:
                obj["harvested_at"] = obj["harvested_at"].strftime(DT_FORMAT)
            if "published_at" in obj:
                obj["published_at"] = obj["published_at"].strftime(DT_FORMAT)
            if "crawled_at" in obj:
                obj["crawled_at"] = obj["crawled_at"].strftime(DT_FORMAT)
            return obj

        obj = [stringify_dates(cur) for cur in self._res]
        write_json(obj, fname, sort_keys=True)

    def split(
            self,
            batch: List[Dict[str, Any]],
            value: pd.Timestamp) -> List[Dict[str, Any]]:
        result = []
        for record in batch:
            if record["harvested_at"] <= value:
                result.append(record)
        return result

    def iterate_data(
            self,
            data: Optional[List[Dict[str, Any]]],
            indicator: ProgressIndicator) -> Iterator[Dict[str, Any]]:
        if data is not None:
            for rec in data:
                indicator.update(1)
                yield rec


class DataClient:
    def __init__(
            self,
            url: str,
            token: str,
            n_errors: int = 5,
            indicator: Optional[Union[Indicators, ProgressIndicator]] = None,
            ) -> None:
        self._base_url = url
        self._token = token
        self._filters: Dict[str, str] = {}
        self._params: Dict[str, str] = {}
        self._mode: Optional[Mode] = None
        if indicator is not None:
            self.set_indicator(indicator)
        else:
            self._indicator_obj = self._parse_indicator("pbar")
        self._error_list: Deque[str] = deque(maxlen=n_errors)

    def reset_error_list(self) -> None:
        self._error_list.clear()

    @staticmethod
    def _validate_filters(
            filters: FiltersType) -> Dict[
                str, Optional[Union[bool, int, str]]]:
        valid_filters: Dict[str, Optional[Union[bool, int, str]]] = {}
        for key, value in filters.items():
            if key not in FILTER_FIELD:
                raise ValueError(
                    f"{key} is not a valid field."
                    f"Possible fields: {FILTER_FIELD}")
            assert isinstance(value, (bool, int, str)) or value is None
            valid_filters[key] = value
        return valid_filters

    @staticmethod
    def _parse_filters(
            filters: Dict[str, Optional[Union[bool, int, str]]]) -> Dict[
                str, str]:
        proper_filters: Dict[str, str] = {}
        for key, value in filters.items():
            assert key not in EXCLUDED_FILTER_FIELD, (
                "filters should not be containing any of "
                f"{EXCLUDED_FILTER_FIELD}")
            if value is not None:
                proper_filters[key] = field_transformation(value)
        return proper_filters

    def set_indicator(
            self, indicator: Union[Indicators, ProgressIndicator]) -> None:
        if isinstance(indicator, ProgressIndicator):
            self._indicator_obj = indicator
        else:
            self._indicator_obj = self._parse_indicator(indicator)

    @staticmethod
    def _parse_indicator(indicator: Indicators) -> ProgressIndicator:
        if indicator not in INDICATORS:
            raise ValueError(
                f"Indicator should be None or one of {INDICATORS}. "
                f"It cannot be '{indicator}'.")
        if indicator == "pbar":
            return BarIndicator()
        if indicator == "silent":
            return SilentIndicator()
        return MessageIndicator()

    def get_indicator(self) -> ProgressIndicator:
        if self._indicator_obj is None:
            raise ValueError("Set indicator first.")
        return self._indicator_obj

    def set_filters(self, filters: FiltersType) -> None:
        self._set_raw_filters(self._validate_filters(filters))

    def _set_raw_filters(
            self, filters: Dict[str, Optional[Union[bool, int, str]]]) -> None:
        self._filters = self._parse_filters(filters)

    def get_filters(self) -> Dict[str, str]:
        return self._filters

    @staticmethod
    def _parse_mode(
            mode: ModeType,
            split_dates: bool = True,
            chunk_size: Optional[int] = None) -> Mode:
        if mode == "json":
            if not split_dates:
                warnings.warn(
                    "In json mode, there is no difference between "
                    "split_dates=True or split_dates=False. Both will work "
                    "the same way.",
                    Warning,
                    stacklevel=2)
            if chunk_size is not None:
                warnings.warn(
                    "In json mode, the number of results are always one at "
                    "a time, i.e., one object at a time.",
                    Warning,
                    stacklevel=2)
            return JSONMode()
        if mode in {"csv", "df"}:
            return CSVMode(is_by_day=split_dates, chunk_size=chunk_size)
        raise ValueError(
            f"Please set proper mode. It is '{mode}' which is not in "
            f"{ALL_MODES}")

    def set_mode(
            self,
            mode: ModeType,
            split_dates: bool,
            chunk_size: Optional[int] = None) -> None:
        self._mode = self._parse_mode(mode, split_dates, chunk_size)

    def get_mode(self) -> Mode:
        assert self._mode is not None, "Set mode first."
        return self._mode.get_instance()

    def get_last_silenced_errors(self) -> List[str]:
        return list(self._error_list)

    def _read_total(
            self,
            cur_date: str,
            filters: Dict[str, str],
            indicator: ProgressIndicator) -> int:
        while True:
            try:
                if is_example_url(self._base_url):
                    resp = get_overall_total_from_dummy(
                        cur_date, filters)
                else:
                    resp = requests.get(
                        self._base_url,
                        params={
                            "token": self._token,
                            **filters,
                            "date": cur_date,
                            "format": "json",
                        })
                if not str(resp.text).strip():  # if nothing is fetched
                    return 0
                return int(resp.json()["overall_total"])
            except KeyboardInterrupt as err:
                raise err
            except (
                    AssertionError,
                    KeyError,
                    requests.exceptions.RequestException):  # NOTE: add more?
                self._error_list.append(traceback.format_exc())
                indicator.log("unknown error...retrying...")
                time.sleep(0.5)

    def _read_date(
            self,
            mode: Mode[T],
            filters: Dict[str, str],
            indicator: ProgressIndicator) -> List[T]:
        while True:
            try:
                if is_example_url(self._base_url):
                    date = self._params["date"]
                    harvested_after = self._params["harvested_after"]
                    resp = generate_file_response(
                        date,
                        harvested_after,
                        mode.get_format(),
                        filters=filters)
                else:
                    resp = requests.get(
                        self._base_url,
                        params={
                            "token": self._token,
                            **filters,
                            **self._params,
                            **{"format": mode.get_format()}
                        })
                if not str(resp.text).strip():
                    return []
                return mode.parse_result(resp)
            except KeyboardInterrupt as err:
                raise err
            except (
                    AssertionError,
                    KeyError,
                    requests.exceptions.RequestException):  # NOTE: add more?
                self._error_list.append(traceback.format_exc())
                indicator.log("unknown error...retrying...")
                time.sleep(0.5)

    def _scroll(
            self,
            start_date: str,
            mode: Mode[T],
            filters: Dict[str, str],
            indicator: ProgressIndicator) -> Iterator[List[T]]:
        self._params["harvested_after"] = start_date
        batch = self._read_date(mode, filters, indicator)
        prev_start = start_date
        while mode.size(batch) > 0:
            try:
                start_date = mode.max_date(batch)
                yield mode.split(batch, pd.to_datetime(start_date))
                self._params["harvested_after"] = start_date
                batch = self._read_date(mode, filters, indicator)
                if start_date == prev_start:
                    # NOTE: redundant check?
                    # batch_size becomes 0, loop gets terminated.
                    break
                prev_start = start_date
            except pd.errors.EmptyDataError:
                break

    def _get_valid_mode(
            self,
            mode: Optional[Union[
                Mode,
                ModeType,
                Tuple[ModeType, bool],
                Tuple[ModeType, bool, Optional[int]]
                ]],
            ) -> Mode:
        if mode is None:
            return self.get_mode()
        if isinstance(mode, Mode):
            return mode.get_instance()
        if isinstance(mode, str):
            return self._parse_mode(mode)
        return self._parse_mode(*mode)

    def _get_valid_filters(
            self, filters: Optional[FiltersType]) -> Dict[str, str]:
        if filters is None:
            return self.get_filters()
        return self._parse_filters(
            {**self.get_filters(), **self._validate_filters(filters)})

    def _get_valid_indicator(
            self, indicator: Optional[Union[Indicators, ProgressIndicator]],
            ) -> ProgressIndicator:
        if indicator is None:
            return self.get_indicator()
        if isinstance(indicator, ProgressIndicator):
            return indicator
        return self._parse_indicator(indicator)

    def download_range(
            self,
            start_date: str,
            output_path: Optional[str] = None,
            output_pattern: Optional[str] = None,
            end_date: Optional[str] = None,
            mode: Optional[Union[
                Mode[T],
                ModeType,
                Tuple[ModeType, bool],
                Tuple[ModeType, bool, Optional[int]]]
                ] = None,
            filters: Optional[FiltersType] = None,
            indicator: Optional[Union[Indicators, ProgressIndicator]] = None,
            ) -> None:
        opath = "." if output_path is None else output_path
        os.makedirs(opath, exist_ok=True)

        valid_mode: Optional[Mode] = None
        cur_date: Optional[pd.Timestamp] = None
        prev_date: Optional[pd.Timestamp] = None
        indicator_obj: Optional[ProgressIndicator] = None

        def set_active_mode(
                mode: Mode,
                date: pd.Timestamp,
                indicator: ProgressIndicator) -> None:
            nonlocal valid_mode, cur_date, indicator_obj
            valid_mode = mode
            cur_date = date
            indicator_obj = indicator

            if cur_date != prev_date:
                if prev_date is not None:
                    valid_mode.finish_day(indicator_obj)
                valid_mode.init_day(
                    cur_date.strftime(r"%Y-%m-%d"),
                    opath,
                    output_pattern,
                    indicator_obj)

        for res in self.iterate_range(
                start_date=start_date,
                end_date=end_date,
                mode=mode,
                filters=filters,
                indicator=indicator,
                set_active_mode=set_active_mode):
            assert valid_mode is not None
            valid_mode.add_result(res)
            prev_date = cur_date

        if prev_date is not None:
            assert valid_mode is not None
            assert indicator_obj is not None
            valid_mode.finish_day(indicator_obj)

    def iterate_range(
            self,
            start_date: str,
            end_date: Optional[str] = None,
            mode: Optional[Union[
                Mode[T],
                ModeType,
                Tuple[ModeType, bool],
                Tuple[ModeType, bool, Optional[int]]]
                ] = None,
            filters: Optional[FiltersType] = None,
            indicator: Optional[Union[Indicators, ProgressIndicator]] = None,
            set_active_mode: Optional[
                Callable[
                    [Mode[T], pd.Timestamp, ProgressIndicator], None]] = None,
            ) -> Iterator[T]:
        valid_mode = self._get_valid_mode(mode)
        valid_filters = self._get_valid_filters(filters)
        valid_mode.clean_buffer()
        if end_date is None:
            end_date = start_date
        indicator_obj = self._get_valid_indicator(indicator)
        indicator_obj.generate_bar(
            total=len(pd.date_range(start_date, end_date)))
        indicator_obj.set_description(desc="Fetching info")
        total = 0
        expected_records: List[int] = []
        for cur_date in pd.date_range(start_date, end_date):
            expected_records.append(
                self._read_total(
                    cur_date, valid_filters, indicator=indicator_obj))
            indicator_obj.update(1)
        total = sum(expected_records)
        indicator_obj.set_total(total=total)
        indicator_obj.set_description(desc="Downloading signals")
        for idx, cur_date in enumerate(pd.date_range(start_date, end_date)):
            indicator_obj.log(f"Expected {expected_records[idx]} signals.")
            if set_active_mode is not None:
                set_active_mode(valid_mode, cur_date, indicator_obj)
            date = cur_date.strftime(r"%Y-%m-%d")
            indicator_obj.set_description(f"Downloading signals for {date}")
            self._params["date"] = date
            for data in self._scroll(
                    "1900-01-01",
                    valid_mode,
                    valid_filters,
                    indicator=indicator_obj):
                yield from valid_mode.iterate_data(
                    data, indicator=indicator_obj)
            yield from valid_mode.iterate_data(None, indicator=indicator_obj)
        # For remaining fragment of data in csv mode only.
        # here buffer.shape < chunk_size
        buffer = valid_mode.get_buffer()
        if buffer is not None:
            indicator_obj.update(buffer.shape[0])
            yield buffer
        indicator_obj.close()


def create_data_client(
        url: str,
        token: str,
        n_errors: int = 5,
        indicator: Optional[Union[Indicators, ProgressIndicator]] = None,
        ) -> DataClient:
    return DataClient(url, token, n_errors, indicator)
