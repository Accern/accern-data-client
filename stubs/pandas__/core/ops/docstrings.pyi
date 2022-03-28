"""
This type stub file was generated by pyright.
"""

"""
Templating for ops docstrings
"""
def make_flex_doc(op_name: str, typ: str) -> str:
    """
    Make the appropriate substitutions for the given operation and class-typ
    into either _flex_doc_SERIES or _flex_doc_FRAME to return the docstring
    to attach to a generated method.

    Parameters
    ----------
    op_name : str {'__add__', '__sub__', ... '__eq__', '__ne__', ...}
    typ : str {series, 'dataframe']}

    Returns
    -------
    doc : str
    """
    ...

_common_examples_algebra_SERIES = ...
_common_examples_comparison_SERIES = ...
_add_example_SERIES = ...
_sub_example_SERIES = ...
_mul_example_SERIES = ...
_div_example_SERIES = ...
_floordiv_example_SERIES = ...
_divmod_example_SERIES = ...
_mod_example_SERIES = ...
_pow_example_SERIES = ...
_ne_example_SERIES = ...
_eq_example_SERIES = ...
_lt_example_SERIES = ...
_le_example_SERIES = ...
_gt_example_SERIES = ...
_ge_example_SERIES = ...
_returns_series = ...
_returns_tuple = ...
_op_descriptions: dict[str, dict[str, str | None]] = ...
_py_num_ref = ...
_op_names = ...
_flex_doc_SERIES = ...
_see_also_reverse_SERIES = ...
_flex_doc_FRAME = ...
_flex_comp_doc_FRAME = ...
