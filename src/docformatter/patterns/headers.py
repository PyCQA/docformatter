#!/usr/bin/env python
#
#       docformatter.patterns.headers.py is part of the docformatter project
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
"""This module provides docformatter's header pattern recognition functions."""


# Standard Library Imports
import re
from re import Match
from typing import Union

# docformatter Package Imports
from docformatter.constants import (
    ALEMBIC_REGEX,
    NUMPY_SECTION_REGEX,
    REST_SECTION_REGEX,
)


def is_alembic_header(line: str) -> Union[Match[str], None]:
    """Check if the line is an Alembic header.

    Parameters
    ----------
    line : str
        The line to check for Alembic header patterns.

    Notes
    -----
    Alembic headers have the following pattern:
        Revision ID: <some id>>
        Revises: <some other id>
        Create Date: 2023-01-06 10:13:28.156709

    Returns
    -------
    bool
        True if the line matches an Alembic header pattern, False otherwise.
    """
    return re.match(ALEMBIC_REGEX, line)


def is_numpy_section_header(line: str) -> Union[Match[str], None]:
    r"""Check if the line is a NumPy section header.

    Parameters
    ----------
    line : str
        The line to check for NumPy section header patterns.

    Notes
    -----
    NumPy section headers have the following pattern:
        header\n----

    The following NumPy section headers are recognized:

        * Parameters
        * Other Parameters
        * Receives
        * Returns
        * Yields
        * Raises
        * Warns
        * Warnings
        * Notes
        * See Also
        * Examples

    Returns
    -------
    Match[str] | None
        A match object if the line matches a NumPy section header pattern, None
        otherwise.
    """
    return re.match(NUMPY_SECTION_REGEX, line)


def is_rest_section_header(line: str) -> Union[Match[str], None]:
    r"""Check if the line is a reST section header.

    Parameters
    ----------
    line : str
        The line to check for reST section header patterns.

    Notes
    -----
    reST section headers have the following patterns:
        ====\ndescription\n====
        ----\ndescription\n----
        description\n----

    The following adornments used in Python documentation are supported (see
    https://devguide.python.org/documentation/markup/#sections):

    #, for parts
    *, for chapters
    =, for sections
    -, for subsections
    ^, for subsubsections

    The following additional docutils recommended adornments are supported (see
    https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html#sections):

    ', single quote
    ", double quote
    +, plus sign
    _, underscore
    ~, tilde
    `, backtick
    ., period
    :, colon

    Returns
    -------
    bool
        True if the line matches a reST section header pattern, False otherwise.
    """
    return re.match(REST_SECTION_REGEX, line)
