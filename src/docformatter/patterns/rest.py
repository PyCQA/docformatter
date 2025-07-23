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
from docformatter.constants import REST_REGEX


def do_find_directives(text: str) -> bool:
    """Determine if docstring contains any reST directives.

    .. todo::

        Currently this function only returns True/False to indicate whether a
        reST directive was found.  Should return a list of tuples containing
        the start and end position of each reST directive found similar to the
        function do_find_links().

    Parameters
    ----------
    text : str
        The docstring text to test.

    Returns
    -------
    is_directive : bool
        Whether the docstring is a reST directive.
    """
    _rest_iter = re.finditer(REST_REGEX, text)
    return bool([(_rest.start(0), _rest.end(0)) for _rest in _rest_iter])
