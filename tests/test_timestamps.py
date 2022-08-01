import pandas as pd
import pandas.testing as pd_test
from accern_data import create_data_client, DATE_FORMAT
from accern_data.util import EXAMPLE_URL, get_data_dir, load_json, set_data_dir

DATA_PATH = "tests/data_mini"
OUTPUT_PATH = "tests/outputs/"


def test_timestamp_csv_date() -> None:
    set_data_dir(DATA_PATH)
    start_date = "2022-01-07T05:04:11"
    end_date = "2022-02-03T03:28:09"
    output_path = OUTPUT_PATH
    output_pattern = "test_timestamp_csv_date"
    client = create_data_client(EXAMPLE_URL, "SomeRandomToken")

    client.download_range(
        start_date=start_date,
        output_path=output_path,
        output_pattern=output_pattern,
        end_date=end_date,
        mode=("csv", True),
        indicator="message")
    start_date_dt = pd.to_datetime(start_date, utc=True)
    end_date_dt = pd.to_datetime(end_date, utc=True)
    for cur_date in pd.date_range(start_date, end_date):
        date = cur_date.strftime(DATE_FORMAT)
        try:
            df_actual = pd.read_csv(f"{get_data_dir()}/csv_date/{date}.csv")
            df_generated = pd.read_csv(
                f"{output_path}{output_pattern}-{date}.csv")
        except FileNotFoundError:
            continue
        filtered_df = df_actual[
            (start_date_dt <= pd.to_datetime(
                df_actual["published_at"], utc=True)) &
            (pd.to_datetime(
                df_actual["published_at"], utc=True) <= end_date_dt)]
        filtered_df = filtered_df.reset_index(drop=True)
        pd_test.assert_frame_equal(
            filtered_df[sorted(filtered_df.columns)],
            df_generated[sorted(df_generated.columns)])


def test_timestamp_csv_full() -> None:
    set_data_dir(DATA_PATH)
    start_date = "2022-01-07T05:04:11"
    end_date = "2022-02-03T03:28:09"
    output_path = OUTPUT_PATH
    output_pattern = "test_timestamp_csv_full"
    client = create_data_client(EXAMPLE_URL, "SomeRandomToken")

    client.download_range(
        start_date=start_date,
        output_path=output_path,
        output_pattern=output_pattern,
        end_date=end_date,
        mode=("csv", False),
        indicator="message")

    df_actual = pd.read_csv(f"{get_data_dir()}/data-2022.csv")
    df_generated = pd.read_csv(f"{output_path}{output_pattern}.csv")

    start_date_dt = pd.to_datetime(start_date, utc=True)
    end_date_dt = pd.to_datetime(end_date, utc=True)
    filtered_df = df_actual[
            (start_date_dt <= pd.to_datetime(
                df_actual["published_at"], utc=True)) &
            (pd.to_datetime(
                df_actual["published_at"], utc=True) <= end_date_dt)]
    filtered_df = filtered_df.reset_index(drop=True)
    df_generated = df_generated.reset_index(drop=True)
    pd_test.assert_frame_equal(
        filtered_df[sorted(filtered_df.columns)],
        df_generated[sorted(df_generated.columns)])


def test_timestamp_json() -> None:
    set_data_dir(DATA_PATH)
    start_date = "2022-01-07T05:04:11"
    end_date = "2022-02-03T03:28:09"
    output_path = "tests/outputs/"
    output_pattern = "test_timestamp_json"
    client = create_data_client(EXAMPLE_URL, "SomeRandomToken")

    client.download_range(
        start_date=start_date,
        output_path=output_path,
        output_pattern=output_pattern,
        end_date=end_date,
        mode=("json", True),
        indicator="message")
    start_date_dt = pd.to_datetime(start_date, utc=True)
    end_date_dt = pd.to_datetime(end_date, utc=True)
    for cur_date in pd.date_range(start_date, end_date):
        date = cur_date.strftime(DATE_FORMAT)
        try:
            json_actual = load_json(f"{get_data_dir()}/json/data-2022.json")
            json_generated = load_json(
                f"{output_path}{output_pattern}-{date}.json")
        except FileNotFoundError:
            continue
        filtered_json = [
            obj for obj in json_actual
            if (start_date_dt <= pd.to_datetime(obj["published_at"], utc=True))
            and (pd.to_datetime(obj["published_at"], utc=True) <= end_date_dt)
        ]
        assert json_generated == filtered_json, f"Failing for {date}."
