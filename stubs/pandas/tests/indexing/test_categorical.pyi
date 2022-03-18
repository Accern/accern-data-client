# Stubs for pandas.tests.indexing.test_categorical (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.
# pylint: disable=unused-argument,redefined-outer-name,no-self-use,invalid-name
# pylint: disable=relative-beyond-top-level,line-too-long,arguments-differ
# pylint: disable=no-member,too-few-public-methods,keyword-arg-before-vararg
# pylint: disable=super-init-not-called,abstract-method,redefined-builtin
# pylint: disable=blacklisted-name

from typing import Any

class TestCategoricalIndex:
    df: Any = ...
    df2: Any = ...
    df3: Any = ...
    df4: Any = ...
    def setup_method(self, method: Any) -> None:
        ...

    def test_loc_scalar(self) -> None:
        ...

    def test_getitem_scalar(self) -> None:
        ...

    def test_slicing_directly(self) -> None:
        ...

    def test_slicing(self) -> None:
        ...

    def test_slicing_and_getting_ops(self) -> None:
        ...

    def test_slicing_doc_examples(self) -> None:
        ...

    def test_getitem_category_type(self) -> None:
        ...

    def test_loc_listlike(self) -> None:
        ...

    def test_loc_listlike_dtypes(self) -> None:
        ...

    def test_get_indexer_array(self) -> None:
        ...

    def test_get_indexer_same_categories_same_order(self) -> None:
        ...

    def test_get_indexer_same_categories_different_order(self) -> None:
        ...

    def test_getitem_with_listlike(self) -> None:
        ...

    def test_setitem_listlike(self) -> None:
        ...

    def test_ix_categorical_index(self) -> None:
        ...

    def test_read_only_source(self) -> None:
        ...

    def test_reindexing(self) -> None:
        ...

    def test_loc_slice(self) -> None:
        ...

    def test_loc_and_at_with_categorical_index(self) -> None:
        ...

    def test_boolean_selection(self) -> None:
        ...

    def test_indexing_with_category(self) -> None:
        ...

    def test_map_with_dict_or_series(self) -> None:
        ...
