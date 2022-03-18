# Stubs for pandas.tests.frame.test_block_internals (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.
# pylint: disable=unused-argument,redefined-outer-name,no-self-use,invalid-name
# pylint: disable=relative-beyond-top-level

from typing import Any

class TestDataFrameBlockInternals:
    def test_setitem_invalidates_datetime_index_freq(self) -> None:
        ...

    def test_cast_internals(self, float_frame: Any) -> None:
        ...

    def test_consolidate(self, float_frame: Any) -> None:
        ...

    def test_consolidate_inplace(self, float_frame: Any) -> None:
        ...

    def test_values_consolidate(self, float_frame: Any) -> None:
        ...

    def test_modify_values(self, float_frame: Any) -> None:
        ...

    def test_boolean_set_uncons(self, float_frame: Any) -> None:
        ...

    def test_values_numeric_cols(self, float_frame: Any) -> None:
        ...

    def test_values_lcd(
            self, mixed_float_frame: Any, mixed_int_frame: Any) -> None:
        ...

    def test_constructor_with_convert(self) -> None:
        ...

    def test_construction_with_mixed(self, float_string_frame: Any) -> None:
        ...

    def test_construction_with_conversions(self) -> None:
        ...

    def test_constructor_compound_dtypes(self):
        ...

    def test_equals_different_blocks(self) -> None:
        ...

    def test_copy_blocks(self, float_frame: Any) -> None:
        ...

    def test_no_copy_blocks(self, float_frame: Any) -> None:
        ...

    def test_copy(self, float_frame: Any, float_string_frame: Any) -> None:
        ...

    def test_pickle(
            self, float_string_frame: Any, timezone_frame: Any) -> None:
        ...

    def test_consolidate_datetime64(self) -> None:
        ...

    def test_is_mixed_type(
            self, float_frame: Any, float_string_frame: Any) -> None:
        ...

    def test_get_numeric_data(self) -> None:
        ...

    def test_get_numeric_data_extension_dtype(self) -> None:
        ...

    def test_convert_objects(self, float_string_frame: Any) -> None:
        ...

    def test_convert_objects_no_conversion(self) -> None:
        ...

    def test_infer_objects(self) -> None:
        ...

    def test_stale_cached_series_bug_473(self) -> None:
        ...

    def test_get_X_columns(self) -> None:
        ...

    def test_strange_column_corruption_issue(self) -> None:
        ...

    def test_constructor_no_pandas_array(self) -> None:
        ...

    def test_add_column_with_pandas_array(self) -> None:
        ...
