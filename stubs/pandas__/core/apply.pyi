"""
This type stub file was generated by pyright.
"""

import abc
from typing import Any, Callable, Dict, Hashable, Iterable, Iterator, TYPE_CHECKING
from pandas._typing import AggFuncType, AggFuncTypeDict, AggObjType, Axis, NDFrameT
from pandas.util._decorators import cache_readonly
from pandas import DataFrame, Index, Series
from pandas.core.groupby import GroupBy
from pandas.core.resample import Resampler
from pandas.core.window.rolling import BaseWindow

if TYPE_CHECKING:
    ...
ResType = Dict[int, Any]
def frame_apply(obj: DataFrame, func: AggFuncType, axis: Axis = ..., raw: bool = ..., result_type: str | None = ..., args=..., kwargs=...) -> FrameApply:
    """construct and return a row or column based frame apply object"""
    ...

class Apply(metaclass=abc.ABCMeta):
    axis: int
    def __init__(self, obj: AggObjType, func, raw: bool, result_type: str | None, args, kwargs) -> None:
        ...
    
    @abc.abstractmethod
    def apply(self) -> DataFrame | Series:
        ...
    
    def agg(self) -> DataFrame | Series | None:
        """
        Provide an implementation for the aggregators.

        Returns
        -------
        Result of aggregation, or None if agg cannot be performed by
        this method.
        """
        ...
    
    def transform(self) -> DataFrame | Series:
        """
        Transform a DataFrame or Series.

        Returns
        -------
        DataFrame or Series
            Result of applying ``func`` along the given axis of the
            Series or DataFrame.

        Raises
        ------
        ValueError
            If the transform function fails or does not transform.
        """
        ...
    
    def transform_dict_like(self, func):
        """
        Compute transform in the case of a dict-like func
        """
        ...
    
    def transform_str_or_callable(self, func) -> DataFrame | Series:
        """
        Compute transform in the case of a string or callable func
        """
        ...
    
    def agg_list_like(self) -> DataFrame | Series:
        """
        Compute aggregation in the case of a list-like argument.

        Returns
        -------
        Result of aggregation.
        """
        ...
    
    def agg_dict_like(self) -> DataFrame | Series:
        """
        Compute aggregation in the case of a dict-like argument.

        Returns
        -------
        Result of aggregation.
        """
        ...
    
    def apply_str(self) -> DataFrame | Series:
        """
        Compute apply in case of a string.

        Returns
        -------
        result: Series or DataFrame
        """
        ...
    
    def apply_multiple(self) -> DataFrame | Series:
        """
        Compute apply in case of a list-like or dict-like.

        Returns
        -------
        result: Series, DataFrame, or None
            Result when self.f is a list-like or dict-like, None otherwise.
        """
        ...
    
    def normalize_dictlike_arg(self, how: str, obj: DataFrame | Series, func: AggFuncTypeDict) -> AggFuncTypeDict:
        """
        Handler for dict-like argument.

        Ensures that necessary columns exist if obj is a DataFrame, and
        that a nested renamer is not passed. Also normalizes to all lists
        when values consists of a mix of list and non-lists.
        """
        ...
    


class NDFrameApply(Apply):
    """
    Methods shared by FrameApply and SeriesApply but
    not GroupByApply or ResamplerWindowApply
    """
    @property
    def index(self) -> Index:
        ...
    
    @property
    def agg_axis(self) -> Index:
        ...
    


class FrameApply(NDFrameApply):
    obj: DataFrame
    @property
    @abc.abstractmethod
    def result_index(self) -> Index:
        ...
    
    @property
    @abc.abstractmethod
    def result_columns(self) -> Index:
        ...
    
    @property
    @abc.abstractmethod
    def series_generator(self) -> Iterator[Series]:
        ...
    
    @abc.abstractmethod
    def wrap_results_for_axis(self, results: ResType, res_index: Index) -> DataFrame | Series:
        ...
    
    @property
    def res_columns(self) -> Index:
        ...
    
    @property
    def columns(self) -> Index:
        ...
    
    @cache_readonly
    def values(self): # -> ndarray:
        ...
    
    @cache_readonly
    def dtypes(self) -> Series:
        ...
    
    def apply(self) -> DataFrame | Series:
        """compute the results"""
        ...
    
    def agg(self): # -> DataFrame | Series | Any:
        ...
    
    def apply_empty_result(self): # -> DataFrame | Series:
        """
        we have an empty result; at least 1 axis is 0

        we will try to apply the function to an empty
        series in order to see if this is a reduction function
        """
        ...
    
    def apply_raw(self): # -> DataFrame | Series:
        """apply to the values as a numpy array"""
        ...
    
    def apply_broadcast(self, target: DataFrame) -> DataFrame:
        ...
    
    def apply_standard(self): # -> DataFrame | Series:
        ...
    
    def apply_series_generator(self) -> tuple[ResType, Index]:
        ...
    
    def wrap_results(self, results: ResType, res_index: Index) -> DataFrame | Series:
        ...
    
    def apply_str(self) -> DataFrame | Series:
        ...
    


class FrameRowApply(FrameApply):
    axis = ...
    def apply_broadcast(self, target: DataFrame) -> DataFrame:
        ...
    
    @property
    def series_generator(self): # -> Generator[Series, None, None]:
        ...
    
    @property
    def result_index(self) -> Index:
        ...
    
    @property
    def result_columns(self) -> Index:
        ...
    
    def wrap_results_for_axis(self, results: ResType, res_index: Index) -> DataFrame | Series:
        """return the results for the rows"""
        ...
    


class FrameColumnApply(FrameApply):
    axis = ...
    def apply_broadcast(self, target: DataFrame) -> DataFrame:
        ...
    
    @property
    def series_generator(self): # -> Generator[Series, None, None]:
        ...
    
    @property
    def result_index(self) -> Index:
        ...
    
    @property
    def result_columns(self) -> Index:
        ...
    
    def wrap_results_for_axis(self, results: ResType, res_index: Index) -> DataFrame | Series:
        """return the results for the columns"""
        ...
    
    def infer_to_same_shape(self, results: ResType, res_index: Index) -> DataFrame:
        """infer the results to the same shape as the input object"""
        ...
    


class SeriesApply(NDFrameApply):
    obj: Series
    axis = ...
    def __init__(self, obj: Series, func: AggFuncType, convert_dtype: bool, args, kwargs) -> None:
        ...
    
    def apply(self) -> DataFrame | Series:
        ...
    
    def agg(self): # -> DataFrame | Series:
        ...
    
    def apply_empty_result(self) -> Series:
        ...
    
    def apply_standard(self) -> DataFrame | Series:
        ...
    


class GroupByApply(Apply):
    def __init__(self, obj: GroupBy[NDFrameT], func: AggFuncType, args, kwargs) -> None:
        ...
    
    def apply(self):
        ...
    
    def transform(self):
        ...
    


class ResamplerWindowApply(Apply):
    axis = ...
    obj: Resampler | BaseWindow
    def __init__(self, obj: Resampler | BaseWindow, func: AggFuncType, args, kwargs) -> None:
        ...
    
    def apply(self):
        ...
    
    def transform(self):
        ...
    


def reconstruct_func(func: AggFuncType | None, **kwargs) -> tuple[bool, AggFuncType | None, list[str] | None, list[int] | None]:
    """
    This is the internal function to reconstruct func given if there is relabeling
    or not and also normalize the keyword to get new order of columns.

    If named aggregation is applied, `func` will be None, and kwargs contains the
    column and aggregation function information to be parsed;
    If named aggregation is not applied, `func` is either string (e.g. 'min') or
    Callable, or list of them (e.g. ['min', np.max]), or the dictionary of column name
    and str/Callable/list of them (e.g. {'A': 'min'}, or {'A': [np.min, lambda x: x]})

    If relabeling is True, will return relabeling, reconstructed func, column
    names, and the reconstructed order of columns.
    If relabeling is False, the columns and order will be None.

    Parameters
    ----------
    func: agg function (e.g. 'min' or Callable) or list of agg functions
        (e.g. ['min', np.max]) or dictionary (e.g. {'A': ['min', np.max]}).
    **kwargs: dict, kwargs used in is_multi_agg_with_relabel and
        normalize_keyword_aggregation function for relabelling

    Returns
    -------
    relabelling: bool, if there is relabelling or not
    func: normalized and mangled func
    columns: list of column names
    order: list of columns indices

    Examples
    --------
    >>> reconstruct_func(None, **{"foo": ("col", "min")})
    (True, defaultdict(<class 'list'>, {'col': ['min']}), ('foo',), array([0]))

    >>> reconstruct_func("min")
    (False, 'min', None, None)
    """
    ...

def is_multi_agg_with_relabel(**kwargs) -> bool:
    """
    Check whether kwargs passed to .agg look like multi-agg with relabeling.

    Parameters
    ----------
    **kwargs : dict

    Returns
    -------
    bool

    Examples
    --------
    >>> is_multi_agg_with_relabel(a="max")
    False
    >>> is_multi_agg_with_relabel(a_max=("a", "max"), a_min=("a", "min"))
    True
    >>> is_multi_agg_with_relabel()
    False
    """
    ...

def normalize_keyword_aggregation(kwargs: dict) -> tuple[dict, list[str], list[int]]:
    """
    Normalize user-provided "named aggregation" kwargs.
    Transforms from the new ``Mapping[str, NamedAgg]`` style kwargs
    to the old Dict[str, List[scalar]]].

    Parameters
    ----------
    kwargs : dict

    Returns
    -------
    aggspec : dict
        The transformed kwargs.
    columns : List[str]
        The user-provided keys.
    col_idx_order : List[int]
        List of columns indices.

    Examples
    --------
    >>> normalize_keyword_aggregation({"output": ("input", "sum")})
    (defaultdict(<class 'list'>, {'input': ['sum']}), ('output',), array([0]))
    """
    ...

def relabel_result(result: DataFrame | Series, func: dict[str, list[Callable | str]], columns: Iterable[Hashable], order: Iterable[int]) -> dict[Hashable, Series]:
    """
    Internal function to reorder result if relabelling is True for
    dataframe.agg, and return the reordered result in dict.

    Parameters:
    ----------
    result: Result from aggregation
    func: Dict of (column name, funcs)
    columns: New columns name for relabelling
    order: New order for relabelling

    Examples:
    ---------
    >>> result = DataFrame({"A": [np.nan, 2, np.nan],
    ...       "C": [6, np.nan, np.nan], "B": [np.nan, 4, 2.5]})  # doctest: +SKIP
    >>> funcs = {"A": ["max"], "C": ["max"], "B": ["mean", "min"]}
    >>> columns = ("foo", "aab", "bar", "dat")
    >>> order = [0, 1, 2, 3]
    >>> _relabel_result(result, func, columns, order)  # doctest: +SKIP
    dict(A=Series([2.0, NaN, NaN, NaN], index=["foo", "aab", "bar", "dat"]),
         C=Series([NaN, 6.0, NaN, NaN], index=["foo", "aab", "bar", "dat"]),
         B=Series([NaN, NaN, 2.5, 4.0], index=["foo", "aab", "bar", "dat"]))
    """
    ...

def maybe_mangle_lambdas(agg_spec: Any) -> Any:
    """
    Make new lambdas with unique names.

    Parameters
    ----------
    agg_spec : Any
        An argument to GroupBy.agg.
        Non-dict-like `agg_spec` are pass through as is.
        For dict-like `agg_spec` a new spec is returned
        with name-mangled lambdas.

    Returns
    -------
    mangled : Any
        Same type as the input.

    Examples
    --------
    >>> maybe_mangle_lambdas('sum')
    'sum'
    >>> maybe_mangle_lambdas([lambda: 1, lambda: 2])  # doctest: +SKIP
    [<function __main__.<lambda_0>,
     <function pandas...._make_lambda.<locals>.f(*args, **kwargs)>]
    """
    ...

def validate_func_kwargs(kwargs: dict) -> tuple[list[str], list[str | Callable[..., Any]]]:
    """
    Validates types of user-provided "named aggregation" kwargs.
    `TypeError` is raised if aggfunc is not `str` or callable.

    Parameters
    ----------
    kwargs : dict

    Returns
    -------
    columns : List[str]
        List of user-provied keys.
    func : List[Union[str, callable[...,Any]]]
        List of user-provided aggfuncs

    Examples
    --------
    >>> validate_func_kwargs({'one': 'min', 'two': 'max'})
    (['one', 'two'], ['min', 'max'])
    """
    ...

