# pylint: skip-file
# type: ignore
#
#       tests.formatter.test_format_methods.py is part of the docformatter project
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
"""Module for testing various Formatter class methods."""

# Standard Library Imports
import contextlib
import sys
import tokenize
from io import BytesIO
from tokenize import TokenInfo

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
from docformatter.format import Formatter

with open("tests/_data/string_files/format_methods.toml", "rb") as f:
    TEST_STRINGS = tomllib.load(f)


def _get_tokens(source):
    return list(tokenize.tokenize(BytesIO(source.encode()).readline))


def _get_docstring_token_and_index(tokens):
    for i, tok in enumerate(tokens):
        if tok.type == tokenize.STRING:
            return i
    raise ValueError("No docstring found in token stream.")


@pytest.mark.unit
@pytest.mark.parametrize("args", [[""]])
def test_do_add_blank_lines(args):
    uut = Formatter(
        args,
        sys.stderr,
        sys.stdin,
        sys.stdout,
    )
    uut._do_add_blank_lines(2, 2, 2)

    assert uut.new_tokens == [
        TokenInfo(type=4, string="\n", start=(2, 0), end=(2, 1), line="\n"),
        TokenInfo(type=4, string="\n", start=(3, 0), end=(3, 1), line="\n"),
    ]


@pytest.mark.unit
@pytest.mark.parametrize(
    "test_key",
    [
        "do_add_unformatted_docstring",
    ],
)
@pytest.mark.parametrize("args", [[""]])
def test_do_add_unformatted_docstring(test_key, args):
    uut = Formatter(
        args,
        sys.stderr,
        sys.stdin,
        sys.stdout,
    )
    token = tokenize.TokenInfo(
        type=TEST_STRINGS[test_key]["token"][0],
        string=TEST_STRINGS[test_key]["token"][1],
        start=tuple(TEST_STRINGS[test_key]["token"][2]),
        end=tuple(TEST_STRINGS[test_key]["token"][3]),
        line=TEST_STRINGS[test_key]["token"][4],
    )
    expected = [
        TokenInfo(
            type=3,
            string='"""This is a docstring.\\n\\n\\n    That should be on less lines\\n"""',
            start=(3, 4),
            end=(6, 7),
            line='    """This is a docstring.\\n\\n\\n    That should be on less lines\\n"""',
        ),
        TokenInfo(
            type=4,
            string="\n",
            start=(6, 7),
            end=(6, 8),
            line='    """This is a docstring.\\n\\n\\n    That should be on less lines\\n"""',
        ),
    ]

    uut._do_add_unformatted_docstring(token, "function")
    assert (
        uut.new_tokens == expected
    ), f"\nFailed {test_key}\nExpected {expected}\nGot {uut.new_tokens}"


@pytest.mark.integration
@pytest.mark.order(5)
@pytest.mark.parametrize(
    "test_key, args",
    [
        ("do_add_formatted_docstring", [""]),
    ],
)
def test_do_add_formatted_docstring(test_key, test_args, args):
    uut = Formatter(
        test_args,
        sys.stderr,
        sys.stdin,
        sys.stdout,
    )

    token = tokenize.TokenInfo(
        type=TEST_STRINGS[test_key]["token"][0],
        string=TEST_STRINGS[test_key]["token"][1],
        start=tuple(TEST_STRINGS[test_key]["token"][2]),
        end=tuple(TEST_STRINGS[test_key]["token"][3]),
        line=TEST_STRINGS[test_key]["token"][4],
    )
    next_token = tokenize.TokenInfo(
        type=TEST_STRINGS[test_key]["next_token"][0],
        string=TEST_STRINGS[test_key]["next_token"][1],
        start=tuple(TEST_STRINGS[test_key]["next_token"][2]),
        end=tuple(TEST_STRINGS[test_key]["next_token"][3]),
        line=TEST_STRINGS[test_key]["next_token"][4],
    )
    expected = [
        tokenize.TokenInfo(
            type=3,
            string='"""This is a docstring.\\n."""',
            start=(3, 4),
            end=(6, 7),
            line='    """This is a docstring.\\n."""\n',
        ),
        tokenize.TokenInfo(
            type=4,
            string="\n",
            start=(6, 7),
            end=(6, 8),
            line='    """This is a docstring.\\n."""\n',
        ),
        tokenize.TokenInfo(type=4, string="\n", start=(7, 0), end=(7, 1), line="\n"),
    ]

    uut._do_add_formatted_docstring(token, next_token, "function", 1)
    assert (
        uut.new_tokens == expected
    ), f"\nFailed {test_key}\nExpected {expected}\nGot {uut.new_tokens}"


@pytest.mark.integration
@pytest.mark.order(3)
@pytest.mark.parametrize(
    "test_key, args",
    [
        ("do_format_oneline_docstring", [""]),
        ("do_format_oneline_docstring_that_ends_in_quote", [""]),
        ("do_format_oneline_docstring_with_wrap", ["--wrap-summaries", "72", ""]),
        (
            "do_format_oneline_docstring_with_quotes_newline",
            ["--close-quotes-on-newline", ""],
        ),
        (
            "do_format_oneline_docstring_make_multiline",
            ["--make-summary-multi-line", ""],
        ),
    ],
)
def test_format_one_line_docstring(test_key, test_args, args):
    uut = Formatter(
        test_args,
        sys.stderr,
        sys.stdin,
        sys.stdout,
    )

    source = TEST_STRINGS[test_key]["source"]
    expected = TEST_STRINGS[test_key]["expected"]

    result = uut._do_format_oneline_docstring(
        "    ",
        source,
        '"""',
    )
    assert result == expected, f"\nFailed {test_key}\nExpected {expected}\nGot {result}"


@pytest.mark.integration
@pytest.mark.parametrize(
    "test_key, args",
    [
        ("do_format_multiline_docstring", [""]),
        (
            "do_format_multiline_docstring_pre_summary_newline",
            ["--pre-summary-newline", ""],
        ),
        (
            "do_format_multiline_docstring_post_description_blank",
            ["--blank", ""],
        ),
    ],
)
def test_format_multiline_docstring(test_key, test_args, args):
    uut = Formatter(
        test_args,
        sys.stderr,
        sys.stdin,
        sys.stdout,
    )

    source = TEST_STRINGS[test_key]["source"]
    expected = TEST_STRINGS[test_key]["expected"]

    result = uut._do_format_multiline_docstring(
        "    ",
        source[0],
        source[1],
        '"""',
    )
    assert result == expected, f"\nFailed {test_key}\nExpected {expected}\nGot {result}"


@pytest.mark.integration
@pytest.mark.order(6)
@pytest.mark.parametrize(
    "test_key, args",
    [
        ("do_rewrite_docstring_blocks", [""]),
    ],
)
def test_do_rewrite_docstring_blocks(test_key, test_args, args):
    uut = Formatter(
        test_args,
        sys.stderr,
        sys.stdin,
        sys.stdout,
    )

    tokens = []
    for token in TEST_STRINGS[test_key]["tokens"]:
        tokens.append(
            tokenize.TokenInfo(
                type=token[0],
                string=token[1],
                start=tuple(token[2]),
                end=tuple(token[3]),
                line=token[4],
            )
        )
    expected = []
    for token in TEST_STRINGS[test_key]["expected"]:
        expected.append(
            tokenize.TokenInfo(
                type=token[0],
                string=token[1],
                start=tuple(token[2]),
                end=tuple(token[3]),
                line=token[4],
            )
        )

    uut._do_rewrite_docstring_blocks(tokens)
    assert (
        uut.new_tokens == expected
    ), f"\nFailed {test_key}\nExpected {expected}\nGot {uut.new_tokens}"
