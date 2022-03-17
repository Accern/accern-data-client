# pylint: disable=unused-argument
from typing import Any, Iterable, List


def find_packages(
        where: str,
        exclude: Iterable[str],
        include: Iterable[str]) -> List[str]:
    ...


def setup(*args: Any, **kwargs: Any) -> None:
    ...
