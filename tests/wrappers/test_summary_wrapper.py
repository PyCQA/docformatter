# pylint: skip-file
# type: ignore
#
#       tests.wrappers.test_summary_wrapper.py is part of the docformatter project
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
"""Module for testing functions that wrap summary text."""

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
from docformatter.wrappers import do_unwrap_summary, do_wrap_summary

with open("tests/_data/string_files/summary_wrappers.toml", "rb") as f:
    TEST_STRINGS = tomllib.load(f)


@pytest.mark.unit
@pytest.mark.parametrize(
    "test_key",
    [
        "do_unwrap_summary",
        "do_unwrap_summary_empty",
        "do_unwrap_summary_only_newlines",
        "do_unwrap_summary_double_newlines",
        "do_unwrap_summary_leading_trailing",
    ],
)
def test_do_unwrap_summary(test_key):
    source = TEST_STRINGS[test_key]["instring"]
    expected = TEST_STRINGS[test_key]["expected"]

    result = do_unwrap_summary(source)

    assert (
        result == expected
    ), f"Failed {test_key}:\nExpected:\n{expected!r}\nGot:\n{result!r}"


@pytest.mark.integration
@pytest.mark.order(2)
@pytest.mark.parametrize(
    "test_key, initial_indent, subsequent_indent, wrap_length",
    [
        ("do_wrap_summary_no_wrap", "    ", "    ", 88),
        ("do_wrap_summary_disabled", "    ", "    ", 0),
        ("do_wrap_summary_with_wrap", "    ", "    ", 50),
        ("do_wrap_summary_empty", "", "", 50),
        ("do_wrap_summary_long_word", "", "", 50),
        ("do_wrap_summary_exact_length", "", "", 50),
        ("do_wrap_summary_tabs_spaces", "  ", "  ", 40),
        ("do_wrap_summary_wrap_length_1", ">", "-", 1),
    ],
)
def test_do_wrap_summary(
    test_key,
    initial_indent,
    subsequent_indent,
    wrap_length,
):
    source = TEST_STRINGS[test_key]["instring"]
    expected = TEST_STRINGS[test_key]["expected"]

    result = do_wrap_summary(
        source,
        initial_indent=initial_indent,
        subsequent_indent=subsequent_indent,
        wrap_length=wrap_length,
    )
    assert (
        result == expected
    ), f"Failed {test_key}:\nExpected:\n{expected!r}\nGot:\n{result!r}"
