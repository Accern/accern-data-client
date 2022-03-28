# Stubs for pandas.tests.extension.base.ops (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.
# pylint: disable=unused-argument,redefined-outer-name,no-self-use,invalid-name
# pylint: disable=relative-beyond-top-level,line-too-long,arguments-differ
# pylint: disable=no-member,too-few-public-methods,keyword-arg-before-vararg
# pylint: disable=super-init-not-called,abstract-method,redefined-builtin
# pylint: disable=unused-import,useless-import-alias,signature-differs
# pylint: disable=blacklisted-name,c-extension-no-member,import-error

from typing import Any
from .base import BaseExtensionTests


class BaseOpsUtil(BaseExtensionTests):
    def get_op_from_name(self, op_name: Any) -> Any:
        ...

    def check_opname(self, s: Any, op_name: Any, other: Any, exc: Any = ...) -> None:
        ...


class BaseArithmeticOpsTests(BaseOpsUtil):
    series_scalar_exc: Any = ...
    frame_scalar_exc: Any = ...
    series_array_exc: Any = ...
    divmod_exc: Any = ...
    def test_arith_series_with_scalar(self, data: Any, all_arithmetic_operators: Any) -> None:
        ...

    def test_arith_frame_with_scalar(self, data: Any, all_arithmetic_operators: Any) -> None:
        ...

    def test_arith_series_with_array(self, data: Any, all_arithmetic_operators: Any) -> None:
        ...

    def test_divmod(self, data: Any) -> None:
        ...

    def test_divmod_series_array(self, data: Any, data_for_twos: Any) -> None:
        ...

    def test_add_series_with_extension_array(self, data: Any) -> None:
        ...

    def test_error(self, data: Any, all_arithmetic_operators: Any) -> None:
        ...

    def test_direct_arith_with_series_returns_not_implemented(self, data: Any) -> None:
        ...


class BaseComparisonOpsTests(BaseOpsUtil):
    def test_compare_scalar(self, data: Any, all_compare_operators: Any) -> None:
        ...

    def test_compare_array(self, data: Any, all_compare_operators: Any) -> None:
        ...

    def test_direct_arith_with_series_returns_not_implemented(self, data: Any) -> None:
        ...