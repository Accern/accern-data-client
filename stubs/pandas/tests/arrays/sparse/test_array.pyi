# Stubs for pandas.tests.arrays.sparse.test_array (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.
# pylint: disable=unused-argument,redefined-outer-name,no-self-use,invalid-name
# pylint: disable=relative-beyond-top-level,line-too-long,arguments-differ
# pylint: disable=no-member,too-few-public-methods,keyword-arg-before-vararg
# pylint: disable=super-init-not-called,abstract-method,redefined-builtin
# pylint: disable=unused-import,useless-import-alias,signature-differs
# pylint: disable=blacklisted-name,c-extension-no-member,import-error

from typing import Any

def kind(request: Any) -> Any:
    ...


class TestSparseArray:
    arr_data: Any = ...
    arr: Any = ...
    zarr: Any = ...
    def setup_method(self, method: Any) -> None:
        ...

    def test_constructor_dtype(self) -> None:
        ...

    def test_constructor_dtype_str(self) -> None:
        ...

    def test_constructor_sparse_dtype(self) -> None:
        ...

    def test_constructor_sparse_dtype_str(self) -> None:
        ...

    def test_constructor_object_dtype(self) -> None:
        ...

    def test_constructor_na_dtype(self, dtype: Any) -> None:
        ...

    def test_constructor_spindex_dtype(self) -> None:
        ...

    def test_constructor_spindex_dtype_scalar(self, sparse_index: Any) -> None:
        ...

    def test_constructor_spindex_dtype_scalar_broadcasts(self) -> None:
        ...

    def test_constructor_inferred_fill_value(self, data: Any, fill_value: Any) -> None:
        ...

    def test_from_spmatrix(self, size: Any, format: Any) -> None:
        ...

    def test_from_spmatrix_raises(self) -> None:
        ...

    def test_scalar_with_index_infer_dtype(self, scalar: Any, dtype: Any) -> None:
        ...

    def test_sparse_series_round_trip(self, kind: Any, fill: Any) -> None:
        ...

    def test_sparse_series_round_trip2(self, kind: Any, fill: Any) -> None:
        ...

    def test_get_item(self) -> None:
        ...

    def test_take_scalar_raises(self) -> None:
        ...

    def test_take(self) -> None:
        ...

    def test_take_fill_value(self) -> None:
        ...

    def test_take_negative(self) -> None:
        ...

    def test_shift_fill_value(self, fill_value: Any) -> None:
        ...

    def test_bad_take(self) -> None:
        ...

    def test_take_filling(self) -> None:
        ...

    def test_take_filling_fill_value(self) -> None:
        ...

    def test_take_filling_all_nan(self) -> None:
        ...

    def test_set_item(self) -> None:
        ...

    def test_constructor_from_too_large_array(self) -> None:
        ...

    def test_constructor_from_sparse(self) -> None:
        ...

    def test_constructor_copy(self) -> None:
        ...

    def test_constructor_bool(self) -> None:
        ...

    def test_constructor_bool_fill_value(self) -> None:
        ...

    def test_constructor_float32(self) -> None:
        ...

    def test_astype(self) -> None:
        ...

    def test_astype_bool(self) -> None:
        ...

    def test_astype_all(self, any_real_dtype: Any) -> None:
        ...

    def test_astype_more(self, array: Any, dtype: Any, expected: Any) -> None:
        ...

    def test_astype_nan_raises(self) -> None:
        ...

    def test_set_fill_value(self) -> None:
        ...

    def test_set_fill_invalid_non_scalar(self, val: Any) -> None:
        ...

    def test_copy(self) -> None:
        ...

    def test_values_asarray(self) -> None:
        ...

    def test_shape(self, data: Any, shape: Any, dtype: Any) -> None:
        ...

    def test_dense_repr(self, vals: Any, fill_value: Any) -> None:
        ...

    def test_getitem(self) -> None:
        ...

    def test_getitem_arraylike_mask(self) -> None:
        ...

    def test_getslice(self) -> None:
        ...

    def test_getslice_tuple(self) -> None:
        ...

    def test_boolean_slice_empty(self) -> None:
        ...

    def test_binary_operators(self, op: Any) -> None:
        ...

    def test_pickle(self) -> None:
        ...

    def test_generator_warnings(self) -> None:
        ...

    def test_fillna(self) -> None:
        ...

    def test_fillna_overlap(self) -> None:
        ...

    def test_nonzero(self) -> None:
        ...


class TestSparseArrayAnalytics:
    def test_all(self, data: Any, pos: Any, neg: Any) -> None:
        ...

    def test_numpy_all(self, data: Any, pos: Any, neg: Any) -> None:
        ...

    def test_any(self, data: Any, pos: Any, neg: Any) -> None:
        ...

    def test_numpy_any(self, data: Any, pos: Any, neg: Any) -> None:
        ...

    def test_sum(self) -> None:
        ...

    def test_numpy_sum(self) -> None:
        ...

    def test_cumsum(self, data: Any, expected: Any, numpy: Any) -> None:
        ...

    def test_mean(self) -> None:
        ...

    def test_numpy_mean(self) -> None:
        ...

    def test_ufunc(self) -> None:
        ...

    def test_ufunc_args(self) -> None:
        ...

    def test_modf(self, fill_value: Any) -> None:
        ...

    def test_nbytes_integer(self) -> None:
        ...

    def test_nbytes_block(self) -> None:
        ...

    def test_asarray_datetime64(self) -> None:
        ...

    def test_density(self) -> None:
        ...

    def test_npoints(self) -> None:
        ...


class TestAccessor:
    def test_get_attributes(self, attr: Any) -> None:
        ...

    def test_from_coo(self) -> None:
        ...

    def test_to_coo(self) -> None:
        ...

    def test_non_sparse_raises(self) -> None:
        ...


def test_setting_fill_value_fillna_still_works() -> None:
    ...

def test_setting_fill_value_updates() -> None:
    ...

def test_first_fill_value_loc(arr: Any, loc: Any) -> None:
    ...

def test_unique_na_fill(arr: Any, fill_value: Any) -> None:
    ...

def test_unique_all_sparse() -> None:
    ...

def test_map() -> None:
    ...

def test_map_missing() -> None:
    ...

def test_deprecated_values() -> None:
    ...