#!/usr/bin/env python
#
#       docformatter.patterns.url.py is part of the docformatter project
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
"""This module provides docformatter's URL pattern recognition functions."""


# Standard Library Imports
import contextlib
import re
from typing import List, Tuple

# docformatter Package Imports
from docformatter.constants import URL_REGEX, URL_SKIP_REGEX


def do_find_links(text: str) -> List[Tuple[int, int]]:
    r"""Determine if docstring contains any links.

    Parameters
    ----------
    text : str
        The docstring description to check for link patterns.

    Returns
    -------
    url_index : list
        A list of tuples with each tuple containing the starting and ending
        position of each URL found in the passed description.
    """
    _url_iter = re.finditer(URL_REGEX, text)
    return [(_url.start(0), _url.end(0)) for _url in _url_iter]


def do_skip_link(text: str, index: Tuple[int, int]) -> bool:
    """Check if the identified URL is other than a complete link.

    Parameters
    ----------
    text : str
        The description text containing the link.
    index : tuple
        The index in the text of the starting and ending position of the
        identified link.

    Notes
    -----
    Is the identified link simply:
        1. The URL scheme pattern such as 's3://' or 'file://' or 'dns:'.
        2. The beginning of a URL link that has been wrapped by the user.

    Returns
    -------
    _do_skip : bool
        Whether to skip this link and simpley treat it as a standard text word.
    """
    _do_skip = re.search(URL_SKIP_REGEX, text[index[0] : index[1]]) is not None

    with contextlib.suppress(IndexError):
        _do_skip = _do_skip or (text[index[0]] == "<" and text[index[1]] != ">")

    return _do_skip
