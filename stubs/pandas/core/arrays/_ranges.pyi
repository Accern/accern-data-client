# Stubs for pandas.core.arrays._ranges (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.
# pylint: disable=unused-argument,redefined-outer-name,no-self-use,invalid-name
# pylint: disable=relative-beyond-top-level,line-too-long,arguments-differ
# pylint: disable=no-member,too-few-public-methods,keyword-arg-before-vararg
# pylint: disable=super-init-not-called,abstract-method,redefined-builtin

from typing import Tuple
from pandas._libs.tslibs import Timestamp
from pandas.tseries.offsets import DateOffset
import numpy as np

def generate_regular_range(start: Timestamp, end: Timestamp, periods: int, freq: DateOffset) -> Tuple[np.ndarray, str]:
    ...
