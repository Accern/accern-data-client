from ..auto import tqdm as tqdm_auto
from .utils_worker import MonoWorker
from typing import Any

class DiscordIO(MonoWorker):
    text: Any = ...
    message: Any = ...
    def __init__(self, token: Any, channel_id: Any) -> None: ...
    def write(self, s: Any): ...

class tqdm_discord(tqdm_auto):
    dio: Any = ...
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def display(self, **kwargs: Any) -> None: ...
    def clear(self, *args: Any, **kwargs: Any) -> None: ...

def tdrange(*args: Any, **kwargs: Any): ...
tqdm = tqdm_discord
trange = tdrange
