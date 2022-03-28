# Stubs for pandas.tests.io.test_pickle (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.
# pylint: disable=unused-argument,redefined-outer-name,no-self-use,invalid-name
# pylint: disable=relative-beyond-top-level,line-too-long,arguments-differ
# pylint: disable=no-member,too-few-public-methods,keyword-arg-before-vararg
# pylint: disable=super-init-not-called,abstract-method,redefined-builtin

from typing import Any, Optional

def current_pickle_data():
    ...


def compare_element(result: Any, expected: Any, typ: Any, version: Optional[Any] = ...) -> None:
    ...


def compare(data: Any, vf: Any, version: Any) -> None:
    ...


def compare_sp_series_ts(res: Any, exp: Any, typ: Any, version: Any) -> None:
    ...


def compare_series_ts(result: Any, expected: Any, typ: Any, version: Any) -> None:
    ...


def compare_series_dt_tz(result: Any, expected: Any, typ: Any, version: Any) -> None:
    ...


def compare_series_cat(result: Any, expected: Any, typ: Any, version: Any) -> None:
    ...


def compare_frame_dt_mixed_tzs(result: Any, expected: Any, typ: Any, version: Any) -> None:
    ...


def compare_frame_cat_onecol(result: Any, expected: Any, typ: Any, version: Any) -> None:
    ...


def compare_frame_cat_and_float(result: Any, expected: Any, typ: Any, version: Any) -> None:
    ...


def compare_index_period(result: Any, expected: Any, typ: Any, version: Any) -> None:
    ...


def compare_sp_frame_float(result: Any, expected: Any, typ: Any, version: Any) -> None:
    ...



files: Any

def legacy_pickle(request: Any, datapath: Any) -> Any:
    ...


def test_pickles(current_pickle_data: Any, legacy_pickle: Any) -> None:
    ...


def test_round_trip_current(current_pickle_data: Any) -> None:
    ...


def test_pickle_v0_14_1(datapath: Any) -> None:
    ...


def test_pickle_v0_15_2(datapath: Any) -> None:
    ...


def test_pickle_path_pathlib() -> None:
    ...


def test_pickle_path_localpath() -> None:
    ...


def get_random_path():
    ...



class TestCompression:
    def compress_file(self, src_path: Any, dest_path: Any, compression: Any) -> None:
        ...


    def test_write_explicit(self, compression: Any, get_random_path: Any) -> None:
        ...


    def test_write_explicit_bad(self, compression: Any, get_random_path: Any) -> None:
        ...


    def test_write_infer(self, ext: Any, get_random_path: Any) -> None:
        ...


    def test_read_explicit(self, compression: Any, get_random_path: Any) -> None:
        ...


    def test_read_infer(self, ext: Any, get_random_path: Any) -> None:
        ...



class TestProtocol:
    def test_read(self, protocol: Any, get_random_path: Any) -> None:
        ...