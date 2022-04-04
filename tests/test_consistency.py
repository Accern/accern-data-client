import pandas as pd
import pandas.testing as pd_test
import accern_data
from accern_data.util import load_json


def test_csv_full_csv_date_consistency() -> None:
    start_date = "2022-01-03"
    end_date = "2022-03-04"
    client = accern_data.create_data_client(
        "http://api.example.com/", "SomeRandomToken")
    client.set_mode("csv_date")
    client.download_range(
        start_date=start_date,
        output_path="./tests/outputs/",
        output_pattern="test-data-2022",
        end_date=end_date,
        verbose=True)
    csv_date_arr = []
    for cur_date in pd.date_range(start_date, end_date):
        date = cur_date.strftime("%Y-%m-%d")
        try:
            df_generated = pd.read_csv(
                f"tests/outputs/test-data-2022-{date}.csv")
            csv_date_arr.append(df_generated)
        except FileNotFoundError:
            continue
    combined_df = pd.concat(csv_date_arr)
    combined_df.reset_index(drop=True, inplace=True)
    client.set_mode("csv_full")
    client.download_range(
        start_date=start_date,
        output_path="./tests/outputs/",
        output_pattern="test-data-2022",
        end_date=end_date,
        verbose=True)

    df_csv_full = pd.read_csv("tests/outputs/test-data-2022.csv")

    pd_test.assert_frame_equal(
        df_csv_full[sorted(df_csv_full.columns)],
        combined_df[sorted(combined_df.columns)])


def test_json_csv_date_consistency() -> None:
    start_date = "2022-01-03"
    end_date = "2022-03-04"
    client = accern_data.create_data_client(
        "http://api.example.com/", "SomeRandomToken")
    client.set_mode("csv_date")
    client.download_range(
        start_date=start_date,
        output_path="./tests/outputs/",
        output_pattern="test-data-2022",
        end_date=end_date,
        verbose=True)

    client.set_mode("json")
    client.download_range(
        start_date=start_date,
        output_path="./tests/outputs/",
        output_pattern="test-data-2022",
        end_date=end_date,
        verbose=True)

    for cur_date in pd.date_range(start_date, end_date):
        date = cur_date.strftime("%Y-%m-%d")
        try:
            json_obj = load_json(f"tests/data/json/{date}.json")
            csv_obj = pd.read_csv(f"tests/data/csv/{date}.json")
        except FileNotFoundError:
            continue
        csv_json = csv_obj.to_dict("records")
        assert csv_json == json_obj, f"Results for {date} are different."
