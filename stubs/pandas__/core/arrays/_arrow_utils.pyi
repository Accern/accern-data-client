"""
This type stub file was generated by pyright.
"""

import pyarrow

def pyarrow_array_to_numpy_and_mask(arr, dtype): # -> tuple[Any, ndarray]:
    """
    Convert a primitive pyarrow.Array to a numpy array and boolean mask based
    on the buffers of the Array.

    At the moment pyarrow.BooleanArray is not supported.

    Parameters
    ----------
    arr : pyarrow.Array
    dtype : numpy.dtype

    Returns
    -------
    (data, mask)
        Tuple of two numpy arrays with the raw data (with specified dtype) and
        a boolean mask (validity mask, so False means missing)
    """
    ...

class ArrowPeriodType(pyarrow.ExtensionType):
    def __init__(self, freq) -> None:
        ...
    
    @property
    def freq(self):
        ...
    
    def __arrow_ext_serialize__(self): # -> bytes:
        ...
    
    @classmethod
    def __arrow_ext_deserialize__(cls, storage_type, serialized): # -> ArrowPeriodType:
        ...
    
    def __eq__(self, other) -> bool:
        ...
    
    def __hash__(self) -> int:
        ...
    
    def to_pandas_dtype(self): # -> PeriodDtype | PandasExtensionDtype:
        ...
    


_period_type = ...
class ArrowIntervalType(pyarrow.ExtensionType):
    def __init__(self, subtype, closed) -> None:
        ...
    
    @property
    def subtype(self):
        ...
    
    @property
    def closed(self):
        ...
    
    def __arrow_ext_serialize__(self): # -> bytes:
        ...
    
    @classmethod
    def __arrow_ext_deserialize__(cls, storage_type, serialized): # -> ArrowIntervalType:
        ...
    
    def __eq__(self, other) -> bool:
        ...
    
    def __hash__(self) -> int:
        ...
    
    def to_pandas_dtype(self): # -> IntervalDtype | PandasExtensionDtype:
        ...
    


_interval_type = ...
