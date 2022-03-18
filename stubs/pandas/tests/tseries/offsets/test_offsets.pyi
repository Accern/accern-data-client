# Stubs for pandas.tests.tseries.offsets.test_offsets (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.
# pylint: disable=unused-argument,redefined-outer-name,no-self-use,invalid-name
# pylint: disable=relative-beyond-top-level,line-too-long,arguments-differ
# pylint: disable=no-member,too-few-public-methods,keyword-arg-before-vararg
# pylint: disable=super-init-not-called,abstract-method,redefined-builtin
# pylint: disable=unused-import,useless-import-alias,signature-differs
# pylint: disable=blacklisted-name,c-extension-no-member,too-many-ancestors

from typing import Any

class WeekDay:
    MON: int = ...
    TUE: int = ...
    WED: int = ...
    THU: int = ...
    FRI: int = ...
    SAT: int = ...
    SUN: int = ...

def test_to_M8() -> None:
    ...


class Base:
    d: Any = ...
    timezones: Any = ...

    def test_apply_out_of_range(self, tz_naive_fixture: Any) -> None:
        ...

    def test_offsets_compare_equal(self) -> None:
        ...

    def test_rsub(self) -> None:
        ...

    def test_radd(self) -> None:
        ...

    def test_sub(self) -> None:
        ...

    def testMult1(self) -> None:
        ...

    def testMult2(self) -> None:
        ...

    def test_compare_str(self) -> None:
        ...


class TestCommon(Base):
    expecteds: Any = ...

    def test_immutable(self, offset_types: Any) -> None:
        ...

    def test_return_type(self, offset_types: Any) -> None:
        ...

    def test_offset_n(self, offset_types: Any) -> None:
        ...

    def test_offset_timedelta64_arg(self, offset_types: Any) -> None:
        ...

    def test_offset_mul_ndarray(self, offset_types: Any) -> None:
        ...

    def test_offset_freqstr(self, offset_types: Any) -> None:
        ...

    def test_apply(self, offset_types: Any) -> None:
        ...

    def test_rollforward(self, offset_types: Any) -> None:
        ...

    def test_rollback(self, offset_types: Any) -> None:
        ...

    def test_onOffset(self, offset_types: Any) -> None:
        ...

    def test_add(self, offset_types: Any, tz_naive_fixture: Any) -> None:
        ...

    def test_pickle_v0_15_2(self, datapath: Any) -> None:
        ...


class TestDateOffset(Base):
    d: Any = ...
    def setup_method(self, method: Any) -> None:
        ...

    def test_repr(self) -> None:
        ...

    def test_mul(self) -> None:
        ...

    def test_constructor(self) -> None:
        ...

    def test_copy(self) -> None:
        ...

    def test_eq(self) -> None:
        ...


class TestBusinessDay(Base):
    d: Any = ...
    offset: Any = ...
    offset1: Any = ...
    offset2: Any = ...

    def setup_method(self, method: Any) -> None:
        ...

    def test_different_normalize_equals(self) -> None:
        ...

    def test_repr(self) -> None:
        ...

    def test_with_offset(self) -> None:
        ...

    def test_eq(self) -> None:
        ...

    def test_mul(self) -> None:
        ...

    def test_hash(self) -> None:
        ...

    def test_call(self) -> None:
        ...

    def testRollback1(self) -> None:
        ...

    def testRollback2(self) -> None:
        ...

    def testRollforward1(self) -> None:
        ...

    def testRollforward2(self) -> None:
        ...

    def test_roll_date_object(self) -> None:
        ...

    def test_onOffset(self) -> None:
        ...

    apply_cases: Any = ...
    def test_apply(self, case: Any) -> None:
        ...

    def test_apply_large_n(self) -> None:
        ...

    def test_apply_corner(self) -> None:
        ...


class TestBusinessHour(Base):
    d: Any = ...
    offset1: Any = ...
    offset2: Any = ...
    offset3: Any = ...
    offset4: Any = ...
    offset5: Any = ...
    offset6: Any = ...
    offset7: Any = ...
    offset8: Any = ...
    offset9: Any = ...
    offset10: Any = ...
    def setup_method(self, method: Any) -> None:
        ...

    def test_constructor_errors(self, start: Any, end: Any, match: Any) -> None:
        ...

    def test_different_normalize_equals(self) -> None:
        ...

    def test_repr(self) -> None:
        ...

    def test_with_offset(self) -> None:
        ...

    def test_eq_attribute(self, offset_name: Any) -> None:
        ...

    def test_eq(self, offset1: Any, offset2: Any) -> None:
        ...

    def test_neq(self, offset1: Any, offset2: Any) -> None:
        ...

    def test_hash(self, offset_name: Any) -> None:
        ...

    def test_call(self) -> None:
        ...

    def test_sub(self) -> None:
        ...

    def testRollback1(self) -> None:
        ...

    def testRollback2(self) -> None:
        ...

    def testRollforward1(self) -> None:
        ...

    def testRollforward2(self) -> None:
        ...

    def test_roll_date_object(self) -> None:
        ...

    normalize_cases: Any = ...
    def test_normalize(self, case: Any) -> None:
        ...

    on_offset_cases: Any = ...
    def test_onOffset(self, case: Any) -> None:
        ...

    opening_time_cases: Any = ...
    def test_opening_time(self, case: Any) -> None:
        ...

    apply_cases: Any = ...
    def test_apply(self, case: Any) -> None:
        ...

    apply_large_n_cases: Any = ...
    def test_apply_large_n(self, case: Any) -> None:
        ...

    def test_apply_nanoseconds(self) -> None:
        ...

    def test_datetimeindex(self) -> None:
        ...


class TestCustomBusinessHour(Base):
    holidays: Any = ...
    d: Any = ...
    offset1: Any = ...
    offset2: Any = ...
    def setup_method(self, method: Any) -> None:
        ...

    def test_constructor_errors(self) -> None:
        ...

    def test_different_normalize_equals(self) -> None:
        ...

    def test_repr(self) -> None:
        ...

    def test_with_offset(self) -> None:
        ...

    def test_eq(self) -> None:
        ...

    def test_sub(self) -> None:
        ...

    def test_hash(self) -> None:
        ...

    def test_call(self) -> None:
        ...

    def testRollback1(self) -> None:
        ...

    def testRollback2(self) -> None:
        ...

    def testRollforward1(self) -> None:
        ...

    def testRollforward2(self) -> None:
        ...

    def test_roll_date_object(self) -> None:
        ...

    normalize_cases: Any = ...
    def test_normalize(self, norm_cases: Any) -> None:
        ...

    def test_onOffset(self) -> None:
        ...

    apply_cases: Any = ...
    def test_apply(self, apply_case: Any) -> None:
        ...

    nano_cases: Any = ...
    def test_apply_nanoseconds(self, nano_case: Any) -> None:
        ...


class TestCustomBusinessDay(Base):
    d: Any = ...
    nd: Any = ...
    offset: Any = ...
    offset1: Any = ...
    offset2: Any = ...
    def setup_method(self, method: Any) -> None:
        ...

    def test_different_normalize_equals(self) -> None:
        ...

    def test_repr(self) -> None:
        ...

    def test_with_offset(self) -> None:
        ...

    def test_eq(self) -> None:
        ...

    def test_mul(self) -> None:
        ...

    def test_hash(self) -> None:
        ...

    def test_call(self) -> None:
        ...

    def testRollback1(self) -> None:
        ...

    def testRollback2(self) -> None:
        ...

    def testRollforward1(self) -> None:
        ...

    def testRollforward2(self) -> None:
        ...

    def test_roll_date_object(self) -> None:
        ...

    on_offset_cases: Any = ...
    def test_onOffset(self, case: Any) -> None:
        ...

    apply_cases: Any = ...
    def test_apply(self, case: Any) -> None:
        ...

    def test_apply_large_n(self) -> None:
        ...

    def test_apply_corner(self) -> None:
        ...

    def test_holidays(self) -> None:
        ...

    def test_weekmask(self) -> None:
        ...

    def test_weekmask_and_holidays(self) -> None:
        ...

    def test_calendar(self) -> None:
        ...

    def test_roundtrip_pickle(self) -> None:
        ...

    def test_pickle_compat_0_14_1(self, datapath: Any) -> None:
        ...


class CustomBusinessMonthBase:
    d: Any = ...
    offset: Any = ...
    offset1: Any = ...
    offset2: Any = ...
    def setup_method(self, method: Any) -> None:
        ...

    def test_eq(self) -> None:
        ...

    def test_mul(self) -> None:
        ...

    def test_hash(self) -> None:
        ...

    def test_roundtrip_pickle(self) -> None:
        ...

    def test_copy(self) -> None:
        ...


class TestCustomBusinessMonthEnd(CustomBusinessMonthBase, Base):
    def test_different_normalize_equals(self) -> None:
        ...

    def test_repr(self) -> None:
        ...

    def testCall(self) -> None:
        ...

    def testRollback1(self) -> None:
        ...

    def testRollback2(self) -> None:
        ...

    def testRollforward1(self) -> None:
        ...

    def test_roll_date_object(self) -> None:
        ...

    on_offset_cases: Any = ...
    def test_onOffset(self, case: Any) -> None:
        ...

    apply_cases: Any = ...
    def test_apply(self, case: Any) -> None:
        ...

    def test_apply_large_n(self) -> None:
        ...

    def test_holidays(self) -> None:
        ...

    def test_datetimeindex(self) -> None:
        ...


class TestCustomBusinessMonthBegin(CustomBusinessMonthBase, Base):
    def test_different_normalize_equals(self) -> None:
        ...

    def test_repr(self) -> None:
        ...

    def testCall(self) -> None:
        ...

    def testRollback1(self) -> None:
        ...

    def testRollback2(self) -> None:
        ...

    def testRollforward1(self) -> None:
        ...

    def test_roll_date_object(self) -> None:
        ...

    on_offset_cases: Any = ...
    def test_onOffset(self, case: Any) -> None:
        ...

    apply_cases: Any = ...
    def test_apply(self, case: Any) -> None:
        ...

    def test_apply_large_n(self) -> None:
        ...

    def test_holidays(self) -> None:
        ...

    def test_datetimeindex(self) -> None:
        ...


class TestWeek(Base):
    d: Any = ...
    offset1: Any = ...
    offset2: Any = ...
    def test_repr(self) -> None:
        ...

    def test_corner(self) -> None:
        ...

    def test_isAnchored(self) -> None:
        ...

    offset_cases: Any = ...
    def test_offset(self, case: Any) -> None:
        ...

    def test_onOffset(self, weekday: Any) -> None:
        ...


class TestWeekOfMonth(Base):
    offset1: Any = ...
    offset2: Any = ...
    def test_constructor(self) -> None:
        ...

    def test_repr(self) -> None:
        ...

    def test_offset(self) -> None:
        ...

    on_offset_cases: Any = ...
    def test_onOffset(self, case: Any) -> None:
        ...


class TestLastWeekOfMonth(Base):
    offset1: Any = ...
    offset2: Any = ...
    def test_constructor(self) -> None:
        ...

    def test_offset(self) -> None:
        ...

    on_offset_cases: Any = ...
    def test_onOffset(self, case: Any) -> None:
        ...


class TestSemiMonthEnd(Base):
    offset1: Any = ...
    offset2: Any = ...
    def test_offset_whole_year(self) -> None:
        ...

    offset_cases: Any = ...
    def test_offset(self, case: Any) -> None:
        ...

    def test_apply_index(self, case: Any) -> None:
        ...

    on_offset_cases: Any = ...
    def test_onOffset(self, case: Any) -> None:
        ...

    def test_vectorized_offset_addition(self, klass: Any) -> None:
        ...


class TestSemiMonthBegin(Base):
    offset1: Any = ...
    offset2: Any = ...

    def test_offset_whole_year(self) -> None:
        ...

    offset_cases: Any = ...
    def test_offset(self, case: Any) -> None:
        ...

    def test_apply_index(self, case: Any) -> None:
        ...

    on_offset_cases: Any = ...
    def test_onOffset(self, case: Any) -> None:
        ...

    def test_vectorized_offset_addition(self, klass: Any) -> None:
        ...


def test_Easter() -> None:
    ...


class TestOffsetNames:
    def test_get_offset_name(self) -> None:
        ...


def test_get_offset() -> None:
    ...


def test_get_offset_legacy() -> None:
    ...


class TestOffsetAliases:
    def setup_method(self, method: Any) -> None:
        ...

    def test_alias_equality(self) -> None:
        ...

    def test_rule_code(self) -> None:
        ...


def test_dateoffset_misc() -> None:
    ...


def test_freq_offsets() -> None:
    ...


class TestReprNames:
    def test_str_for_named_is_name(self) -> None:
        ...


def get_utc_offset_hours(ts: Any) -> Any:
    ...


class TestDST:
    ts_pre_fallback: str = ...
    ts_pre_springfwd: str = ...
    timezone_utc_offsets: Any = ...
    valid_date_offsets_singular: Any = ...
    valid_date_offsets_plural: Any = ...

    def test_springforward_plural(self) -> None:
        ...

    def test_fallback_singular(self) -> None:
        ...

    def test_springforward_singular(self) -> None:
        ...

    offset_classes: Any = ...

    def test_all_offset_classes(self, tup: Any) -> None:
        ...


def test_get_offset_day_error() -> None:
    ...


def test_valid_default_arguments(offset_types: Any) -> None:
    ...


def test_valid_month_attributes(kwd: Any, month_classes: Any) -> None:
    ...


def test_valid_relativedelta_kwargs(kwd: Any) -> None:
    ...


def test_valid_tick_attributes(kwd: Any, tick_classes: Any) -> None:
    ...


def test_validate_n_error() -> None:
    ...


def test_require_integers(offset_types: Any) -> None:
    ...


def test_tick_normalize_raises(tick_classes: Any) -> None:
    ...


def test_weeks_onoffset() -> None:
    ...


def test_weekofmonth_onoffset() -> None:
    ...


def test_last_week_of_month_on_offset() -> None:
    ...
