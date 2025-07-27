# pylint: skip-file
# type: ignore
#
#       tests.patterns.test_rest_patterns.py is part of the docformatter project
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
"""Module for testing the reST directive pattern detection functions."""

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
from docformatter.patterns import do_find_rest_directives, do_find_inline_rest_markup

with open("tests/_data/string_files/rest_patterns.toml", "rb") as f:
    TEST_STRINGS = tomllib.load(f)


@pytest.mark.unit
@pytest.mark.parametrize(
    "test_key",
    [
        "is_double_dot_directive",
        "is_double_dot_directive_indented",
    ],
)
def test_do_find_rest_directives(test_key):
    source = TEST_STRINGS[test_key]["instring"]
    expected = TEST_STRINGS[test_key]["expected"]

    result = do_find_rest_directives(source)
    assert (
        result[0][0] == expected[0]
    ), f"\nFailed {test_key}\nExpected {expected[0]}\nGot {result[0][0]}"
    assert (
        result[0][1] == expected[1]
    ), f"\nFailed {test_key}\nExpected {expected[0]}\nGot {result[0][1]}"


@pytest.mark.unit
@pytest.mark.parametrize(
    "test_key",
    [
        "is_inline_directive",
        "is_double_backtick_directive",
    ],
)
def test_do_find_inline_rest_markup(test_key):
    source = TEST_STRINGS[test_key]["instring"]
    expected = TEST_STRINGS[test_key]["expected"]

    result = do_find_inline_rest_markup(source)
    print(result)
    assert (
        result[0][0] == expected[0]
    ), f"\nFailed {test_key}\nExpected {expected[0]}\nGot {result[0][0]}"
    assert (
        result[0][1] == expected[1]
    ), f"\nFailed {test_key}\nExpected {expected[0]}\nGot {result[0][1]}"
