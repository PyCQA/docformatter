# pylint: skip-file
# type: ignore
#
#       tests.wrappers.test_url_wrapper.py is part of the docformatter project
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
"""Module for testing functions that wrap URL text."""

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
from docformatter.wrappers import do_wrap_urls

with open("tests/_data/string_files/url_wrappers.toml", "rb") as f:
    TEST_STRINGS = tomllib.load(f)


@pytest.mark.unit
@pytest.mark.parametrize(
    "test_key, url_idx, text_idx",
    [
        ("elaborate_inline_url", [(134, 226)], 0),
        ("short_inline_url", [(8, 42)], 0),
        ("long_inline_url", [(44, 168)], 0),
        ("simple_url", [(4, 100)], 0),
        ("short_url", [(8, 32)], 0),
        ("inline_url_retain_space", [(47, 171)], 0),
        ("keep_inline_url_together", [(20, 133)], 0),
        ("inline_url_two_paragraphs", [(26, 153)], 0),
        ("url_no_delete_words", [(36, 92)], 0),
        ("no_newline_after_url", [(113, 167), (229, 280)], 0),
        ("only_url_in_description", [(4, 99)], 0),
        ("no_indent_string_on_newline", [(43, 91)], 0),
        ("short_anonymous_url", [(137, 190)], 0),
        ("quoted_url", [(59, 80)], 0),
    ],
)
def test_do_wrap_urls(test_key, url_idx, text_idx):
    source = TEST_STRINGS[test_key]["instring"]
    expected = TEST_STRINGS[test_key]["expected"]

    # We convert the returned tuple to a list because we can't store a tuple in a
    # TOML file.
    result = list(do_wrap_urls(source, url_idx, text_idx, "    ", 72))
    assert result == expected, f"\nFailed {test_key}\nExpected {expected}\nGot {result}"
