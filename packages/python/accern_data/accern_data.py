
import json
import os
import time
import traceback
from typing import Any, Dict, Iterator, List, Optional, TypedDict, Union
import io
import pandas as pd
import requests

FiltersType = TypedDict("FiltersType", {
    "provider_ID": Optional[str],
    "entity_name": Optional[str],
    "event": Optional[str],
    "entity_ticker": Optional[str],
    "entity_accern_id": Optional[str],
}, total=False)


FilterField = {
    "provider_ID",
    "entity_name",
    "event",
    "entity_ticker",
    "entity_accern_id"
}


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
            pattern: str,
            is_first_day: bool) -> None:
        self._cur_date = cur_date
        self._cur_path = path
        self._cur_pattern = pattern
        self.do_init(is_first_day)

    def do_init(self, is_first_day: bool) -> None:
        raise NotImplementedError()

    def add_result(self, signal) -> None:
        raise NotImplementedError()

    def finish_day(self) -> None:
        raise NotImplementedError()

    def get_path(self, is_by_day: bool) -> str:
        day_str = f"-{self._cur_date}" if is_by_day else ''
        assert self._cur_path is not None and self._cur_pattern is not None
        return os.path.join(
            self._cur_path,
            f"{self._cur_pattern}{day_str}.{self.get_format()}")


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

    def size(self, batch: List[pd.DataFrame]) -> int:
        return sum(len(cur) for cur in batch)

    def max_date(self, batch: List[pd.DataFrame]) -> str:
        dates = (sorted(set(row for cur in batch for row in list(cur["harvested_at"]))))
        if len(dates) <= 1:
            return dates[0].strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        # Second last date.
        return max(dates[:-1]).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    def do_init(self, is_first_day: bool) -> None:
        fname = self.get_path(self._is_by_day)
        if is_first_day or self._is_by_day:
            pd.DataFrame([], columns=self._cols).to_csv(
                fname, index=False, header=True, mode="w")
        print(f"current file is {fname}")

    def add_result(self, signal) -> None:
        fname = self.get_path(is_by_day=self._is_by_day)
        signal.to_csv(fname, index=False, header=False, mode="a")

    def finish_day(self) -> None:
        pass


class JSONMode(Mode):
    def __init__(self, debug_json: bool = False) -> None:
        super().__init__()
        self._res = []
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
            # FIXME: need to check?
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
        dates: List[pd.Timestamp] = sorted(
            set(cur["harvested_at"] for cur in batch))
        if len(dates) <= 1:
            return dates[0].strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        return max(dates[:-1]).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    def do_init(self, is_first_day: bool) -> None:
        self._res = []

    def add_result(self, signal) -> None:
        self._res.append(signal)

    def finish_day(self) -> None:
        fname = self.get_path(is_by_day=True)
        dt_format = "%Y-%m-%dT%H:%M:%S.%fZ"
        print(f"writing results to {fname}")

        def stringify_dates(obj: Dict[str, Any]) -> Dict[str, Any]:
            if "harvested_at" in obj:
                obj["harvested_at"] = obj["harvested_at"].strftime(dt_format)
            if "published_at" in obj:
                obj["published_at"] = obj["published_at"].strftime(dt_format)
            if "crawled_at" in obj:
                obj["crawled_at"] = obj["crawled_at"].strftime(dt_format)
            return obj

        with open(fname, "w") as fout:
            json.dump(
                [
                    stringify_dates(cur)
                    for cur in self._res
                ],
                fp=fout,
                indent=2,
                sort_keys=True)


class DataClient():
    def __init__(self, url: str, token: str, filters: FiltersType) -> None:
        self._base_url = url
        self._token = token
        self._filters = self.validate_filters(filters)
        self._params: Dict[str, str] = {}
        self._mode: Optional[Mode] = None
        self._first_error = True

    @staticmethod
    def validate_filters(filters: FiltersType) -> FiltersType:
        for key in filters.keys():
            if key not in FilterField:
                raise ValueError(
                    f"{key} is not a valid filed."
                    f"Possible fileds: {FilterField}")
        return filters

    def set_mode(self, mode: str) -> None:
        all_modes = {"json", "csv_full", "csv_date"}
        if mode not in all_modes:
            raise ValueError(
                f"Please set proper mode. It is '{mode}' which is not in "
                f"{all_modes}")
        mode_mapping: Dict[str, Mode] = {
            "json": JSONMode(),
            "csv_full": CSVMode(is_by_day=False),
            "csv_date": CSVMode(is_by_day=True),
        }
        self._mode = mode_mapping[mode]
        self._params["format"] = self.get_mode().get_format()

    def get_mode(self) -> Mode:
        assert self._mode is not None, "Set mode first."
        return self._mode

    def _read_total(self) -> int:
        while True:
            try:
                resp = requests.get(
                    self._base_url,
                    params={
                        "token": self._token,
                        **{
                            key: f"{val}"
                            for key, val in self._filters.items()
                        },
                        "date": self._params["date"],
                        "format": "json",
                    })
                if not str(resp.text).strip():  # if nothing is fetched
                    return 0
                return int(resp.json()["overall_total"])
            except KeyboardInterrupt:
                raise
            except:
                if self._first_error:
                    print(traceback.format_exc())
                    self._first_error = False
                print(f"unknown error...retrying...{resp.url}")
                time.sleep(0.5)

    def _read_date(self) -> Union[List[pd.DataFrame], List[Dict[str, Any]]]:
        while True:
            try:
                resp = requests.get(
                    self._base_url,
                    params={
                        "token": self._token,
                        **{
                            key: f"{val}"
                            for key, val in self._filters.items()
                        },
                        **self._params,
                    })
                if not str(resp.text).strip():
                    return []
                return self.get_mode().parse_result(resp)
            except KeyboardInterrupt:
                raise
            except:
                if self._first_error:
                    print(traceback.format_exc())
                    self._first_error = False
                print(f"unknown error...retrying...{resp.url}")
                time.sleep(0.5)

    def _scroll(self, start_date: str) -> Iterator[pd.DataFrame]:
        print("new day")
        remainder = None
        self._params["harvested_after"] = start_date
        batch = self._read_date()
        total = self.get_mode().size(batch)
        prev_start = start_date
        while self.get_mode().size(batch) > 0:
            try:
                start_date = self.get_mode().max_date(batch)
                remainder = []
                for b in batch:
                    yield b[b['harvested_at'] <= start_date]
                    remainder.append(b[b['harvested_at'] > start_date])
                self._params["harvested_after"] = start_date
                batch = self._read_date()
                total += self.get_mode().size(batch)
                if start_date == prev_start:
                    break
                prev_start = start_date
            except pd.errors.EmptyDataError:
                break
        if remainder is None:
            yield from batch
        else:
            yield from remainder

    def _process_date(
            self,
            cur_date: str,
            output_path: str,
            output_pattern: str,
            *,
            is_first_day: bool) -> None:
        self._params["date"] = cur_date
        print(f"expected {self._read_total()}")
        first = True
        for res in self._scroll("1900-01-01"):
            if first:
                self.get_mode().init_day(
                    cur_date, output_path, output_pattern, is_first_day)
                first = False
            if not res.empty:
                self.get_mode().add_result(res)
        if not first:
            self.get_mode().finish_day()

    def download_range(
            self,
            start_date: str,
            end_date: Optional[str],
            output_path: str,
            output_pattern: str) -> None:
        if end_date is None:
            print(f"single day {start_date}")
            self._process_date(
                start_date, output_path, output_pattern, is_first_day=True)
        else:
            is_first_day = True
            for cur_date in pd.date_range(start_date, end_date):
                print(f"now processing {cur_date}")
                self._process_date(
                    cur_date.strftime("%Y-%m-%d"),
                    output_path,
                    output_pattern,
                    is_first_day=is_first_day)
                is_first_day = False


def create_data_client(
        url: str,
        token: str,
        filters: FiltersType = {}) -> DataClient:
    return DataClient(url, token, filters)
