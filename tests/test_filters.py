import pandas as pd
import pytest
from accern_data import create_data_client, DATE_FORMAT, FiltersType, ModeType
from accern_data.util import (
    EXAMPLE_URL,
    field_transformation,
    load_json,
    set_data_dir,
)

FILTERS: FiltersType = {
    "provider_id": 5,
    "entity_name": "Hurco Companies, Inc.",
    "entity_ticker": "HURC",
    "entity_accern_id": "BBG000BLLFK1",
}
DATA_PATH = "tests/data_mini"
OUTPUT_PATH = "tests/outputs/"


@pytest.mark.parametrize("sheet_mode", ["csv", "df"])
@pytest.mark.parametrize("uses_filter_method", [True, False])
def test_filters_csv_full(
        sheet_mode: ModeType, uses_filter_method: bool) -> None:
    set_data_dir(DATA_PATH)
    start_date = "2022-01-03"
    end_date = "2022-03-04"
    output_path = OUTPUT_PATH
    output_pattern = f"test_filters_csv_full_{sheet_mode}_{uses_filter_method}"
    client = create_data_client(EXAMPLE_URL, "SomeRandomToken")
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
        indicator="message")

    df = pd.read_csv(f"{output_path}{output_pattern}.csv")
    for key, value in client.get_filters().items():
        transformed_val = field_transformation(value)
        transformed_col = df[key].apply(field_transformation)
        assert (transformed_col == transformed_val).all(), \
            f"Column {key} of dataframe does not match with the value: {value}"


@pytest.mark.parametrize("sheet_mode", ["csv", "df"])
@pytest.mark.parametrize("uses_filter_method", [True, False])
def test_filters_csv_date(
        sheet_mode: ModeType, uses_filter_method: bool) -> None:
    set_data_dir(DATA_PATH)
    start_date = "2022-01-03"
    end_date = "2022-03-04"
    output_path = OUTPUT_PATH
    output_pattern = f"test_filters_csv_date_{sheet_mode}_{uses_filter_method}"
    client = create_data_client(EXAMPLE_URL, "SomeRandomToken")
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
        indicator="message")

    for cur_date in pd.date_range(start_date, end_date):
        date = cur_date.strftime(DATE_FORMAT)
        try:
            df = pd.read_csv(f"{output_path}{output_pattern}-{date}.csv")
        except FileNotFoundError:
            continue
        for key, value in client.get_filters().items():
            transformed_val = field_transformation(value)
            transformed_col = df[key].apply(field_transformation)
            assert (transformed_col == transformed_val).all(), (
                f"Column {key} of dataframe does not match with the value: "
                f"{value}")


@pytest.mark.parametrize("uses_filter_method", [True, False])
def test_filters_json(uses_filter_method: bool) -> None:
    set_data_dir(DATA_PATH)
    start_date = "2022-01-03"
    end_date = "2022-03-04"
    output_path = OUTPUT_PATH
    output_pattern = f"test_filters_json_{uses_filter_method}"
    client = create_data_client(EXAMPLE_URL, "SomeRandomToken")
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
        indicator="message")

    for cur_date in pd.date_range(start_date, end_date):
        date = cur_date.strftime(DATE_FORMAT)
        try:
            json_obj = load_json(f"{output_path}{output_pattern}-{date}.json")
        except FileNotFoundError:
            continue

        for rec in json_obj:
            for key, value in client.get_filters().items():
                assert field_transformation(rec[key]) == field_transformation(
                    value), f"expected {value} for {key}, but got {rec[key]}"
