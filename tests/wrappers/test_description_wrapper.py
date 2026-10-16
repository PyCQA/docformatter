# pylint: skip-file
# type: ignore
#
#       tests.wrappers.test_description_wrapper.py is part of the docformatter project
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
from docformatter.wrappers import do_close_description, do_wrap_description

with open("tests/_data/string_files/description_wrappers.toml", "rb") as f:
    TEST_STRINGS = tomllib.load(f)


@pytest.mark.unit
@pytest.mark.parametrize(
    "test_key, text_index",
    [
        ("do_close_description", 24),
    ],
)
def test_do_close_description(test_key, text_index):
    source = TEST_STRINGS[test_key]["instring"]
    expected = TEST_STRINGS[test_key]["expected"]

    result = do_close_description(source, text_index, "    ")
    assert result == expected, f"\nFailed {test_key}\nExpected {expected}\nGot {result}"


@pytest.mark.integration
@pytest.mark.order(2)
@pytest.mark.parametrize(
    "test_key, force_wrap",
    [
        ("do_wrap_description", False),
        ("do_wrap_description_with_doctest", False),
        ("do_wrap_description_with_list", False),
        ("do_wrap_description_with_heuristic_list", False),
        ("do_wrap_description_with_heuristic_list_force_wrap", True),
        ("do_wrap_description_with_directive", False),
    ],
)
def test_do_wrap_description(test_key, force_wrap):
    source = TEST_STRINGS[test_key]["instring"]
    expected = TEST_STRINGS[test_key]["expected"]

    result = do_wrap_description(source, "    ", 72, force_wrap, False, "", "sphinx")
    assert result == expected, f"\nFailed {test_key}\nExpected {expected}\nGot {result}"


@pytest.mark.integration
@pytest.mark.parametrize("marker", [r"\b", "\b"])
@pytest.mark.parametrize("indentation", ["", "    "])
def test_click_paragraph_keeps_lines_and_url(marker, indentation):
    """Keep explicit Click no-wrap paragraphs while wrapping ordinary prose."""
    paragraph = (
        marker + "\nThis is\na paragraph\nwithout rewrapping.\n"
        "https://example.com/a/very/long/link/that/must/not/be/wrapped"
    )
    prose = "This ordinary paragraph is long enough to need wrapping."
    source = f"{prose}\n\n{paragraph}\n\n{prose}"

    result = do_wrap_description(source, indentation, 35, False, False, "", "sphinx")

    before, protected, after = result.split("\n\n")
    assert protected == "\n".join(indentation + line for line in paragraph.splitlines())
    assert "\n" in before and before == after
    assert (
        do_wrap_description(result, indentation, 35, False, False, "", "sphinx")
        == result
    )


@pytest.mark.integration
def test_click_marker_only_applies_at_start_of_a_paragraph():
    """Inline or escaped markers do not protect an ordinary paragraph."""
    for paragraph in [r"Ordinary \b text", r"\\b" + "\nOrdinary text"]:
        result = do_wrap_description(paragraph, "", 72, False, False, "", "sphinx")
        assert "\n" not in result


@pytest.mark.integration
def test_force_wrap_overrides_click_marker():
    """Explicit force wrapping keeps treating descriptions as ordinary prose."""
    result = do_wrap_description(
        "\\b\nThis is\na paragraph.", "", 72, True, False, "", "sphinx"
    )
    assert result == r"\b This is a paragraph."


@pytest.mark.integration
@pytest.mark.parametrize(
    "source",
    [
        "\\b\nFirst line\nsecond line.",
        "\\b\nFirst line.\n\n\\b\nSecond\nparagraph.",
    ],
)
def test_click_paragraphs_without_surrounding_prose(source):
    """Keep literal paragraphs at either edge and in successive paragraphs."""
    assert do_wrap_description(source, "", 20, False, False, "", "sphinx") == source
