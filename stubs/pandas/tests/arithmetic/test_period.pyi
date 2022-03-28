# Stubs for pandas.tests.arithmetic.test_period (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.
# pylint: disable=unused-argument,redefined-outer-name,no-self-use,invalid-name
# pylint: disable=relative-beyond-top-level,line-too-long,arguments-differ
# pylint: disable=no-member,too-few-public-methods,keyword-arg-before-vararg
# pylint: disable=super-init-not-called,abstract-method,redefined-builtin
# pylint: disable=unused-import,useless-import-alias,signature-differs
# pylint: disable=blacklisted-name,c-extension-no-member,import-error

from typing import Any

class TestPeriodArrayLikeComparisons:
    def test_compare_zerodim(self, box_with_array: Any) -> None:
        ...


class TestPeriodIndexComparisons:
    def test_eq(self, other: Any) -> None:
        ...

    def test_pi_cmp_period(self) -> None:
        ...

    def test_parr_cmp_period_scalar2(self, box_with_array: Any) -> None:
        ...

    def test_parr_cmp_period_scalar(
            self, freq: Any, box_with_array: Any) -> None:
        ...

    def test_parr_cmp_pi(self, freq: Any, box_with_array: Any) -> None:
        ...

    def test_parr_cmp_pi_mismatched_freq_raises(
            self, freq: Any, box_with_array: Any) -> None:
        ...

    def test_pi_cmp_nat(self, freq: Any) -> None:
        ...

    def test_pi_cmp_nat_mismatched_freq_raises(self, freq: Any) -> None:
        ...

    def test_comp_nat(self, dtype: Any) -> None:
        ...


class TestPeriodSeriesComparisons:
    def test_cmp_series_period_series_mixed_freq(self) -> None:
        ...


class TestPeriodIndexSeriesComparisonConsistency:
    def test_pi_comp_period(self):
        ...

    def test_pi_comp_period_nat(self):
        ...


class TestPeriodFrameArithmetic:
    def test_ops_frame_period(self) -> None:
        ...


class TestPeriodIndexArithmetic:
    def test_parr_add_iadd_parr_raises(self, box_with_array: Any) -> None:
        ...

    def test_pi_sub_isub_pi(self) -> None:
        ...

    def test_pi_sub_pi_with_nat(self) -> None:
        ...

    def test_parr_sub_pi_mismatched_freq(self, box_with_array: Any) -> None:
        ...

    def test_sub_n_gt_1_ticks(self, tick_classes: Any, n: Any) -> None:
        ...

    def test_sub_n_gt_1_offsets(
            self, offset: Any, kwd_name: Any, n: Any) -> None:
        ...

    def test_parr_add_sub_float_raises(
            self, op: Any, other: Any, box_with_array: Any) -> None:
        ...

    def test_parr_add_sub_datetime_scalar(
            self, other: Any, box_with_array: Any) -> None:
        ...

    def test_parr_add_sub_dt64_array_raises(self, box_with_array: Any) -> None:
        ...

    def test_pi_add_sub_td64_array_non_tick_raises(self) -> None:
        ...

    def test_pi_add_sub_td64_array_tick(self) -> None:
        ...

    def test_pi_add_offset_array(self, box: Any) -> None:
        ...

    def test_pi_sub_offset_array(self, box: Any) -> None:
        ...

    def test_pi_add_iadd_int(self, one: Any) -> None:
        ...

    def test_pi_sub_isub_int(self, one: Any) -> None:
        ...

    def test_pi_sub_intlike(self, five: Any) -> None:
        ...

    def test_pi_sub_isub_offset(self) -> None:
        ...

    def test_pi_add_offset_n_gt1(self, box_transpose_fail: Any) -> None:
        ...

    def test_pi_add_offset_n_gt1_not_divisible(
            self, box_with_array: Any) -> None:
        ...

    def test_pi_add_intarray(self, int_holder: Any, op: Any) -> None:
        ...

    def test_pi_sub_intarray(self, int_holder: Any) -> None:
        ...

    def test_pi_add_timedeltalike_minute_gt1(self, three_days: Any) -> None:
        ...

    def test_pi_add_timedeltalike_tick_gt1(
            self, three_days: Any, freqstr: Any) -> None:
        ...

    def test_pi_add_iadd_timedeltalike_daily(self, three_days: Any) -> None:
        ...

    def test_pi_sub_isub_timedeltalike_daily(self, three_days: Any) -> None:
        ...

    def test_pi_add_sub_timedeltalike_freq_mismatch_daily(
            self, not_daily: Any) -> None:
        ...

    def test_pi_add_iadd_timedeltalike_hourly(self, two_hours: Any) -> None:
        ...

    def test_pi_add_timedeltalike_mismatched_freq_hourly(
            self, not_hourly: Any) -> None:
        ...

    def test_pi_sub_isub_timedeltalike_hourly(self, two_hours: Any) -> None:
        ...

    def test_add_iadd_timedeltalike_annual(self) -> None:
        ...

    def test_pi_add_sub_timedeltalike_freq_mismatch_annual(
            self, mismatched_freq: Any) -> None:
        ...

    def test_pi_add_iadd_timedeltalike_M(self) -> None:
        ...

    def test_pi_add_sub_timedeltalike_freq_mismatch_monthly(
            self, mismatched_freq: Any) -> None:
        ...

    def test_parr_add_sub_td64_nat(self, box_transpose_fail: Any) -> None:
        ...


class TestPeriodSeriesArithmetic:
    def test_ops_series_timedelta(self) -> None:
        ...

    def test_ops_series_period(self) -> None:
        ...


class TestPeriodIndexSeriesMethods:
    def test_pi_ops(self):
        ...

    def test_parr_ops_errors(
            self, ng: Any, func: Any, box_with_array: Any) -> None:
        ...

    def test_pi_ops_nat(self):
        ...

    def test_pi_ops_array_int(self):
        ...

    def test_pi_ops_offset(self):
        ...

    def test_pi_offset_errors(self) -> None:
        ...

    def test_pi_sub_period(self) -> None:
        ...

    def test_pi_sub_pdnat(self) -> None:
        ...

    def test_pi_sub_period_nat(self) -> None:
        ...