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

EXAMPLE_URL = "http://api.example.com/"
IS_JUPYTER: Optional[bool] = None
IS_TEST: Optional[bool] = None
L_BAR = """{desc}: |"""
R_BAR = """| {percentage:3.0f}% [{n}/{total}]"""
BAR_FMT = f"{L_BAR}{{bar}}{R_BAR}"


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


def generate_file_response(
        date: str,
        harvested_after: str,
        mode: str,
        filters: Dict[str, str],
        encoding: str = "utf-8") -> Response:
    response_obj = Response()
    date_dt = pd.to_datetime(date, utc=True)
    harvested_after_dt = pd.to_datetime(harvested_after, utc=True)

    if mode == "csv":
        if is_test():
            path = "tests/data/data-2022.csv"
        else:
            path = get_master_file(mode)
        df = pd.read_csv(path)
        df["harvested_at"] = pd.to_datetime(df["harvested_at"])
        df["published_at"] = pd.to_datetime(df["published_at"])

        valid_df: pd.DataFrame = df[
            (df["published_at"] == date_dt) &
            (df["harvested_at"] > harvested_after_dt)
        ]
        if valid_df.empty:
            filtered_df = valid_df
        else:
            result = pd.Series(
                [True for _ in range(valid_df.shape[0])], index=valid_df.index)
            for key, val in filters.items():
                result &= (valid_df[key].apply(field_transformation) == val)
            filtered_df = valid_df[result]
        obj = io.BytesIO()
        filtered_df.to_csv(obj, index=False)
    else:
        if is_test():
            path = "tests/data/data-2022.json"
        else:
            path = get_master_file(mode)
        json_obj = load_json(path)
        filtered_json = {
            key: val
            for key, val in json_obj.items()
            if key != "signals"
        }
        filtered_json["signals"] = []
        for record in json_obj["signals"]:
            if (
                    pd.to_datetime(record["published_at"]) == date_dt
                    and
                    pd.to_datetime(record["harvested_at"]) > harvested_after_dt
                    ) and check_filters(record, filters):
                filtered_json["signals"].append(record)
        obj = io.BytesIO(json.dumps(filtered_json).encode(encoding))
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


class ProgressBar:
    def __init__(
            self,
            total: Optional[int] = None,
            desc: Optional[str] = None,
            verbose: bool = False,
            unit_scale: bool = True) -> None:
        self._verbosity = verbose
        if verbose:
            self._pbar: Optional[tqdm.tqdm] = None
            self._total: Optional[int] = -1
        elif total is None:
            self._pbar = None
            self._total = None
        elif is_jupyter():
            self._pbar = tqdm.tqdm_notebook(
                total=total,
                desc=desc,
                unit_scale=unit_scale,
                bar_format=BAR_FMT)
        else:
            self._pbar = tqdm.tqdm(
                total=total,
                desc=desc,
                unit_scale=unit_scale,
                bar_format=BAR_FMT)

    def update(self, num: int) -> None:
        if self._pbar is not None:
            self._pbar.update(num)

    def set_description(self, desc: str) -> None:
        if self._pbar is not None:
            self._pbar.set_description_str(desc)

    def set_total(self, total: int) -> None:
        if self._pbar is not None:
            self._pbar.reset(total=total)

    def get_total(self) -> Optional[int]:
        if self._pbar is not None:
            return self._pbar.total
        return self._total

    def close(self) -> None:
        if self._pbar is not None:
            self._pbar.close()
