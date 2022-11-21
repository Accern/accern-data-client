import pandas as pd
import pandas.testing as pd_test
from accern_data import create_data_client
from accern_data.util import EXAMPLE_URL, get_data_dir, set_data_dir

DATA_PATH = "tests/data_with_missing_fields"
OUTPUT_PATH = "tests/outputs/"


def test_inconsistent_fields_csv_full() -> None:
    set_data_dir(DATA_PATH)
    start_date = "2022-01-03"
    end_date = "2022-03-04"
    output_path = OUTPUT_PATH
    output_pattern = "test_inconsistent_fields_csv_full"
    client = create_data_client(EXAMPLE_URL, "SomeRandomToken")
    client.set_mode("csv", split_dates=False, chunk_size=60)

    client.download_range(
        start_date=start_date,
        output_path=output_path,
        output_pattern=output_pattern,
        end_date=end_date,
        indicator="message",
        url_params={
            "size": 36
        })

    df_gen = pd.read_csv(f"{output_path}{output_pattern}.csv")
    df_actual = pd.read_csv(f"{get_data_dir()}/data-2022.csv")

    pd_test.assert_frame_equal(
        df_actual[sorted(df_actual.columns)],
        df_gen[sorted(df_gen.columns)])
