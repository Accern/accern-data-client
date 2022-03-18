# Stubs for pandas.core.apply (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.
# pylint: disable=unused-argument,redefined-outer-name,no-self-use,invalid-name
# pylint: disable=relative-beyond-top-level,line-too-long,arguments-differ
# pylint: disable=no-member,too-few-public-methods,keyword-arg-before-vararg
# pylint: disable=super-init-not-called,abstract-method,redefined-builtin


from typing import Any, Optional


def frame_apply(obj: Any, func: Any, axis: int = ...,
                broadcast: Optional[Any] = ..., raw: bool = ...,
                reduce: Optional[Any] = ..., result_type: Optional[Any] = ...,
                ignore_failures: bool = ..., args: Optional[Any] = ...,
                kwds: Optional[Any] = ...) -> Any:
    ...


class FrameApply:
    obj: Any = ...
    raw: Any = ...
    ignore_failures: Any = ...
    args: Any = ...
    kwds: Any = ...
    result_type: Any = ...
    f: Any = ...
    result: Any = ...
    res_index: Any = ...
    res_columns: Any = ...

    def __init__(self, obj: Any, func: Any, broadcast: Any, raw: Any,
                 reduce: Any, result_type: Any, ignore_failures: Any,
                 args: Any, kwds: Any) -> None:
        ...

    @property
    def columns(self) -> Any:
        ...

    @property
    def index(self) -> Any:
        ...

    def values(self) -> Any:
        ...

    def dtypes(self) -> Any:
        ...

    @property
    def agg_axis(self) -> Any:
        ...

    def get_result(self) -> Any:
        ...

    def apply_empty_result(self) -> Any:
        ...

    def apply_raw(self) -> Any:
        ...

    def apply_broadcast(self, target: Any) -> Any:
        ...

    def apply_standard(self) -> Any:
        ...

    results: Any = ...

    def apply_series_generator(self) -> None:
        ...

    def wrap_results(self) -> Any:
        ...


class FrameRowApply(FrameApply):
    axis: int = ...
    def apply_broadcast(self) -> Any:  # type: ignore
        ...

    @property
    def series_generator(self) -> Any:
        ...

    @property
    def result_index(self) -> Any:
        ...

    @property
    def result_columns(self) -> Any:
        ...

    def wrap_results_for_axis(self) -> Any:
        ...


class FrameColumnApply(FrameApply):
    axis: int = ...

    def apply_broadcast(self) -> Any:  # type: ignore
        ...

    @property
    def series_generator(self) -> Any:
        ...

    @property
    def result_index(self) -> Any:
        ...

    @property
    def result_columns(self) -> Any:
        ...

    def wrap_results_for_axis(self) -> Any:
        ...

    def infer_to_same_shape(self) -> Any:
        ...
