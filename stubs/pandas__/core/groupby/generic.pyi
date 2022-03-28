"""
This type stub file was generated by pyright.
"""

from typing import Any, Callable, Hashable, NamedTuple, Sequence, TypeVar, Union
from pandas.util._decorators import Appender, Substitution, doc
from pandas.core.frame import DataFrame
from pandas.core.groupby import base
from pandas.core.groupby.groupby import GroupBy, _agg_template, _apply_docs, _transform_template
from pandas.core.series import Series

"""
Define the SeriesGroupBy and DataFrameGroupBy
classes that hold the groupby interfaces (and some implementations).

These are user facing as the result of the ``df.groupby(...)`` operations,
which here returns a DataFrameGroupBy object.
"""
AggScalar = Union[str, Callable[..., Any]]
ScalarResult = TypeVar("ScalarResult")
class NamedAgg(NamedTuple):
    column: Hashable
    aggfunc: AggScalar
    ...


def generate_property(name: str, klass: type[DataFrame | Series]): # -> property:
    """
    Create a property for a GroupBy subclass to dispatch to DataFrame/Series.

    Parameters
    ----------
    name : str
    klass : {DataFrame, Series}

    Returns
    -------
    property
    """
    ...

def pin_allowlisted_properties(klass: type[DataFrame | Series], allowlist: frozenset[str]): # -> (cls: Unknown) -> Unknown:
    """
    Create GroupBy member defs for DataFrame/Series names in a allowlist.

    Parameters
    ----------
    klass : DataFrame or Series class
        class where members are defined.
    allowlist : frozenset[str]
        Set of names of klass methods to be constructed

    Returns
    -------
    class decorator

    Notes
    -----
    Since we don't want to override methods explicitly defined in the
    base class, any such name is skipped.
    """
    ...

@pin_allowlisted_properties(Series, base.series_apply_allowlist)
class SeriesGroupBy(GroupBy[Series]):
    _apply_allowlist = ...
    _agg_examples_doc = ...
    @Appender(_apply_docs["template"].format(input="series", examples=_apply_docs["series_examples"]))
    def apply(self, func, *args, **kwargs):
        ...
    
    @doc(_agg_template, examples=_agg_examples_doc, klass="Series")
    def aggregate(self, func=..., *args, engine=..., engine_kwargs=..., **kwargs):
        ...
    
    agg = ...
    @Substitution(klass="Series")
    @Appender(_transform_template)
    def transform(self, func, *args, engine=..., engine_kwargs=..., **kwargs): # -> DataFrame | Series | Any:
        ...
    
    def filter(self, func, dropna: bool = ..., *args, **kwargs): # -> NDFrameT@GroupBy | Series* | None:
        """
        Return a copy of a Series excluding elements from groups that
        do not satisfy the boolean criterion specified by func.

        Parameters
        ----------
        func : function
            To apply to each group. Should return True or False.
        dropna : Drop groups that do not pass the filter. True by default;
            if False, groups that evaluate False are filled with NaNs.

        Notes
        -----
        Functions that mutate the passed object can produce unexpected
        behavior or errors and are not supported. See :ref:`gotchas.udf-mutation`
        for more details.

        Examples
        --------
        >>> df = pd.DataFrame({'A' : ['foo', 'bar', 'foo', 'bar',
        ...                           'foo', 'bar'],
        ...                    'B' : [1, 2, 3, 4, 5, 6],
        ...                    'C' : [2.0, 5., 8., 1., 2., 9.]})
        >>> grouped = df.groupby('A')
        >>> df.groupby('A').B.filter(lambda x: x.mean() > 3.)
        1    2
        3    4
        5    6
        Name: B, dtype: int64

        Returns
        -------
        filtered : Series
        """
        ...
    
    def nunique(self, dropna: bool = ...) -> Series:
        """
        Return number of unique elements in the group.

        Returns
        -------
        Series
            Number of unique values within each group.
        """
        ...
    
    @doc(Series.describe)
    def describe(self, **kwargs): # -> Any | DataFrame | Series:
        ...
    
    def value_counts(self, normalize: bool = ..., sort: bool = ..., ascending: bool = ..., bins=..., dropna: bool = ...): # -> Series:
        ...
    
    @doc(Series.nlargest)
    def nlargest(self, n: int = ..., keep: str = ...): # -> DataFrame | Series:
        ...
    
    @doc(Series.nsmallest)
    def nsmallest(self, n: int = ..., keep: str = ...): # -> DataFrame | Series:
        ...
    


@pin_allowlisted_properties(DataFrame, base.dataframe_apply_allowlist)
class DataFrameGroupBy(GroupBy[DataFrame]):
    _apply_allowlist = ...
    _agg_examples_doc = ...
    @doc(_agg_template, examples=_agg_examples_doc, klass="DataFrame")
    def aggregate(self, func=..., *args, engine=..., engine_kwargs=..., **kwargs):
        ...
    
    agg = ...
    @Substitution(klass="DataFrame")
    @Appender(_transform_template)
    def transform(self, func, *args, engine=..., engine_kwargs=..., **kwargs): # -> DataFrame | Series | Any:
        ...
    
    def filter(self, func, dropna=..., *args, **kwargs):
        """
        Return a copy of a DataFrame excluding filtered elements.

        Elements from groups are filtered if they do not satisfy the
        boolean criterion specified by func.

        Parameters
        ----------
        func : function
            Function to apply to each subframe. Should return True or False.
        dropna : Drop groups that do not pass the filter. True by default;
            If False, groups that evaluate False are filled with NaNs.

        Returns
        -------
        filtered : DataFrame

        Notes
        -----
        Each subframe is endowed the attribute 'name' in case you need to know
        which group you are working on.

        Functions that mutate the passed object can produce unexpected
        behavior or errors and are not supported. See :ref:`gotchas.udf-mutation`
        for more details.

        Examples
        --------
        >>> df = pd.DataFrame({'A' : ['foo', 'bar', 'foo', 'bar',
        ...                           'foo', 'bar'],
        ...                    'B' : [1, 2, 3, 4, 5, 6],
        ...                    'C' : [2.0, 5., 8., 1., 2., 9.]})
        >>> grouped = df.groupby('A')
        >>> grouped.filter(lambda x: x['B'].mean() > 3.)
             A  B    C
        1  bar  2  5.0
        3  bar  4  1.0
        5  bar  6  9.0
        """
        ...
    
    def __getitem__(self, key) -> DataFrameGroupBy | SeriesGroupBy:
        ...
    
    def nunique(self, dropna: bool = ...) -> DataFrame:
        """
        Return DataFrame with counts of unique elements in each position.

        Parameters
        ----------
        dropna : bool, default True
            Don't include NaN in the counts.

        Returns
        -------
        nunique: DataFrame

        Examples
        --------
        >>> df = pd.DataFrame({'id': ['spam', 'egg', 'egg', 'spam',
        ...                           'ham', 'ham'],
        ...                    'value1': [1, 5, 5, 2, 5, 5],
        ...                    'value2': list('abbaxy')})
        >>> df
             id  value1 value2
        0  spam       1      a
        1   egg       5      b
        2   egg       5      b
        3  spam       2      a
        4   ham       5      x
        5   ham       5      y

        >>> df.groupby('id').nunique()
              value1  value2
        id
        egg        1       1
        ham        1       2
        spam       2       1

        Check for rows with the same id but conflicting values:

        >>> df.groupby('id').filter(lambda g: (g.nunique() > 1).any())
             id  value1 value2
        0  spam       1      a
        3  spam       2      a
        4   ham       5      x
        5   ham       5      y
        """
        ...
    
    @Appender(DataFrame.idxmax.__doc__)
    def idxmax(self, axis=..., skipna: bool = ...): # -> DataFrame | Series:
        ...
    
    @Appender(DataFrame.idxmin.__doc__)
    def idxmin(self, axis=..., skipna: bool = ...): # -> DataFrame | Series:
        ...
    
    boxplot = ...
    def value_counts(self, subset: Sequence[Hashable] | None = ..., normalize: bool = ..., sort: bool = ..., ascending: bool = ..., dropna: bool = ...) -> DataFrame | Series:
        """
        Return a Series or DataFrame containing counts of unique rows.

        .. versionadded:: 1.4.0

        Parameters
        ----------
        subset : list-like, optional
            Columns to use when counting unique combinations.
        normalize : bool, default False
            Return proportions rather than frequencies.
        sort : bool, default True
            Sort by frequencies.
        ascending : bool, default False
            Sort in ascending order.
        dropna : bool, default True
            Don’t include counts of rows that contain NA values.

        Returns
        -------
        Series or DataFrame
            Series if the groupby as_index is True, otherwise DataFrame.

        See Also
        --------
        Series.value_counts: Equivalent method on Series.
        DataFrame.value_counts: Equivalent method on DataFrame.
        SeriesGroupBy.value_counts: Equivalent method on SeriesGroupBy.

        Notes
        -----
        - If the groupby as_index is True then the returned Series will have a
          MultiIndex with one level per input column.
        - If the groupby as_index is False then the returned DataFrame will have an
          additional column with the value_counts. The column is labelled 'count' or
          'proportion', depending on the ``normalize`` parameter.

        By default, rows that contain any NA values are omitted from
        the result.

        By default, the result will be in descending order so that the
        first element of each group is the most frequently-occurring row.

        Examples
        --------
        >>> df = pd.DataFrame({
        ...    'gender': ['male', 'male', 'female', 'male', 'female', 'male'],
        ...    'education': ['low', 'medium', 'high', 'low', 'high', 'low'],
        ...    'country': ['US', 'FR', 'US', 'FR', 'FR', 'FR']
        ... })

        >>> df
            gender 	education 	country
        0 	male 	low 	    US
        1 	male 	medium 	    FR
        2 	female 	high 	    US
        3 	male 	low 	    FR
        4 	female 	high 	    FR
        5 	male 	low 	    FR

        >>> df.groupby('gender').value_counts()
        gender  education  country
        female  high       FR         1
                           US         1
        male    low        FR         2
                           US         1
                medium     FR         1
        dtype: int64

        >>> df.groupby('gender').value_counts(ascending=True)
        gender  education  country
        female  high       FR         1
                           US         1
        male    low        US         1
                medium     FR         1
                low        FR         2
        dtype: int64

        >>> df.groupby('gender').value_counts(normalize=True)
        gender  education  country
        female  high       FR         0.50
                           US         0.50
        male    low        FR         0.50
                           US         0.25
                medium     FR         0.25
        dtype: float64

        >>> df.groupby('gender', as_index=False).value_counts()
           gender education country  count
        0  female      high      FR      1
        1  female      high      US      1
        2    male       low      FR      2
        3    male       low      US      1
        4    male    medium      FR      1

        >>> df.groupby('gender', as_index=False).value_counts(normalize=True)
           gender education country  proportion
        0  female      high      FR        0.50
        1  female      high      US        0.50
        2    male       low      FR        0.50
        3    male       low      US        0.25
        4    male    medium      FR        0.25
        """
        ...
    


