import json

import pandas as pd
import pandas.testing as pd_test
import pytest
from accern_data.accern_data import create_data_client, DT_FORMAT, ModeType
from accern_data.util import load_json


@pytest.mark.parametrize("sheet_mode", ["csv", "df"])
def test_csv_full_csv_date_consistency(sheet_mode: ModeType) -> None:
    start_date = "2022-01-03"
    end_date = "2022-03-04"
    output_pattern = f"test_csv_full_csv_date_consistency_{sheet_mode}"
    output_path = "./tests/outputs/"
    client = create_data_client(
        "http://api.example.com/", "SomeRandomToken")
    client.set_mode(sheet_mode, split_dates=True)
    client.download_range(
        start_date=start_date,
        output_path=output_path,
        output_pattern=output_pattern,
        end_date=end_date,
        verbose=True)
    csv_date_arr = []
    for cur_date in pd.date_range(start_date, end_date):
        date = cur_date.strftime("%Y-%m-%d")
        try:
            df_generated = pd.read_csv(
                f"{output_path}{output_pattern}-{date}.csv")
            csv_date_arr.append(df_generated)
        except FileNotFoundError:
            continue
    combined_df = pd.concat(csv_date_arr)
    combined_df.reset_index(drop=True, inplace=True)
    client.set_mode(sheet_mode, split_dates=False)
    client.download_range(
        start_date=start_date,
        output_path=output_path,
        output_pattern=output_pattern,
        end_date=end_date,
        verbose=True)
    df_csv_full = pd.read_csv(f"{output_path}{output_pattern}.csv")

    pd_test.assert_frame_equal(
        df_csv_full[sorted(df_csv_full.columns)],
        combined_df[sorted(combined_df.columns)])


@pytest.mark.parametrize("sheet_mode", ["csv", "df"])
def test_json_csv_date_consistency(sheet_mode: ModeType) -> None:
    start_date = "2022-01-03"
    end_date = "2022-03-04"
    output_pattern = f"test_json_csv_date_consistency_{sheet_mode}"
    output_path = "./tests/outputs/"
    client = create_data_client(
        "http://api.example.com/", "SomeRandomToken")
    client.set_mode(sheet_mode, split_dates=True)
    client.download_range(
        start_date=start_date,
        output_path=output_path,
        output_pattern=output_pattern,
        end_date=end_date,
        verbose=True)

    client.set_mode("json", split_dates=True)
    client.download_range(
        start_date=start_date,
        output_path=output_path,
        output_pattern=output_pattern,
        end_date=end_date,
        verbose=True)
    for cur_date in pd.date_range(start_date, end_date):
        date = cur_date.strftime("%Y-%m-%d")
        try:
            json_obj = load_json(f"{output_path}{output_pattern}-{date}.json")
            csv_obj = pd.read_csv(f"{output_path}{output_pattern}-{date}.csv")
        except FileNotFoundError:
            continue
        csv_obj["event_accern_id"] = csv_obj["event_accern_id"].astype("str")
        for col in {"harvested_at", "crawled_at", "published_at"}:
            csv_obj[col] = csv_obj[col].apply(
                lambda x: pd.to_datetime(x).strftime(DT_FORMAT))
        jsonified_cols = {
            "event_hits",
            "entity_hits",
            "entity_indices",
        }
        for col in jsonified_cols:
            csv_obj[col] = csv_obj[col].apply(json.loads)
        csv_obj["entity_sector"].fillna("N/A", inplace=True)
        csv_obj.fillna("", inplace=True)
        csv_json = csv_obj.to_dict("records")
        assert csv_json == json_obj, f"Results for {date} are different."
