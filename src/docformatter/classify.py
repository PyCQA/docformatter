#!/usr/bin/env python
#
#       docformatter.classify.py is part of the docformatter project
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
"""This module provides docformatter's classification functions."""


# Standard Library Imports
import re
import sys
import tokenize
from tokenize import TokenInfo
from typing import Union

# docformatter Package Imports
from docformatter.constants import MAX_PYTHON_VERSION

PY312 = (sys.version_info[0], sys.version_info[1]) > MAX_PYTHON_VERSION


def do_find_docstring_blocks(tokens: list[TokenInfo]) -> list[tuple[int, int, str]]:
    """Identify all docstring blocks and their anchor points.

    Parameters
    ----------
    tokens (list[TokenInfo]):
        A list of tokenized Python source code.

    Returns
    -------
    list[tuple[int, int, str]]:
        A list of tuples representing each docstring block.  Each tuple contains:
            - anchor_index (int): Index of the anchor (class, def, async def, or
              assignment).
            - string_index (int): Index of the docstring token.
            - docstring_type (str): One of "module", "class", "function", or
              "attribute".
    """
    docstring_blocks = []

    for i, token in enumerate(tokens):
        if (
            token.type != tokenize.STRING
            or not (
                token.string.startswith('"""')
                or token.string.startswith('r"""')
                or token.string.startswith('R"""')
                or token.string.startswith('u"""')
                or token.string.startswith('U"""')
                or token.string.startswith("'''")
                or token.string.startswith("r'''")
                or token.string.startswith("R'''")
                or token.string.startswith("u'''")
                or token.string.startswith("U'''")
            )
            or " = " in token.line
        ):
            continue

        if is_module_docstring(tokens, i):
            docstring_blocks.append((0, i, "module"))
            continue

        if is_attribute_docstring(tokens, i):
            anchor_idx = _do_find_anchor_index(tokens, i, target="attribute")
            if anchor_idx is not None:
                docstring_blocks.append((anchor_idx, i, "attribute"))
            continue

        if is_class_docstring(tokens, i):
            anchor_idx = _do_find_anchor_index(tokens, i, target="class")
            if anchor_idx is not None:
                docstring_blocks.append((anchor_idx, i, "class"))
            continue

        if is_function_or_method_docstring(tokens, i):
            anchor_idx = _do_find_anchor_index(tokens, i, target="def")
            if anchor_idx is not None:
                docstring_blocks.append((anchor_idx, i, "function"))
            continue

    # If adjacent docstrings have the same anchor index, remove the second one as
    # there can only be one docstring per anchor.
    i = 1
    while i < len(docstring_blocks):
        if docstring_blocks[i][0] == docstring_blocks[i - 1][0]:
            docstring_blocks.pop(i)
        i += 1

    return docstring_blocks


def _do_find_anchor_index(
    tokens: list[TokenInfo],
    docstring_index: int,
    target: str,
) -> Union[int, None]:
    """Walk backward from a docstring to find the matching anchor.

    The matching anchor would be one of `class`, `def`, `async def`, or an assignment.

    Parameters
    ----------
    tokens (list[TokenInfo]):
        A list of tokenized Python source code.
    docstring_index (int):
        Index of the STRING token representing the docstring.
    target (str):
        One of "class", "def", or "attribute" indicating what to search for.

    Returns
    -------
    int | None:
        Index of the anchor token if found, otherwise None.
    """
    i = docstring_index - 1
    saw_decorator = False

    while i >= 0:
        tok = tokens[i]

        if tok.type == tokenize.OP and tok.string == "@":
            saw_decorator = True

        if target == "class" and tok.type == tokenize.NAME and tok.string == "class":
            return i

        if target == "def" and tok.type == tokenize.NAME and tok.string == "def":
            # Handle @decorator above def
            if saw_decorator:
                while i > 0 and tokens[i - 1].type != tokenize.NEWLINE:
                    i -= 1
            return i

        if target == "attribute":
            if tok.type == tokenize.NAME:
                return i

        i -= 1

    return None


def is_attribute_docstring(
    tokens: list[tokenize.TokenInfo],
    index: int,
) -> bool:
    """Return True if the string token is an attribute docstring.

    Parameters
    ----------
    tokens : list[TokenInfo]
        A list of tokenized Python source code.
    index : int
        Index of the anchor token.

    Returns
    -------
        True if attribute docstring, False otherwise.
    """
    if index < 2:  # noqa: PLR2004
        return False

    # Step 1: Find the previous NEWLINE before the docstring
    k = index - 1
    while k > 0 and tokens[k].type != tokenize.NEWLINE:
        k -= 1

    # Step 2: Check for '=' or ':' on the line *before* the docstring
    seen_equal_or_colon = False
    for tok in tokens[0:index]:
        if tok.type == tokenize.OP and tok.string == "=" and '"""' not in tok.line:
            seen_equal_or_colon = True
            break
        else:
            seen_equal_or_colon = False

    if not seen_equal_or_colon:
        return False

    return True


def is_class_docstring(
    tokens: list[tokenize.TokenInfo],
    index: int,
) -> bool:
    """Determine if docstring is a class docstring."""
    # Walk backward to find the most recent `class` keyword before the string,
    # without crossing over a `def`, `async`, or another block
    for i in range(index - 1, -1, -1):
        tok = tokens[i]
        if tok.type == tokenize.NAME and tok.string == "class":
            return True
        if tok.type == tokenize.NAME and tok.string in ("def", "async"):
            return False  # Hit enclosing function or method first.
        if tok.type == tokenize.OP and tok.string == "=":
            return False  # Hit assignment, not a class docstring.

    return False


def is_closing_quotes(
    token: tokenize.TokenInfo, prev_token: tokenize.TokenInfo
) -> bool:
    """Determine if token is a closing quote for a docstring.

    Parameters
    ----------
    token : tokenize.TokenInfo
        The token to check.
    prev_token : tokenize.TokenInfo
        The previous token in the stream.

    Returns
    -------
    bool
        True if the token is a closing quote for a docstring, False otherwise.
    """
    _offset = prev_token.line.split("\n")[-1]
    if prev_token.line.endswith("\n"):
        _offset = prev_token.line.split("\n")[-2]

    if (
        token.line.strip() == '"""'
        and token.type == tokenize.NEWLINE
        or token.line == _offset
    ):
        return True

    return False


def is_code_line(token: tokenize.TokenInfo) -> bool:
    """Determine if token is a line of code.

    Parameters
    ----------
    token : tokenize.TokenInfo
        The token to check.

    Returns
    -------
    bool
        True if the token is a code line, False otherwise.
    """
    if token.type == tokenize.NAME and not (
        token.line.strip().startswith("def ")
        or token.line.strip().startswith("async ")
        or token.line.strip().startswith("class ")
    ):
        return True

    return False


def is_definition_line(token: tokenize.TokenInfo) -> bool:
    """Determine if token is a class or function/method definition line.

    Parameters
    ----------
    token : tokenize.TokenInfo
        The token to check.

    Returns
    -------
    bool
        True if the token is a definition line, False otherwise.
    """
    if token.type == tokenize.NAME and (
        token.line.startswith("def ")
        or token.line.startswith("async ")
        or token.line.startswith("class ")
    ):
        return True

    return False


def is_f_string(token: tokenize.TokenInfo, prev_token: tokenize.TokenInfo) -> bool:
    """Determine if token is an f-string.

    Parameters
    ----------
    token : tokenize.TokenInfo
        The token to check.
    prev_token : tokenize.TokenInfo
        The previous token in the stream.

    Returns
    -------
    bool
        True if the token is an f-string, False otherwise.
    """
    if PY312:
        if tokenize.FSTRING_MIDDLE in [token.type, prev_token.type]:
            return True

    return False


def is_function_or_method_docstring(
    tokens: list[tokenize.TokenInfo],
    index: int,
) -> bool:
    """Determine if docstring is a function or method docstring."""
    for i in range(index - 1, -1, -1):
        tok = tokens[i]
        if tok.type == tokenize.NAME and tok.string in ("def", "async"):
            return True
        if tok.type == tokenize.NAME and tok.string == "class":
            return False  # hit enclosing class first

    return False


def is_inline_comment(token: tokenize.TokenInfo) -> bool:
    """Determine if token is an inline comment.

    Parameters
    ----------
    token : tokenize.TokenInfo
        The token to check.

    Returns
    -------
    bool
        True if the token is an inline comment, False otherwise.
    """
    if token.line.strip().startswith('"""') and token.string.startswith("#"):
        return True
    return False


def is_line_following_indent(
    token: tokenize.TokenInfo,
    prev_token: tokenize.TokenInfo,
) -> bool:
    """Determine if token is a line that follows an indent.

    Parameters
    ----------
    token : tokenize.TokenInfo
        The token to check.
    prev_token : tokenize.TokenInfo
        The previous token in the stream.

    Returns
    -------
    bool
        True if the token is a line that follows an indent, False otherwise.
    """
    if prev_token.type == tokenize.INDENT and prev_token.line in token.line:
        return True

    return False


def is_module_docstring(
    tokens: list[tokenize.TokenInfo],
    index: int,
) -> bool:
    """Determine if docstring is a module docstring."""
    # No code tokens before the string
    for k in range(index):
        if tokens[k][0] not in (
            tokenize.ENCODING,
            tokenize.COMMENT,
            tokenize.NEWLINE,
            tokenize.NL,
        ):
            return False
    return True


def is_nested_definition_line(token: tokenize.TokenInfo) -> bool:
    """Determine if token is a nested class or function/method definition line.

    Parameters
    ----------
    token : tokenize.TokenInfo
        The token to check.

    Returns
    -------
    bool
        True if the token is a nested definition line, False otherwise.
    """
    return re.match(r"^ {4,}(async|class|def) ", token.line) is not None


def is_newline_continuation(
    token: tokenize.TokenInfo,
    prev_token: tokenize.TokenInfo,
) -> bool:
    """Determine if token is a continuation of a previous line.

    Parameters
    ----------
    token : tokenize.TokenInfo
        The token to check.
    prev_token : tokenize.TokenInfo
        The previous token in the stream.

    Returns
    -------
    bool
        True if the token is a continuation of a previous line, False otherwise.
    """
    if (
        token.type in (tokenize.NEWLINE, tokenize.NL)
        and token.line.strip() in prev_token.line.strip()
        and token.line != "\n"
    ):
        return True

    return False


def is_string_variable(
    token: tokenize.TokenInfo,
    prev_token: tokenize.TokenInfo,
) -> bool:
    """Determine if token is a string variable assignment.

    Parameters
    ----------
    token : tokenize.TokenInfo
        The token to check.
    prev_token : tokenize.TokenInfo
        The previous token in the stream.

    Returns
    -------
    bool
        True if the token is a string variable assignment, False otherwise.
    """
    # TODO: The AWAIT token is removed in Python 3.13 and later.  Only Python 3.9
    # seems to generate the AWAIT token, so we can safely remove the check for it when
    # support for Python 3.9 is dropped in April 2026.
    if sys.version_info <= (3, 12):
        _token_types = (tokenize.AWAIT, tokenize.OP)
    else:
        _token_types = (tokenize.OP,)

    if prev_token.type in _token_types and (
        '= """' in token.line or token.line in prev_token.line
    ):
        return True

    return False


def is_docstring_at_end_of_file(tokens: list[tokenize.TokenInfo], index: int) -> bool:
    """Determine if the docstring is at the end of the file."""
    for i in range(index + 1, len(tokens)):
        tok = tokens[i]
        if tok.type not in (
            tokenize.NL,
            tokenize.NEWLINE,
            tokenize.DEDENT,
            tokenize.ENDMARKER,
        ):
            return False

    return True
