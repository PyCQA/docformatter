# pylint: skip-file
# type: ignore
#
#       tests.test_utility_functions.py is part of the docformatter project
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
"""Module for testing utility functions used when processing docstrings."""


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
from docformatter.util import find_py_files, has_correct_length, is_in_range

with open("tests/_data/string_files/utility_functions.toml", "rb") as f:
    TEST_STRINGS = tomllib.load(f)


@pytest.mark.unit
@pytest.mark.parametrize(
    "test_key",
    [
        "has_correct_length_none",
        "has_correct_length_start_in_range",
        "has_correct_length_end_in_range",
        "has_correct_length_both_in_range",
        "has_correct_length_start_out_of_range",
        "has_correct_length_end_out_of_range",
        "has_correct_length_both_out_of_range",
    ],
)
def test_has_correct_length(test_key):
    """Test has_correct_length() function."""
    length_range = TEST_STRINGS[test_key]["length_range"]
    start = TEST_STRINGS[test_key]["start"]
    end = TEST_STRINGS[test_key]["end"]
    expected = TEST_STRINGS[test_key]["expected"]

    if length_range == "None":
        length_range = None

    result = has_correct_length(length_range, start, end)
    assert result == expected, f"\nFailed {test_key}\nExpected {expected}\nGot {result}"


@pytest.mark.unit
@pytest.mark.parametrize(
    "test_key",
    [
        "is_in_range_none",
        "is_in_range_start_in_range",
        "is_in_range_end_in_range",
        "is_in_range_both_in_range",
        "is_in_range_out_of_range",
    ],
)
def test_is_in_range(test_key):
    """Test is_in_range() function."""
    line_range = TEST_STRINGS[test_key]["line_range"]
    start = TEST_STRINGS[test_key]["start"]
    end = TEST_STRINGS[test_key]["end"]
    expected = TEST_STRINGS[test_key]["expected"]

    if line_range == "None":
        line_range = None

    result = is_in_range(line_range, start, end)
    assert result == expected, f"\nFailed {test_key}\nExpected {expected}\nGot {result}"


@pytest.mark.unit
@pytest.mark.parametrize(
    "test_key, recursive",
    [
        ("find_py_file", False),
        ("find_py_file_recursive", True),
        ("skip_hidden_py_file", False),
        ("skip_hidden_py_file_recursive", True),
        ("ignore_non_py_file", False),
        ("ignore_non_py_file_recursive", True),
        ("exclude_py_file", False),
        ("exclude_py_file_recursive", True),
        ("exclude_multiple_files", False),
        ("exclude_multiple_files_recursive", True),
    ],
)
def test_find_py_files(test_key, recursive):
    """Test find_py_files() function."""
    sources = TEST_STRINGS[test_key]["sources"]
    exclude = TEST_STRINGS[test_key]["exclude"]
    expected = TEST_STRINGS[test_key]["expected"]

    result = list(find_py_files(sources, recursive, exclude))
    assert result == expected, f"\nFailed {test_key}\nExpected {expected}\nGot {result}"
