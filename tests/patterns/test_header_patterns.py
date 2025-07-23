# pylint: skip-file
# type: ignore
#
#       tests.patterns.test_header_patterns.py is part of the docformatter project
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
"""Module for testing the field list pattern detection functions."""

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
from docformatter.patterns import (
    is_alembic_header,
    is_numpy_section_header,
    is_rest_section_header,
)

with open("tests/_data/string_files/header_patterns.toml", "rb") as f:
    TEST_STRINGS = tomllib.load(f)


@pytest.mark.unit
@pytest.mark.parametrize(
    "test_key, patternizer",
    [
        ("is_alembic_header", is_alembic_header),
        ("is_not_alembic_header_epytext", is_alembic_header),
        ("is_not_alembic_header_numpy", is_alembic_header),
        ("is_not_alembic_header_google", is_alembic_header),
        ("is_numpy_section_header_parameters", is_numpy_section_header),
        ("is_numpy_section_header_returns", is_numpy_section_header),
        ("is_numpy_section_header_yields", is_numpy_section_header),
        ("is_numpy_section_header_raises", is_numpy_section_header),
        ("is_numpy_section_header_receives", is_numpy_section_header),
        ("is_numpy_section_header_other_parameters", is_numpy_section_header),
        ("is_numpy_section_header_warns", is_numpy_section_header),
        ("is_numpy_section_header_warnings", is_numpy_section_header),
        ("is_numpy_section_header_see_also", is_numpy_section_header),
        ("is_numpy_section_header_examples", is_numpy_section_header),
        ("is_numpy_section_header_notes", is_numpy_section_header),
        ("is_not_numpy_section_header", is_numpy_section_header),
        ("is_not_numpy_section_header_wrong_dashes", is_numpy_section_header),
        ("is_rest_section_header_pound", is_rest_section_header),
        ("is_rest_section_header_star", is_rest_section_header),
        ("is_rest_section_header_equal", is_rest_section_header),
        ("is_rest_section_header_dash", is_rest_section_header),
        ("is_rest_section_header_circumflex", is_rest_section_header),
        ("is_rest_section_header_single_quote", is_rest_section_header),
        ("is_rest_section_header_double_quote", is_rest_section_header),
        ("is_rest_section_header_plus", is_rest_section_header),
        ("is_rest_section_header_underscore", is_rest_section_header),
        ("is_rest_section_header_tilde", is_rest_section_header),
        ("is_rest_section_header_backtick", is_rest_section_header),
        ("is_rest_section_header_period", is_rest_section_header),
        ("is_rest_section_header_colon", is_rest_section_header),
        ("is_not_rest_section_header_unknown_adornments", is_rest_section_header),
    ],
)
def test_is_header(test_key, patternizer):
    source = TEST_STRINGS[test_key]["instring"]
    expected = TEST_STRINGS[test_key]["expected"]

    result = patternizer(source)
    if result:
        assert (
            result.group(0) == expected
        ), f"\nFailed {test_key}\nExpected {expected}\nGot {result.group(0)}"
    else:
        result = "None" if result is None else result
        assert (
            result == expected
        ), f"\nFailed {test_key}\nExpected {expected}\nGot {result}"
