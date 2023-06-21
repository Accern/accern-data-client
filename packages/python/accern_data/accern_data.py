import csv
import io
import os
import time
import traceback
import warnings
from collections import deque
from copy import deepcopy
from typing import (  # get_args, Literal, TypedDict,
    Any,
    Callable,
    Deque,
    Dict,
    Generic,
    Iterator,
    List,
    Optional,
    Set,
    Tuple,
    TypeVar,
    Union,
)

import pandas as pd
import requests
from typing_extensions import get_args, Literal, TypedDict

from .util import (
    BarIndicator,
    convert_to_date,
    DATE_FORMAT,
    DATETIME_FORMAT,
    END_TIME,
    generate_file_response,
    get_by_date_after,
    get_header_file_name,
    get_overall_total_from_dummy,
    get_tmp_file_name,
    has_iprogress,
    is_example_url,
    MessageIndicator,
    micro_to_millisecond,
    ProgressIndicator,
    SilentIndicator,
    START_TIME,
    write_json,
)

ExcludedFilterField = Literal[
    "crawled_at",
    "date",
    "end_time",
    "exclude",
    "format",
    "harvested_at",
    "include",
    "max_harvested_at",
    "max_published_at",
    "min_harvested_at",
    "min_published_at",
    "published_at",
    "size",
    "start_time",
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
        "doc_cluster_id": Optional[Union[str, List[str]]],
        "doc_id": Optional[Union[str, List[str]]],
        "doc_source": Optional[Union[str, List[str]]],
        "doc_title": Optional[Union[str, List[str]]],
        "doc_type": Optional[Union[str, List[str]]],
        "doc_url": Optional[Union[str, List[str]]],
        "entity_accern_id": Optional[Union[str, List[str]]],
        "entity_country": Optional[Union[str, List[str]]],
        "entity_exchcode": Optional[Union[str, List[str]]],
        "entity_figi": Optional[Union[str, List[str]]],
        "entity_hits": Optional[Union[str, List[str]]],
        "entity_indices": Optional[Union[str, List[str]]],
        "entity_name": Optional[Union[str, List[str]]],
        "entity_region": Optional[Union[str, List[str]]],
        "entity_relevance": Optional[Union[int, List[int]]],
        "entity_sector": Optional[Union[str, List[str]]],
        "entity_share_class": Optional[Union[str, List[str]]],
        "entity_text": Optional[Union[str, List[str]]],
        "entity_ticker": Optional[Union[str, List[str]]],
        "entity_type": Optional[Union[str, List[str]]],
        "event": Optional[Union[str, List[str]]],
        "event_accern_id": Optional[Union[int, List[int]]],
        "event_group": Optional[Union[str, List[str]]],
        "event_hits": Optional[Union[str, List[str]]],
        "event_text": Optional[Union[str, List[str]]],
        "primary_signal": Optional[Union[str, bool, List[str], List[bool]]],
        "provider_id": Optional[Union[int, List[int]]],
        "signal_id": Optional[Union[str, List[str]]],
        "signal_tag": Optional[Union[str, List[str]]],
    },
    total=False)
FilterValue = Optional[Union[bool, int, str, List[bool], List[int], List[str]]]
ErrorTuple = Tuple[Optional[Dict[str, Union[str, int]]], str]

ModeType = Literal["csv", "df", "json"]
Indicators = Literal["pbar", "silent", "message"]
ByDate = Literal["date", "harvested_at", "published_at"]
BY_DATE = get_args(ByDate)
INDICATORS = get_args(Indicators)
FILTER_FIELD = get_args(FilterField)
EXCLUDED_FILTER_FIELD = get_args(ExcludedFilterField)
ALL_MODES: Set[ModeType] = {"csv", "df", "json"}

T = TypeVar('T')

MAX_CSV_FIELD_SIZE = 10000000
# constant value to increase the download limit of the csv.
# if the limit is still less, change this value for csv.field_size_limit


class Mode(Generic[T]):
    """
    Mode in which the data has to be generated.
    """
    def __init__(self) -> None:
        self._cur_date: Optional[str] = None
        self._cur_path: Optional[str] = None
        self._cur_pattern: Optional[str] = None

    def get_format(self) -> str:
        """
        Returns file format of the mode.
        """
        raise NotImplementedError()

    def split_dates(self) -> bool:
        """
        Whether or not split files on the basis of dates.
        """
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

    def max_date(self, batch: List[T], by_date: str) -> str:
        raise NotImplementedError()

    def init_day(
            self,
            cur_date: str,
            path: str,
            pattern: Optional[str],
            indicator: ProgressIndicator) -> None:
        """
        Intializes files & variables required before retrieving signals for a
        day.

        Parameters:
            cur_date: Day to intialize.
            path: The path in your local file system where you want to
                store those downloaded files.
            pattern: Patterns are the file name prefix that the downloaded
                files should have.
            indicator: Indicator to show progress of the whole process.
        """
        self._cur_date = cur_date
        self._cur_path = path
        self._cur_pattern = pattern
        self.do_init(indicator)

    def do_init(self, indicator: ProgressIndicator) -> None:
        """
        Intializes resources & files.
        """
        raise NotImplementedError()

    def add_result(self, signal: T) -> None:
        raise NotImplementedError()

    def finish_day(self, force_finish: bool = False) -> None:
        raise NotImplementedError()

    def iterate_data(
            self,
            data: Optional[List[T]],
            by_date: str,
            indicator: ProgressIndicator,
            helper: Callable[[str], None]) -> Iterator[T]:
        raise NotImplementedError()

    def stringify_dates(self, obj: T) -> T:
        raise NotImplementedError()

    def split(
            self,
            batch: List[T],
            value: pd.Timestamp,
            by_date: str) -> List[T]:
        raise NotImplementedError()

    def get_current_date(
            self, obj: T, by_date: str) -> Optional[str]:
        raise NotImplementedError()

    def get_path(self, is_by_day: bool) -> str:
        """
        Generates file path.

        Parameters:
            is_by_day: Flag to determine whether or not file is divided on the
            basis of dates.

        Returns:
            File path.
        """
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
        self._cols: Optional[List[str]] = None
        self._is_by_day = is_by_day
        self._chunk_size = chunk_size
        self._buffer: List[pd.DataFrame] = []
        self._buffer_size = 0
        csv.field_size_limit(MAX_CSV_FIELD_SIZE)

    def get_format(self) -> str:
        """
        Returns file format of the mode.
        """
        return "csv"

    def split_dates(self) -> bool:
        """
        Whether or not split files on the basis of dates.
        """
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
        """
        Parses response from the feed API to pandas dataframe.

        Paramteres:
            resp: Response from the API.

        Returns:
            List of dataframes processed from the API response.
        """
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
        """
        Returns number of signals returned from the feed API.

        Paramteres:
            batch: List of pandas dataframe from the API.

        Returns:
            Total number of signals in the input batch.
        """
        return sum(cur.shape[0] for cur in batch)

    def max_date(self, batch: List[pd.DataFrame], by_date: str) -> str:
        """
        Returns second maximum date from signals.

        Paramteres:
            batch: List of pandas dataframe from the API.
            by_date: Can be either published_at or harvested_at.

        Returns:
            Second maximum harvested_at or published_at date (depends on
            by_date parameter) from all the signals in the batch.
        """
        temp = set()
        for cur in batch:
            date_at_list = cur[by_date].to_list()
            for date_at in date_at_list:
                assert isinstance(date_at, pd.Timestamp)
                temp.add(date_at)
        dates: List[pd.Timestamp] = sorted(temp)
        if len(dates) <= 1:
            return dates[0].strftime(DATETIME_FORMAT)
        # Second last date.
        return max(dates[:-1]).strftime(DATETIME_FORMAT)

    def do_init(self, indicator: ProgressIndicator) -> None:
        """
        Intializes resources & files.
        """
        fname = self.get_path(self._is_by_day)
        indicator.log(f"current file is {fname}")

    def _write_cols(self) -> None:
        fname = self.get_path(is_by_day=self._is_by_day)
        header = pd.DataFrame(columns=self._cols)
        header.to_csv(get_header_file_name(fname), index=False)

    def add_result(self, signal: pd.DataFrame) -> None:
        """
        Appends signals to already existing file or writes to a new file.

        Paramteres:
            signal: Dataframe containing signals as rows.
        """
        fname = self.get_path(is_by_day=self._is_by_day)
        tmp_fname = get_tmp_file_name(fname)

        if self._cols is None:  # Writing a fresh file.
            self._cols = sorted(signal.columns.to_list())
            self._write_cols()
            signal[self._cols].to_csv(
                tmp_fname, index=False, header=False, mode="w")
        else:  # Appending to already existing file.
            # Field/column inconsistency.
            cur_cols_set = set(self._cols)
            sig_cols_set = set(signal.columns)
            missing_cols = cur_cols_set.difference(sig_cols_set)
            extra_cols = sig_cols_set.difference(cur_cols_set)
            for col in missing_cols:
                signal[col] = None
            if extra_cols:
                self._cols += sorted(extra_cols)
                self._write_cols()
            signal[self._cols].to_csv(
                tmp_fname, index=False, header=False, mode="a")

    def finish_day(self, force_finish: bool = False) -> None:
        # csv files are saved by add_result
        fname = self.get_path(is_by_day=self._is_by_day)
        if (self._is_by_day or force_finish) and self._cols:
            merge_csv_file(fname)
            self._cols = None

    def stringify_dates(self, obj: pd.DataFrame) -> pd.DataFrame:
        """
        Process the signals to convert dates to their string representation.

        Parameters:
            obj: Pandas dataframe containing signals as rows.

        Returns:
            Pandas dataframe containing signals as rows with date values as
            string.
        """
        def micro_to_milli(timestamp: pd.Timestamp) -> str:
            return micro_to_millisecond(
                pd.to_datetime(timestamp).strftime(DATETIME_FORMAT))
        new_obj = obj.copy()
        for col in ["harvested_at", "crawled_at", "published_at"]:
            new_obj.loc[:, col] = obj[col].apply(micro_to_milli)
        return new_obj

    def split(
            self,
            batch: List[pd.DataFrame],
            value: pd.Timestamp,
            by_date: str) -> List[pd.DataFrame]:
        """
        Filters signals having harvested_at or published_at (governed by
        by_date parameter) less than a provided value.

        Parameters:
            batch: List of pandas dataframe from the API.
            value: Date of & before which the signals has to be filtered.
            by_date: Can be either published_at or harvested_at.

        Returns:
            List of filters pandas dataframe from the API.
        """
        df = batch[0]
        return [self.stringify_dates(df[df[by_date] <= value])]

    def get_current_date(
            self, obj: pd.DataFrame, by_date: str) -> Optional[str]:
        """
        Returns first harvested_at or published_at (governed by
        by_date parameter) in the dataframe.

        Parameters:
            obj: Dataframe containing signals as rows.
            by_date: can be either published_at or harvested_at.

        Returns:
            Current date from input dataframe. If the input dataframe is empty
            then it returns None.
        """
        if obj.empty:
            return None
        # NOTE: check date format
        return convert_to_date(obj.loc[0, by_date])

    def iterate_data(
            self,
            data: Optional[List[pd.DataFrame]],
            by_date: str,
            indicator: ProgressIndicator,
            helper: Callable[[str], None]) -> Iterator[pd.DataFrame]:
        """
        Streams data.

        Parameters:
            data: List of pandas dataframe containing signals as rows.
            by_date: Can be either published_at or harvested_at.
            indicator: Indicator to show progress of the whole process.

        Returns:
            Streams pandas dataframe containing signals as rows. Number of
            signals returned are governed by the defined chunk size.
        """
        assert self._chunk_size is None or self._chunk_size > 0
        if self._chunk_size is None:
            if data is not None:
                df = data[0]
                indicator.update(df.shape[0])
                if not df.empty:
                    if self.split_dates():
                        while not df.empty:
                            cur_date = self.get_current_date(df, by_date)
                            assert cur_date is not None
                            helper(cur_date)
                            idx = df[df[by_date].apply(
                                convert_to_date) == cur_date].index[-1]
                            result = df.iloc[:idx + 1]
                            df = df.iloc[idx + 1:].reset_index(drop=True)
                            yield result
                    else:
                        yield df
        else:
            if data is not None:
                self._buffer.append(data[0])
                self._buffer_size += data[0].shape[0]
            while self._buffer_size >= self._chunk_size:
                res_df = pd.concat(self._buffer, ignore_index=True)
                cur_date = self.get_current_date(res_df, by_date)
                assert cur_date is not None
                helper(cur_date)
                idx = res_df[res_df[by_date].apply(
                        convert_to_date) == cur_date].index[-1]

                if self.split_dates() and idx < self._chunk_size:
                    result = res_df.iloc[:idx + 1]
                    remainder: pd.DataFrame = res_df.iloc[idx + 1:]
                else:
                    result = res_df.iloc[:self._chunk_size]
                    remainder = res_df.iloc[self._chunk_size:]
                if remainder.empty:
                    self._buffer = []
                else:
                    self._buffer = [remainder]
                self._buffer_size = remainder.shape[0]
                indicator.update(result.shape[0])
                yield result.reset_index(drop=True)


class JSONMode(Mode[Dict[str, Any]]):
    def __init__(self, debug_json: bool = False) -> None:
        super().__init__()
        self._res: List[Dict[str, Any]] = []
        self._debug_json = debug_json
        self._debug_ix = 0

    def get_format(self) -> str:
        """
        Returns file format of the mode.
        """
        return "json"

    def split_dates(self) -> bool:
        """
        Whether or not split files on the basis of dates.
        """
        return True

    def clean_buffer(self) -> None:
        # json mode has no buffer
        pass

    def get_buffer(self) -> Optional[Dict[str, Any]]:
        return None

    def parse_result(self, resp: requests.Response) -> List[Dict[str, Any]]:
        """
        Parses response from the feed API to python dictionary object.

        Paramteres:
            resp: Response from the API.

        Returns:
            List of dictionary objects processed from the API response.
        """
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
        """
        Returns number of signals returned from the feed API.

        Paramteres:
            batch: List of signals in json format from the API.

        Returns:
            Total number of signals in the input batch.
        """
        return len(batch)

    def max_date(self, batch: List[Dict[str, Any]], by_date: str) -> str:
        """
        Returns second maximum date from signals.

        Paramteres:
            batch: List of signals in json format from the API.
            by_date: Can be either published_at or harvested_at.

        Returns:
            Second maximum harvested_at or published_at date (depends on
            by_date parameter) from all the signals in the batch.
        """
        temp = set()
        for cur in batch:
            date_at = cur[by_date]
            assert isinstance(date_at, pd.Timestamp)
            temp.add(date_at)
        dates: List[pd.Timestamp] = sorted(temp)
        if len(dates) <= 1:
            return dates[0].strftime(DATETIME_FORMAT)
        return max(dates[:-1]).strftime(DATETIME_FORMAT)

    def do_init(self, indicator: ProgressIndicator) -> None:
        """
        Intializes resources & files.
        """
        self._res = []

    def add_result(self, signal: Dict[str, Any]) -> None:
        """
        Appends signals to signals list.

        Paramteres:
            signal: A signal in form of dictionary object.
        """
        self._res.append(signal)

    def finish_day(self, force_finish: bool = False) -> None:
        """
        Writes json file.
        """
        fname = self.get_path(is_by_day=True)
        if len(self._res) > 0:
            write_json(self._res, fname, sort_keys=True)

    def stringify_dates(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the signals to convert dates to their string representation.

        Parameters:
            obj: A signal in form of dictionary object.

        Returns:
            A signal in form of dictionary object containing date values as
            string.
        """
        if "harvested_at" in obj:
            obj["harvested_at"] = micro_to_millisecond(
                obj["harvested_at"].strftime(DATETIME_FORMAT))
        if "published_at" in obj:
            obj["published_at"] = micro_to_millisecond(
                obj["published_at"].strftime(DATETIME_FORMAT))
        if "crawled_at" in obj:
            obj["crawled_at"] = micro_to_millisecond(
                obj["crawled_at"].strftime(DATETIME_FORMAT))
        return obj

    def split(
            self,
            batch: List[Dict[str, Any]],
            value: pd.Timestamp,
            by_date: str) -> List[Dict[str, Any]]:
        result = []
        for record in batch:
            if record[by_date] <= value:
                result.append(self.stringify_dates(record))
        return result

    def get_current_date(
            self, obj: Dict[str, Any], by_date: str) -> Optional[str]:
        """
        Returns first harvested_at or published_at (governed by
        by_date parameter) in the signal.

        Parameters:
            obj: Signal as a dictionary object.
            by_date: can be either published_at or harvested_at.

        Returns:
            Current date from input dictionary object.
        """
        # NOTE: check date format
        return convert_to_date(obj[by_date])

    def iterate_data(
            self,
            data: Optional[List[Dict[str, Any]]],
            by_date: str,
            indicator: ProgressIndicator,
            helper: Callable[[str], None]) -> Iterator[Dict[str, Any]]:
        """
        Streams data.

        Parameters:
            data: List of dictionary objects containing signals as rows.
            by_date: Can be either published_at or harvested_at.
            indicator: Indicator to show progress of the whole process.

        Returns:
            Streams signals from the input one by one.
        """
        if data is not None:
            for rec in data:
                cur_date = self.get_current_date(rec, by_date)
                assert cur_date is not None
                helper(cur_date)
                indicator.update(1)
                yield rec


class DataClient:
    """
    Client for downloading & processing feed API data.
    """
    def __init__(
            self,
            url: str,
            token: str,
            n_errors: int = 5,
            indicator: Optional[Union[Indicators, ProgressIndicator]] = None,
            ) -> None:
        self._base_url = url
        self._token = token
        self._filters: Dict[str, FilterValue] = {}
        self._mode: Optional[Mode] = None
        if indicator is not None:
            self.set_indicator(indicator)
        else:
            self._indicator_obj = self._parse_indicator("pbar")
        self._error_list: Deque[ErrorTuple] = deque(maxlen=n_errors)

    def reset_error_list(self) -> None:
        """
        Resets the error list.
        """
        self._error_list.clear()

    @staticmethod
    def _validate_filters(filters: FiltersType) -> Dict[str, FilterValue]:
        """
        Function to check if provided filters are valid ones & contain valid
        data type.

        Parameters:
            filters: Mapping with key as field name & value as field value on
            which the data has to be filtered.

        Returns:
            Valid filters.
        """
        valid_filters: Dict[str, FilterValue] = {}
        for key, value in filters.items():
            if key not in FILTER_FIELD:
                raise ValueError(
                    f"{key} is not a valid field."
                    f"Possible fields: {FILTER_FIELD}")
            assert isinstance(value, (bool, int, str, list)) or value is None
            valid_filters[key] = value
        return valid_filters

    @staticmethod
    def _parse_filters(
            filters: Dict[str, FilterValue]) -> Dict[str, FilterValue]:
        """
        Function to validate if reserved API parameters are not included in
        filters.

        Parameters:
            filters: Mapping with key as field name & value as field value on
            which the data has to be filtered.

        Returns:
            Valid filters.
        """
        for key in filters.keys():
            assert key not in EXCLUDED_FILTER_FIELD, (
                "filters should not be containing any of "
                f"{EXCLUDED_FILTER_FIELD}")
        return filters

    def set_indicator(
            self, indicator: Union[Indicators, ProgressIndicator]) -> None:
        """
        Sets progress indicator for the download process.

        Parameters:
            indicator: Can either be a string (pbar, message, silent) or
            ProgressIndicator object.
        """
        if isinstance(indicator, ProgressIndicator):
            self._indicator_obj = indicator
        else:
            self._indicator_obj = self._parse_indicator(indicator)

    @staticmethod
    def _parse_indicator(indicator: Indicators) -> ProgressIndicator:
        """
        Checks if given indicator is valid & parses string format indicator to
        corresponding ProgressIndicator object.

        Parameters:
            indicator: Can either be a pbar, message or silent

        Returns:
            BarIndicator(interactive progress bar) if input is pbar.
            MessageIndicator(message logs) if input is message.
            SilentIndicator(nothing at all) if input is silent.
        """
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
        """
        Returns current indicator in use.
        """
        if self._indicator_obj is None:
            raise ValueError("Set indicator first.")
        return self._indicator_obj

    def set_filters(self, filters: FiltersType) -> None:
        """
        Sets filters to use in the current execution.
        """
        self._set_raw_filters(self._validate_filters(filters))

    def _set_raw_filters(self, filters: Dict[str, FilterValue]) -> None:
        self._filters = self._parse_filters(filters)

    def get_filters(self) -> Dict[str, FilterValue]:
        """
        Returns current filters in use.
        """
        return self._filters

    @staticmethod
    def _parse_mode(
            mode: ModeType,
            split_dates: bool = True,
            chunk_size: Optional[int] = None) -> Mode:
        """
        Checks if given mode is valid & parses string format mode to
        corresponding Mode object.

        Parameters:
            mode: Can either be a csv, df or json. csv and df are same thing.
            split_dates: Flag to determine if the data has to be kept in
                separate files on the basis of dates.
            chunk_size: Number of signals to process at a time.

        Returns:
            A Mode object functioning as the following:
            1. csv or df with split_dates=False downloads all the signals for
            each day/date into one single csv file.
            2. csv or df with split_dates=True downloads all the signals for
            each day/date into respective csv files(based on dates).
            3. json downloads all the signals for each day/date into
            respective json files(based on dates). It does not matter what
            value split_dates contain in this case.
        """
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
        """
        Sets mode to use in the current execution.
        """
        self._mode = self._parse_mode(mode, split_dates, chunk_size)

    def get_mode(self) -> Mode:
        """
        Returns current mode in use.
        """
        assert self._mode is not None, "Set mode first."
        return self._mode.get_instance()

    def get_last_silenced_errors(
            self) -> List[ErrorTuple]:
        """
        Returns list of errors occurred during previous execution.
        """
        return list(self._error_list)

    def _read_total(
            self,
            params: Dict[str, str],
            filters: Dict[str, FilterValue],
            indicator: ProgressIndicator,
            request_kwargs: Optional[Dict[Any, Any]]) -> int:
        """
        Generates overall total for a given set of feed API parameters.

        Parameters:
            params: Parameters of the API call.
            filters: Filters to apply on the response.
            indicator: Indicator to show progress of the whole process.
            request_kwargs: Keywords to pass to the post function of requests
                module. For ex: Proxy.

        Returns:
            Total number of signals for given parameters.
        """
        rkwargs = {} if request_kwargs is None else request_kwargs
        while True:
            try:
                req_params: Optional[Dict[str, Union[str, int]]] = None
                if is_example_url(self._base_url):  # Mock API
                    resp = get_overall_total_from_dummy(params, filters)
                else:  # Real API
                    # Size is 1 and we exclude all signal fields because we are
                    # interested in only overall_total. This reduces the load
                    # on the API.
                    req_params = {
                        **params,
                        "format": "json",
                        "size": 1,
                        "exclude": "*",
                    }
                    resp = requests.post(
                        self._base_url,
                        headers={"authorization": self._token},
                        json={**req_params, **filters},
                        **rkwargs)
                if not str(resp.text).strip():  # if nothing is fetched
                    return 0
                return int(resp.json()["overall_total"])
            except KeyboardInterrupt as err:
                raise err
            except (
                    AssertionError,
                    KeyError,
                    requests.exceptions.RequestException):  # NOTE: add more?
                self._error_list.append((req_params, traceback.format_exc()))
                indicator.log("unknown error...retrying...")
                time.sleep(0.5)

    def _read_date(
            self,
            mode: Mode[T],
            params: Dict[str, str],
            filters: Dict[str, FilterValue],
            by_date: str,
            indicator: ProgressIndicator,
            url_params: Optional[Dict[str, str]],
            json_params: Optional[Dict[str, Any]],
            request_kwargs: Optional[Dict[Any, Any]]) -> List[T]:
        """
        Generates signals for a given set of feed API parameters.

        Parameters:
            mode: Type of response.
            params: Parameters of the API call.
            filters: Filters to apply on the response.
            by_date: can be either published_at or harvested_at.
            indicator: Indicator to show progress of the whole process.
            url_params: Extra parameters to pass in the URL.
            json_params: Extra parameters to pass in the request body.
            request_kwargs: Keywords to pass to the post function of requests
                module. For ex: Proxy.

        Returns:
            List of signals for given parameters.
        """
        while True:
            req_params = None
            url_params = url_params if url_params is not None else {}
            json_params = json_params if json_params is not None else {}
            rkwargs = {} if request_kwargs is None else request_kwargs
            try:
                if is_example_url(self._base_url):
                    resp = generate_file_response(
                        {**params, **url_params},
                        mode.get_format(),
                        filters=filters,
                        by_date=by_date)
                else:
                    resp = requests.post(
                        self._base_url,
                        headers={"authorization": self._token},
                        params=url_params,
                        json={
                            **params,
                            **filters,
                            **{"format": mode.get_format()}
                        },
                        **rkwargs)
                if not str(resp.text).strip():
                    return []
                return mode.parse_result(resp)
            except KeyboardInterrupt as err:
                raise err
            except (
                    AssertionError,
                    KeyError,
                    requests.exceptions.RequestException):  # NOTE: add more?
                self._error_list.append((req_params, traceback.format_exc()))
                indicator.log("unknown error...retrying...")
                time.sleep(0.5)

    def _scroll(
            self,
            mode: Mode[T],
            params: Dict[str, str],
            filters: Dict[str, FilterValue],
            by_date: str,
            indicator: ProgressIndicator,
            url_params: Optional[Dict[str, str]] = None,
            json_params: Optional[Dict[str, Any]] = None,
            request_kwargs: Optional[Dict[Any, Any]] = None,
                ) -> Iterator[List[T]]:
        """
        Streams signals for a given set of feed API parameters. This function
        bypasses the signals size restriction provided by the API. It paginates
        using the by_date parameter.

        Parameters:
            mode: Type of response.
            params: Parameters of the API call.
            filters: Filters to apply on the response.
            by_date: can be either published_at or harvested_at.
            indicator: Indicator to show progress of the whole process.
            url_params: Extra parameters to pass in the URL.
            json_params: Extra parameters to pass in the request body.
            request_kwargs: Keywords to pass to the post function of requests
                module. For ex: Proxy.

        Returns:
            Streams a list of signals for given parameters.
        """
        batch = self._read_date(
            mode,
            params,
            filters,
            by_date,
            indicator,
            url_params,
            json_params,
            request_kwargs)
        prev_start = params[get_by_date_after(by_date)]
        while mode.size(batch) > 0:
            try:
                date_after = mode.max_date(batch, by_date)
                yield mode.split(batch, pd.to_datetime(date_after), by_date)
                params[get_by_date_after(by_date)] = date_after
                batch = self._read_date(
                    mode,
                    params,
                    filters,
                    by_date,
                    indicator,
                    url_params,
                    json_params,
                    request_kwargs)
                if date_after == prev_start:
                    # NOTE: redundant check?
                    # batch_size becomes 0, loop gets terminated.
                    break
                prev_start = date_after
            except pd.errors.EmptyDataError:
                break

    def scroll(
            self,
            harvested_after: str,
            params: Dict[str, str],
            url_params: Optional[Dict[str, str]] = None) -> Iterator[List[T]]:
        warnings.warn(
            "scroll method is deprecated and will be removed in later "
            "versions.",
            DeprecationWarning,
            stacklevel=2)
        params["harvested_after"] = harvested_after
        return self._scroll(
            params=params,
            mode=self.get_mode(),
            indicator=self.get_indicator(),
            filters={},
            by_date="harvested_at",
            url_params=url_params)

    def read_total(
            self,
            cur_date: str,
            filters: Dict[str, FilterValue],
            request_kwargs: Optional[Dict[Any, Any]] = None) -> int:
        warnings.warn(
            "read_total method is deprecated and will be removed in later "
            "versions.",
            DeprecationWarning,
            stacklevel=2)
        return self._read_total(
            params={"date": cur_date},
            filters=filters,
            indicator=self.get_indicator(),
            request_kwargs=request_kwargs)

    def _get_valid_mode(
            self,
            mode: Optional[Union[
                Mode,
                ModeType,
                Tuple[ModeType, bool],
                Tuple[ModeType, bool, Optional[int]]
                ]],
            ) -> Mode:
        """
        Generates mode object for provided input mode.

        Parameters:
            mode: There are numerous methods by which you can set up mode here:
                1. (mode_type, split_dates), where mode_type can be one of
                    {csv, df, json} and split_dates can be True or False.
                    chunk_size is None by default in this case
                2. (mode_type, split_dates, chunk_size), where mode_type can be
                    one of {csv, df, json}, split_dates can be True or False
                    and chunk_size being an integer value.
                3. mode_type, in this case split_dates is True by default.That
                    means it's not for the combined csv mode.
                4. mode can also be any object of the class Mode. There are two
                    classes shipped with the library, CSVMode, JSONMode and can
                    be found by doing:
                        from accern_data import CSVMode, JSONMode
                5. If nothing or null value is provided, then the program will
                    take mode set by the set_mode method.

        Returns:
            A Mode object.
        """
        if mode is None:
            return self.get_mode()
        if isinstance(mode, Mode):
            return mode.get_instance()
        if isinstance(mode, str):
            return self._parse_mode(mode)
        return self._parse_mode(*mode)

    def _get_valid_filters(
            self, filters: Optional[FiltersType]) -> Dict[str, FilterValue]:
        """
        Generates an indicator object for provided input indicator.

        Parameters:
            filters: There are numerous methods by which you can set up
                filters here:
                1. By providing dictionary mapping of filters.
                2. If nothing or null value is provided, then the program will
                    take filters set by the set_filters method.

        Returns:
            Dictionary containing filters.
        """
        if filters is None:
            return self.get_filters()
        return self._parse_filters(
            {**self.get_filters(), **self._validate_filters(filters)})

    def _get_valid_indicator(
            self,
            indicator: Optional[Union[Indicators, ProgressIndicator]]
            ) -> ProgressIndicator:
        """
        Generates an indicator object for provided input indicator.

        Parameters:
            indicator: There are numerous methods by which you can set up
                indicator here:
                1. By providing indicator string which can be one of
                    {pbar, message, silent}.
                2. indicator can also be any object of the class
                    ProgressIndicator. There are three classes shipped with the
                    library, BarIndicator, MessageIndicator, SilentIndicator
                    and can be found by doing:
                        from accern_data.utils import BarIndicator,
                        MessageIndicator, SilentIndicator
                3. If nothing or null value is provided, then the program will
                    take indicator set by the set_indicator method.

        Returns:
            An indicator object.
        """
        if indicator is None:
            indicator_obj = self.get_indicator()
        elif isinstance(indicator, ProgressIndicator):
            indicator_obj = indicator
        else:
            indicator_obj = self._parse_indicator(indicator)

        if isinstance(indicator_obj, BarIndicator) and not has_iprogress():
            warnings.warn(
                "Falling back to `message` indicator.\n"
                "Reason: The jupyter extended functionality is not available. "
                "In order to activate it install using accern-data[jupyter] "
                "(e.g., `pip install accern-data[jupyter]`).",
                Warning,
                stacklevel=2)
            indicator_obj = self._parse_indicator("message")
        return indicator_obj

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
            by_date: ByDate = "published_at",
            url_params: Optional[Dict[str, str]] = None,
            json_params: Optional[Dict[str, Any]] = None,
            request_kwargs: Optional[Dict[Any, Any]] = None) -> None:
        """
        Downloads signals into files.

        Parameters:
            start_date: The starting date from where you want to download the
                data.
            end_date: The ending date till where you want to download the data.
                If provided, data would be downloaded from start_date to
                end_date (both inclusive). If not provided, then it would
                consider only start_date to download the data, i.e., download
                single day's (start_date) data.
            output_path: The path in your local file system where you want to
                store those downloaded files. By default, it points to the
                current working directory.
            output_pattern: Patterns are the file name prefix that the
                downloaded files should have.
            mode: There are numerous methods by which you can set up mode here:
                1. (mode_type, split_dates), where mode_type can be one of
                    {csv, df, json} and split_dates can be True or False.
                    chunk_size is None by default in this case
                2. (mode_type, split_dates, chunk_size), where mode_type can be
                    one of {csv, df, json}, split_dates can be True or False
                    and chunk_size being an integer value.
                3. mode_type, in this case split_dates is True by default.That
                    means it's not for the combined csv mode.
                4. mode can also be any object of the class Mode. There are two
                    classes shipped with the library, CSVMode, JSONMode and can
                    be found by doing:
                        from accern_data import CSVMode, JSONMode
                5. If nothing or null value is provided, then the program will
                    take mode set by the set_mode method.
            filters: There are numerous methods by which you can set up
                filters here:
                1. By providing dictionary mapping of filters.
                2. If nothing or null value is provided, then the program will
                    take filters set by the set_filters method.
            indicator: There are numerous methods by which you can set up
                indicator here:
                1. By providing indicator string which can be one of
                    {pbar, message, silent}.
                2. indicator can also be any object of the class
                    ProgressIndicator. There are three classes shipped with the
                    library, BarIndicator, MessageIndicator, SilentIndicator
                    and can be found by doing:
                        from accern_data.utils import BarIndicator,
                        MessageIndicator, SilentIndicator
                3. If nothing or null value is provided, then the program will
                    take indicator set by the set_indicator method.
            by_date: can be either published_at or harvested_at.
            url_params: Extra parameters to pass in the URL.
            json_params: Extra parameters to pass in the request body.
            request_kwargs: Keywords to pass to the post function of requests
                module. For ex: Proxy.
        """
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
                    valid_mode.finish_day()
                valid_mode.init_day(
                    cur_date.strftime(DATE_FORMAT),
                    opath,
                    output_pattern,
                    indicator_obj)

        for res in self.iterate_range(
                start_date=start_date,
                end_date=end_date,
                mode=mode,
                filters=filters,
                indicator=indicator,
                set_active_mode=set_active_mode,
                by_date=by_date,
                url_params=url_params,
                json_params=json_params,
                request_kwargs=request_kwargs):
            assert valid_mode is not None
            valid_mode.add_result(res)
            prev_date = cur_date

        if prev_date is not None:
            assert valid_mode is not None
            assert indicator_obj is not None
            valid_mode.finish_day(force_finish=True)

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
            by_date: ByDate = "published_at",
            url_params: Optional[Dict[str, str]] = None,
            json_params: Optional[Dict[str, Any]] = None,
            request_kwargs: Optional[Dict[Any, Any]] = None) -> Iterator[T]:
        """
        Instead of downloading the data into files, it can be kept in the
        memory(variables). This function is basically the same as
        download_range, but it yields signals, which can then be stored in
        variables for further processing.

        Parameters:
            start_date: The starting date from where you want to download the
                data.
            end_date: The ending date till where you want to download the data.
                If provided, data would be downloaded from start_date to
                end_date (both inclusive). If not provided, then it would
                consider only start_date to download the data, i.e., download
                single day's (start_date) data.
            mode: There are numerous methods by which you can set up mode here:
                1. (mode_type, split_dates), where mode_type can be one of
                    {csv, df, json} and split_dates can be True or False.
                    chunk_size is None by default in this case
                2. (mode_type, split_dates, chunk_size), where mode_type can be
                    one of {csv, df, json}, split_dates can be True or False
                    and chunk_size being an integer value.
                3. mode_type, in this case split_dates is True by default.That
                    means it's not for the combined csv mode.
                4. mode can also be any object of the class Mode. There are two
                    classes shipped with the library, CSVMode, JSONMode and can
                    be found by doing:
                        from accern_data import CSVMode, JSONMode
                5. If nothing or null value is provided, then the program will
                    take mode set by the set_mode method.
            filters: There are numerous methods by which you can set up
                filters here:
                1. By providing dictionary mapping of filters.
                2. If nothing or null value is provided, then the program will
                    take filters set by the set_filters method.
            indicator: There are numerous methods by which you can set up
                indicator here:
                1. By providing indicator string which can be one of
                    {pbar, message, silent}.
                2. indicator can also be any object of the class
                    ProgressIndicator. There are three classes shipped with the
                    library, BarIndicator, MessageIndicator, SilentIndicator
                    and can be found by doing:
                        from accern_data.utils import BarIndicator,
                        MessageIndicator, SilentIndicator
                3. If nothing or null value is provided, then the program will
                    take indicator set by the set_indicator method.
            set_active_mode: Not for end users.
            by_date: can be either published_at or harvested_at.
            url_params: Extra parameters to pass in the URL.
            json_params: Extra parameters to pass in the request body.
            request_kwargs: Keywords to pass to the post function of requests
                module. For ex: Proxy.

        Returns:
            Streams data into the memory.
        """

        # NOTE: Deprecate this.
        if by_date == "date":
            warnings.warn(
                "\"date\" is deprecated and will be removed in later "
                "versions. Use \"published_at\" instead.",
                DeprecationWarning,
                stacklevel=2)
            by_date = "published_at"

        valid_mode = self._get_valid_mode(mode)
        valid_filters = self._get_valid_filters(filters)
        valid_mode.clean_buffer()
        if end_date is None:
            end_date = start_date
        indicator_obj = self._get_valid_indicator(indicator)
        indicator_obj.generate_bar(
            total=len(pd.date_range(start_date, end_date)))
        indicator_obj.set_description(desc="Fetching info")
        overall_total = 0

        def get_min_max_date_param(
                start_date: str,
                end_date: str,
                by_date: str) -> Dict[str, str]:
            """
            Generates date range in feed API convention.
            """
            if by_date not in BY_DATE:
                raise ValueError(
                    f"Incorrect value {by_date} for by_date. "
                    f"Must be one of {BY_DATE}")
            if convert_to_date(start_date) == start_date:
                start_date = f"{start_date}T{START_TIME}"
            if convert_to_date(end_date) == end_date:
                end_date = f"{end_date}T{END_TIME}"
            return {f"min_{by_date}": start_date, f"max_{by_date}": end_date}

        overall_total = self._read_total(
            get_min_max_date_param(start_date, end_date, by_date),
            filters=valid_filters,
            indicator=indicator_obj,
            request_kwargs=request_kwargs)

        indicator_obj.set_total(total=overall_total)
        indicator_obj.set_description(desc="Downloading signals")
        indicator_obj.log(f"Expected {overall_total} signals.")

        params = get_min_max_date_param(start_date, end_date, by_date)
        params[get_by_date_after(by_date)] = "1900-01-01"
        prev_cur_date = None

        def helper(cur_date: str) -> None:
            nonlocal prev_cur_date, set_active_mode
            if set_active_mode is not None:
                set_active_mode(
                    valid_mode, pd.to_datetime(cur_date), indicator_obj)
            if prev_cur_date != cur_date:
                indicator_obj.set_description(
                    f"Downloading signals for {cur_date}")
                prev_cur_date = cur_date

        for data in self._scroll(
                valid_mode,
                params,
                valid_filters,
                by_date,
                indicator=indicator_obj,
                url_params=url_params,
                json_params=json_params,
                request_kwargs=request_kwargs):
            cur_date = valid_mode.get_current_date(data[0], by_date)
            assert cur_date is not None
            helper(cur_date)
            yield from valid_mode.iterate_data(
                data, by_date, indicator=indicator_obj, helper=helper)

        # For remaining fragment of data in csv mode only.
        # here buffer.shape < chunk_size
        buffer = valid_mode.get_buffer()
        if buffer is not None:
            indicator_obj.update(buffer.shape[0])
            yield buffer
        indicator_obj.set_description("Download complete")
        indicator_obj.close()


def create_data_client(
        url: str,
        token: str,
        n_errors: int = 5,
        indicator: Optional[Union[Indicators, ProgressIndicator]] = None,
        ) -> DataClient:
    """
    Creates client for downloading signals/data from the feed API.

    Parameters:
        url: Feed URL provided by the accern platform.
        token: Authorization token provided by the accern platform.
        n_errors: Maximum number of errors to keep in the queue.
        indicator: progress indicator of the process in form of:
            1. An interactive progress bar
            2. Message logs
            3. Silent indication (nothing at all)

    Returns:
        Client for querying the data from the feed API.
    """
    return DataClient(url, token, n_errors, indicator)


def merge_csv_file(fname: str) -> None:
    """
    Generates csv file out of header(containing columns names) & temporary
    file. After merge, columns & temporary file gets deleted.

    Parameters:
        fname: Name of header file & temporary file. This name will be same
            for both. Column file will have .~columns extension & temporary
            file will have .~tmp extension.
    """
    tmp_fname = get_tmp_file_name(fname)
    col_fname = get_header_file_name(fname)
    cols = pd.read_csv(col_fname).columns.to_list()
    total_cols = len(cols)
    with open(fname, "w", encoding="utf-8") as file, \
            open(tmp_fname, "r", encoding="utf-8") as tmp_csv:
        csv_reader = csv.reader(tmp_csv)
        csv_writer = csv.writer(file)
        csv_writer.writerow(cols)
        for row in csv_reader:
            csv_writer.writerow(
                row + [""] * (total_cols - len(row)))
    os.remove(tmp_fname)
    os.remove(col_fname)
