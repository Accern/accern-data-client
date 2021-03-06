from ..utils import ObjectWrapper
from typing import Any, Optional

class DummyTqdmFile(ObjectWrapper):
    def __init__(self, wrapped: Any) -> None: ...
    def write(self, x: Any, nolock: bool = ...) -> None: ...
    def __del__(self) -> None: ...

def tenumerate(iterable: Any, start: int = ..., total: Optional[Any] = ..., tqdm_class: Any = ..., **tqdm_kwargs: Any): ...
def tzip(iter1: Any, *iter2plus: Any, **tqdm_kwargs: Any) -> None: ...
def tmap(function: Any, *sequences: Any, **tqdm_kwargs: Any) -> None: ...
