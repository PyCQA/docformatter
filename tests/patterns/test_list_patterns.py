# pylint: skip-file
# type: ignore
#
#       tests.patterns.test_list_patterns.py is part of the docformatter project
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
"""Module for testing the list pattern detection functions."""

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
from docformatter.patterns import is_type_of_list

with open("tests/_data/string_files/list_patterns.toml", "rb") as f:
    TEST_STRINGS = tomllib.load(f)


@pytest.mark.integration
@pytest.mark.order(3)
@pytest.mark.parametrize(
    "test_key",
    [
        "is_bullet_list",
        "is_enum_list",
        "is_option_list",
        "is_option_list_indented",
        "is_list_with_single_hyphen",
        "is_list_with_double_hyphen",
        "is_list_with_at_sign",
        "is_heuristic_list",
        "is_not_list_sphinx_style",
        "is_sphinx_list_numpy_style",
        "is_numpy_list_sphinx_style",
        "is_google_list_numpy_style",
        "is_type_of_list_strict_wrap",
        "is_type_of_list_non_strict_wrap",
        "is_literal_block",
        "is_reST_header",
        "is_type_of_list_alembic_header",
        "is_epytext_field_list",
        "is_sphinx_field_list",
    ],
)
def test_is_type_of_list(test_key):
    text = TEST_STRINGS[test_key]["instring"]
    strict = TEST_STRINGS[test_key]["strict"]
    style = TEST_STRINGS[test_key]["style"]
    expected = TEST_STRINGS[test_key]["expected"]

    result = is_type_of_list(text, strict, style)
    assert result == expected, f"\nFailed {test_key}\nExpected {expected}\nGot {result}"
