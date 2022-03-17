# Stubs for pandas.tests.indexing.multiindex.test_loc (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.
# pylint: disable=unused-argument,redefined-outer-name,no-self-use,invalid-name
# pylint: disable=relative-beyond-top-level,line-too-long,arguments-differ
# pylint: disable=no-member,too-few-public-methods,keyword-arg-before-vararg
# pylint: disable=super-init-not-called,abstract-method,redefined-builtin

from typing import Any

def single_level_multiindex():
    ...

def frame_random_data_integer_multi_index():
    ...


class TestMultiIndexLoc:
    def test_loc_getitem_series(self) -> None:
        ...

    def test_loc_getitem_array(self) -> None:
        ...

    def test_loc_multiindex_labels(self) -> None:
        ...

    def test_loc_multiindex_ints(self) -> None:
        ...

    def test_loc_multiindex_missing_label_raises(self) -> None:
        ...

    def test_loc_multiindex_list_missing_label(self, key: Any, pos: Any) -> None:
        ...

    def test_loc_multiindex_too_many_dims_raises(self) -> None:
        ...

    def test_loc_multiindex_indexer_none(self) -> None:
        ...

    def test_loc_multiindex_incomplete(self) -> None:
        ...

    def test_get_loc_single_level(self, single_level_multiindex: Any) -> None:
        ...

    def test_loc_getitem_int_slice(self) -> None:
        ...

    def test_loc_getitem_nested_indexer(self, indexer_type_1: Any, indexer_type_2: Any) -> None:
        ...


def test_loc_getitem_duplicates_multiindex_missing_indexers(indexer: Any, pos: Any) -> None:
    ...

def test_series_loc_getitem_fancy(multiindex_year_month_day_dataframe_random_data: Any) -> None:
    ...

def test_loc_getitem_duplicates_multiindex_empty_indexer(columns_indexer: Any) -> None:
    ...

def test_loc_getitem_duplicates_multiindex_non_scalar_type_object() -> None:
    ...

def test_loc_getitem_tuple_plus_slice() -> None:
    ...

def test_loc_getitem_int(frame_random_data_integer_multi_index: Any) -> None:
    ...

def test_loc_getitem_int_raises_exception(frame_random_data_integer_multi_index: Any) -> None:
    ...

def test_loc_getitem_lowerdim_corner(multiindex_dataframe_random_data: Any) -> None:
    ...
