#!/usr/bin/env python
#
#       docformatter.patterns.lists.py is part of the docformatter project
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
"""This module provides docformatter's list pattern recognition functions."""


# Standard Library Imports
import re
from re import Match
from typing import Union

# docformatter Package Imports
from docformatter.constants import (
    BULLET_REGEX,
    ENUM_REGEX,
    HEURISTIC_MIN_LIST_ASPECT_RATIO,
    OPTION_REGEX,
)

# docformatter Local Imports
from .fields import (
    is_epytext_field_list,
    is_field_list,
    is_google_field_list,
    is_numpy_field_list,
    is_sphinx_field_list,
    is_user_defined_field_list,
)
from .headers import is_alembic_header, is_numpy_section_header, is_rest_section_header
from .misc import is_inline_math, is_literal_block


def is_type_of_list(
    text: str,
    strict: bool,
    style: str,
) -> bool:
    """Determine if docstring line is a list.

    Parameters
    ----------
    text : str
        The text to check for potential lists.
    strict : bool
        Whether to strictly adhere to the wrap length argument.  If True,
        even heuristic lists will be wrapped.
    style : str
        The docstring style in use.  One of 'epytext', 'sphinx', numpy', or 'googlw'.

    Returns
    -------
    bool
        True if a list pattern is identified, False otherwise.
    """
    split_lines = text.rstrip().splitlines()

    if is_heuristic_list(text, strict):
        return True

    if is_field_list(text, style):
        return False

    return any(
        (
            is_bullet_list(line)
            or is_enumerated_list(line)
            or is_rest_section_header(line)
            or is_option_list(line)
            or is_epytext_field_list(line)
            or is_sphinx_field_list(line)
            or is_numpy_field_list(line)
            or is_numpy_section_header(line)
            or is_google_field_list(line)
            or is_user_defined_field_list(line)
            or is_literal_block(line)
            or is_inline_math(line)
            or is_alembic_header(line)
        )
        for line in split_lines
    )


def is_bullet_list(line: str) -> Union[Match[str], None]:
    """Check if the line is a bullet list item.

    Parameters
    ----------
    line : str
        The line to check for bullet list patterns.

    Notes
    -----
    Bullet list items have the following pattern:
        - item
        * item
        + item

    See <https://docutils.sourceforge.io/docs/user/rst/quickref.html#bullet-lists>`_

    Returns
    -------
    Match[str] | None
        A match object if the line matches a bullet list pattern, None otherwise.
    """
    return re.match(BULLET_REGEX, line)


def is_definition_list(line: str) -> Union[Match[str], None]:
    """Check if the line is a definition list item.

    Parameters
    ----------
    line : str
        The line to check for definition list patterns.

    Notes
    -----
    Definition list items have the following pattern:
        term: definition

    See <https://docutils.sourceforge.io/docs/user/rst/quickref.html#definition-lists>`_

    Returns
    -------
    Match[str] | None
        A match object if the line matches a definition list pattern, None otherwise.
    """
    return re.match(ENUM_REGEX, line)


def is_enumerated_list(line: str) -> Union[Match[str], None]:
    """Check if the line is an enumerated list item.

    Parameters
    ----------
    line : str
        The line to check for enumerated list patterns.

    Notes
    -----
    Enumerated list items have the following pattern:
        1. item
        2. item

    See <https://docutils.sourceforge.io/docs/user/rst/quickref.html#enumerated-lists>`_

    Returns
    -------
    Match[str] | None
        A match object if the line matches an enumerated list pattern, None otherwise.
    """
    return re.match(ENUM_REGEX, line)


def is_heuristic_list(text: str, strict: bool) -> bool:
    """Check if the line is a heuristic list item.

    Heuristic lists are identified by a long number of lines with short columns.

    Parameters
    ----------
    text : str
        The text to check for heuristic list patterns.
    strict: bool
        If True, the function will return False.
        If False, it will return True if the text has a high aspect ratio,
        indicating it is likely a list.

    Returns
    -------
    Match[str] | None
        A match object if the line matches a heuristic list pattern, None otherwise.
    """
    split_lines = text.rstrip().splitlines()

    # TODO: Find a better way of doing this.  Conversely, create a logger and log
    #  potential lists for the user to decide if they are lists or not.
    # Very large number of lines but short columns probably means a list of
    # items.
    if (
        len(split_lines) / max([len(line.strip()) for line in split_lines] + [1])
        > HEURISTIC_MIN_LIST_ASPECT_RATIO
    ) and not strict:
        return True

    return False


def is_option_list(line: str) -> Union[Match[str], None]:
    """Check if the line is an option list item.

    Parameters
    ----------
    line : str
        The line to check for option list patterns.

    Notes
    -----
    Option list items have the following pattern:
        -a, --all: Show all items.
        -h, --help: Show help message.

    See <https://docutils.sourceforge.io/docs/user/rst/quickref.html#option-lists>`_

    Returns
    -------
    Match[str] | None
        A match object if the line matches an option list pattern, None otherwise.
    """
    return re.match(OPTION_REGEX, line)
