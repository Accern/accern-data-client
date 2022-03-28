# Stubs for pandas.tests.reshape.merge.test_merge_index_as_string (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.
# pylint: disable=unused-argument,redefined-outer-name,no-self-use,invalid-name
# pylint: disable=relative-beyond-top-level,line-too-long,arguments-differ
# pylint: disable=no-member,too-few-public-methods,keyword-arg-before-vararg
# pylint: disable=super-init-not-called,abstract-method,redefined-builtin

from typing import Any, Optional

def df1():
    ...


def df2():
    ...


def left_df(request: Any, df1: Any) -> Any:
    ...


def right_df(request: Any, df2: Any) -> Any:
    ...


def compute_expected(df_left: Any, df_right: Any, on: Optional[Any] = ..., left_on: Optional[Any] = ..., right_on: Optional[Any] = ..., how: Optional[Any] = ...) -> Any:
    ...


def test_merge_indexes_and_columns_on(left_df: Any, right_df: Any, on: Any, how: Any) -> None:
    ...


def test_merge_indexes_and_columns_lefton_righton(left_df: Any, right_df: Any, left_on: Any, right_on: Any, how: Any) -> None:
    ...


def test_join_indexes_and_columns_on(df1: Any, df2: Any, left_index: Any, join_type: Any) -> None:
    ...