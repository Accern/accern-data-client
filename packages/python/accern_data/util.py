import io
import json
import os
import site
import sys
from typing import Any, Dict, List, Optional, Tuple, TYPE_CHECKING, Union

import pandas as pd
import tqdm
from requests import Response

from . import __version__

if TYPE_CHECKING:
    from .accern_data import FilterValue

EXAMPLE_URL = "https://api.example.com/"
IS_JUPYTER: Optional[bool] = None
IS_TEST: Optional[bool] = None
HAS_IPROGRESS: Optional[bool] = None
L_BAR = """{desc}: |"""
R_BAR = """| {percentage:3.0f}% [{n}/{total}]"""
BAR_FMT = f"{L_BAR}{{bar}}{R_BAR}"
DEFAULT_CHUNK_SIZE = 100
DATA_DIR = "tests/data"
DATETIME_FORMAT = r"%Y-%m-%dT%H:%M:%S.%fZ"
DATE_FORMAT = r"%Y-%m-%d"
TIME_FORMAT = r"%H:%M:%S.000Z"
START_TIME = "00:00:00.000Z"
END_TIME = "23:59:59.999Z"


def is_example_url(url: str) -> bool:
    return url.startswith(EXAMPLE_URL)


def load_json(path: str) -> Any:
    """
    Helper function for loading a JSON file.
    """
    with open(path, "r") as file:
        json_obj = json.load(file)
    return json_obj


def write_json(obj: Any, path: str, **kwargs: Any) -> None:
    """
    Helper function for writing a JSON file.
    """
    with open(path, "w") as file:
        json.dump(obj, file, indent=4, **kwargs)


def is_test() -> int:
    """
    Accern data client can be executed in two ways. One is actual execution
    that requires real world data and the other one is test execution which
    requires dummy data to ensure proper functioning of the code. This function
    returns True if it is a test execution otherwise False.
    """
    global IS_TEST

    if IS_TEST is None:
        IS_TEST = int(os.environ.get("IS_TEST", "0")) != 0
    return IS_TEST


def set_data_dir(path: str) -> None:
    """
    Function used to set the dummy data directory.

    Parameters:
        path: dummy data directory path.
    """
    global DATA_DIR
    DATA_DIR = path


def get_data_dir() -> str:
    """
    Function used to retrieve the dummy data directory.

    Returns:
        Dummy data directory path.
    """
    return DATA_DIR


def check_filters(
        record: Dict[str, Any], filters: Dict[str, 'FilterValue']) -> bool:
    """
    Checks if an input dictionary contains values provided by the filter
    object.

    Parameters:
        record: dictionary to check.
        filters: filter values to check for.

    Returns:
        True if the input dictionary contains filter values otherwise False.
    """

    for key, value in filters.items():
        transformed_val = field_transformation(value)
        if isinstance(transformed_val, list):
            if field_transformation(record[key]) not in transformed_val:
                return False
        if field_transformation(record[key]) != transformed_val:
            return False
    return True


def field_transformation(value: Any) -> Union[str, List[str]]:
    if isinstance(value, list):
        for idx, item in enumerate(value):
            value[idx] = f"{item}"
        return value
    return f"{value}"


def get_date_type(obj: Dict[str, str]) -> str:
    if "min_published_at" in obj.keys():
        return "published_at"
    return "harvested_at"


def get_overall_total_from_dummy(
        params: Dict[str, str],
        filters: Dict[str, 'FilterValue'],
        encoding: str = "utf-8") -> Response:
    """
    Mocks overall total (refer this term with respect to feed API) for a
    combination of parameters.

    Parameters:
        params: Parameters of the API call.
        filters: Filters to apply on the response.
        encoding: Response encoding.

    Returns:
        A response containing data that follow rules as provided by params &
        filters.
    """
    response_obj = Response()
    date_type = get_date_type(params)
    start_dt, end_dt = get_min_max_dates(params, date_type)
    if is_test():
        path = f"{get_data_dir()}/data-2022.json"
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
                pd.to_datetime(record[date_type]) >= start_dt
                and pd.to_datetime(record[date_type]) <= end_dt
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


def get_min_max_dates(
        params: Dict[str, str],
        by_date: str) -> Tuple[pd.Timestamp, pd.Timestamp]:
    """
    Generates date range.

    Parameters:
        params: Parameters of the API call.
        by_date: can be either published_at or harvested_at.

    Returns:
        Tuple containing start & end date.
    """
    start_dt = pd.to_datetime(params[f"min_{by_date}"], utc=True)
    end_dt = pd.to_datetime(params[f"max_{by_date}"], utc=True)
    return (start_dt, end_dt)


def generate_csv_object(
        path: str,
        params: Dict[str, str],
        date_after: pd.Timestamp,
        filters: Dict[str, 'FilterValue'],
        by_date: str,
        encoding: str) -> io.BytesIO:
    """
    Mocks CSV file creation capability of actual API.

    Parameters:
        path: Dummy file path.
        params: Parameters of the API call.
        date_after: Date to paginate after.
        filters:  Filters to apply on the response.
        by_date: can be either published_at or harvested_at.
        encoding: Response encoding.

    Returns:
        Bytes object containing data in CSV format.
    """
    df = pd.read_csv(path)
    df["harvested_at"] = pd.to_datetime(df["harvested_at"])
    df["published_at"] = pd.to_datetime(df["published_at"])
    date_type = get_date_type(params)
    start_dt, end_dt = get_min_max_dates(params, date_type)
    valid_df: pd.DataFrame = df[
        (df[date_type] >= start_dt) &
        (df[date_type] <= end_dt) &
        (df[by_date] > date_after)
    ]
    valid_df = valid_df.sort_values(by=[by_date, "signal_id"])
    if valid_df.empty:
        filtered_df = valid_df
    else:
        result = pd.Series(True, index=valid_df.index)
        for key, val in filters.items():
            transformed_val = field_transformation(val)
            transformed_col = valid_df[key].apply(field_transformation)
            if isinstance(val, list):
                result &= transformed_col.isin(transformed_val)
            else:
                result &= (transformed_col == transformed_val)
        filtered_df = valid_df[result]
    obj = io.BytesIO()
    for col in filtered_df.columns:
        if filtered_df.loc[:, col].isna().all():
            filtered_df = filtered_df.drop(col, axis=1)
    size = int(params.get("size", DEFAULT_CHUNK_SIZE))
    filtered_df.iloc[:size, :].to_csv(
        obj, index=False, encoding=encoding)
    return obj


def generate_json_object(
        path: str,
        params: Dict[str, str],
        date_after: pd.Timestamp,
        filters: Dict[str, 'FilterValue'],
        by_date: str,
        encoding: str) -> io.BytesIO:
    """
    Mocks JSON file creation capability of actual API.

    Parameters:
        path: Dummy file path.
        params: Parameters of the API call.
        date_after: Date to paginate after.
        filters:  Filters to apply on the response.
        by_date: can be either published_at or harvested_at.
        encoding: Response encoding.

    Returns:
        Bytes object containing data in JSON format.
    """
    json_obj = load_json(path)
    date_type = get_date_type(params)
    filtered_json = {
        key: val
        for key, val in json_obj.items()
        if key != "signals"
    }
    start_dt, end_dt = get_min_max_dates(params, date_type)
    filtered_json["signals"] = []
    for record in json_obj["signals"]:
        if (
                pd.to_datetime(record[date_type]) >= start_dt
                and pd.to_datetime(record[date_type]) <= end_dt
                and pd.to_datetime(record[by_date]) > date_after
                ) and check_filters(record, filters):
            filtered_json["signals"].append(record)
    filtered_json["signals"].sort(
        key=lambda x: (pd.to_datetime(x[by_date]), x["signal_id"]))
    obj = io.BytesIO(json.dumps(filtered_json).encode(encoding))
    return obj


def generate_file_response(
        params: Dict[str, str],
        mode: str,
        filters: Dict[str, 'FilterValue'],
        by_date: str,
        encoding: str = "utf-8") -> Response:
    """
    Mocks file creation capability of actual API.

    Parameters:
        params: Parameters of the API call.
        mode: Type of response. Can be either csv or json.
        filters:  Filters to apply on the response.
        by_date: can be either published_at or harvested_at.
        encoding: Response encoding.

    Returns:
        Bytes object containing data in CSV format.
    """
    response_obj = Response()
    date_after_dt = pd.to_datetime(
        params[get_by_date_after(by_date)], utc=True)

    if is_test():
        path = f"{get_data_dir()}/data-2022.{mode}"
    else:
        path = get_master_file(mode)

    if mode == "csv":
        obj = generate_csv_object(
            path, params, date_after_dt, filters, by_date, encoding)
    else:
        obj = generate_json_object(
            path, params, date_after_dt, filters, by_date, encoding)
    obj.seek(0)
    response_obj._content = obj.read()
    response_obj.encoding = encoding
    response_obj.status_code = 200
    response_obj.url = path
    return response_obj


def get_master_file(extension: str) -> str:
    """
    This function is used to get the dummy/mock file name.

    Parameters:
        extension: Type of file, csv or json.

    Returns:
        File path.
    """
    full_dir = os.path.join(
        sys.prefix, "accern_data", f"data-2022.{extension}")
    if not os.path.exists(full_dir) and site.USER_BASE is not None:
        full_dir = os.path.join(
            site.USER_BASE, "accern_data", f"data-2022.{extension}")
    return full_dir


def is_jupyter() -> bool:
    """
    This function is used to check whether current environment is jupiter or
    not.
    """
    global IS_JUPYTER

    if IS_JUPYTER is not None:
        return IS_JUPYTER

    try:
        from IPython import get_ipython

        IS_JUPYTER = get_ipython() is not None
    except (NameError, ModuleNotFoundError) as _:
        IS_JUPYTER = False
    return IS_JUPYTER


def get_tmp_file_name(fname: str) -> str:
    return f"{fname}.~tmp"


def get_header_file_name(fname: str) -> str:
    return f"{fname}.~columns"


def micro_to_millisecond(timestamp: str) -> str:
    return f"{timestamp[:-4]}Z"


def get_by_date_after(by_date: str) -> str:
    return f"{by_date[:-3]}_after"


def convert_to_date(date: str) -> str:
    return pd.to_datetime(date).strftime(DATE_FORMAT)


class ProgressIndicator:
    """
    Class for indicating progress of the process.
    """
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
    """
    Class for indicating progress of the process in form of an interactive
    progress bar. This is the default indicator.
    """
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
    """
    Class for indicating progress of the process in form of message logs. It
    prints log messages to stdout.
    """
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
    """
    Class for indicating progress of the process silently. Does not show
    anything. Keeps output stream clean. Quite ironical!
    """

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


def has_iprogress() -> bool:
    """
    Function to check whether current environment has IProgress or not.
    """
    global HAS_IPROGRESS

    if HAS_IPROGRESS is not None:
        return HAS_IPROGRESS

    from tqdm import notebook
    HAS_IPROGRESS = notebook.IProgress is not None  # type: ignore
    return HAS_IPROGRESS
