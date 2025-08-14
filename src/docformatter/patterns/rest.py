#!/usr/bin/env python
#
#       docformatter.patterns.rest.py is part of the docformatter project
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
"""This module provides docformatter's reST directive pattern recognition functions."""


# Standard Library Imports
import re

# docformatter Package Imports
from docformatter.constants import REST_DIRECTIVE_REGEX, REST_INLINE_REGEX


def do_find_rest_directives(
    text: str,
) -> list[tuple[int, int]]:
    """Determine if docstring contains any reST directives.

    Parameters
    ----------
    text : str
        The docstring text to test.
    indent : int
        The number of spaces the reST directive line is indented.

    Returns
    -------
    bool
        True if the docstring is a reST directive, False otherwise.
    """
    _rest_iter = re.finditer(REST_DIRECTIVE_REGEX, text, flags=re.MULTILINE)
    return [(_rest.start(0), _rest.end(0)) for _rest in _rest_iter]


def do_find_inline_rest_markup(text: str) -> list[tuple[int, int]]:
    """Determine if docstring contains any inline reST markup.

    Parameters
    ----------
    text : str
        The docstring text to test.

    Returns
    -------
    bool
        True if the docstring is a reST directive, False otherwise.
    """
    _rest_iter = re.finditer(REST_INLINE_REGEX, text, flags=re.MULTILINE)
    return [(_rest.start(0), _rest.end(0)) for _rest in _rest_iter]
