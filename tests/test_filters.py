import pandas as pd
import pytest
from accern_data import create_data_client, FiltersType, ModeType
from accern_data.util import field_transformation, load_json

FILTERS: FiltersType = {
    "provider_id": 5,
    "entity_name": "Hurco Companies, Inc.",
    "event": "Governance - Product Development, R&D and Innovation",
    "entity_ticker": "HURC",
    "entity_accern_id": "BBG000BLLFK1",
}


@pytest.mark.parametrize(
    "sheet_mode, uses_filter_method",
    [("csv", True), ("csv", False), ("df", True), ("df", False)])
def test_filters_csv_full(
        sheet_mode: ModeType, uses_filter_method: bool) -> None:
    start_date = "2022-01-03"
    end_date = "2022-03-04"
    output_path = "./tests/outputs/"
    output_pattern = f"test_filters_csv_full_{sheet_mode}_{uses_filter_method}"
    client = create_data_client(
        "http://api.example.com/", "SomeRandomToken")
    client.set_mode(sheet_mode, split_dates=False)
    if uses_filter_method:
        client.set_filters(FILTERS)
        filters = None
    else:
        filters = FILTERS

    client.download_range(
        start_date=start_date,
        output_path=output_path,
        output_pattern=output_pattern,
        end_date=end_date,
        filters=filters,
        verbose=True)

    df = pd.read_csv(f"{output_path}{output_pattern}.csv")
    for key, value in client.get_filters().items():
        assert (df[key].apply(field_transformation) == value).all(), \
            f"Column {key} of dataframe does not match with the value: {value}"


@pytest.mark.parametrize(
    "sheet_mode, uses_filter_method",
    [("csv", True), ("csv", False), ("df", True), ("df", False)])
def test_filters_csv_date(
        sheet_mode: ModeType, uses_filter_method: bool) -> None:
    start_date = "2022-01-03"
    end_date = "2022-03-04"
    output_path = "./tests/outputs/"
    output_pattern = f"test_filters_csv_date_{sheet_mode}_{uses_filter_method}"
    client = create_data_client(
        "http://api.example.com/", "SomeRandomToken")
    client.set_mode(sheet_mode, split_dates=True)
    if uses_filter_method:
        client.set_filters(FILTERS)
        filters = None
    else:
        filters = FILTERS

    client.download_range(
        start_date=start_date,
        output_path=output_path,
        output_pattern=output_pattern,
        end_date=end_date,
        filters=filters,
        verbose=True)

    for cur_date in pd.date_range(start_date, end_date):
        date = cur_date.strftime("%Y-%m-%d")
        try:
            df = pd.read_csv(f"{output_path}{output_pattern}-{date}.csv")
        except FileNotFoundError:
            continue
        for key, value in client.get_filters().items():
            assert (df[key].apply(field_transformation) == value).all(), (
                f"Column {key} of dataframe does not match with the value: "
                f"{value}")


@pytest.mark.parametrize("uses_filter_method", [True, False])
def test_filters_json(uses_filter_method: bool) -> None:
    start_date = "2022-01-03"
    end_date = "2022-03-04"
    output_path = "./tests/outputs/"
    output_pattern = f"test_filters_json_{uses_filter_method}"
    client = create_data_client(
        "http://api.example.com/", "SomeRandomToken")
    client.set_mode("json", split_dates=True)
    if uses_filter_method:
        client.set_filters(FILTERS)
        filters = None
    else:
        filters = FILTERS

    client.download_range(
        start_date=start_date,
        output_path=output_path,
        output_pattern=output_pattern,
        end_date=end_date,
        filters=filters,
        verbose=True)

    for cur_date in pd.date_range(start_date, end_date):
        date = cur_date.strftime("%Y-%m-%d")
        try:
            json_obj = load_json(f"{output_path}{output_pattern}-{date}.json")
        except FileNotFoundError:
            continue

        for rec in json_obj:
            for key, value in client.get_filters().items():
                assert field_transformation(rec[key]) == value, \
                    f"expected {value} for {key}, but got {rec[key]}"
