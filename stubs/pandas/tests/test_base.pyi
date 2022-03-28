# Stubs for pandas.tests.test_base (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.
# pylint: disable=unused-argument,redefined-outer-name,no-self-use,invalid-name
# pylint: disable=relative-beyond-top-level,line-too-long,arguments-differ
# pylint: disable=no-member,too-few-public-methods,keyword-arg-before-vararg
# pylint: disable=super-init-not-called,abstract-method,redefined-builtin
# pylint: disable=unused-import,useless-import-alias,signature-differs
# pylint: disable=blacklisted-name,c-extension-no-member,too-many-ancestors

from typing import Any, Optional
from pandas.core.accessor import PandasDelegate
from pandas.core.base import PandasObject


class CheckStringMixin:
    def test_string_methods_dont_fail(self) -> None:
        ...

    def test_tricky_container(self) -> None:
        ...


class CheckImmutable:
    mutable_regex: Any = ...

    def check_mutable_error(self, *args: Any, **kwargs: Any) -> None:
        ...

    def test_no_mutable_funcs(self) -> None:
        ...

    def test_slicing_maintains_type(self) -> None:
        ...

    def check_result(self, result: Any, expected: Any,
                     klass: Optional[Any] = ...) -> None:
        ...


class TestPandasDelegate:
    class Delegator:
        foo: Any = ...

        def bar(self, *args: Any, **kwargs: Any) -> None:
            ...

    class Delegate(PandasDelegate, PandasObject):
        obj: Any = ...

        def __init__(self, obj: Any) -> None:
            ...

    def setup_method(self, method: Any) -> None:
        ...

    def test_invalid_delegation(self) -> None:
        ...

    def test_memory_usage(self) -> None:
        ...


class Ops:
    bool_index: Any = ...
    int_index: Any = ...
    float_index: Any = ...
    dt_index: Any = ...
    dt_tz_index: Any = ...
    period_index: Any = ...
    string_index: Any = ...
    unicode_index: Any = ...
    bool_series: Any = ...
    int_series: Any = ...
    float_series: Any = ...
    dt_series: Any = ...
    dt_tz_series: Any = ...
    period_series: Any = ...
    string_series: Any = ...
    unicode_series: Any = ...
    indexes: Any = ...
    series: Any = ...
    objs: Any = ...

    def setup_method(self, method: Any) -> None:
        ...

    def check_ops_properties(
            self, props: Any, filter: Optional[Any] = ...,
            ignore_failures: bool = ...) -> None:
        ...

    def test_binary_ops_docs(self, klass: Any) -> None:
        ...


class TestIndexOps(Ops):
    is_valid_objs: Any = ...
    not_valid_objs: Any = ...

    def setup_method(self, method: Any) -> None:
        ...

    def test_none_comparison(self) -> None:
        ...

    def test_ndarray_compat_properties(self) -> None:
        ...

    def test_value_counts_unique_nunique(self) -> None:
        ...

    def test_value_counts_unique_nunique_null(self, null_obj: Any) -> None:
        ...

    def test_value_counts_inferred(self, klass: Any) -> None:
        ...

    def test_value_counts_bins(self, klass: Any) -> None:
        ...

    def test_value_counts_datetime64(self, klass: Any) -> None:
        ...

    def test_factorize(self) -> None:
        ...

    def test_factorize_repeated(self) -> None:
        ...

    def test_duplicated_drop_duplicates_index(self) -> None:
        ...

    def test_drop_duplicates_series_vs_dataframe(self) -> None:
        ...

    def test_fillna(self) -> None:
        ...

    def test_memory_usage(self) -> None:
        ...

    def test_searchsorted(self) -> None:
        ...

    def test_validate_bool_args(self) -> None:
        ...

    def test_getitem(self) -> None:
        ...

    def test_bool_indexing(self, indexer_klass: Any, indexer: Any) -> None:
        ...


class TestTranspose(Ops):
    errmsg: str = ...
    def test_transpose(self) -> None:
        ...

    def test_transpose_non_default_axes(self) -> None:
        ...

    def test_numpy_transpose(self) -> None:
        ...


class TestNoNewAttributesMixin:
    def test_mixin(self) -> None:
        ...


class TestToIterable:
    dtypes: Any = ...

    def test_iterable(
            self, typ: Any, method: Any, dtype: Any, rdtype: Any) -> None:
        ...

    def test_iterable_object_and_category(
            self, typ: Any, method: Any, dtype: Any, rdtype: Any,
            obj: Any) -> None:
        ...

    def test_iterable_items(self, dtype: Any, rdtype: Any) -> None:
        ...

    def test_iterable_map(self, typ: Any, dtype: Any, rdtype: Any) -> None:
        ...

    def test_categorial_datetimelike(self, method: Any) -> None:
        ...

    def test_iter_box(self) -> None:
        ...


def test_values_consistent(array: Any, expected_type: Any, dtype: Any) -> None:
    ...


def test_ndarray_values(array: Any, expected: Any) -> None:
    ...


def test_numpy_array(arr: Any) -> None:
    ...


def test_numpy_array_all_dtypes(any_numpy_dtype: Any) -> None:
    ...


def test_array(array: Any, attr: Any, box: Any) -> None:
    ...


def test_array_multiindex_raises() -> None:
    ...


def test_to_numpy(array: Any, expected: Any, box: Any) -> None:
    ...


def test_to_numpy_copy(arr: Any, as_series: Any) -> None:
    ...


def test_to_numpy_dtype(as_series: Any) -> None:
    ...


class TestConstruction:
    def test_constructor_datetime_outofbound(self, a: Any, klass: Any) -> None:
        ...