# Stubs for pandas.tests.extension.test_external_block (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.
# pylint: disable=unused-argument,redefined-outer-name,no-self-use,invalid-name
# pylint: disable=relative-beyond-top-level,line-too-long,arguments-differ
# pylint: disable=no-member,too-few-public-methods,keyword-arg-before-vararg
# pylint: disable=super-init-not-called,abstract-method,redefined-builtin
# pylint: disable=unused-import,useless-import-alias,signature-differs
# pylint: disable=blacklisted-name,c-extension-no-member,too-many-ancestors

from typing import Any, Optional
from pandas.core.internals.blocks import Block, NonConsolidatableMixIn

class CustomBlock(NonConsolidatableMixIn, Block):
    def formatting_values(self) -> Any:
        ...

    def concat_same_type(self, to_concat: Any, placement: Optional[Any] = ...) -> Any:
        ...


def df():
    ...


def test_custom_repr() -> None:
    ...


def test_concat_series() -> None:
    ...


def test_concat_dataframe(df: Any) -> None:
    ...


def test_concat_axis1(df: Any) -> None:
    ...
