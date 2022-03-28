# Stubs for pandas.tests.io.parser.test_network (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.
# pylint: disable=unused-argument,redefined-outer-name,no-self-use,invalid-name
# pylint: disable=relative-beyond-top-level,line-too-long,arguments-differ
# pylint: disable=no-member,too-few-public-methods,keyword-arg-before-vararg
# pylint: disable=super-init-not-called,abstract-method,redefined-builtin

from typing import Any

def test_compressed_urls(salaries_table: Any, compress_type: Any, extension: Any, mode: Any, engine: Any) -> None:
    ...

def check_compressed_urls(salaries_table: Any, compression: Any, extension: Any, mode: Any, engine: Any) -> None:
    ...

def tips_df(datapath: Any) -> Any:
    ...


class TestS3:
    def test_parse_public_s3_bucket(self, tips_df: Any) -> None:
        ...

    def test_parse_public_s3n_bucket(self, tips_df: Any) -> None:
        ...

    def test_parse_public_s3a_bucket(self, tips_df: Any) -> None:
        ...

    def test_parse_public_s3_bucket_nrows(self, tips_df: Any) -> None:
        ...

    def test_parse_public_s3_bucket_chunked(self, tips_df: Any) -> None:
        ...

    def test_parse_public_s3_bucket_chunked_python(self, tips_df: Any) -> None:
        ...

    def test_parse_public_s3_bucket_python(self, tips_df: Any) -> None:
        ...

    def test_infer_s3_compression(self, tips_df: Any) -> None:
        ...

    def test_parse_public_s3_bucket_nrows_python(self, tips_df: Any) -> None:
        ...

    def test_s3_fails(self) -> None:
        ...

    def test_read_csv_handles_boto_s3_object(self, s3_resource: Any, tips_file: Any) -> None:
        ...

    def test_read_csv_chunked_download(self, s3_resource: Any, caplog: Any) -> None:
        ...

    def test_read_s3_with_hash_in_key(self, tips_df: Any) -> None:
        ...