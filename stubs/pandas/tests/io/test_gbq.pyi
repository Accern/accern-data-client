# Stubs for pandas.tests.io.test_gbq (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.
# pylint: disable=unused-argument,redefined-outer-name,no-self-use,invalid-name
# pylint: disable=relative-beyond-top-level,line-too-long,arguments-differ
# pylint: disable=no-member,too-few-public-methods,keyword-arg-before-vararg
# pylint: disable=super-init-not-called,abstract-method,redefined-builtin

from typing import Any

api_exceptions: Any
bigquery: Any
service_account: Any
pandas_gbq: Any
PROJECT_ID: Any
PRIVATE_KEY_JSON_PATH: Any
PRIVATE_KEY_JSON_CONTENTS: Any
DATASET_ID: str
TABLE_ID: str
DESTINATION_TABLE: Any
VERSION: Any

def make_mixed_dataframe_v2(test_size: Any) -> Any:
    ...

def test_read_gbq_with_deprecated_kwargs(monkeypatch: Any) -> None:
    ...

def test_read_gbq_without_deprecated_kwargs(monkeypatch: Any) -> None:
    ...

def test_read_gbq_with_new_kwargs(monkeypatch: Any) -> None:
    ...

def test_read_gbq_without_new_kwargs(monkeypatch: Any) -> None:
    ...


class TestToGBQIntegrationWithServiceAccountKeyPath:
    @classmethod
    def setup_class(cls) -> None:
        ...

    @classmethod
    def teardown_class(cls) -> None:
        ...

    def test_roundtrip(self) -> None:
        ...