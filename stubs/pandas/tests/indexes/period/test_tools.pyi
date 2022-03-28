# Stubs for pandas.tests.indexes.period.test_tools (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.
# pylint: disable=unused-argument,redefined-outer-name,no-self-use,invalid-name
# pylint: disable=relative-beyond-top-level,line-too-long,arguments-differ

from typing import Any


class TestPeriodRepresentation:
    def test_annual(self) -> None:
        ...

    def test_monthly(self) -> None:
        ...

    def test_freq(self, freq: Any) -> None:
        ...

    def test_negone_ordinals(self) -> None:
        ...


class TestPeriodIndex:
    def test_to_timestamp(self):
        ...

    def test_to_timestamp_freq(self) -> None:
        ...

    def test_to_timestamp_repr_is_code(self) -> None:
        ...

    def test_to_timestamp_to_period_astype(self) -> None:
        ...

    def test_dti_to_period(self) -> None:
        ...

    def test_to_period_quarterly(self, month: Any) -> None:
        ...

    def test_to_period_quarterlyish(self, off: Any) -> None:
        ...

    def test_to_period_annualish(self, off: Any) -> None:
        ...

    def test_to_period_monthish(self) -> None:
        ...

    def test_period_dt64_round_trip(self) -> None:
        ...

    def test_combine_first(self) -> None:
        ...

    def test_searchsorted(self, freq: Any) -> None:
        ...


class TestPeriodIndexConversion:
    def test_tolist(self) -> None:
        ...

    def test_to_timestamp_pi_nat(self) -> None:
        ...

    def test_to_timestamp_preserve_name(self) -> None:
        ...

    def test_to_timestamp_quarterly_bug(self) -> None:
        ...

    def test_to_timestamp_pi_mult(self) -> None:
        ...

    def test_to_timestamp_pi_combined(self) -> None:
        ...

    def test_period_astype_to_timestamp(self) -> None:
        ...

    def test_to_timestamp_1703(self) -> None:
        ...