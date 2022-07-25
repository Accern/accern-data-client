from datetime import datetime

import pandas as pd
import pandas.testing as pd_test
import pytest
from accern_data import ByDate, create_data_client, DATE_FORMAT
from accern_data.util import EXAMPLE_URL, load_json


@pytest.mark.parametrize("by_date", ["published_at", "harvested_at"])
def test_by_date_csv_full(by_date: ByDate) -> None:
    start_date = "2022-01-06"
    end_date = "2022-02-02"
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
    start_date_dt = pd.to_datetime(start_date, utc=True)
    end_date_dt = pd.to_datetime(end_date, utc=True) + pd.Timedelta(days=1)
    df_full[by_date] = pd.to_datetime(df_full[by_date])
    df_generated[by_date] = pd.to_datetime(df_generated[by_date])
    filtered_df = df_full[df_full[by_date].between(start_date_dt, end_date_dt)]
    filtered_df = filtered_df.reset_index(drop=True)
    pd_test.assert_frame_equal(
        filtered_df[sorted(filtered_df.columns)],
        df_generated[sorted(df_generated.columns)])


@pytest.mark.parametrize("by_date", ["published_at", "harvested_at"])
def test_by_date_csv_date(by_date: ByDate) -> None:
    start_date = "2022-01-06"
    end_date = "2022-02-02"
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
    df_full = pd.read_csv("tests/data/data-2022.csv")
    for cur_date in pd.date_range(start_date, end_date):
        date = cur_date.strftime(DATE_FORMAT)
        try:
            df_generated = pd.read_csv(
                f"{output_path}{output_pattern}-{date}.csv")
        except FileNotFoundError:
            continue
        df_generated[by_date] = pd.to_datetime(df_generated[by_date])
        df_full[by_date] = pd.to_datetime(df_full[by_date], utc=True)
        all_dates = df_generated[by_date].apply(
            datetime.strftime, format=DATE_FORMAT)
        assert all_dates.between(start_date, end_date).all()
        cur_date = pd.to_datetime(cur_date, utc=True)
        filtered_df = df_full[df_full[by_date].between(
            cur_date, cur_date + pd.Timedelta(days=1))]
        filtered_df = filtered_df.reset_index(drop=True)
        pd_test.assert_frame_equal(
            filtered_df[sorted(filtered_df.columns)],
            df_generated[sorted(df_generated.columns)])


@pytest.mark.parametrize("by_date", ["published_at", "harvested_at"])
def test_by_date_json(by_date: ByDate) -> None:
    start_date = "2022-01-06"
    end_date = "2022-02-02"
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
    json_full = load_json("tests/data/data-2022.json")
    start_date_dt = pd.to_datetime(start_date, utc=True)
    end_date_dt = pd.to_datetime(end_date, utc=True)
    for cur_date in pd.date_range(start_date, end_date):
        date = cur_date.strftime(DATE_FORMAT)
        cur_date = pd.to_datetime(cur_date, utc=True)
        try:
            json_generated = load_json(
                f"{output_path}{output_pattern}-{date}.json")
        except FileNotFoundError:
            continue

        all_dates = set()
        for obj in json_generated:
            all_dates.add(pd.to_datetime(obj[by_date]).strftime(DATE_FORMAT))

            # assert start_date_dt <= pd.to_datetime(pd.to_datetime(
            #     obj[by_date]).strftime(DATE_FORMAT)) <= end_date_dt
        print("all_dates", all_dates)
        assert pd.Series(list(all_dates)).between(start_date, end_date).all()

        filtered_json = [
            obj
            for obj in json_full["signals"]
            if
            (cur_date <= pd.to_datetime(obj[by_date], utc=True))
            and
            (pd.to_datetime(obj[by_date], utc=True) < (
                cur_date + pd.Timedelta(days=1)))
        ]

        assert filtered_json == json_generated
