# Stubs for pandas.tests.tslibs.test_liboffsets (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.
# pylint: disable=unused-argument,redefined-outer-name,no-self-use,invalid-name
# pylint: disable=relative-beyond-top-level

from typing import Any


def day_opt(request: Any) -> Any:
    ...


def test_get_last_bday(dt: Any, exp_week_day: Any, exp_last_day: Any) -> None:
    ...


def test_get_first_bday(
        wdt: Any, exp_week_day: Any, exp_first_day: Any) -> None:
    ...


def test_shift_month_dt(months: Any, day_opt: Any, expected: Any) -> None:
    ...


def test_shift_month_ts(months: Any, day_opt: Any, expected: Any) -> None:
    ...


def test_shift_month_error() -> None:
    ...


def test_roll_yearday(other: Any, expected: Any, n: Any) -> None:
    ...


def test_roll_yearday2(other: Any, expected: Any, n: Any) -> None:
    ...


def test_get_day_of_month_error() -> None:
    ...


def test_roll_qtr_day_not_mod_unequal(
        day_opt: Any, month: Any, n: Any) -> None:
    ...


def test_roll_qtr_day_mod_equal(
        other: Any, month: Any, exp_dict: Any, n: Any, day_opt: Any) -> None:
    ...


def test_roll_convention(n: Any, expected: Any, compare: Any) -> None:
    ...
