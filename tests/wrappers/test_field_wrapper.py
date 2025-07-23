# pylint: skip-file
# type: ignore
#
#       tests.wrappers.test_field_wrapper.py is part of the docformatter project
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
"""Module for testing the description wrapper functions."""

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
from docformatter.wrappers import fields

with open("tests/_data/string_files/field_wrappers.toml", "rb") as f:
    TEST_STRINGS = tomllib.load(f)


@pytest.mark.unit
@pytest.mark.parametrize(
    "test_key, field_idx, idx",
    [
        (
            "do_join_field_body",
            [(146, 161), (185, 208), (319, 342), (372, 395), (425, 433), (598, 605)],
            0,
        ),
        (
            "do_join_field_body_2",
            [(146, 161), (185, 208), (319, 342), (372, 395), (425, 433), (598, 605)],
            1,
        ),
        (
            "do_join_field_body_3",
            [(146, 161), (185, 208), (319, 342), (372, 395), (425, 433), (598, 605)],
            2,
        ),
    ],
)
def test_do_join_field_body(test_key, field_idx, idx):
    source = TEST_STRINGS[test_key]["instring"]
    expected = TEST_STRINGS[test_key]["expected"]

    result = fields._do_join_field_body(source, field_idx, idx)
    assert result == expected, f"\nFailed {test_key}\nExpected {expected}\nGot {result}"


@pytest.mark.unit
@pytest.mark.parametrize(
    "test_key",
    [
        "do_wrap_field",
        "do_wrap_long_field",
    ],
)
def test_do_wrap_field(test_key):
    source = TEST_STRINGS[test_key]["instring"]
    expected = TEST_STRINGS[test_key]["expected"]

    result = fields._do_wrap_field(source[0], source[1], "    ", 72)
    assert result == expected, f"\nFailed {test_key}\nExpected {expected}\nGot {result}"


@pytest.mark.integration
@pytest.mark.order(0)
@pytest.mark.parametrize(
    "test_key, field_idx, text_idx",
    [
        (
            "do_wrap_field_list",
            [(146, 162), (186, 209), (320, 343), (373, 396), (426, 434), (599, 606)],
            140,
        ),
    ],
)
def test_do_wrap_field_lists(test_key, field_idx, text_idx):
    source = TEST_STRINGS[test_key]["instring"]
    lines = TEST_STRINGS[test_key]["lines"]
    expected = TEST_STRINGS[test_key]["expected"]

    # We convert the returned tuple to a list because we can't store tuple in a TOML
    # file.
    result = list(
        fields.do_wrap_field_lists(source, field_idx, lines, text_idx, "    ", 72)
    )
    assert result == expected, f"\nFailed {test_key}\nExpected {expected}\nGot {result}"
