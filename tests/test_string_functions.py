# pylint: skip-file
# type: ignore
#
#       tests.test_string_functions.py is part of the docformatter project
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
"""Module for testing functions that manipulate text."""

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
from docformatter.strings import (
    description_to_list,
    do_clean_excess_whitespace,
    do_find_shortest_indentation,
    do_normalize_line,
    do_normalize_line_endings,
    do_normalize_summary,
    do_reindent,
    do_split_description,
    do_split_first_sentence,
    do_split_summary,
    do_split_summary_and_description,
    do_strip_docstring,
    do_strip_leading_blank_lines,
)

with open("tests/_data/string_files/string_functions.toml", "rb") as f:
    TEST_STRINGS = tomllib.load(f)


@pytest.mark.unit
@pytest.mark.parametrize(
    "test_key, indentation",
    [
        ("do_reindent", "    "),
        ("do_reindent_should_expand_tabs_to_indentation", "    "),
        ("do_reindent_with_no_indentation_expand_tabs", ""),
        ("do_reindent_should_maintain_indentation", "    "),
        ("do_reindent_tab_indentation", "\t"),
    ],
)
def test_do_reindent(test_key, indentation):
    """Test the do_reindent function."""
    source = TEST_STRINGS[test_key]["instring"]
    expected = TEST_STRINGS[test_key]["expected"]

    result = do_reindent(source, indentation)

    assert result == expected, (
        f"\nFailed {test_key}:\nExpected {expected}" f"\nGot {result}"
    )


@pytest.mark.unit
def test_do_find_shortest_indentation():
    """Test the do_find_shorted_indentation function."""
    assert " " == do_find_shortest_indentation(
        ["    ", " b", "  a"],
    )


@pytest.mark.unit
@pytest.mark.parametrize(
    "test_key",
    [
        "do_normalize_summary",
        "do_normalize_summary_multiline",
        "do_normalize_summary_question_mark",
        "do_normalize_summary_exclamation_point",
        "do_normalize_summary_with_title",
        "do_normalize_summary_capitalize_first_letter",
        "do_normalize_summary_with_proprer_noun",
        "do_normalize_summary_capitalize_first_letter_with_period",
        "do_normalize_summary_dont_capitalize_first_letter_if_variable",
    ],
)
def test_do_normalize_summary(test_key):
    """Test the do_normalize_summary function."""
    source = TEST_STRINGS[test_key]["instring"]
    expected = TEST_STRINGS[test_key]["expected"]

    result = do_normalize_summary(source)

    assert result == expected, (
        f"\nFailed {test_key}:\nExpected {expected}" f"\nGot {result}"
    )


@pytest.mark.unit
@pytest.mark.parametrize("test_key", ["do_normalize_line"])
def test_do_normalize_line(test_key):
    """Test the do_normalize_line function."""
    source = TEST_STRINGS[test_key]["instring"]
    expected = TEST_STRINGS[test_key]["expected"]

    result = do_normalize_line(source, "\n")

    assert result == expected, (
        f"\nFailed {test_key}:\nExpected {expected}" f"\nGot {result}"
    )


@pytest.mark.unit
@pytest.mark.parametrize(
    "test_key, indentation, wrap_length", [("description_to_list", "    ", 72)]
)
def test_description_to_list(test_key, indentation, wrap_length):
    """Test the description_to_list function."""
    source = TEST_STRINGS[test_key]["instring"]
    expected = TEST_STRINGS[test_key]["expected"]

    result = description_to_list(source, indentation, wrap_length)

    assert result == expected, (
        f"\nFailed {test_key}:\nExpected {expected}" f"\nGot {result}"
    )


@pytest.mark.unit
@pytest.mark.parametrize(
    "test_key",
    [
        "do_split_first_sentence",
        "do_split_first_sentence_2",
        "do_split_first_sentence_3",
    ],
)
def test_do_split_first_sentence(test_key):
    """Test the do_split_first_sentence function."""
    source = TEST_STRINGS[test_key]["instring"]
    expected = TEST_STRINGS[test_key]["expected"]

    # We convert the tuple return to a list since we can't store a tuple in a TOML file.
    result = list(do_split_first_sentence(source))

    assert result == expected, (
        f"\nFailed {test_key}:\nExpected {expected}" f"\nGot {result}"
    )


@pytest.mark.unit
@pytest.mark.parametrize(
    "test_key",
    [
        "do_split_summary",
        "do_split_summary_2",
        "do_split_multi_sentence_summary",
        "do_split_multi_sentence_summary_2",
    ],
)
def test_do_split_summary(test_key):
    """Test the do_split_summary function."""
    source = TEST_STRINGS[test_key]["instring"]
    expected = TEST_STRINGS[test_key]["expected"]

    # We convert the tuple returned to a list since we can't store a tuple in a TOML
    # file.
    result = do_split_summary(source)

    assert result == expected, (
        f"\nFailed {test_key}:\nExpected {expected}" f"\nGot {result}"
    )


@pytest.mark.unit
@pytest.mark.parametrize(
    "test_key",
    [
        "do_strip_docstring",
        "do_strip_docstring_triple_single_quotes",
        "do_strip_docstring_empty_string",
        "do_strip_docstring_raw_string",
        "do_strip_docstring_raw_string_2",
        "do_strip_docstring_unicode_string",
        "do_strip_docstring_unicode_string_2",
        "do_strip_docstring_with_unknown",
        "do_strip_docstring_with_single_quotes",
        "do_strip_docstring_with_double_quotes",
    ],
)
def test_do_strip_docstring(test_key):
    """Test the do_strip_docstring function."""
    source = TEST_STRINGS[test_key]["instring"]
    expected = TEST_STRINGS[test_key]["expected"]
    raises = TEST_STRINGS[test_key].get("raises")

    if raises:
        with pytest.raises(eval(raises)):
            do_strip_docstring(source)
    else:
        # We convert the tuple returned to a list since we can't store a tuple in a TOML
        # file.
        result = list(do_strip_docstring(source))

        assert result == expected, (
            f"\nFailed {test_key}:\nExpected {expected}" f"\nGot {result}"
        )


@pytest.mark.unit
@pytest.mark.parametrize(
    "test_key",
    [
        "do_strip_leading_blank_lines",
    ],
)
def test_do_strip_leading_blank_lines(test_key):
    """Test the do_strup_leading_blank_lines function."""
    source = TEST_STRINGS[test_key]["instring"]
    expected = TEST_STRINGS[test_key]["expected"]

    result = do_strip_leading_blank_lines(source)

    assert result == expected, (
        f"\nFailed {test_key}:\nExpected {expected}" f"\nGot {result}"
    )


@pytest.mark.unit
@pytest.mark.parametrize(
    "test_key, indentation",
    [
        ("do_clean_excess_whitespace", "    "),
    ],
)
def test_do_clean_excess_whitespace(test_key, indentation):
    """Test the do_clean_excess_whitespace function."""
    source = TEST_STRINGS[test_key]["instring"]
    expected = TEST_STRINGS[test_key]["expected"]

    result = do_clean_excess_whitespace(source, indentation)

    assert result == expected, (
        f"\nFailed {test_key}:\nExpected {expected}" f"\nGot {result}"
    )


@pytest.mark.integration
@pytest.mark.order(5)
@pytest.mark.parametrize("test_key", ["do_normalize_line_endings"])
def test_do_normalize_line_endings(test_key):
    """Test the do_normalize_line_endings function."""
    source = TEST_STRINGS[test_key]["instring"]
    expected = TEST_STRINGS[test_key]["expected"]

    result = do_normalize_line_endings(source, "\n")

    assert result == expected, (
        f"\nFailed {test_key}:\nExpected {expected}" f"\nGot {result}"
    )


@pytest.mark.integration
@pytest.mark.order(1)
@pytest.mark.parametrize(
    "test_key, indentation, wrap_length, style",
    [
        ("do_split_description_url_outside_param", "    ", 72, "sphinx"),
        ("do_split_description_single_url_in_param", "    ", 72, "sphinx"),
        ("do_split_description_single_url_in_multiple_params", "    ", 72, "sphinx"),
        ("do_split_description_multiple_urls_in_param", "    ", 72, "sphinx"),
    ],
)
def test_do_split_description(test_key, indentation, wrap_length, style):
    """Test the do_split_description function."""
    source = TEST_STRINGS[test_key]["instring"]
    expected = TEST_STRINGS[test_key]["expected"]

    result = do_split_description(source, indentation, wrap_length, style)

    assert result == expected, (
        f"\nFailed {test_key}:\nExpected {expected}" f"\nGot {result}"
    )


@pytest.mark.integration
@pytest.mark.order(3)
@pytest.mark.parametrize(
    "test_key",
    [
        "do_split_summary_and_description",
        "do_split_summary_and_description_complex",
        "do_split_summary_and_description_more_complex",
        "do_split_summary_and_description_with_list",
        "do_split_summary_and_description_with_list_of_parameters",
        "do_split_summary_and_description_with_capital",
        "do_split_summary_and_description_with_list_on_other_line",
        "do_split_summary_and_description_with_other_symbol",
        "do_split_summary_and_description_with_colon",
        "do_split_summary_and_description_with_exclamation",
        "do_split_summary_and_description_with_question_mark",
        "do_split_summary_and_description_with_double_quote",
        "do_split_summary_and_description_with_single_quote",
        "do_split_summary_and_description_with_double_backtick",
        "do_split_summary_and_description_with_punctuation",
        "do_split_summary_and_description_without_punctuation",
        "do_split_summary_and_description_with_abbreviation",
        "do_split_summary_and_description_with_url",
    ],
)
def test_do_split_summary_and_description(test_key):
    """Test the do_split_summary_and_description function."""
    source = TEST_STRINGS[test_key]["instring"]
    expected = TEST_STRINGS[test_key]["expected"]

    # We convert the tuple returned to a list since we can't store a tuple in a TOML
    # file.
    result = list(do_split_summary_and_description(source))

    assert result == expected, (
        f"\nFailed {test_key}:\nExpected {expected}" f"\nGot {result}"
    )
