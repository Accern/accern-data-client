import io
import os
import time
import traceback
import warnings
from collections import deque
from copy import deepcopy
from typing import (
    Any,
    Deque,
    Dict,
    get_args,
    Iterator,
    List,
    Literal,
    Optional,
    Set,
    Tuple,
    TypedDict,
    Union,
)

import pandas as pd
import requests

from .util import (
    field_transformation,
    generate_file_response,
    get_overall_total_from_dummy,
    is_example_url,
    ProgressBar,
    write_json,
)

ExcludedFilterField = Literal[
    "crawled_at",
    "date",
    "format",
    "harvested_at",
    "published_at",
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

FILTER_FIELD = get_args(FilterField)
EXCLUDED_FILTER_FIELD = get_args(ExcludedFilterField)
ALL_MODES: Set[ModeType] = {"csv", "df", "json"}
DT_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
VERBOSE = False


def print_fn(msg: str) -> None:
    if VERBOSE:
        print(msg)


class Mode:
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

    def get_buffer(self) -> Optional[pd.DataFrame]:
        raise NotImplementedError

    def get_instance(self) -> 'Mode':
        return deepcopy(self)

    def parse_result(
            self,
            resp: requests.Response) -> Union[
                List[pd.DataFrame], List[Dict[str, Any]]]:
        raise NotImplementedError()

    def size(
            self,
            batch: Union[List[pd.DataFrame], List[Dict[str, Any]]]) -> int:
        raise NotImplementedError()

    def max_date(
            self,
            batch: Union[List[pd.DataFrame], List[Dict[str, Any]]]) -> str:
        raise NotImplementedError()

    def init_day(
            self,
            cur_date: str,
            path: str,
            pattern: Optional[str],
            is_first_day: bool) -> None:
        self._cur_date = cur_date
        self._cur_path = path
        self._cur_pattern = pattern
        self.do_init(is_first_day)

    def do_init(self, is_first_day: bool) -> None:
        raise NotImplementedError()

    def add_result(
            self,
            signal: Union[pd.DataFrame, Dict[str, Any]]) -> None:
        raise NotImplementedError()

    def finish_day(self) -> None:
        raise NotImplementedError()

    def iterate_data(
            self,
            data: Optional[Union[pd.DataFrame, List[Dict[str, Any]]]],
            progress_bar: ProgressBar,
            chunk_size: Optional[int] = None) -> Iterator[
                Union[pd.DataFrame, Dict[str, Any]]]:
        raise NotImplementedError()

    def split(
            self,
            batch: Union[List[pd.DataFrame], List[Dict[str, Any]]],
            value: pd.Timestamp) -> Union[pd.DataFrame, List[Dict[str, Any]]]:
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
            "csv_full should have an output pattern."
        if self._cur_pattern is None:
            fname = f"{day_str}.{self.get_format()}"
        elif day_str is None:
            fname = f"{self._cur_pattern}.{self.get_format()}"
        else:
            fname = f"{self._cur_pattern}-{day_str}.{self.get_format()}"
        return os.path.join(self._cur_path, fname)


class CSVMode(Mode):
    def __init__(self, is_by_day: bool) -> None:
        super().__init__()
        self._cols = None
        self._is_by_day = is_by_day
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
        if self._cols is not None:
            res = res[self._cols]
        else:
            self._cols = res.columns
        return [res]

    def size(
            self,
            batch: Union[List[pd.DataFrame], List[Dict[str, Any]]]) -> int:
        return sum(len(cur) for cur in batch)

    def max_date(
            self,
            batch: Union[List[pd.DataFrame], List[Dict[str, Any]]]) -> str:
        temp = set()
        for cur in batch:
            assert isinstance(cur, pd.DataFrame)
            harvested_at_list = cur["harvested_at"].to_list()
            for harvested_at in harvested_at_list:
                assert isinstance(harvested_at, pd.Timestamp)
                temp.add(harvested_at)
        dates: List[pd.Timestamp] = sorted(temp)
        if len(dates) <= 1:
            return dates[0].strftime(DT_FORMAT)
        # Second last date.
        return max(dates[:-1]).strftime(DT_FORMAT)

    def do_init(self, is_first_day: bool) -> None:
        fname = self.get_path(self._is_by_day)
        if is_first_day or self._is_by_day:
            pd.DataFrame([], columns=self._cols).to_csv(
                fname, index=False, header=True, mode="w")
        print_fn(f"current file is {fname}")

    def add_result(
            self,
            signal: Union[pd.DataFrame, Dict[str, Any]]) -> None:
        fname = self.get_path(is_by_day=self._is_by_day)
        assert isinstance(signal, pd.DataFrame)
        signal.to_csv(fname, index=False, header=False, mode="a")

    def finish_day(self) -> None:
        pass

    def split(
            self,
            batch: Union[List[pd.DataFrame], List[Dict[str, Any]]],
            value: pd.Timestamp) -> pd.DataFrame:
        df = batch[0]
        assert isinstance(df, pd.DataFrame)
        return df[df["harvested_at"] <= value]

    def iterate_data(
            self,
            data: Optional[Union[pd.DataFrame, List[Dict[str, Any]]]],
            progress_bar: ProgressBar,
            chunk_size: Optional[int] = None) -> Iterator[
                Union[pd.DataFrame, Dict[str, Any]]]:
        assert chunk_size is not None and chunk_size > 0
        if data is not None:
            assert isinstance(data, pd.DataFrame)
            self._buffer.append(data)
            self._buffer_size += data.shape[0]
        while self._buffer_size >= chunk_size:
            res_df = pd.concat(self._buffer)
            result: pd.DataFrame = res_df.iloc[:chunk_size]
            remainder: pd.DataFrame = res_df.iloc[chunk_size:]
            if remainder.empty:
                self._buffer = []
            else:
                self._buffer = [remainder]
            self._buffer_size = remainder.shape[0]
            progress_bar.update(result.shape[0])
            yield result

        if self.split_dates() and data is None:
            if len(self._buffer) > 0:
                buffer = pd.concat(self._buffer)
                if not buffer.empty:
                    progress_bar.update(buffer.shape[0])
                    yield buffer
            self._buffer = []
            self._buffer_size = 0


class JSONMode(Mode):
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
        pass

    def get_buffer(self) -> Optional[pd.DataFrame]:
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

    def size(
            self,
            batch: Union[List[pd.DataFrame], List[Dict[str, Any]]]) -> int:
        return len(batch)

    def max_date(
            self,
            batch: Union[List[pd.DataFrame], List[Dict[str, Any]]]) -> str:
        assert isinstance(batch[0], dict)
        temp = set()
        for cur in batch:
            assert isinstance(cur, dict)
            harvested_at = cur["harvested_at"]
            assert isinstance(harvested_at, pd.Timestamp)
            temp.add(harvested_at)
        dates: List[pd.Timestamp] = sorted(temp)
        if len(dates) <= 1:
            return dates[0].strftime(DT_FORMAT)
        return max(dates[:-1]).strftime(DT_FORMAT)

    def do_init(self, is_first_day: bool) -> None:
        self._res = []

    def add_result(
            self,
            signal: Union[pd.DataFrame, Dict[str, Any]]) -> None:
        assert isinstance(signal, dict)
        self._res.append(signal)

    def finish_day(self) -> None:
        fname = self.get_path(is_by_day=True)
        print_fn(f"writing results to {fname}")

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
            batch: Union[List[pd.DataFrame], List[Dict[str, Any]]],
            value: pd.Timestamp) -> List[Dict[str, Any]]:
        result = []
        for record in batch:
            assert isinstance(record, dict)
            if record["harvested_at"] <= value:
                result.append(record)
        return result

    def iterate_data(
            self,
            data: Optional[Union[pd.DataFrame, List[Dict[str, Any]]]],
            progress_bar: ProgressBar,
            chunk_size: Optional[int] = None) -> Iterator[
                Union[pd.DataFrame, Dict[str, Any]]]:
        if data is not None:
            assert isinstance(data, list)
            for rec in data:
                progress_bar.update(1)
                yield rec


class DataClient:
    def __init__(
            self,
            url: str,
            token: str,
            n_errors: int = 5) -> None:
        self._base_url = url
        self._token = token
        self._filters: Dict[str, str] = {}
        self._params: Dict[str, str] = {}
        self._mode: Optional[Mode] = None
        self._error_list: Deque[str] = deque(maxlen=n_errors)

    def reset_error_list(self) -> None:
        self._error_list.clear()

    @staticmethod
    def validate_filters(
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
    def parse_filters(
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

    def set_filters(self, filters: FiltersType) -> None:
        self.set_raw_filters(self.validate_filters(filters))

    def set_raw_filters(
            self, filters: Dict[str, Optional[Union[bool, int, str]]]) -> None:
        self._filters = self.parse_filters(filters)

    def get_filters(self) -> Dict[str, str]:
        return self._filters

    @staticmethod
    def parse_mode(mode: ModeType, split_dates: bool = True) -> Mode:
        if mode == "json":
            if not split_dates:
                warnings.warn(
                    "In json mode, there is no difference between "
                    "split_dates=True or split_dates=False. Both will work "
                    "the same way.",
                    Warning,
                    stacklevel=2)
            return JSONMode()
        if mode in {"csv", "df"}:
            return CSVMode(is_by_day=split_dates)
        raise ValueError(
            f"Please set proper mode. It is '{mode}' which is not in "
            f"{ALL_MODES}")

    def set_mode(self, mode: ModeType, split_dates: bool) -> None:
        self._mode = self.parse_mode(mode, split_dates)

    def get_mode(self) -> Mode:
        assert self._mode is not None, "Set mode first."
        return self._mode.get_instance()

    def get_last_silenced_errors(self) -> List[str]:
        return list(self._error_list)

    def _read_total(
            self, cur_date: str, filters: Dict[str, str]) -> int:
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
                            **filters.items(),
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
                    requests.exceptions.RequestException):  # FIXME: add more?
                self._error_list.append(traceback.format_exc())
                print_fn("unknown error...retrying...")
                time.sleep(0.5)

    def _read_date(
            self,
            mode: Mode,
            filters: Dict[str, str]) -> Union[
                List[pd.DataFrame], List[Dict[str, Any]]]:
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
                            **filters.items(),
                            **self._params,
                            **{"format": mode.get_format()}
                        })
                if not str(resp.text).strip():
                    return []  # type: ignore
                return mode.parse_result(resp)
            except KeyboardInterrupt as err:
                raise err
            except (
                    AssertionError,
                    KeyError,
                    requests.exceptions.RequestException):  # FIXME: add more?
                self._error_list.append(traceback.format_exc())
                print_fn("unknown error...retrying...")
                time.sleep(0.5)

    def _scroll(
            self,
            start_date: str,
            mode: Mode,
            filters: Dict[str, str]) -> Iterator[
                Union[pd.DataFrame, List[Dict[str, Any]]]]:
        print_fn("new day")
        self._params["harvested_after"] = start_date
        batch = self._read_date(mode, filters)
        total = mode.size(batch)
        prev_start = start_date
        while mode.size(batch) > 0:
            try:
                start_date = mode.max_date(batch)
                yield mode.split(batch, pd.to_datetime(start_date))
                self._params["harvested_after"] = start_date
                batch = self._read_date(mode, filters)
                total += mode.size(batch)
                if start_date == prev_start:
                    # FIXME: redundant check? batch_size becomes 0
                    # loop gets terminated.
                    break
                prev_start = start_date
            except pd.errors.EmptyDataError:
                break

    def _get_valid_mode(
            self,
            mode: Optional[
                Union[Mode, ModeType, Tuple[ModeType, bool]]]) -> Mode:
        if mode is None:
            return self.get_mode()
        if isinstance(mode, Mode):
            return mode.get_instance()
        if isinstance(mode, str):
            return self.parse_mode(mode)
        return self.parse_mode(*mode)

    def _get_valid_filters(
            self, filters: Optional[FiltersType]) -> Dict[str, str]:
        if filters is None:
            return self.get_filters()
        return self.parse_filters(
            {**self.get_filters(), **self.validate_filters(filters)})

    def _fetch_info(
            self,
            start_date: str,
            end_date: str,
            filters: Dict[str, str],
            verbose: bool) -> Tuple[ProgressBar, List[int]]:
        total = 0
        expected_records: List[int] = []
        progress_bar = ProgressBar(
            total=len(pd.date_range(start_date, end_date)),
            desc="Fetching info",
            verbose=verbose)
        for cur_date in pd.date_range(start_date, end_date):
            expected_records.append(self._read_total(cur_date, filters))
            progress_bar.update(1)
        total = sum(expected_records)
        progress_bar.set_total(total=total)
        return progress_bar, expected_records

    def download_range(
            self,
            start_date: str,
            output_path: Optional[str] = None,
            output_pattern: Optional[str] = None,
            end_date: Optional[str] = None,
            mode: Optional[
                Union[Mode, ModeType, Tuple[ModeType, bool]]] = None,
            filters: Optional[FiltersType] = None,
            verbose: bool = False) -> None:
        global VERBOSE
        VERBOSE = verbose
        if output_path is None:
            output_path = "./"
        os.makedirs(output_path, exist_ok=True)
        valid_mode = self._get_valid_mode(mode)
        valid_filters = self._get_valid_filters(filters)
        if end_date is None:
            end_date = start_date

        progress_bar, expected_records = self._fetch_info(
            start_date, end_date, valid_filters, verbose)
        progress_bar.set_description(desc="Downloading signals")
        is_first_time = True
        for ix, cur_date in enumerate(pd.date_range(start_date, end_date)):
            first = True
            date = cur_date.strftime('%Y-%m-%d')
            print_fn(f"now processing {date}")
            print_fn(f"expected {expected_records[ix]}")
            iterator = self.iterate_range(
                start_date=date,
                end_date=date,  # FIXME: can be omitted
                mode=valid_mode,
                filters=filters,
                chunk_size=100,
                progress_bar=progress_bar)
            for res in iterator:
                if first:
                    valid_mode.init_day(
                        date, output_path, output_pattern, is_first_time)
                    first = False
                is_empty = False
                if isinstance(res, pd.DataFrame) and res.empty:
                    is_empty = True
                if is_first_time and not is_empty:
                    is_first_time = False
                if not is_empty:
                    valid_mode.add_result(res)
            if not first:
                valid_mode.finish_day()
        progress_bar.close()

    def iterate_range(
            self,
            start_date: str,
            end_date: Optional[str] = None,
            mode: Optional[
                Union[Mode, ModeType, Tuple[ModeType, bool]]] = None,
            filters: Optional[FiltersType] = None,
            chunk_size: Optional[int] = None,
            progress_bar: Optional[ProgressBar] = ProgressBar()) -> Iterator[
                Union[pd.DataFrame, Dict[str, Any]]]:
        valid_mode = self._get_valid_mode(mode)
        valid_filters = self._get_valid_filters(filters)
        valid_mode.clean_buffer()
        if end_date is None:
            end_date = start_date
        local = False
        if progress_bar is None:
            progress_bar = ProgressBar(total=0, desc="", verbose=True)
        elif progress_bar.get_total() is None:
            local = True
            progress_bar, _ = self._fetch_info(
                start_date, end_date, valid_filters, verbose=False)
            progress_bar.set_description(desc="Downloading signals")
        for cur_date in pd.date_range(start_date, end_date):
            date = cur_date.strftime("%Y-%m-%d")
            progress_bar.set_description(f"Downloading signals for {date}")
            self._params["date"] = date
            iterator = self._scroll(
                "1900-01-01", valid_mode, valid_filters)
            for data in iterator:
                yield from valid_mode.iterate_data(
                    data, progress_bar=progress_bar, chunk_size=chunk_size)
            yield from valid_mode.iterate_data(
                None, progress_bar=progress_bar, chunk_size=chunk_size)
        # For remaining fragment of data in csv mode only.
        # here buffer.shape < chunk_size
        buffer = valid_mode.get_buffer()
        if buffer is not None:
            progress_bar.update(buffer.shape[0])
            yield buffer
        if local:
            progress_bar.close()


def create_data_client(
        url: str,
        token: str) -> DataClient:
    return DataClient(url, token)
