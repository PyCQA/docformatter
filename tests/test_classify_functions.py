# pylint: skip-file
# type: ignore
#
#       tests.test_classify_functions.py is part of the docformatter project
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
"""Module for testing the classification functions."""

# Standard Library Imports
import contextlib
import sys
import tokenize
from io import BytesIO

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
from docformatter.classify import (
    do_find_docstring_blocks,
    is_attribute_docstring,
    is_class_docstring,
    is_closing_quotes,
    is_code_line,
    is_definition_line,
    is_f_string,
    is_function_or_method_docstring,
    is_inline_comment,
    is_line_following_indent,
    is_module_docstring,
    is_nested_definition_line,
    is_newline_continuation,
    is_string_variable,
)

with open("tests/_data/string_files/classify_functions.toml", "rb") as f:
    TEST_STRINGS = tomllib.load(f)


def get_tokens(source: str) -> list[tokenize.TokenInfo]:
    return list(tokenize.tokenize(BytesIO(source.encode()).readline))


def get_string_index(tokens: list[tokenize.TokenInfo]) -> int:
    for i, tok in enumerate(tokens):
        if tok.type == tokenize.STRING:
            return i
    raise ValueError("No string token found.")


def build_token(prefix: str, test_key: str) -> tokenize.TokenInfo:
    """Build a tokenize.TokenInfo from test data using a prefix ('' or 'prev_')."""
    data = TEST_STRINGS[test_key]
    return tokenize.TokenInfo(
        type=data[f"{prefix}type"],
        string=data[f"{prefix}string"],
        start=tuple(data[f"{prefix}start"]),
        end=tuple(data[f"{prefix}end"]),
        line=data[f"{prefix}line"],
    )


@pytest.mark.unit
@pytest.mark.parametrize(
    "test_key, classifier",
    [
        ("is_module_docstring", is_module_docstring),
        ("is_class_docstring", is_class_docstring),
        ("is_method_docstring", is_function_or_method_docstring),
        ("is_function_docstring", is_function_or_method_docstring),
        ("is_attribute_docstring", is_attribute_docstring),
        ("is_not_attribute_docstring", is_attribute_docstring),
    ],
)
def test_docstring_classifiers(test_key, classifier):
    source = TEST_STRINGS[test_key]["instring"]
    expected = TEST_STRINGS[test_key]["expected"]

    tokens = get_tokens(source)
    index = get_string_index(tokens)

    result = classifier(tokens, index)
    assert result == expected, f"\nFailed {test_key}\nExpected {expected}\nGot {result}"


@pytest.mark.unit
@pytest.mark.parametrize(
    "test_key,classifier",
    [
        ("is_code_line", is_code_line),
        ("is_closing_quotes", is_closing_quotes),
        ("is_definition_line_class", is_definition_line),
        ("is_definition_line_function", is_definition_line),
        ("is_definition_line_async_function", is_definition_line),
        ("is_not_definition_line_function", is_definition_line),
        ("is_inline_comment", is_inline_comment),
        ("is_line_following_indent", is_line_following_indent),
        ("is_nested_definition_line_class", is_nested_definition_line),
        ("is_nested_definition_line_function", is_nested_definition_line),
        ("is_nested_definition_line_async_function", is_nested_definition_line),
        ("is_not_nested_definition_line_function", is_nested_definition_line),
        ("is_newline_continuation", is_newline_continuation),
        ("is_string_variable", is_string_variable),
    ],
)
def test_misc_classifiers(test_key, classifier):
    token = build_token("", test_key)

    try:
        prev_token = build_token("prev_", test_key)
        result = classifier(token, prev_token)
    except KeyError:
        result = classifier(token)

    expected = TEST_STRINGS[test_key]["expected"]
    assert result == expected, f"Failed {test_key}\nExpected {expected}\nGot {result}"


@pytest.mark.unit
@pytest.mark.skipif(sys.version_info < (3, 12), reason="requires Python 3.12 or higher")
def test_is_f_string():
    """Test is_f_string classifier (requires Python 3.12+)."""
    token = build_token("", "is_f_string")
    prev_token = build_token("prev_", "is_f_string")

    if sys.version_info >= (3, 13):
        expected = TEST_STRINGS["is_f_string"]["expected313"]
    else:
        expected = TEST_STRINGS["is_f_string"]["expected"]
    result = is_f_string(token, prev_token)

    assert result == expected, f"Failed is_f_string\nExpected {expected}\nGot {result}"


@pytest.mark.integration
@pytest.mark.order(5)
@pytest.mark.parametrize(
    "test_key, expected",
    [
        ("find_module_docstring", [(0, 1, "module")]),
        ("find_class_docstring", [(1, 6, "class")]),
        ("find_function_docstring", [(1, 8, "function")]),
        ("find_function_docstring_with_decorator", [(4, 11, "function")]),
        ("find_attribute_docstring", [(1, 5, "attribute")]),
        (
            "find_multiple_docstrings",
            [(0, 1, "module"), (4, 9, "class"), (12, 20, "function")],
        ),
    ],
)
def test_find_docstring_blocks(test_key, expected):
    source = TEST_STRINGS[test_key]["instring"]
    tokens = get_tokens(source)

    result = do_find_docstring_blocks(tokens)
    assert result == expected, f"Failed {test_key}\nExpected {expected}\nGot {result}"
