# pylint: skip-file
# type: ignore
#
#       tests.patterns.test_misc_patterns.py is part of the docformatter project
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
"""Module for testing the miscellaneous pattern detection functions."""

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
    is_probably_beginning_of_sentence,
    is_some_sort_of_code,
)

with open("tests/_data/string_files/misc_patterns.toml", "rb") as f:
    TEST_STRINGS = tomllib.load(f)


@pytest.mark.unit
@pytest.mark.parametrize(
    "test_key, patternizer",
    [
        ("is_some_sort_of_code", is_some_sort_of_code),
        pytest.param(
            "is_some_sort_of_code_python",
            is_some_sort_of_code,
            marks=pytest.mark.skip(
                reason="The is_some_sort_of_code function is simply looking for long "
                "words.  This function needs to be re-written to look for actual code "
                "patterns."
            ),
        ),
        ("is_probably_beginning_of_sentence", is_probably_beginning_of_sentence),
        ("is_not_probably_beginning_of_sentence", is_probably_beginning_of_sentence),
        (
            "is_probably_beginning_of_sentence_pydoc_ref",
            is_probably_beginning_of_sentence,
        ),
    ],
)
def test_miscellaneous_patterns(test_key, patternizer):
    source = TEST_STRINGS[test_key]["instring"]
    expected = TEST_STRINGS[test_key]["expected"]

    result = patternizer(source)
    if result:
        assert (
            result == expected
        ), f"\nFailed {test_key}\nExpected {expected}\nGot {result}"
    else:
        result = "None" if result is None else result
        assert (
            result == expected
        ), f"\nFailed {test_key}\nExpected {expected}\nGot {result}"
