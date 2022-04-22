import accern_data
import pandas as pd
import pandas.testing as pd_test
import pytest
from accern_data.util import load_json


@pytest.mark.parametrize(
    "sheet_mode, uses_mode_method",
    [("csv", True), ("csv", False), ("df", True), ("df", False)])
def test_csv_date(
        sheet_mode: str, uses_mode_method: bool) -> None:
    start_date = "2022-01-03"
    end_date = "2022-03-04"
    output_path = "./tests/outputs/"
    output_pattern = "test_csv_date"
    client = accern_data.create_data_client(
        "http://api.example.com/", "SomeRandomToken")
    if uses_mode_method:
        client.set_mode(sheet_mode, split_dates=True)
        mode = None
    else:
        mode = sheet_mode
    client.download_range(
        start_date=start_date,
        output_path=output_path,
        output_pattern=output_pattern,
        end_date=end_date,
        mode=mode,
        split_dates=True,
        verbose=True)
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
    "sheet_mode, uses_mode_method",
    [("csv", True), ("csv", False), ("df", True), ("df", False)])
def test_csv_full(
        sheet_mode: str, uses_mode_method: bool) -> None:
    start_date = "2022-01-03"
    end_date = "2022-03-04"
    output_path = "./tests/outputs/"
    output_pattern = "test_csv_full"
    client = accern_data.create_data_client(
        "http://api.example.com/", "SomeRandomToken")
    if uses_mode_method:
        client.set_mode(sheet_mode, split_dates=False)
        mode = None
    else:
        mode = sheet_mode
    client.download_range(
        start_date=start_date,
        output_path=output_path,
        output_pattern=output_pattern,
        end_date=end_date,
        mode=mode,
        split_dates=False,
        verbose=True)

    df_actual = pd.read_csv("tests/data/data-2022.csv")
    df_generated = pd.read_csv(f"{output_path}{output_pattern}.csv")

    pd_test.assert_frame_equal(
        df_actual[sorted(df_actual.columns)],
        df_generated[sorted(df_generated.columns)])


@pytest.mark.parametrize("uses_mode_method", [True, False])
def test_json(uses_mode_method: bool) -> None:
    start_date = "2022-01-03"
    end_date = "2022-03-04"
    output_path = "./tests/outputs/"
    output_pattern = "test_json"
    client = accern_data.create_data_client(
        "http://api.example.com/", "SomeRandomToken")
    if uses_mode_method:
        client.set_mode("json", split_dates=True)
        mode = None
    else:
        mode = "json"
    client.download_range(
        start_date=start_date,
        output_path=output_path,
        output_pattern=output_pattern,
        end_date=end_date,
        mode=mode,
        split_dates=True,
        verbose=True)
    for cur_date in pd.date_range(start_date, end_date):
        date = cur_date.strftime("%Y-%m-%d")
        try:
            json_actual = load_json(f"tests/data/json/{date}.json")
            json_generated = load_json(
                f"{output_path}{output_pattern}-{date}.json")
        except FileNotFoundError:
            continue

        assert json_actual == json_generated
