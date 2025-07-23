#!/usr/bin/env python
#
#       docformatter.patterns.misc.py is part of the docformatter project
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
"""This module provides docformatter's miscellaneous pattern recognition functions."""


# Standard Library Imports
import re
from re import Match
from typing import Union

# docformatter Package Imports
from docformatter.constants import LITERAL_REGEX, URL_REGEX


# TODO: Create INLINE_MATH_REGEX in constants.py and use it here.
def is_inline_math(line: str) -> Union[Match[str], None]:
    """Check if the line is an inline math expression.

    Parameters
    ----------
    line : str
        The line to check for inline math patterns.

    Notes
    -----
    Inline math expressions have the following pattern:
        c :math:`[0, `]`

    Returns
    -------
    Match[str] | None
        A match object if the line matches an inline math pattern, None otherwise.
    """
    return re.match(r" *\w *:[a-zA-Z0-9_\- ]*:", line)


def is_literal_block(line: str) -> Union[Match[str], None]:
    """Check if the line is a literal block.

    Parameters
    ----------
    line : str
        The line to check for literal block patterns.

    Notes
    -----
    Literal blocks have the following pattern:
        ::
            code

    Returns
    -------
    Match[str] | None
        A match object if the line matches a literal block pattern, None otherwise.
    """
    return re.match(LITERAL_REGEX, line)


def is_probably_beginning_of_sentence(line: str) -> Union[Match[str], None, bool]:
    """Determine if the line begins a sentence.

    Parameters
    ----------
    line : str
        The line to be tested.

    Returns
    -------
    is_beginning : bool
        True if this token is the beginning of a sentence, False otherwise.
    """
    # Check heuristically for a parameter list.
    for token in ["@", "-", r"\*"]:
        if re.search(rf"\s{token}\s", line):
            return True

    stripped_line = line.strip()
    is_beginning_of_sentence = re.match(r"^[-@\)]", stripped_line)
    is_pydoc_ref = re.match(r"^:\w+:", stripped_line)

    return is_beginning_of_sentence and not is_pydoc_ref


def is_some_sort_of_code(text: str) -> bool:
    """Return True if the text looks like code.

    Parameters
    ----------
    text : str
        The text to check for code patterns.

    Returns
    -------
    is_code : bool
        True if the text contains and code patterns, False otherwise.
    """
    return any(
        len(word) > 50 and not re.match(URL_REGEX, word)  # noqa: PLR2004
        for word in text.split()
    )
