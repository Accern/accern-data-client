from typing import Optional, Tuple, Union

import pandas as pd
import pandas.testing as pd_test
import pytest
from accern_data.accern_data import (
    create_data_client,
    CSVMode,
    JSONMode,
    Mode,
    ModeType,
)
from accern_data.util import load_json


@pytest.mark.parametrize(
    "sheet_mode, method_used",
    [
        ("csv", "method"),
        ("csv", "string"),
        ("csv", "tuple"),
        ("csv", "object"),
        ("df", "method"),
        ("df", "string"),
        ("df", "tuple"),
    ])
def test_csv_date(sheet_mode: ModeType, method_used: str) -> None:
    start_date = "2022-01-03"
    end_date = "2022-03-04"
    output_path = "./tests/outputs/"
    output_pattern = f"test_csv_date_{sheet_mode}_{method_used}"
    client = create_data_client(
        "http://api.example.com/", "SomeRandomToken")
    if method_used == "method":
        client.set_mode(sheet_mode, split_dates=True)
        mode: Optional[Union[Mode, ModeType, Tuple[ModeType, bool]]] = None
    elif method_used == "string":
        mode = sheet_mode
    elif method_used == "tuple":
        mode = (sheet_mode, True)
    else:
        mode = CSVMode(is_by_day=True)
    client.download_range(
        start_date=start_date,
        output_path=output_path,
        output_pattern=output_pattern,
        end_date=end_date,
        mode=mode,
        indicator="message")
    for cur_date in pd.date_range(start_date, end_date):
        date = cur_date.strftime("%Y-%m-%d")
        try:
            df_actual = pd.read_csv(
                f"tests/data/csv_date/{date}.csv")
            df_generated = pd.read_csv(
                f"{output_path}{output_pattern}-{date}.csv")
        except FileNotFoundError:
            continue

        pd_test.assert_frame_equal(
            df_actual[sorted(df_actual.columns)],
            df_generated[sorted(df_generated.columns)])


@pytest.mark.parametrize(
    "sheet_mode, method_used",
    [
        ("csv", "method"),
        ("csv", "tuple"),
        ("csv", "object"),
        ("df", "method"),
        ("df", "tuple"),
    ])
def test_csv_full(sheet_mode: ModeType, method_used: str) -> None:
    start_date = "2022-01-03"
    end_date = "2022-03-04"
    output_path = "./tests/outputs/"
    output_pattern = f"test_csv_full_{sheet_mode}_{method_used}"
    client = create_data_client(
        "http://api.example.com/", "SomeRandomToken")

    if method_used == "method":
        client.set_mode(sheet_mode, split_dates=False)
        mode: Optional[Union[Mode, ModeType, Tuple[ModeType, bool]]] = None
    elif method_used == "tuple":
        mode = (sheet_mode, False)
    else:
        mode = CSVMode(is_by_day=False)

    client.download_range(
        start_date=start_date,
        output_path=output_path,
        output_pattern=output_pattern,
        end_date=end_date,
        mode=mode,
        indicator="message")

    df_actual = pd.read_csv("tests/data/data-2022.csv")
    df_generated = pd.read_csv(f"{output_path}{output_pattern}.csv")

    pd_test.assert_frame_equal(
        df_actual[sorted(df_actual.columns)],
        df_generated[sorted(df_generated.columns)])


@pytest.mark.parametrize(
    "method_used", ["method", "string", "tuple", "object"])
def test_json(method_used: str) -> None:
    start_date = "2022-01-03"
    end_date = "2022-03-04"
    output_path = "./tests/outputs/"
    output_pattern = f"test_json_{method_used}"
    client = create_data_client(
        "http://api.example.com/", "SomeRandomToken")
    if method_used == "method":
        client.set_mode("json", split_dates=True)
        mode: Optional[Union[Mode, ModeType, Tuple[ModeType, bool]]] = None
    elif method_used == "string":
        mode = "json"
    elif method_used == "tuple":
        mode = ("json", True)
    else:
        mode = JSONMode()
    client.download_range(
        start_date=start_date,
        output_path=output_path,
        output_pattern=output_pattern,
        end_date=end_date,
        mode=mode,
        indicator="message")
    for cur_date in pd.date_range(start_date, end_date):
        date = cur_date.strftime("%Y-%m-%d")
        try:
            json_actual = load_json(f"tests/data/json/{date}.json")
            json_generated = load_json(
                f"{output_path}{output_pattern}-{date}.json")
        except FileNotFoundError:
            continue

        assert json_actual == json_generated
