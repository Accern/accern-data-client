"""
This type stub file was generated by pyright.
"""

from collections import abc
from typing import IO, Iterator, Literal
from pandas._typing import ReadCsvBuffer
from pandas.io.parsers.base_parser import ParserBase

_BOM = ...
class PythonParser(ParserBase):
    def __init__(self, f: ReadCsvBuffer[str] | list, **kwds) -> None:
        """
        Workhorse function for processing nested list into DataFrame
        """
        ...
    
    def read(self, rows: int | None = ...): # -> tuple[Index, Sequence[Hashable] | MultiIndex, dict[Unknown, Series]] | tuple[ABCMultiIndex | Index | None, Sequence[Hashable], Mapping[Hashable, ArrayLike]]:
        ...
    
    def get_chunk(self, size=...): # -> tuple[Index, Sequence[Hashable] | MultiIndex, dict[Unknown, Series]] | tuple[ABCMultiIndex | Index | None, Sequence[Hashable], Mapping[Hashable, ArrayLike]]:
        ...
    
    _implicit_index = ...


class FixedWidthReader(abc.Iterator):
    """
    A reader of fixed-width lines.
    """
    def __init__(self, f: IO[str], colspecs: list[tuple[int, int]] | Literal["infer"], delimiter: str | None, comment: str | None, skiprows: set[int] | None = ..., infer_nrows: int = ...) -> None:
        ...
    
    def get_rows(self, infer_nrows: int, skiprows: set[int] | None = ...) -> list[str]:
        """
        Read rows from self.f, skipping as specified.

        We distinguish buffer_rows (the first <= infer_nrows
        lines) from the rows returned to detect_colspecs
        because it's simpler to leave the other locations
        with skiprows logic alone than to modify them to
        deal with the fact we skipped some rows here as
        well.

        Parameters
        ----------
        infer_nrows : int
            Number of rows to read from self.f, not counting
            rows that are skipped.
        skiprows: set, optional
            Indices of rows to skip.

        Returns
        -------
        detect_rows : list of str
            A list containing the rows to read.

        """
        ...
    
    def detect_colspecs(self, infer_nrows: int = ..., skiprows: set[int] | None = ...) -> list[tuple[int, int]]:
        ...
    
    def __next__(self) -> list[str]:
        ...
    


class FixedWidthFieldParser(PythonParser):
    """
    Specialization that Converts fixed-width fields into DataFrames.
    See PythonParser for details.
    """
    def __init__(self, f: ReadCsvBuffer[str], **kwds) -> None:
        ...
    


def count_empty_vals(vals) -> int:
    ...

