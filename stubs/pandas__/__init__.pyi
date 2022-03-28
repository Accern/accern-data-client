"""
This type stub file was generated by pyright.
"""

import pandas.core.config_init
from pandas.compat import is_numpy_dev as _is_numpy_dev
from pandas._config import describe_option, get_option, option_context, options, reset_option, set_option
from pandas.core.api import BooleanDtype, Categorical, CategoricalDtype, CategoricalIndex, DataFrame, DateOffset, DatetimeIndex, DatetimeTZDtype, Flags, Float32Dtype, Float64Dtype, Grouper, Index, IndexSlice, Int16Dtype, Int32Dtype, Int64Dtype, Int8Dtype, Interval, IntervalDtype, IntervalIndex, MultiIndex, NA, NaT, NamedAgg, Period, PeriodDtype, PeriodIndex, RangeIndex, Series, StringDtype, Timedelta, TimedeltaIndex, Timestamp, UInt16Dtype, UInt32Dtype, UInt64Dtype, UInt8Dtype, array, bdate_range, date_range, factorize, interval_range, isna, isnull, notna, notnull, period_range, set_eng_float_format, timedelta_range, to_datetime, to_numeric, to_timedelta, unique, value_counts
from pandas.core.arrays.sparse import SparseDtype
from pandas.tseries.api import infer_freq
from pandas.tseries import offsets
from pandas.core.computation.api import eval
from pandas.core.reshape.api import concat, crosstab, cut, get_dummies, lreshape, melt, merge, merge_asof, merge_ordered, pivot, pivot_table, qcut, wide_to_long
from pandas import api, arrays, errors, io, plotting, testing, tseries
from pandas.util._print_versions import show_versions
from pandas.io.api import ExcelFile, ExcelWriter, HDFStore, read_clipboard, read_csv, read_excel, read_feather, read_fwf, read_gbq, read_hdf, read_html, read_json, read_orc, read_parquet, read_pickle, read_sas, read_spss, read_sql, read_sql_query, read_sql_table, read_stata, read_table, read_xml, to_pickle
from pandas.io.json import _json_normalize as json_normalize
from pandas.util._tester import test
from pandas._version import get_versions

__docformat__ = ...
hard_dependencies = ...
missing_dependencies = ...
if missing_dependencies:
    ...
v = ...
__version__ = ...
__git_version__ = ...
__deprecated_num_index_names = ...
def __dir__(): # -> list[str]:
    ...

def __getattr__(name): # -> Type[datetime] | Module("numpy") | Any | Type[SparseArray]:
    ...

__doc__ = ...
__all__ = ["BooleanDtype", "Categorical", "CategoricalDtype", "CategoricalIndex", "DataFrame", "DateOffset", "DatetimeIndex", "DatetimeTZDtype", "ExcelFile", "ExcelWriter", "Flags", "Float32Dtype", "Float64Dtype", "Grouper", "HDFStore", "Index", "IndexSlice", "Int16Dtype", "Int32Dtype", "Int64Dtype", "Int8Dtype", "Interval", "IntervalDtype", "IntervalIndex", "MultiIndex", "NA", "NaT", "NamedAgg", "Period", "PeriodDtype", "PeriodIndex", "RangeIndex", "Series", "SparseDtype", "StringDtype", "Timedelta", "TimedeltaIndex", "Timestamp", "UInt16Dtype", "UInt32Dtype", "UInt64Dtype", "UInt8Dtype", "api", "array", "arrays", "bdate_range", "concat", "crosstab", "cut", "date_range", "describe_option", "errors", "eval", "factorize", "get_dummies", "get_option", "infer_freq", "interval_range", "io", "isna", "isnull", "json_normalize", "lreshape", "melt", "merge", "merge_asof", "merge_ordered", "notna", "notnull", "offsets", "option_context", "options", "period_range", "pivot", "pivot_table", "plotting", "qcut", "read_clipboard", "read_csv", "read_excel", "read_feather", "read_fwf", "read_gbq", "read_hdf", "read_html", "read_json", "read_orc", "read_parquet", "read_pickle", "read_sas", "read_spss", "read_sql", "read_sql_query", "read_sql_table", "read_stata", "read_table", "read_xml", "reset_option", "set_eng_float_format", "set_option", "show_versions", "test", "testing", "timedelta_range", "to_datetime", "to_numeric", "to_pickle", "to_timedelta", "tseries", "unique", "value_counts", "wide_to_long"]
