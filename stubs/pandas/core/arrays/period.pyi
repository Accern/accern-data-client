# Stubs for pandas.core.arrays.period (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.
# pylint: disable=unused-import,unused-argument,invalid-name,redefined-builtin
# pylint: disable=too-few-public-methods,no-self-use,function-redefined
# pylint: disable=redefined-outer-name,too-many-ancestors,super-init-not-called
# pylint: disable=too-many-arguments,no-name-in-module

from typing import Any, Optional, Sequence
from pandas._libs.tslibs.period import Period
from pandas.core.arrays import datetimelike as dtl
from pandas.tseries.offsets import Tick


class PeriodArray(dtl.DatetimeLikeArrayMixin, dtl.DatelikeOps):
    __array_priority__: int = ...

    def __init__(self, values: Any, freq: Optional[Any] = ...,
                 dtype: Optional[Any] = ..., copy: bool = ...) -> None:
        ...

    def dtype(self) -> Any:
        ...

    @property  # type: ignore
    def freq(self) -> Any:
        ...

    def __array__(self, dtype: Optional[Any] = ...) -> Any:
        ...

    year: Any = ...
    month: Any = ...
    day: Any = ...
    hour: Any = ...
    minute: Any = ...
    second: Any = ...
    weekofyear: Any = ...
    week: Any = ...
    dayofweek: Any = ...
    weekday: Any = ...
    dayofyear: Any = ...
    day_of_year: Any = ...
    quarter: Any = ...
    qyear: Any = ...
    days_in_month: Any = ...
    daysinmonth: Any = ...

    @property
    def is_leap_year(self) -> Any:
        ...

    @property
    def start_time(self) -> Any:
        ...

    @property
    def end_time(self) -> Any:
        ...

    def to_timestamp(self, freq: Optional[Any] = ..., how: str = ...) -> Any:
        ...

    def asfreq(self, freq: Optional[Any] = ..., how: str = ...) -> Any:
        ...

    def astype(self, dtype: Any, copy: bool = ...) -> Any:
        ...

    @property
    def flags(self) -> Any:
        ...


def period_array(data: Sequence[Optional[Period]], freq: Optional[Tick] = ...,
                 copy: bool = ...) -> PeriodArray:
    ...


def validate_dtype_freq(dtype: Any, freq: Any) -> Any:
    ...


def dt64arr_to_periodarr(data: Any, freq: Any, tz: Optional[Any] = ...) -> Any:
    ...
