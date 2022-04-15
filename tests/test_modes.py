import accern_data
import pandas as pd
import pandas.testing as pd_test
from accern_data.util import load_json


def test_csv_date() -> None:
    start_date = "2022-01-03"
    end_date = "2022-03-04"
    output_path = "./tests/outputs/"
    output_pattern = "test_csv_date"
    client = accern_data.create_data_client(
        "http://api.example.com/", "SomeRandomToken")
    client.set_mode("csv_date")
    client.download_range(
        start_date=start_date,
        output_path=output_path,
        output_pattern=output_pattern,
        end_date=end_date,
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


def test_csv_full() -> None:
    start_date = "2022-01-03"
    end_date = "2022-03-04"
    output_path = "./tests/outputs/"
    output_pattern = "test_csv_full"
    client = accern_data.create_data_client(
        "http://api.example.com/", "SomeRandomToken")
    client.set_mode("csv_full")
    client.download_range(
        start_date=start_date,
        output_path=output_path,
        output_pattern=output_pattern,
        end_date=end_date,
        verbose=True)

    df_actual = pd.read_csv("tests/data/data-2022.csv")
    df_generated = pd.read_csv(f"{output_path}{output_pattern}.csv")

    pd_test.assert_frame_equal(
        df_actual[sorted(df_actual.columns)],
        df_generated[sorted(df_generated.columns)])


def test_json() -> None:
    start_date = "2022-01-03"
    end_date = "2022-03-04"
    output_path = "./tests/outputs/"
    output_pattern = "test_json"
    client = accern_data.create_data_client(
        "http://api.example.com/", "SomeRandomToken")
    client.set_mode("json")
    client.download_range(
        start_date=start_date,
        output_path=output_path,
        output_pattern=output_pattern,
        end_date=end_date,
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
