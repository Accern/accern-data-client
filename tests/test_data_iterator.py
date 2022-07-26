from typing import Any, Dict, List, Optional

import pandas as pd
import pandas.testing as pd_test
import pytest
from accern_data import create_data_client, DATE_FORMAT, DATETIME_FORMAT
from accern_data.util import DATA_DIR, EXAMPLE_URL, load_json

DEFAULT_CHUNK_SIZE_LIST = [
    1, 5, 8, 3, 57, 13, 88, 86, 18, 9, 91, 68, 1, 99, 1, 22, 1, 12, 3, 8, 16,
    2, 68, 1, 71, 2, 81, 3, 89, 69, 1, 96, 97, 93, 17, 1, 98, 92, 97, 14, 90,
    48, 1, 99, 98, 32, 7, 95, 96, 14, 1, 98, 98, 98, 34, 5, 98, 40, 3,
]


@pytest.mark.parametrize("chunk_size", [1, 5, 1000, None])
def test_csv_full_iterator(chunk_size: Optional[int]) -> None:
    start_date = "2022-01-03"
    end_date = "2022-03-04"
    client = create_data_client(EXAMPLE_URL, "SomeRandomToken")
    client.set_mode("csv", split_dates=False, chunk_size=chunk_size)
    dataframe = pd.read_csv(f"{DATA_DIR}/data-2022.csv")
    n_full_chunks = None
    if chunk_size is not None:
        n_full_chunks = dataframe.shape[0] // chunk_size
    df_lengths = []
    dfs: List[pd.DataFrame] = []
    for df in client.iterate_range(start_date=start_date, end_date=end_date):
        df_lengths.append(df.shape[0])
        dfs.append(df)
    concat_df = pd.concat(dfs).reset_index(drop=True)
    assert (~concat_df.duplicated()).all(), "Duplicate entry is present."
    if chunk_size is not None and n_full_chunks is not None:
        for idx in range(n_full_chunks):
            assert df_lengths[idx] == chunk_size
        if dataframe.shape[0] % chunk_size != 0:
            assert df_lengths[-1] == dataframe.shape[0] % chunk_size
    else:
        for idx, df in enumerate(dfs):
            assert df.shape[0] == DEFAULT_CHUNK_SIZE_LIST[idx]
    assert dataframe.shape[0] == sum(df_lengths)
    for dt in {"crawled_at", "harvested_at", "published_at"}:
        concat_df[dt] = concat_df[dt].astype("str")
    pd_test.assert_frame_equal(
        dataframe[sorted(dataframe.columns)],
        concat_df[sorted(concat_df.columns)])


@pytest.mark.parametrize("chunk_size", [1, 10, 1000, None])
def test_csv_date_iterator(chunk_size: Optional[int]) -> None:
    start_date = "2022-01-03"
    end_date = "2022-03-04"
    client = create_data_client(EXAMPLE_URL, "SomeRandomToken")
    client.set_mode("csv", split_dates=True, chunk_size=chunk_size)
    dfs: List[pd.DataFrame] = list(
        client.iterate_range(start_date=start_date, end_date=end_date))
    beg = 0
    end = 0
    for cur_date in pd.date_range(start_date, end_date):
        date = cur_date.strftime(DATE_FORMAT)
        try:
            df = pd.read_csv(f"{DATA_DIR}/csv_date/{date}.csv")
        except FileNotFoundError:
            continue
        n_full_chunks = None
        if chunk_size is not None:
            n_full_chunks = df.shape[0] // chunk_size

        def func(row: str) -> pd.Timestamp:
            return pd.to_datetime(row, utc=True).strftime(DATE_FORMAT)

        for idx in range(beg, len(dfs)):
            assert dfs[idx]["published_at"].apply(func).nunique() == 1
            if dfs[idx]["published_at"].apply(func)[0] != date:
                break
            end = idx
        if chunk_size is not None and n_full_chunks is not None:
            for idx in range(n_full_chunks):
                assert dfs[beg+idx].shape[0] == chunk_size
            if df.shape[0] % chunk_size != 0:
                assert dfs[end].shape[0] == df.shape[0] % chunk_size
        else:
            for idx in range(beg, end+1):
                assert dfs[idx].shape[0] == DEFAULT_CHUNK_SIZE_LIST[idx]
        df_date = [dfs[idx] for idx in range(beg, end+1)]
        concat_df: pd.DataFrame = pd.concat(df_date).reset_index(drop=True)
        for dt in {"crawled_at", "harvested_at", "published_at"}:
            concat_df[dt] = concat_df[dt].astype("str")
        pd_test.assert_frame_equal(
            df[sorted(df.columns)], concat_df[sorted(concat_df.columns)])
        beg = end + 1


def test_json_iterator() -> None:
    start_date = "2022-01-03"
    end_date = "2022-03-04"
    client = create_data_client(EXAMPLE_URL, "SomeRandomToken")
    client.set_mode("json", split_dates=True)
    jsons: List[Dict[str, Any]] = list(
        client.iterate_range(start_date=start_date, end_date=end_date))
    js_total = load_json(f"{DATA_DIR}/data-2022.json")
    for obj in jsons:
        for dt in {"crawled_at", "harvested_at", "published_at"}:
            obj[dt] = obj[dt].strftime(DATETIME_FORMAT)
    assert jsons == js_total["signals"]
    beg = 0
    end = 0
    for cur_date in pd.date_range(start_date, end_date):
        date = cur_date.strftime(DATE_FORMAT)
        json_date = []
        try:
            js = load_json(f"{DATA_DIR}/json_date/{date}.json")
        except FileNotFoundError:
            continue
        for idx in range(beg, len(jsons)):
            if pd.Timestamp(
                    jsons[idx]["published_at"]).strftime(DATE_FORMAT) != date:
                break
            end = idx
        for idx in range(beg, end+1):
            json_date.append(jsons[idx])

        assert js == json_date
        beg = end + 1
