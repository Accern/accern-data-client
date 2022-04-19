from .std import tqdm as std_tqdm
from typing import Any, Optional

HBox = object

class TqdmHBox(HBox): ...

class tqdm_notebook(std_tqdm):
    @staticmethod
    def status_printer(_: Any, total: Optional[Any] = ..., desc: Optional[Any] = ..., ncols: Optional[Any] = ...) -> TqdmHBox: ...  # type: ignore
    displayed: bool = ...
    def display(self, msg: Optional[Any] = ..., pos: Optional[Any] = ..., close: bool = ..., bar_style: Optional[Any] = ..., check_delay: bool = ...) -> None: ...  # type: ignore
    @property
    def colour(self) -> None: ...
    @colour.setter
    def colour(self, bar_color: Any) -> None: ...
    disp: Any = ...
    ncols: Any = ...
    container: Any = ...
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def __iter__(self) -> Any: ...
    def update(self, n: int = ...) -> 'tqdm_notebook': ...
    def close(self) -> None: ...
    def clear(self, *_: Any, **__: Any) -> None: ...
    def reset(self, total: Optional[Any] = ...) -> None: ...

def tnrange(*args: Any, **kwargs: Any) -> tqdm_notebook: ...
tqdm = tqdm_notebook
trange = tnrange
