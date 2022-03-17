# Stubs for pandas.tests.arrays.sparse.test_libsparse (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.
# pylint: disable=unused-argument,redefined-outer-name,no-self-use,invalid-name
# pylint: disable=relative-beyond-top-level,line-too-long,arguments-differ
# pylint: disable=no-member,too-few-public-methods,keyword-arg-before-vararg
# pylint: disable=super-init-not-called,abstract-method,redefined-builtin
# pylint: disable=unused-import,useless-import-alias,signature-differs
# pylint: disable=blacklisted-name,c-extension-no-member,import-error

from typing import Any

TEST_LENGTH: int
plain_case: Any
delete_blocks: Any
split_blocks: Any
skip_block: Any
no_intersect: Any

def check_cases(_check_case: Any) -> None:
    ...


class TestSparseIndexUnion:
    def test_index_make_union(self) -> None:
        ...

    def test_int_index_make_union(self) -> None:
        ...


class TestSparseIndexIntersect:
    def test_intersect(self) -> None:
        ...

    def test_intersect_empty(self) -> None:
        ...

    def test_intersect_identical(self) -> None:
        ...


class TestSparseIndexCommon:
    def test_int_internal(self) -> None:
        ...

    def test_block_internal(self) -> None:
        ...

    def test_lookup(self) -> None:
        ...

    def test_lookup_array(self) -> None:
        ...

    def test_lookup_basics(self) -> None:
        ...


class TestBlockIndex:
    def test_block_internal(self) -> None:
        ...

    def test_make_block_boundary(self) -> None:
        ...

    def test_equals(self) -> None:
        ...

    def test_check_integrity(self) -> None:
        ...

    def test_to_int_index(self) -> None:
        ...

    def test_to_block_index(self) -> None:
        ...


class TestIntIndex:
    def test_check_integrity(self) -> None:
        ...

    def test_int_internal(self) -> None:
        ...

    def test_equals(self) -> None:
        ...

    def test_to_block_index(self) -> None:
        ...

    def test_to_int_index(self) -> None:
        ...


class TestSparseOperators:
    def test_op(self, opname: Any) -> None:
        ...
