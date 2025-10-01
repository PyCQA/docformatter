#!/usr/bin/env python
#
#       docformatter.patterns.fields.py is part of the docformatter project
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
"""This module provides docformatter's field list pattern recognition functions."""


# Standard Library Imports
import re
from re import Match
from typing import Union

# docformatter Package Imports
from docformatter.constants import (
    EPYTEXT_REGEX,
    GOOGLE_REGEX,
    NUMPY_REGEX,
    SPHINX_REGEX,
)


def do_find_field_lists(
    text: str,
    style: str,
) -> tuple[list[tuple[int, int]], bool]:
    r"""Determine if docstring contains any field lists.

    Parameters
    ----------
    text : str
        The docstring description to check for field list patterns.
    style : str
        The field list style used.

    Returns
    -------
    tuple[list[tuple], bool]
        A tuple containing lists of tuples and a boolean.  Each inner tuple
        contains the starting and ending position of each field list found in the
        description.  The boolean indicates whether long field list lines should
        be wrapped.
    """
    _field_idx = []
    _wrap_parameters = False

    if style == "epytext":
        _field_idx = [
            (_field.start(0), _field.end(0))
            for _field in re.finditer(EPYTEXT_REGEX, text)
        ]
        _wrap_parameters = True
    elif style == "sphinx":
        _field_idx = [
            (_field.start(0), _field.end(0))
            for _field in re.finditer(SPHINX_REGEX, text)
        ]
        _wrap_parameters = True
    elif style == "google":
        _field_idx = [
            (_field.start(0), _field.end(0))
            for _field in re.finditer(GOOGLE_REGEX, text, re.MULTILINE)
        ]
        _wrap_parameters = False  # Don't wrap Google-style field lists
    elif style == "numpy":
        _field_idx = [
            (_field.start(0), _field.end(0))
            for _field in re.finditer(NUMPY_REGEX, text, re.MULTILINE)
        ]
        _wrap_parameters = False  # Don't wrap NumPy-style field lists
    
    # If no field lists were found for the current style, check for field lists
    # from other styles and preserve them as-is (don't wrap).
    if not _field_idx:
        # Check for Google-style field lists (e.g., "Args:", "Returns:").
        # Use a more specific pattern that only matches known Google section names.
        google_sections = r'^ *(Args|Arguments|Attributes|Example|Examples|Note|Notes|' \
                         r'See Also|References|Returns|Return|Raises|Raise|Yields|Yield|' \
                         r'Warns|Warning|Warnings|Receives|Receive|Other Parameters):$'
        google_matches = list(re.finditer(google_sections, text, re.MULTILINE))
        if google_matches:
            _field_idx = [(_field.start(0), _field.end(0)) for _field in google_matches]
            _wrap_parameters = False
        
        # If still nothing, check for NumPy-style field lists
        if not _field_idx:
            numpy_matches = list(re.finditer(NUMPY_REGEX, text, re.MULTILINE))
            if numpy_matches:
                _field_idx = [(_field.start(0), _field.end(0)) for _field in numpy_matches]
                _wrap_parameters = False
                
    return _field_idx, _wrap_parameters


def is_field_list(
    text: str,
    style: str,
) -> bool:
    """Determine if docstring contains field lists.

    Parameters
    ----------
    text : str
        The docstring text.
    style : str
        The field list style to use.

    Returns
    -------
    is_field_list : bool
        Whether the field list pattern for style was found in the docstring.
    """
    split_lines = text.rstrip().splitlines()

    if style == "epytext":
        return any(is_epytext_field_list(line) for line in split_lines)
    elif style == "sphinx":
        return any(is_sphinx_field_list(line) for line in split_lines)

    return False


def is_epytext_field_list(line: str) -> Union[Match[str], None]:
    """Check if the line is an Epytext field list.

    Parameters
    ----------
    line : str
        The line to check for Epytext field list patterns.

    Returns
    -------
    Match[str] | None
        A match object if the line matches an Epytext field list pattern, None
        otherwise.

    Notes
    -----
    Epytext field lists have the following pattern:
        @param x:
        @type x:
    """
    return re.match(EPYTEXT_REGEX, line)


def is_google_field_list(line: str) -> Union[Match[str], None]:
    """Check if the line is a Google field list.

    Parameters
    ----------
    line: str
        The line to check for Google field list patterns.

    Returns
    -------
    Match[str] | None
        A match object if the line matches a Google field list pattern, None otherwise.

    Notes
    -----
    Google field lists have the following pattern:
        x (int): Description of x.
    """
    return re.match(GOOGLE_REGEX, line)


def is_numpy_field_list(line: str) -> Union[Match[str], None]:
    """Check if the line is a NumPy field list.

    Parameters
    ----------
    line: str
        The line to check for NumPy field list patterns.

    Returns
    -------
    Match[str] | None
        A match object if the line matches a NumPy field list pattern, None otherwise.

    Notes
    -----
    NumPy field lists have the following pattern:
        x : int
            Description of x.
        x
            Description of x.
    """
    return re.match(NUMPY_REGEX, line)


def is_sphinx_field_list(line: str) -> Union[Match[str], None]:
    """Check if the line is a Sphinx field list.

    Parameters
    ----------
    line: str
        The line to check for Sphinx field list patterns.

    Returns
    -------
    Match[str] | None
        A match object if the line matches a Sphinx field list pattern, None otherwise.

    Notes
    -----
    Sphinx field lists have the following pattern:
        :parameter: description
    """
    return re.match(SPHINX_REGEX, line)


# TODO: Add a USER_DEFINED_REGEX to constants.py and use that instead of the
#  hardcoded patterns.
def is_user_defined_field_list(line: str) -> Union[Match[str], None]:
    """Check if the line is a user-defined field list.

    Parameters
    ----------
    line: str
        The line to check for user-defined field list patterns.

    Returns
    -------
    Match[str] | None
        A match object if the line matches a user-defined field list pattern, None
        otherwise.

    Notes
    -----
    User-defined field lists have the following pattern:
        parameter - description
        parameter -- description
        @parameter description

    These patterns were in the original docformatter code.  These patterns do not
    conform to any common docstring styles.  There is no documented reason they were
    included and are retained for historical purposes.
    """
    return (
        re.match(r"[\S ]+ - \S+", line)
        or re.match(r"\s*\S+\s+--\s+", line)
        or re.match(r"^ *@[a-zA-Z0-9_\- ]*(?:(?!:).)*$", line)
    )
