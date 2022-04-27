import io
import os
import time
import traceback
from typing import (
    Any,
    Dict,
    get_args,
    Iterator,
    List,
    Literal,
    Optional,
    Set,
    TypedDict,
    Union,
)

import pandas as pd
import requests
from accern_data.util import (
    generate_file_response,
    get_overall_total_from_dummy,
    is_example_url,
    ProgressBar,
    write_json,
)

ExcludedFilterField = Literal[
    "crawled_at",
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
            signal: Union[pd.DataFrame, List[Dict[str, Any]]]) -> None:
        raise NotImplementedError()

    def finish_day(self) -> None:
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

    def get_format(self) -> str:
        return "csv"

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
            signal: Union[pd.DataFrame, List[Dict[str, Any]]]) -> None:
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


class JSONMode(Mode):
    def __init__(self, debug_json: bool = False) -> None:
        super().__init__()
        self._res: List[Dict[str, Any]] = []
        self._debug_json = debug_json
        self._debug_ix = 0

    def get_format(self) -> str:
        return "json"

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
            signal: Union[pd.DataFrame, List[Dict[str, Any]]]) -> None:
        assert isinstance(signal, list)
        self._res.extend(signal)

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


class DataClient():
    def __init__(
            self,
            url: str,
            token: str) -> None:
        self._base_url = url
        self._token = token
        self._filters = self.validate_filters(None)
        self._params: Dict[str, str] = {}
        self._mode: Optional[Mode] = None
        self._first_error = True
        self._expected_records: List[int] = []

    @staticmethod
    def validate_filters(filters: Optional[FiltersType]) -> FiltersType:
        if filters is None:
            return {}
        for key in filters.keys():
            if key not in FILTER_FIELD:
                raise ValueError(
                    f"{key} is not a valid field."
                    f"Possible fields: {FILTER_FIELD}")
            if key == "primary_signal":
                val = filters["primary_signal"]
                if isinstance(val, bool):
                    filters["primary_signal"] = f"{val}".lower()
        return filters

    def set_filters(self, filters: FiltersType) -> None:
        self._filters = self.validate_filters(filters)

    def set_raw_filters(self, filters: FiltersType) -> None:
        for key in filters:
            if key == "primary_signal":
                val = filters["primary_signal"]
                if isinstance(val, bool):
                    filters["primary_signal"] = f"{val}".lower()

            assert key not in EXCLUDED_FILTER_FIELD, (
                "filters should not be containing any of "
                f"{EXCLUDED_FILTER_FIELD}")
        self._filters = filters

    def get_filters(self) -> FiltersType:
        return self._filters

    @staticmethod
    def parse_mode(mode: ModeType, split_dates: bool) -> Mode:
        if mode == "json":
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
        return self._mode

    def _read_total(self, cur_date: str, filters: FiltersType) -> int:
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
                            **{
                                key: f"{val}"
                                for key, val in filters.items()
                            },
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
                if self._first_error:
                    print_fn(traceback.format_exc())
                    self._first_error = False
                print_fn("unknown error...retrying...")
                time.sleep(0.5)

    def _read_date(
            self,
            mode: Mode,
            filters: FiltersType) -> Union[
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
                            **{
                                key: f"{val}"
                                for key, val in filters.items()
                            },
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
                if self._first_error:
                    print_fn(traceback.format_exc())
                    self._first_error = False
                print_fn("unknown error...retrying...")
                time.sleep(0.5)

    def _scroll(
            self,
            start_date: str,
            mode: Mode,
            filters: FiltersType) -> Iterator[
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

    def _process_date(
            self,
            cur_date: str,
            output_path: str,
            output_pattern: Optional[str],
            *,
            is_first_time: bool,
            mode: Mode,
            filters: FiltersType,
            progress_bar: ProgressBar) -> bool:
        self._params["date"] = cur_date
        first = True
        for res in self._scroll("1900-01-01", mode, filters):
            is_empty = False
            if first:
                mode.init_day(
                    cur_date, output_path, output_pattern, is_first_time)
                first = False

            if isinstance(res, pd.DataFrame) and res.empty:
                is_empty = True
            elif isinstance(res, list) and len(res) == 0:
                is_empty = True

            if is_first_time and not is_empty:
                is_first_time = False

            if not is_empty:
                mode.add_result(res)
                progress_bar.update(len(res))

        if not first:
            mode.finish_day()
        return is_first_time

    def download_range(
            self,
            start_date: str,
            output_path: Optional[str] = None,
            output_pattern: Optional[str] = None,
            end_date: Optional[str] = None,
            mode: Optional[ModeType] = None,
            split_dates: bool = False,
            filters: Optional[FiltersType] = None,
            verbose: bool = False) -> None:
        global VERBOSE
        VERBOSE = verbose
        if output_path is None:
            output_path = "./"
        os.makedirs(output_path, exist_ok=True)
        valid_mode = self.get_mode() \
            if mode is None else self.parse_mode(mode, split_dates)
        valid_filters = self.get_filters() if filters is None else filters
        if end_date is None:
            self._expected_records.append(
                self._read_total(start_date, valid_filters))
            print_fn(f"single day {start_date}")
            print_fn(f"expected {self._expected_records[0]}")
            progress_bar = ProgressBar(
                    total=self._expected_records[0],
                    desc="Downloading signals",
                    verbose=verbose)
            self._process_date(
                start_date,
                output_path,
                output_pattern,
                is_first_time=True,
                mode=valid_mode,
                filters=valid_filters,
                progress_bar=progress_bar)
        else:
            is_first_time = True
            total = 0
            progress_bar = ProgressBar(
                total=len(pd.date_range(start_date, end_date)),
                desc="Fetching info",
                verbose=verbose)

            for cur_date in pd.date_range(start_date, end_date):
                self._expected_records.append(
                    self._read_total(cur_date, valid_filters))
                progress_bar.update(1)

            total = sum(self._expected_records)
            progress_bar.set_total(total=total)
            progress_bar.set_description(desc="Downloading signals")

            for ix, cur_date in enumerate(pd.date_range(start_date, end_date)):
                print_fn(f"now processing {cur_date}")
                print_fn(f"expected {self._expected_records[ix]}")
                progress_bar.set_description(
                    f"Downloading signals for {cur_date.strftime('%Y-%m-%d')}")
                is_first_time = self._process_date(
                    cur_date.strftime("%Y-%m-%d"),
                    output_path,
                    output_pattern,
                    is_first_time=is_first_time,
                    mode=valid_mode,
                    filters=valid_filters,
                    progress_bar=progress_bar)
        progress_bar.close()
        self._expected_records = []


def create_data_client(
        url: str,
        token: str) -> DataClient:
    return DataClient(url, token)
