from typing import Optional

import tqdm

IS_JUPYTER: Optional[bool] = None
L_BAR = "{desc}: |"
R_BAR = "| {percentage:3.0f}%"
BAR_FMT = f"{L_BAR}{{bar}}{R_BAR}"


def is_jupyter() -> bool:
    global IS_JUPYTER

    if IS_JUPYTER is not None:
        return IS_JUPYTER

    try:
        from IPython import get_ipython

        IS_JUPYTER = get_ipython() is not None
    except (NameError, ModuleNotFoundError) as _:
        IS_JUPYTER = False
    return IS_JUPYTER


class ProgressBar:
    def __init__(
            self,
            total: int,
            desc: str,
            verbose: bool,
            unit_scale: bool = True) -> None:
        self._verbosity = verbose
        if verbose:
            self._pbar = None
        elif is_jupyter():
            self._pbar = tqdm.tqdm_notebook(
                total=total,
                desc=desc,
                unit_scale=unit_scale,
                bar_format=BAR_FMT)
        else:
            self._pbar = tqdm.tqdm(
                total=total,
                desc=desc,
                unit_scale=unit_scale,
                bar_format=BAR_FMT)

    def update(self, num: int) -> None:
        if self._pbar is not None:
            self._pbar.update(num)

    def set_description(self, desc: str) -> None:
        if self._pbar is not None:
            self._pbar.set_description(desc)

    def close(self) -> None:
        if self._pbar is not None:
            self._pbar.close()
