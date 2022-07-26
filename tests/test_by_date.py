from datetime import datetime

import pandas as pd
import pandas.testing as pd_test
import pytest
from accern_data import ByDate, create_data_client, DATE_FORMAT
from accern_data.util import EXAMPLE_URL, load_json


@pytest.mark.parametrize("by_date", ["published_at", "harvested_at"])
def test_by_date_csv_full(by_date: ByDate) -> None:
    start_date = "2022-01-03"
    end_date = "2022-03-04"
    output_path = "tests/outputs/"
    output_pattern = f"test_by_date_csv_full_{by_date}"
    client = create_data_client(EXAMPLE_URL, "SomeRandomToken")

    client.download_range(
        start_date=start_date,
        output_path=output_path,
        output_pattern=output_pattern,
        end_date=end_date,
        mode=("csv", False),
        indicator="message",
        by_date=by_date)
    df_generated = pd.read_csv(f"{output_path}{output_pattern}.csv")
    df_full = pd.read_csv("tests/data/data-2022.csv")
    if by_date != "published_at":
        df_full = pd.read_csv(f"tests/data/data-2022-{by_date}.csv")
    # start_date_dt = pd.to_datetime(start_date, utc=True)
    # end_date_dt = pd.to_datetime(end_date, utc=True) + pd.Timedelta(days=1)
    # df_full[by_date] = pd.to_datetime(df_full[by_date])
    # df_generated[by_date] = pd.to_datetime(df_generated[by_date])
    # filtered_df = df_full[df_full[by_date].between(start_date_dt, end_date_dt)]
    # filtered_df = filtered_df.reset_index(drop=True)
    pd_test.assert_frame_equal(
        df_full[sorted(df_full.columns)],
        df_generated[sorted(df_generated.columns)])


@pytest.mark.parametrize("by_date", ["published_at", "harvested_at"])
def test_by_date_csv_date(by_date: ByDate) -> None:
    start_date = "2022-01-03"
    end_date = "2022-03-04"
    output_path = "tests/outputs/"
    output_pattern = f"test_by_date_csv_date_{by_date}"
    client = create_data_client(EXAMPLE_URL, "SomeRandomToken")

    client.download_range(
        start_date=start_date,
        output_path=output_path,
        output_pattern=output_pattern,
        end_date=end_date,
        mode=("csv", True),
        indicator="message",
        by_date=by_date)
    for cur_date in pd.date_range(start_date, end_date):
        date = cur_date.strftime(DATE_FORMAT)
        try:
            df_generated = pd.read_csv(
                f"{output_path}{output_pattern}-{date}.csv")
            path = f"tests/data/csv_date/{cur_date}.csv"
            if by_date != "published_at":
                path = f"tests/data/{by_date}/csv_date/{cur_date}.csv"
            df_actual = pd.read_csv(path)
        except FileNotFoundError:
            continue
        pd_test.assert_frame_equal(
            df_actual[sorted(df_actual.columns)],
            df_generated[sorted(df_generated.columns)])


@pytest.mark.parametrize("by_date", ["published_at", "harvested_at"])
def test_by_date_json(by_date: ByDate) -> None:
    start_date = "2022-01-03"
    end_date = "2022-03-04"
    output_path = "tests/outputs/"
    output_pattern = f"test_by_date_json_{by_date}"
    client = create_data_client(EXAMPLE_URL, "SomeRandomToken")

    client.download_range(
        start_date=start_date,
        output_path=output_path,
        output_pattern=output_pattern,
        end_date=end_date,
        mode=("json", True),
        indicator="message",
        by_date=by_date)
    for cur_date in pd.date_range(start_date, end_date):
        date = cur_date.strftime(DATE_FORMAT)
        cur_date = pd.to_datetime(cur_date, utc=True)
        try:
            json_generated = load_json(
                f"{output_path}{output_pattern}-{date}.json")
            path = f"tests/data/json/{cur_date}.csv"
            if by_date != "published_at":
                path = f"tests/data/{by_date}/json/{cur_date}.csv"
            json_actual = load_json(path)
        except FileNotFoundError:
            continue
        assert json_actual == json_generated
