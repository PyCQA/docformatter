# pylint: skip-file
# type: ignore
#
#       tests.formatter.test_do_format_code.py is part of the docformatter project
#
# Copyright (C) 2012-2023 Steven Myint
# Copyright (C) 2023-2025 Doyle "weibullguy" Rowland
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""Module for testing the Formattor _do_format_code method."""

# Standard Library Imports
import contextlib
import sys

with contextlib.suppress(ImportError):
    if sys.version_info >= (3, 11):
        # Standard Library Imports
        import tomllib
    else:
        # Third Party Imports
        import tomli as tomllib

# Third Party Imports
import pytest

# docformatter Package Imports
from docformatter import Formatter

NO_ARGS = [""]

with open("tests/_data/string_files/do_format_code.toml", "rb") as f:
    TEST_STRINGS = tomllib.load(f)


@pytest.mark.integration
@pytest.mark.order(7)
@pytest.mark.parametrize(
    "test_key, args",
    [
        ("one_line", NO_ARGS),
        ("module_docstring", NO_ARGS),
        ("newline_module_variable", NO_ARGS),
        ("class_docstring", NO_ARGS),
        ("newline_class_variable", NO_ARGS),
        ("newline_outside_docstring", NO_ARGS),
        pytest.param(
            "preserve_line_ending",
            NO_ARGS,
            marks=pytest.mark.skipif(
                sys.platform != "win32", reason="Not running on Windows"
            ),
        ),
        ("non_docstring", NO_ARGS),
        ("tabbed_indentation", NO_ARGS),
        ("mixed_indentation", NO_ARGS),
        ("escaped_newlines", NO_ARGS),
        ("code_comments", NO_ARGS),
        ("inline_comment", NO_ARGS),
        ("raw_lowercase", NO_ARGS),
        ("raw_uppercase", NO_ARGS),
        ("raw_lowercase_single", NO_ARGS),
        ("raw_uppercase_single", NO_ARGS),
        ("unicode_lowercase", NO_ARGS),
        ("unicode_uppercase", NO_ARGS),
        ("unicode_lowercase_single", NO_ARGS),
        ("unicode_uppercase_single", NO_ARGS),
        ("nested_triple", NO_ARGS),
        ("multiple_sentences", NO_ARGS),
        ("multiple_sentences_same_line", NO_ARGS),
        ("multiline_summary", NO_ARGS),
        ("empty_lines", NO_ARGS),
        ("class_empty_lines", NO_ARGS),
        ("class_empty_lines_2", NO_ARGS),
        ("method_empty_lines", NO_ARGS),
        ("trailing_whitespace", NO_ARGS),
        ("parameter_list", NO_ARGS),
        ("single_quote", NO_ARGS),
        ("double_quote", NO_ARGS),
        ("nested_triple_quote", NO_ARGS),
        ("first_line_assignment", NO_ARGS),
        ("regular_strings", NO_ARGS),
        ("syntax_error", NO_ARGS),
        ("slash_r", NO_ARGS),
        ("slash_r_slash_n", NO_ARGS),
        ("strip_blank_lines", ["--black", ""]),
        ("range_miss", ["--range", "1", "1", ""]),
        ("range_hit", ["--range", "1", "2", ""]),
        ("length_ignore", ["--docstring-length", "1", "1", ""]),
        ("class_attribute_wrap", NO_ARGS),
        ("issue_51", NO_ARGS),
        ("issue_51_2", NO_ARGS),
        (
            "issue_79",
            NO_ARGS
            + [
                "--wrap-summaries",
                "100",
                "--wrap-descriptions",
                "100",
            ],
        ),
        ("issue_97", NO_ARGS),
        ("issue_97_2", NO_ARGS),
        ("issue_130", NO_ARGS),
        ("issue_139", NO_ARGS),
        ("issue_139_2", NO_ARGS),
        ("issue_156", NO_ARGS),
        ("issue_156_2", NO_ARGS),
        ("issue_156_173", NO_ARGS),
        ("issue_157_7", ["--wrap-descriptions", "88", ""]),
        ("issue_157_8", ["--wrap-descriptions", "88", ""]),
        ("issue_157_9", ["--wrap-descriptions", "88", ""]),
        ("issue_157_10", ["--wrap-descriptions", "88", ""]),
        ("issue_176", NO_ARGS),
        ("issue_176_black", NO_ARGS),
        ("issue_187", NO_ARGS),
        ("issue_203", NO_ARGS),
        ("issue_243", NO_ARGS),
    ],
)
def test_do_format_code(test_key, test_args, args):
    uut = Formatter(
        test_args,
        sys.stderr,
        sys.stdin,
        sys.stdout,
    )

    source = TEST_STRINGS[test_key]["source"]
    expected = TEST_STRINGS[test_key]["expected"]

    result = uut._do_format_code(source)
    assert result == expected, f"\nFailed {test_key}\nExpected {expected}\nGot {result}"
