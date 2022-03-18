# Stubs for pandas.tests.io.parser.test_common (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.
# pylint: disable=unused-argument,redefined-outer-name,no-self-use,invalid-name
# pylint: disable=relative-beyond-top-level,line-too-long,arguments-differ
# pylint: disable=no-member,too-few-public-methods,keyword-arg-before-vararg
# pylint: disable=super-init-not-called,abstract-method,redefined-builtin


from typing import Any

def test_override_set_noconvert_columns() -> None:
    ...


def test_bytes_io_input(all_parsers: Any) -> None:
    ...


def test_empty_decimal_marker(all_parsers: Any) -> None:
    ...


def test_bad_stream_exception(all_parsers: Any, csv_dir_path: Any) -> None:
    ...


def test_read_csv_local(all_parsers: Any, csv1: Any) -> None:
    ...


def test_1000_sep(all_parsers: Any) -> None:
    ...


def test_squeeze(all_parsers: Any) -> None:
    ...


def test_malformed(all_parsers: Any) -> None:
    ...


def test_malformed_chunks(all_parsers: Any, nrows: Any) -> None:
    ...


def test_unnamed_columns(all_parsers: Any) -> None:
    ...


def test_csv_mixed_type(all_parsers: Any) -> None:
    ...


def test_read_csv_low_memory_no_rows_with_index(all_parsers: Any) -> None:
    ...


def test_read_csv_dataframe(all_parsers: Any, csv1: Any) -> None:
    ...


def test_read_csv_no_index_name(all_parsers: Any, csv_dir_path: Any) -> None:
    ...


def test_read_csv_unicode(all_parsers: Any) -> None:
    ...


def test_read_csv_wrong_num_columns(all_parsers: Any) -> None:
    ...


def test_read_duplicate_index_explicit(all_parsers: Any) -> None:
    ...


def test_read_duplicate_index_implicit(all_parsers: Any) -> None:
    ...


def test_parse_bool(all_parsers: Any, data: Any, kwargs: Any, expected: Any) -> None:
    ...


def test_int_conversion(all_parsers: Any) -> None:
    ...


def test_read_nrows(all_parsers: Any, nrows: Any) -> None:
    ...


def test_read_nrows_bad(all_parsers: Any, nrows: Any) -> None:
    ...


def test_read_chunksize_with_index(all_parsers: Any, index_col: Any) -> None:
    ...


def test_read_chunksize_bad(all_parsers: Any, chunksize: Any) -> None:
    ...


def test_read_chunksize_and_nrows(all_parsers: Any, chunksize: Any) -> None:
    ...


def test_read_chunksize_and_nrows_changing_size(all_parsers: Any) -> None:
    ...


def test_get_chunk_passed_chunksize(all_parsers: Any) -> None:
    ...


def test_read_chunksize_compat(all_parsers: Any, kwargs: Any) -> None:
    ...


def test_read_chunksize_jagged_names(all_parsers: Any) -> None:
    ...


def test_read_data_list(all_parsers: Any) -> None:
    ...


def test_iterator(all_parsers: Any) -> None:
    ...


def test_iterator2(all_parsers: Any) -> None:
    ...


def test_reader_list(all_parsers: Any) -> None:
    ...


def test_reader_list_skiprows(all_parsers: Any) -> None:
    ...


def test_iterator_stop_on_chunksize(all_parsers: Any) -> None:
    ...


def test_iterator_skipfooter_errors(all_parsers: Any, kwargs: Any) -> None:
    ...


def test_nrows_skipfooter_errors(all_parsers: Any) -> None:
    ...


def test_pass_names_with_index(all_parsers: Any, data: Any, kwargs: Any, expected: Any) -> None:
    ...


def test_multi_index_no_level_names(all_parsers: Any, index_col: Any) -> None:
    ...


def test_multi_index_no_level_names_implicit(all_parsers: Any) -> None:
    ...


def test_multi_index_blank_df(all_parsers: Any, data: Any, expected: Any, header: Any, round_trip: Any) -> None:
    ...


def test_no_unnamed_index(all_parsers: Any) -> None:
    ...


def test_read_csv_parse_simple_list(all_parsers: Any) -> None:
    ...


def test_url(all_parsers: Any, csv_dir_path: Any) -> None:
    ...


def test_local_file(all_parsers: Any, csv_dir_path: Any) -> None:
    ...


def test_path_path_lib(all_parsers: Any) -> None:
    ...


def test_path_local_path(all_parsers: Any) -> None:
    ...


def test_nonexistent_path(all_parsers: Any) -> None:
    ...


def test_missing_trailing_delimiters(all_parsers: Any) -> None:
    ...


def test_skip_initial_space(all_parsers: Any) -> None:
    ...


def test_utf16_bom_skiprows(all_parsers: Any, sep: Any, encoding: Any) -> None:
    ...


def test_utf16_example(all_parsers: Any, csv_dir_path: Any) -> None:
    ...


def test_unicode_encoding(all_parsers: Any, csv_dir_path: Any) -> None:
    ...


def test_trailing_delimiters(all_parsers: Any) -> None:
    ...


def test_escapechar(all_parsers: Any) -> None:
    ...


def test_int64_min_issues(all_parsers: Any) -> None:
    ...


def test_parse_integers_above_fp_precision(all_parsers: Any) -> None:
    ...


def test_chunks_have_consistent_numerical_type(all_parsers: Any) -> None:
    ...


def test_warn_if_chunks_have_mismatched_type(all_parsers: Any) -> None:
    ...


def test_integer_overflow_bug(all_parsers: Any, sep: Any) -> None:
    ...


def test_catch_too_many_names(all_parsers: Any) -> None:
    ...


def test_ignore_leading_whitespace(all_parsers: Any) -> None:
    ...


def test_chunk_begins_with_newline_whitespace(all_parsers: Any) -> None:
    ...


def test_empty_with_index(all_parsers: Any) -> None:
    ...


def test_empty_with_multi_index(all_parsers: Any) -> None:
    ...


def test_empty_with_reversed_multi_index(all_parsers: Any) -> None:
    ...


def test_float_parser(all_parsers: Any) -> None:
    ...


def test_scientific_no_exponent(all_parsers: Any) -> None:
    ...


def test_int64_overflow(all_parsers: Any, conv: Any) -> None:
    ...


def test_int64_uint64_range(all_parsers: Any, val: Any) -> None:
    ...


def test_outside_int64_uint64_range(all_parsers: Any, val: Any) -> None:
    ...


def test_numeric_range_too_wide(all_parsers: Any, exp_data: Any) -> None:
    ...


def test_empty_with_nrows_chunksize(all_parsers: Any, iterator: Any) -> None:
    ...


def test_eof_states(all_parsers: Any, data: Any, kwargs: Any, expected: Any, msg: Any) -> None:
    ...


def test_uneven_lines_with_usecols(all_parsers: Any, usecols: Any) -> None:
    ...


def test_read_empty_with_usecols(all_parsers: Any, data: Any, kwargs: Any, expected: Any) -> None:
    ...


def test_trailing_spaces(all_parsers: Any, kwargs: Any, expected: Any) -> None:
    ...


def test_raise_on_sep_with_delim_whitespace(all_parsers: Any) -> None:
    ...


def test_single_char_leading_whitespace(all_parsers: Any, delim_whitespace: Any) -> None:
    ...


def test_empty_lines(all_parsers: Any, sep: Any, skip_blank_lines: Any, exp_data: Any) -> None:
    ...


def test_whitespace_lines(all_parsers: Any) -> None:
    ...


def test_whitespace_regex_separator(all_parsers: Any, data: Any, expected: Any) -> None:
    ...


def test_verbose_read(all_parsers: Any, capsys: Any) -> None:
    ...


def test_verbose_read2(all_parsers: Any, capsys: Any) -> None:
    ...


def test_iteration_open_handle(all_parsers: Any) -> None:
    ...


def test_1000_sep_with_decimal(all_parsers: Any, data: Any, thousands: Any, decimal: Any) -> None:
    ...


def test_euro_decimal_format(all_parsers: Any) -> None:
    ...


def test_inf_parsing(all_parsers: Any, na_filter: Any) -> None:
    ...


def test_raise_on_no_columns(all_parsers: Any, nrows: Any) -> None:
    ...


def test_memory_map(all_parsers: Any, csv_dir_path: Any) -> None:
    ...


def test_null_byte_char(all_parsers: Any) -> None:
    ...


def test_utf8_bom(all_parsers: Any, data: Any, kwargs: Any, expected: Any) -> None:
    ...


def test_temporary_file(all_parsers: Any) -> None:
    ...


def test_read_csv_utf_aliases(all_parsers: Any, byte: Any, fmt: Any) -> None:
    ...


def test_internal_eof_byte(all_parsers: Any) -> None:
    ...


def test_internal_eof_byte_to_file(all_parsers: Any) -> None:
    ...


def test_sub_character(all_parsers: Any, csv_dir_path: Any) -> None:
    ...


def test_file_handle_string_io(all_parsers: Any) -> None:
    ...


def test_file_handles_with_open(all_parsers: Any, csv1: Any) -> None:
    ...


def test_invalid_file_buffer_class(all_parsers: Any) -> None:
    ...


def test_invalid_file_buffer_mock(all_parsers: Any) -> None:
    ...


def test_valid_file_buffer_seems_invalid(all_parsers: Any) -> None:
    ...


def test_error_bad_lines(all_parsers: Any, kwargs: Any, warn_kwargs: Any) -> None:
    ...


def test_warn_bad_lines(all_parsers: Any, capsys: Any) -> None:
    ...


def test_suppress_error_output(all_parsers: Any, capsys: Any) -> None:
    ...


def test_filename_with_special_chars(all_parsers: Any, filename: Any) -> None:
    ...


def test_read_csv_memory_growth_chunksize(all_parsers: Any) -> None:
    ...


def test_read_table_equivalency_to_read_csv(all_parsers: Any) -> None:
    ...


def test_first_row_bom(all_parsers: Any) -> None:
    ...
