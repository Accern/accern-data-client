import io
import json
import os
import site
import sys
from typing import Any, Dict, Optional

import pandas as pd
import tqdm
from requests import Response

from . import __version__

EXAMPLE_URL = "https://api.example.com/"
IS_JUPYTER: Optional[bool] = None
IS_TEST: Optional[bool] = None
L_BAR = """{desc}: |"""
R_BAR = """| {percentage:3.0f}% [{n}/{total}]"""
BAR_FMT = f"{L_BAR}{{bar}}{R_BAR}"
DEFAULT_CHUNK_SIZE = 100


def is_example_url(url: str) -> bool:
    return url.startswith(EXAMPLE_URL)


def load_json(path: str) -> Any:
    with open(path, "r") as file:
        json_obj = json.load(file)
    return json_obj


def write_json(obj: Any, path: str, **kwargs: Any) -> None:
    with open(path, "w") as file:
        json.dump(obj, file, indent=4, **kwargs)


def is_test() -> int:
    global IS_TEST

    if IS_TEST is None:
        IS_TEST = int(os.environ.get("IS_TEST", "0")) != 0
    return IS_TEST


def check_filters(
        record: Dict[str, Any], filters: Dict[str, str]) -> bool:
    for key, value in filters.items():
        if field_transformation(record[key]) != value:
            return False
    return True


def field_transformation(value: Any) -> str:
    if isinstance(value, bool):
        return f"{value}".lower()
    return f"{value}"


def get_overall_total_from_dummy(
        date: str,
        filters: Dict[str, str],
        encoding: str = "utf-8") -> Response:
    response_obj = Response()
    date_dt = pd.to_datetime(date, utc=True)
    if is_test():
        path = "tests/data/data-2022.json"
    else:
        path = get_master_file("json")
    json_obj = load_json(path)
    filtered = {
        key: val
        for key, val in json_obj.items()
        if key != "signals"
    }
    filtered["signals"] = []
    overall_total = 0
    for record in json_obj["signals"]:
        if (
                pd.to_datetime(record["published_at"]) == date_dt
                and check_filters(record, filters)):
            overall_total += 1
    filtered["overall_total"] = overall_total
    obj = io.BytesIO(json.dumps(filtered).encode(encoding))
    obj.seek(0)
    response_obj._content = obj.read()
    response_obj.encoding = encoding
    response_obj.status_code = 200
    response_obj.url = path
    return response_obj


def generate_csv_object(
        path: str,
        date: pd.Timestamp,
        harvested_after: pd.Timestamp,
        filters: Dict[str, str],
        encoding: str) -> io.BytesIO:
    df = pd.read_csv(path)
    df["harvested_at"] = pd.to_datetime(df["harvested_at"])
    df["published_at"] = pd.to_datetime(df["published_at"])

    valid_df: pd.DataFrame = df[
        (df["published_at"] == date) &
        (df["harvested_at"] > harvested_after)
    ]
    if valid_df.empty:
        filtered_df = valid_df
    else:
        result = pd.Series(True, index=valid_df.index)
        for key, val in filters.items():
            result &= (valid_df[key].apply(field_transformation) == val)
        filtered_df = valid_df[result]
    obj = io.BytesIO()
    filtered_df.iloc[:DEFAULT_CHUNK_SIZE, :].to_csv(
        obj, index=False, encoding=encoding)
    return obj


def generate_json_object(
        path: str,
        date: pd.Timestamp,
        harvested_after: pd.Timestamp,
        filters: Dict[str, str],
        encoding: str) -> io.BytesIO:
    json_obj = load_json(path)
    filtered_json = {
        key: val
        for key, val in json_obj.items()
        if key != "signals"
    }
    filtered_json["signals"] = []
    for record in json_obj["signals"]:
        if (
                pd.to_datetime(record["published_at"]) == date
                and
                pd.to_datetime(record["harvested_at"]) > harvested_after
                ) and check_filters(record, filters):
            filtered_json["signals"].append(record)
    obj = io.BytesIO(json.dumps(filtered_json).encode(encoding))
    return obj


def generate_file_response(
        date: str,
        harvested_after: str,
        mode: str,
        filters: Dict[str, str],
        encoding: str = "utf-8") -> Response:
    response_obj = Response()
    date_dt = pd.to_datetime(date, utc=True)
    harvested_after_dt = pd.to_datetime(harvested_after, utc=True)

    if is_test():
        path = f"tests/data/data-2022.{mode}"
    else:
        path = get_master_file(mode)

    if mode == "csv":
        obj = generate_csv_object(
            path, date_dt, harvested_after_dt, filters, encoding)
    else:
        obj = generate_json_object(
            path, date_dt, harvested_after_dt, filters, encoding)
    obj.seek(0)
    response_obj._content = obj.read()
    response_obj.encoding = encoding
    response_obj.status_code = 200
    response_obj.url = path
    return response_obj


def get_master_file(extension: str) -> str:
    full_dir = os.path.join(
        sys.prefix, "accern_data", f"data-2022.{extension}")
    if not os.path.exists(full_dir) and site.USER_BASE is not None:
        full_dir = os.path.join(
            site.USER_BASE, "accern_data", f"data-2022.{extension}")
    return full_dir


def is_jupyter() -> bool:
    global IS_JUPYTER

    if IS_JUPYTER is not None:
        return IS_JUPYTER

    try:
        from IPython import get_ipython

        IS_JUPYTER = get_ipython() is not None
    except (NameError, ModuleNotFoundError) as _:
        IS_JUPYTER = False
    return IS_JUPYTER


class ProgressIndicator:
    def log(self, msg: str) -> None:
        raise NotImplementedError()

    def update(self, num: int) -> None:
        raise NotImplementedError()

    def set_description(self, desc: str) -> None:
        raise NotImplementedError()

    def set_total(self, total: int) -> None:
        raise NotImplementedError()

    def generate_bar(self, total: int) -> None:
        raise NotImplementedError()

    def close(self) -> None:
        raise NotImplementedError()


class BarIndicator(ProgressIndicator):
    def __init__(self) -> None:
        self._pbar: Optional[tqdm.tqdm] = None

    def generate_bar(self, total: int) -> None:
        if is_jupyter():
            self._pbar = tqdm.tqdm_notebook(total=total, bar_format=BAR_FMT)
        else:
            self._pbar = tqdm.tqdm(total=total, bar_format=BAR_FMT)

    def update(self, num: int) -> None:
        assert self._pbar is not None
        self._pbar.update(num)

    def set_description(self, desc: str) -> None:
        assert self._pbar is not None
        self._pbar.set_description_str(desc)

    def set_total(self, total: int) -> None:
        assert self._pbar is not None
        self._pbar.reset(total=total)

    def close(self) -> None:
        assert self._pbar is not None
        self._pbar.close()

    def log(self, msg: str) -> None:
        # not required in progress bar.
        pass


class MessageIndicator(ProgressIndicator):
    def log(self, msg: str) -> None:
        print(msg)

    def update(self, num: int) -> None:
        # not required in message logging.
        pass

    def set_description(self, desc: str) -> None:
        print(desc)

    def set_total(self, total: int) -> None:
        # not required in message logging.
        pass

    def generate_bar(self, total: int) -> None:
        # not required in message logging.
        pass

    def close(self) -> None:
        # not required in message logging.
        pass


class SilentIndicator(ProgressIndicator):
    def log(self, msg: str) -> None:
        # not required in silent logging.
        pass

    def update(self, num: int) -> None:
        # not required in silent logging.
        pass

    def set_description(self, desc: str) -> None:
        # not required in silent logging.
        pass

    def set_total(self, total: int) -> None:
        # not required in silent logging.
        pass

    def generate_bar(self, total: int) -> None:
        # not required in silent logging.
        pass

    def close(self) -> None:
        # not required in silent logging.
        pass
