from typing import List

import pandas as pd
import pandas.testing as pd_test
import pytest

from packages.python.accern_data import create_data_client
from packages.python.accern_data.util import EXAMPLE_URL


@pytest.mark.parametrize(
    "sheet_mode, chunk_size",
    [
        ("df", 1),
        ("df", 5),
        ("df", 1000),
        ("csv", 1),
        ("csv", 5),
        ("csv", 1000)
    ])
def test_csv_full_iterator(sheet_mode: str, chunk_size: int) -> None:
    start_date = "2022-01-03"
    end_date = "2022-03-04"
    client = create_data_client(EXAMPLE_URL, "SomeRandomToken")
    client.set_mode(sheet_mode, split_dates=False, chunk_size=chunk_size)
    dataframe = pd.read_csv("./tests/data/data-2022.csv")
    n_full_chunks = dataframe.shape[0]//chunk_size
    iterator = client.iterate_range(start_date=start_date, end_date=end_date)
    df_lengths = []
    dfs = []
    for df in iterator:
        df_lengths.append(df.shape[0])
        dfs.append(df)
    concat_df = pd.concat(dfs)
    assert (~concat_df.duplicated()).all(), "Duplicate entry is present."

    for idx in range(n_full_chunks):
        assert df_lengths[idx] == chunk_size
    assert dataframe.shape[0] == sum(df_lengths)


@pytest.mark.parametrize(
    "sheet_mode, chunk_size",
    [
        ("df", 1),
        ("df", 10),
        ("csv", 1),
        ("csv", 10),
    ])
def test_csv_date_iterator(sheet_mode: str, chunk_size: int) -> None:
    start_date = "2022-01-03"
    end_date = "2022-03-04"
    client = create_data_client(EXAMPLE_URL, "SomeRandomToken")
    client.set_mode(sheet_mode, split_dates=True, chunk_size=chunk_size)
    iterator = client.iterate_range(start_date=start_date, end_date=end_date)
    dfs: List[pd.DataFrame] = list(iterator)
    beg = 0
    end = 0
    for cur_date in pd.date_range(start_date, end_date):
        # print(beg, end)
        date = cur_date.strftime("%Y-%m-%d")
        df_date = []
        try:
            df = pd.read_csv(f"./tests/data/csv_date/{date}.csv")
        except FileNotFoundError:
            continue
        for idx in range(beg, len(dfs)):
            assert dfs[idx]["published_at"].nunique() == 1
            if pd.Timestamp(
                    dfs[idx]["published_at"][0]).strftime("%Y-%m-%d") != date:
                break
            end = idx
        for idx in range(beg, end+1):
            assert dfs[idx].shape[0] <= chunk_size
            df_date.append(dfs[idx])
        concat_df: pd.DataFrame = pd.concat(df_date).reset_index(drop=True)
        for dt in {"crawled_at", "harvested_at", "published_at"}:
            concat_df[dt] = concat_df[dt].astype("str")
        print("df", df["crawled_at"])
        print("concat", concat_df["crawled_at"])

        pd_test.assert_frame_equal(
            df[sorted(df.columns)], concat_df[sorted(concat_df.columns)])
        beg = end + 1






