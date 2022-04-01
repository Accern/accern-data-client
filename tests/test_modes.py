import pandas as pd
import pandas.testing as pd_test
import accern_data


def test_csv_date() -> None:
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
    for cur_date in pd.date_range(start_date, end_date):
        date = cur_date.strftime("%Y-%m-%d")
        try:
            df_actual = pd.read_csv(
                f"tests/data/csv_date/{date}.csv")
            df_generated = pd.read_csv(
                f"tests/outputs/test-data-2022-{date}.csv")
        except FileNotFoundError:
            pass

        pd_test.assert_frame_equal(
            df_actual[sorted(df_actual.columns)],
            df_generated[sorted(df_generated.columns)])


def test_csv_full() -> None:
    start_date = "2022-01-03"
    end_date = "2022-03-04"
    client = accern_data.create_data_client(
        "http://api.example.com/", "SomeRandomToken")
    client.set_mode("csv_full")
    client.download_range(
        start_date=start_date,
        output_path="./tests/outputs/",
        output_pattern="test-data-2022",
        end_date=end_date,
        verbose=True)

    df_actual = pd.read_csv("tests/data/data-2022.csv")
    df_generated = pd.read_csv("tests/outputs/test-data-2022.csv")

    pd_test.assert_frame_equal(
        df_actual[sorted(df_actual.columns)],
        df_generated[sorted(df_generated.columns)])
