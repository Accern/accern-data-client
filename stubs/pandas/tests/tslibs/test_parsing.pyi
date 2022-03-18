# Stubs for pandas.tests.tslibs.test_parsing (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.
# pylint: disable=unused-argument,redefined-outer-name,no-self-use,invalid-name
# pylint: disable=relative-beyond-top-level

from typing import Any


def test_parse_time_string() -> None:
    ...


def test_parse_time_quarter_with_dash(dashed: Any, normal: Any) -> None:
    ...


def test_parse_time_quarter_with_dash_error(dashed: Any) -> None:
    ...


def test_does_not_convert_mixed_integer(
        date_string: Any, expected: Any) -> None:
    ...


def test_parsers_quarterly_with_freq_error(
        date_str: Any, kwargs: Any, msg: Any) -> None:
    ...


def test_parsers_quarterly_with_freq(
        date_str: Any, freq: Any, expected: Any) -> None:
    ...


def test_parsers_quarter_invalid(date_str: Any) -> None:
    ...


def test_parsers_month_freq(date_str: Any, expected: Any) -> None:
    ...


def test_guess_datetime_format_with_parseable_formats(
        string: Any, fmt: Any) -> None:
    ...


def test_guess_datetime_format_with_dayfirst(
        dayfirst: Any, expected: Any) -> None:
    ...


def test_guess_datetime_format_with_locale_specific_formats(
        string: Any, fmt: Any) -> None:
    ...


def test_guess_datetime_format_invalid_inputs(invalid_dt: Any) -> None:
    ...


def test_guess_datetime_format_no_padding(string: Any, fmt: Any) -> None:
    ...


def test_try_parse_dates() -> None:
    ...
