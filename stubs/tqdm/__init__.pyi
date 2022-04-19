from ._monitor import TMonitor as TMonitor, TqdmSynchronisationWarning as TqdmSynchronisationWarning
from ._tqdm_pandas import tqdm_pandas as tqdm_pandas
from .cli import main as main
from .gui import tqdm as tqdm_gui, trange as tgrange
from .notebook import tqdm as _tqdm_nb
from .std import TqdmDeprecationWarning as TqdmDeprecationWarning, TqdmExperimentalWarning as TqdmExperimentalWarning, TqdmKeyError as TqdmKeyError, TqdmMonitorWarning as TqdmMonitorWarning, TqdmTypeError as TqdmTypeError, TqdmWarning as TqdmWarning, tqdm as tqdm, trange as trange
from typing import Any

def tqdm_notebook(*args: Any, **kwargs: Any) -> _tqdm_nb: ...
def tnrange(*args: Any, **kwargs: Any) -> Any: ...
