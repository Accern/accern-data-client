# pylint: disable=unused-argument,too-few-public-methods,no-self-use
# Stubs for pandas._libs.tslibs (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.
from typing import Any, TYPE_CHECKING, overload, Union
import datetime
if TYPE_CHECKING:
    from pandas import Timestamp

TDistance = Union['Timedelta', datetime.timedelta]


class Timedelta:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        ...

    @overload
    def __add__(self, other: 'Timestamp') -> 'Timestamp':
        ...

    @overload
    def __add__(self, other: TDistance) -> 'Timedelta':
        ...

    def __sub__(self, other: TDistance) -> 'Timedelta':
        ...

    def __truediv__(self, other: TDistance) -> float:
        ...

    def __rtruediv__(self, other: TDistance) -> float:
        ...

    seconds: int = ...

    def __lt__(self, other: TDistance) -> bool:
        ...

    def __le__(self, other: TDistance) -> bool:
        ...

    def __eq__(self, other: object) -> bool:
        ...

    def __ne__(self, other: object) -> bool:
        ...

    def __gt__(self, other: TDistance) -> bool:
        ...

    def __ge__(self, other: TDistance) -> bool:
        ...

    def total_seconds(self) -> int:
        ...


delta_to_nanoseconds: Any
ints_to_pytimedelta: Any