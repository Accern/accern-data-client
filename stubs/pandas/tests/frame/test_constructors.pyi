# Stubs for pandas.tests.frame.test_constructors (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.
# pylint: disable=unused-argument,redefined-outer-name,no-self-use,invalid-name
# pylint: disable=relative-beyond-top-level

from typing import Any

MIXED_FLOAT_DTYPES: Any
MIXED_INT_DTYPES: Any


class TestDataFrameConstructors:
    def test_empty_constructor(self, constructor: Any) -> None:
        ...

    def test_emptylike_constructor(
            self, emptylike: Any, expected_index: Any,
            expected_columns: Any) -> None:
        ...

    def test_constructor_mixed(self, float_string_frame: Any) -> None:
        ...

    def test_constructor_cast_failure(self) -> None:
        ...

    def test_constructor_dtype_copy(self) -> None:
        ...

    def test_constructor_dtype_nocast_view(self) -> None:
        ...

    def test_constructor_dtype_list_data(self) -> None:
        ...

    def test_constructor_list_frames(self) -> None:
        ...

    def test_constructor_mixed_dtypes(self):
        ...

    def test_constructor_complex_dtypes(self) -> None:
        ...

    def test_constructor_dtype_str_na_values(self, string_dtype: Any) -> None:
        ...

    def test_constructor_rec(self, float_frame: Any) -> None:
        ...

    def test_constructor_bool(self) -> None:
        ...

    def test_constructor_overflow_int64(self) -> None:
        ...

    def test_constructor_int_overflow(self, values: Any) -> None:
        ...

    def test_constructor_ordereddict(self) -> None:
        ...

    def test_constructor_dict(self) -> None:
        ...

    def test_constructor_invalid_items_unused(self, scalar: Any) -> None:
        ...

    def test_constructor_dict_nan_key(self, value: Any) -> None:
        ...

    def test_constructor_dict_nan_tuple_key(self, value: Any) -> None:
        ...

    def test_constructor_dict_order_insertion(self) -> None:
        ...

    def test_constructor_dict_order_by_values(self) -> None:
        ...

    def test_constructor_multi_index(self) -> None:
        ...

    def test_constructor_error_msgs(self) -> None:
        ...

    def test_constructor_with_embedded_frames(self) -> None:
        ...

    def test_constructor_subclass_dict(self, float_frame: Any) -> None:
        ...

    def test_constructor_dict_block(self) -> None:
        ...

    def test_constructor_dict_cast(self) -> None:
        ...

    def test_constructor_dict_dont_upcast(self) -> None:
        ...

    def test_constructor_dict_of_tuples(self) -> None:
        ...

    def test_constructor_dict_of_ranges(self) -> None:
        ...

    def test_constructor_dict_of_iterators(self) -> None:
        ...

    def test_constructor_dict_of_generators(self) -> None:
        ...

    def test_constructor_dict_multiindex(self):
        ...

    def test_constructor_dict_datetime64_index(self):
        ...

    def test_constructor_dict_timedelta64_index(self):
        ...

    def test_constructor_period(self) -> None:
        ...

    def test_nested_dict_frame_constructor(self) -> None:
        ...

    def test_constructor_ndarray(self) -> None:
        ...

    def test_constructor_maskedarray(self) -> None:
        ...

    def test_constructor_maskedarray_nonfloat(self) -> None:
        ...

    def test_constructor_maskedarray_hardened(self) -> None:
        ...

    def test_constructor_maskedrecarray_dtype(self) -> None:
        ...

    def test_constructor_mrecarray(self) -> None:
        ...

    def test_constructor_corner_shape(self) -> None:
        ...

    def test_constructor_dtype(
            self, data: Any, index: Any, columns: Any, dtype: Any,
            expected: Any) -> None:
        ...

    def test_constructor_scalar_inference(self) -> None:
        ...

    def test_constructor_arrays_and_scalars(self) -> None:
        ...

    def test_constructor_DataFrame(self, float_frame: Any) -> None:
        ...

    def test_constructor_more(self, float_frame: Any) -> None:
        ...

    def test_constructor_empty_list(self) -> None:
        ...

    def test_constructor_list_of_lists(self) -> None:
        ...

    def test_constructor_sequence_like(self):
        ...

    def test_constructor_range(self) -> None:
        ...

    def test_constructor_list_of_ranges(self) -> None:
        ...

    def test_constructor_iterable(self) -> None:
        ...

    def test_constructor_iterator(self) -> None:
        ...

    def test_constructor_list_of_iterators(self) -> None:
        ...

    def test_constructor_generator(self) -> None:
        ...

    def test_constructor_list_of_odicts(self) -> None:
        ...

    def test_constructor_ordered_dict_preserve_order(self) -> None:
        ...

    def test_constructor_ordered_dict_conflicting_orders(self) -> None:
        ...

    def test_constructor_list_of_series(self) -> None:
        ...

    def test_constructor_list_of_series_aligned_index(self) -> None:
        ...

    def test_constructor_list_of_derived_dicts(self) -> None:
        ...

    def test_constructor_ragged(self) -> None:
        ...

    def test_constructor_scalar(self) -> None:
        ...

    def test_constructor_Series_copy_bug(self, float_frame: Any) -> None:
        ...

    def test_constructor_mixed_dict_and_Series(self) -> None:
        ...

    def test_constructor_mixed_type_rows(self) -> None:
        ...

    def test_constructor_tuple(self, tuples: Any, lists: Any) -> None:
        ...

    def test_constructor_list_of_tuples(self) -> None:
        ...

    def test_constructor_list_of_namedtuples(self) -> None:
        ...

    def test_constructor_list_of_dict_order(self) -> None:
        ...

    def test_constructor_orient(self, float_string_frame: Any) -> None:
        ...

    def test_constructor_from_ordered_dict(self) -> None:
        ...

    def test_from_dict_columns_parameter(self) -> None:
        ...

    def test_constructor_Series_named(self) -> None:
        ...

    def test_constructor_Series_named_and_columns(self) -> None:
        ...

    def test_constructor_Series_differently_indexed(self) -> None:
        ...

    def test_constructor_manager_resize(self, float_frame: Any) -> None:
        ...

    def test_constructor_from_items(
            self, float_frame: Any, float_string_frame: Any) -> None:
        ...

    def test_constructor_from_items_scalars(self) -> None:
        ...

    def test_from_items_deprecation(self) -> None:
        ...

    def test_constructor_mix_series_nonseries(self, float_frame: Any) -> None:
        ...

    def test_constructor_miscast_na_int_dtype(self) -> None:
        ...

    def test_constructor_column_duplicates(self) -> None:
        ...

    def test_constructor_empty_with_string_dtype(self) -> None:
        ...

    def test_constructor_single_value(self) -> None:
        ...

    def test_constructor_with_datetimes(self) -> None:
        ...

    def test_constructor_datetimes_with_nulls(self) -> None:
        ...

    def test_constructor_for_list_with_dtypes(self) -> None:
        ...

    def test_constructor_frame_copy(self, float_frame: Any) -> None:
        ...

    def test_constructor_ndarray_copy(self, float_frame: Any) -> None:
        ...

    def test_constructor_series_copy(self, float_frame: Any) -> None:
        ...

    def test_constructor_with_nas(self) -> None:
        ...

    def test_constructor_lists_to_object_dtype(self) -> None:
        ...

    def test_constructor_categorical(self) -> None:
        ...

    def test_constructor_categorical_series(self) -> None:
        ...

    def test_from_records_to_records(self) -> None:
        ...

    def test_from_records_nones(self) -> None:
        ...

    def test_from_records_iterator(self) -> None:
        ...

    def test_from_records_tuples_generator(self) -> None:
        ...

    def test_from_records_lists_generator(self) -> None:
        ...

    def test_from_records_columns_not_modified(self) -> None:
        ...

    def test_from_records_decimal(self) -> None:
        ...

    def test_from_records_duplicates(self) -> None:
        ...

    def test_from_records_set_index_name(self):
        ...

    def test_from_records_misc_brokenness(self) -> None:
        ...

    def test_from_records_empty(self) -> None:
        ...

    def test_from_records_empty_with_nonempty_fields_gh3682(self) -> None:
        ...

    def test_from_records_with_datetimes(self) -> None:
        ...

    def test_from_records_sequencelike(self) -> None:
        ...

    def test_from_records_dictlike(self) -> None:
        ...

    def test_from_records_with_index_data(self) -> None:
        ...

    def test_from_records_bad_index_column(self) -> None:
        ...

    args: Any = ...
    def test_from_records_non_tuple(self):
        ...

    def test_from_records_len0_with_columns(self) -> None:
        ...

    def test_from_records_series_list_dict(self) -> None:
        ...

    def test_to_frame_with_falsey_names(self) -> None:
        ...

    def test_constructor_range_dtype(self, dtype: Any) -> None:
        ...

    def test_frame_from_list_subclass(self) -> None:
        ...


class TestDataFrameConstructorWithDatetimeTZ:
    def test_from_dict(self) -> None:
        ...

    def test_from_index(self) -> None:
        ...

    def test_frame_dict_constructor_datetime64_1680(self) -> None:
        ...

    def test_frame_datetime64_mixed_index_ctor_1681(self) -> None:
        ...

    def test_frame_timeseries_to_records(self) -> None:
        ...

    def test_frame_timeseries_column(self) -> None:
        ...

    def test_nested_dict_construction(self) -> None:
        ...

    def test_from_tzaware_object_array(self) -> None:
        ...

    def test_from_tzaware_mixed_object_array(self) -> None:
        ...
