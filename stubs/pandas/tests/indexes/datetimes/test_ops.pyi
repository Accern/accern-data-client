# Stubs for pandas.tests.indexes.datetimes.test_ops (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.
# pylint: disable=unused-argument,redefined-outer-name,no-self-use,invalid-name
# pylint: disable=relative-beyond-top-level,line-too-long

from typing import Any
from pandas.tests.test_base import Ops

START: Any
END: Any

class TestDatetimeIndexOps(Ops):
    is_valid_objs: Any = ...
    not_valid_objs: Any = ...
    def setup_method(self, method: Any) -> Any:
        ...

    def test_ops_properties(self):
        ...

    def test_ops_properties_basic(self) -> None:
        ...

    def test_repeat_range(self, tz_naive_fixture: Any) -> None:
        ...

    def test_repeat(self, tz_naive_fixture: Any) -> None:
        ...

    def test_resolution(self, tz_naive_fixture: Any) -> None:
        ...

    def test_value_counts_unique(self, tz_naive_fixture: Any) -> None:
        ...

    def test_nonunique_contains(self) -> None:
        ...

    def test_order_with_freq(self, idx: Any) -> None:
        ...

    def test_order_without_freq(self, index_dates: Any, expected_dates: Any, tz_naive_fixture: Any) -> None:
        ...

    def test_drop_duplicates_metadata(self) -> None:
        ...

    def test_drop_duplicates(self) -> None:
        ...

    def test_infer_freq(self, freq: Any) -> None:
        ...

    def test_nat(self, tz_naive_fixture: Any) -> None:
        ...

    def test_equals(self) -> None:
        ...

    def test_freq_setter(self, values: Any, freq: Any, tz: Any) -> None:
        ...

    def test_freq_setter_errors(self) -> None:
        ...

    def test_offset_deprecated(self) -> None:
        ...


class TestBusinessDatetimeIndex:
    rng: Any = ...
    def setup_method(self, method: Any) -> None:
        ...

    def test_comparison(self) -> None:
        ...

    def test_pickle_unpickle(self) -> None:
        ...

    def test_copy(self) -> None:
        ...

    def test_shift(self) -> None:
        ...

    def test_equals(self) -> None:
        ...

    def test_identical(self) -> None:
        ...


class TestCustomDatetimeIndex:
    rng: Any = ...
    def setup_method(self, method: Any) -> None:
        ...

    def test_comparison(self) -> None:
        ...

    def test_copy(self) -> None:
        ...

    def test_shift(self) -> None:
        ...

    def test_shift_periods(self) -> None:
        ...

    def test_pickle_unpickle(self) -> None:
        ...

    def test_equals(self) -> None:
        ...
