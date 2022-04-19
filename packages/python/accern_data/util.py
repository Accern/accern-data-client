import io
import json
import os
from typing import Any, Optional

import pandas as pd
import requests
import tqdm
from requests import Response

EXAMPLE_URL = "http://api.example.com/"
IS_JUPYTER: Optional[bool] = None
L_BAR = """{desc}: |"""  # FIXME
R_BAR = """| {percentage:3.0f}% [{n}/{total}]"""  # FIXME
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


def check_is_test() -> bool:
    if os.environ.get("IS_TEST", "0") == "0":
        return False
    return True


def get_overall_total_from_dummy(
        date: str, encoding: str = "utf-8") -> Response:
    response_obj = Response()
    date_dt = pd.to_datetime(date, utc=True)
    is_test = check_is_test()
    if is_test:
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
        if pd.to_datetime(record["published_at"]) == date_dt:
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
        encoding: str = "utf-8") -> Response:
    is_test = check_is_test()
    response_obj = Response()
    date_dt = pd.to_datetime(date, utc=True)
    harvested_after_dt = pd.to_datetime(harvested_after, utc=True)
    if mode == "csv":
        if is_test:
            path = "tests/data/data-2022.csv"
        else:
            path = get_master_file(mode)
        df = pd.read_csv(path)
        df["harvested_at"] = pd.to_datetime(df["harvested_at"])
        df["published_at"] = pd.to_datetime(df["published_at"])

        filtered = df[
            (df["published_at"] == date_dt) &
            (df["harvested_at"] > harvested_after_dt)
        ]
        obj = io.BytesIO()
        filtered.to_csv(obj, index=False)
    else:
        if is_test:
            path = "tests/data/data-2022.json"
        else:
            path = get_master_file(mode)
        json_obj = load_json(path)
        filtered = {
            key: val
            for key, val in json_obj.items()
            if key != "signals"
        }
        filtered["signals"] = []
        for record in json_obj["signals"]:
            if (
                    pd.to_datetime(record["published_at"]) == date_dt
                    and
                    pd.to_datetime(record["harvested_at"]) > harvested_after_dt
                    ):
                filtered["signals"].append(record)
        obj = io.BytesIO(json.dumps(filtered).encode(encoding))
    obj.seek(0)
    response_obj._content = obj.read()
    response_obj.encoding = encoding
    response_obj.status_code = 200
    response_obj.url = path
    return response_obj


def get_master_file(file: str) -> str:
    import accern_data
    directory = os.path.split(accern_data.__file__)[0]
    full_dir = os.path.join(directory, "data", f"data-2022.{file}")
    if os.path.exists(full_dir):
        return full_dir
    url = (
        "https://raw.githubusercontent.com/Accern/accern-data-client/main/"
        f"tests/data/data-2022.{file}")
    response = requests.get(url)
    assert response.status_code == 200
    with open(full_dir, "w") as file_obj:
        file_obj.write(response.text)
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
            total: int,
            desc: str,
            verbose: bool,
            unit_scale: bool = True) -> None:
        self._verbosity = verbose
        if verbose:
            self._pbar: Optional[tqdm.tqdm] = None
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

    def close(self) -> None:
        if self._pbar is not None:
            self._pbar.close()
