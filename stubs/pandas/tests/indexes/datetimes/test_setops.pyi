# Stubs for pandas.tests.indexes.datetimes.test_setops (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.
# pylint: disable=unused-argument,redefined-outer-name,no-self-use,invalid-name
# pylint: disable=relative-beyond-top-level,line-too-long

from typing import Any

START: Any
END: Any


class TestDatetimeIndexSetOps:
    tz: Any = ...
    def test_union2(self, sort: Any) -> None:
        ...

    def test_union3(self, sort: Any, box: Any) -> None:
        ...

    def test_union(self, tz: Any, sort: Any) -> None:
        ...

    def test_union_coverage(self, sort: Any) -> None:
        ...

    def test_union_bug_1730(self, sort: Any) -> None:
        ...

    def test_union_bug_1745(self, sort: Any) -> None:
        ...

    def test_union_bug_4564(self, sort: Any) -> None:
        ...

    def test_union_freq_both_none(self, sort: Any) -> None:
        ...

    def test_union_dataframe_index(self) -> None:
        ...

    def test_union_with_DatetimeIndex(self, sort: Any) -> None:
        ...

    def test_intersection2(self) -> None:
        ...

    def test_intersection(self, tz: Any, sort: Any) -> None:
        ...

    def test_intersection_empty(self) -> None:
        ...

    def test_intersection_bug_1708(self) -> None:
        ...

    def test_difference(self, tz: Any, sort: Any) -> None:
        ...

    def test_difference_freq(self, sort: Any) -> None:
        ...

    def test_datetimeindex_diff(self, sort: Any) -> None:
        ...

    def test_datetimeindex_union_join_empty(self, sort: Any) -> None:
        ...

    def test_join_nonunique(self) -> None:
        ...


class TestBusinessDatetimeIndex:
    rng: Any = ...
    def setup_method(self, method: Any) -> None:
        ...

    def test_union(self, sort: Any) -> None:
        ...

    def test_outer_join(self) -> None:
        ...

    def test_union_not_cacheable(self, sort: Any) -> None:
        ...

    def test_intersection(self) -> None:
        ...

    def test_intersection_bug(self) -> None:
        ...

    def test_month_range_union_tz_pytz(self, sort: Any) -> None:
        ...

    def test_month_range_union_tz_dateutil(self, sort: Any) -> None:
        ...


class TestCustomDatetimeIndex:
    rng: Any = ...
    def setup_method(self, method: Any) -> None:
        ...

    def test_union(self, sort: Any) -> None:
        ...

    def test_outer_join(self) -> None:
        ...

    def test_intersection_bug(self) -> None:
        ...
