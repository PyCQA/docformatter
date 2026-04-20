# pylint: skip-file
# type: ignore
#
#       tests.formatter.test_format_functions.py is part of the docformatter project
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
"""Module for testing formatting functions."""

# Standard Library Imports
import contextlib
import sys
import tokenize
from io import BytesIO, StringIO

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
from docformatter import format as _format

with open("tests/_data/string_files/format_functions.toml", "rb") as f:
    TEST_STRINGS = tomllib.load(f)


def _get_tokens(source):
    return list(tokenize.tokenize(BytesIO(source.encode()).readline))


def _get_docstring_token_and_index(tokens):
    for i, tok in enumerate(tokens):
        if tok.type == tokenize.STRING:
            return i
    raise ValueError("No docstring found in token stream.")


@pytest.mark.unit
@pytest.mark.parametrize(
    "test_key",
    [
        "module_docstring_followed_by_string",
        "module_docstring_followed_by_code",
        "module_docstring_followed_by_comment_then_code",
        "module_docstring_followed_by_comment_then_string",
        "module_docstring_in_black",
    ],
)
def test_module_docstring_newlines(test_key):
    expected = TEST_STRINGS[test_key]["expected"]

    result = _format._get_module_docstring_newlines()
    assert (
        result == expected
    ), f"\nFailed {test_key}:\nExpected {expected}\nGot {result}"


@pytest.mark.unit
@pytest.mark.order(4)
@pytest.mark.parametrize(
    "test_key, classifier",
    [
        (
            "class_docstring_followed_by_statement",
            _format._get_class_docstring_newlines,
        ),
        ("class_docstring_followed_by_def", _format._get_class_docstring_newlines),
        ("class_docstring_with_decorator", _format._get_class_docstring_newlines),
        ("class_docstring_with_class_variable", _format._get_class_docstring_newlines),
        ("function_with_expr", _format._get_function_docstring_newlines),
        ("function_with_inner_def", _format._get_function_docstring_newlines),
        ("function_with_inner_async_def", _format._get_function_docstring_newlines),
        ("function_with_decorator_and_def", _format._get_function_docstring_newlines),
        (
            "function_with_decorator_and_async_def",
            _format._get_function_docstring_newlines,
        ),
        (
            "function_docstring_with_inner_class",
            _format._get_function_docstring_newlines,
        ),
        ("attribute_docstring_single_line", _format._get_attribute_docstring_newlines),
        ("attribute_docstring_multi_line", _format._get_attribute_docstring_newlines),
        (
            "attribute_docstring_outside_class",
            _format._get_attribute_docstring_newlines,
        ),
        (
            "attribute_docstring_inside_method",
            _format._get_attribute_docstring_newlines,
        ),
        ("attribute_docstring_with_comment", _format._get_attribute_docstring_newlines),
        (
            "attribute_docstring_multiple_assignments",
            _format._get_attribute_docstring_newlines,
        ),
        ("attribute_docstring_equiv_expr", _format._get_attribute_docstring_newlines),
    ],
)
def test_get_docstring_newlines(test_key, classifier):
    source = TEST_STRINGS[test_key]["source"]
    expected = TEST_STRINGS[test_key]["expected"]

    tokens = _get_tokens(source)
    index = _get_docstring_token_and_index(tokens)

    result = classifier(tokens, index)
    assert (
        result == expected
    ), f"\nFailed {test_key}:\nExpected {expected}\nGot {result}"


@pytest.mark.unit
@pytest.mark.parametrize(
    "test_key",
    [
        "get_num_rows_columns",
    ],
)
def test_get_num_rows_columns(test_key):
    token = tokenize.TokenInfo(
        type=TEST_STRINGS[test_key]["token"][0],
        string=TEST_STRINGS[test_key]["token"][1],
        start=TEST_STRINGS[test_key]["token"][2],
        end=TEST_STRINGS[test_key]["token"][3],
        line=TEST_STRINGS[test_key]["token"][4],
    )
    expected = TEST_STRINGS[test_key]["expected"]

    result = _format._get_num_rows_columns(token)
    assert (
        result[0] == expected[0]
    ), f"\nFailed {test_key}\nExpected {expected[0]} rows\nGot {result[0]} rows"
    assert (
        result[1] == expected[1]
    ), f"\nFailed {test_key}\nExpected {expected[1]} columns\nGot {result[1]} columns"


@pytest.mark.unit
@pytest.mark.parametrize(
    "test_key",
    [
        "get_start_end_indices",
    ],
)
def test_get_start_end_indices(test_key):
    prev_token = tokenize.TokenInfo(
        type=TEST_STRINGS[test_key]["prev_token"][0],
        string=TEST_STRINGS[test_key]["prev_token"][1],
        start=TEST_STRINGS[test_key]["prev_token"][2],
        end=TEST_STRINGS[test_key]["prev_token"][3],
        line=TEST_STRINGS[test_key]["prev_token"][4],
    )
    token = tokenize.TokenInfo(
        type=TEST_STRINGS[test_key]["token"][0],
        string=TEST_STRINGS[test_key]["token"][1],
        start=TEST_STRINGS[test_key]["token"][2],
        end=TEST_STRINGS[test_key]["token"][3],
        line=TEST_STRINGS[test_key]["token"][4],
    )
    expected = TEST_STRINGS[test_key]["expected"]

    result = _format._get_start_end_indices(token, prev_token, 3, 17)
    for i in 0, 1:
        for j in 0, 1:
            assert (
                result[i][j] == expected[i][j]
            ), f"\nFailed {test_key}\nExpected {expected[i][j]}\nGot {result[i][j]}"


@pytest.mark.unit
@pytest.mark.parametrize(
    "test_key, block",
    [
        ("do_remove_preceding_blank_lines_module", [(0, 4, "module")]),
        ("do_remove_preceding_blank_lines_class", [(0, 7, "class")]),
        ("do_remove_preceding_blank_lines_function", [(0, 9, "function")]),
        ("do_remove_preceding_blank_lines_attribute", [(1, 6, "attribute")]),
    ],
)
def test_do_remove_preceding_blank_lines(test_key, block):
    source = TEST_STRINGS[test_key]["source"]
    expected = TEST_STRINGS[test_key]["expected"]

    tokens = list(tokenize.generate_tokens(StringIO(source, newline="").readline))

    result = _format._do_remove_preceding_blank_lines(tokens, block)
    for _idx in range(len(result)):
        assert (
            result[_idx].string == expected[_idx]
        ), f"\nFailed {test_key}\nExpected {expected[_idx]}\nGot {result[_idx].string}"


@pytest.mark.integration
@pytest.mark.order(5)
@pytest.mark.parametrize(
    "test_key",
    [
        "get_newlines_by_type_module_docstring",
        "get_newlines_by_type_module_docstring_black",
        "get_newlines_by_type_class_docstring",
        "get_newlines_by_type_function_docstring",
        "get_newlines_by_type_attribute_docstring",
    ],
)
def test_get_newlines_by_type(test_key):
    source = TEST_STRINGS[test_key]["source"]
    expected = TEST_STRINGS[test_key]["expected"]

    tokens = _get_tokens(source)
    index = _get_docstring_token_and_index(tokens)

    result = _format._get_newlines_by_type(tokens, index)
    assert result == expected, f"\nFailed {test_key}\nExpected {expected}\nGot {result}"


@pytest.mark.integration
@pytest.mark.order(4)
@pytest.mark.parametrize(
    "test_key",
    [
        "get_unmatched_start_end_indices",
    ],
)
def test_get_unmatched_start_end_indices(test_key):
    prev_token = tokenize.TokenInfo(
        type=TEST_STRINGS[test_key]["prev_token"][0],
        string=TEST_STRINGS[test_key]["prev_token"][1],
        start=TEST_STRINGS[test_key]["prev_token"][2],
        end=TEST_STRINGS[test_key]["prev_token"][3],
        line=TEST_STRINGS[test_key]["prev_token"][4],
    )
    token = tokenize.TokenInfo(
        type=TEST_STRINGS[test_key]["token"][0],
        string=TEST_STRINGS[test_key]["token"][1],
        start=TEST_STRINGS[test_key]["token"][2],
        end=TEST_STRINGS[test_key]["token"][3],
        line=TEST_STRINGS[test_key]["token"][4],
    )
    expected = TEST_STRINGS[test_key]["expected"]

    result = _format._get_unmatched_start_end_indices(token, prev_token, 4)
    for i in 0, 1:
        for j in 0, 1:
            assert (
                result[i][j] == expected[i][j]
            ), f"\nFailed {test_key}\nExpected {expected[i][j]}\nGot {result[i][j]}"


@pytest.mark.integration
@pytest.mark.order(5)
@pytest.mark.parametrize(
    "test_key",
    [
        "do_update_token_indices",
    ],
)
def test_do_update_token_indices(test_key):
    tokens = []
    for token in TEST_STRINGS[test_key]["tokens"]:
        tokens.append(
            tokenize.TokenInfo(
                type=token[0],
                string=token[1],
                start=token[2],
                end=token[3],
                line=token[4],
            )
        )
    expected = TEST_STRINGS[test_key]["expected"]

    result = _format._do_update_token_indices(tokens)
    for idx, _expected in enumerate(expected):
        # We convert the start and end tuples to lists because we can't store tuples
        # in a TOML file.
        assert list(result[idx].start) == _expected[0], (
            f"\nFailed {test_key} start index\n"
            f"Expected {expected[0]}\nGot {result[idx].start}"
        )
        assert list(result[idx].end) == _expected[1], (
            f"\nFailed {test_key} end index\n"
            f"Expected {expected[1]}\nGot {result[idx].end}"
        )
