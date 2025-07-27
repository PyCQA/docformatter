#!/usr/bin/env python
#
#       docformatter.wrappers.description.py is part of the docformatter project
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
"""This module provides docformatter's description wrapper functions."""


# Standard Library Imports
import contextlib
from typing import List

# docformatter Package Imports
import docformatter.patterns as _patterns
import docformatter.strings as _strings


def do_wrap_description(  # noqa: PLR0913
    text,
    indentation,
    wrap_length,
    force_wrap,
    strict,
    rest_sections,
    style: str = "sphinx",
):
    """Return line-wrapped description text.

    We only wrap simple descriptions. We leave doctests, multi-paragraph text, and
    bulleted lists alone.

    Parameters
    ----------
    text : str
        The unwrapped description text.
    indentation : str
        The indentation string.
    wrap_length : int
        The line length at which to wrap long lines.
    force_wrap : bool
        Whether to force docformatter to wrap long lines when normally they
        would remain untouched.
    strict : bool
        Whether to strictly follow reST syntax to identify lists.
    rest_sections : str
        A regular expression used to find reST section header adornments.
    style : str
        The name of the docstring style to use when dealing with parameter
        lists (default is sphinx).

    Returns
    -------
    str
        The description wrapped at wrap_length characters.
    """
    text = _strings.do_strip_leading_blank_lines(text)

    # TODO: Don't wrap the doctests, but wrap the remainder of the docstring.
    # Do not modify docstrings with doctests at all.
    if ">>>" in text:
        return text

    text = _strings.do_reindent(text, indentation).rstrip()

    # TODO: Don't wrap the code section or the lists, but wrap everything else.
    # Ignore possibly complicated cases.
    if wrap_length <= 0 or (
        not force_wrap
        and (
            _patterns.is_some_sort_of_code(text)
            or _patterns.do_find_rest_directives(text, len(indentation))
            or _patterns.is_type_of_list(text, strict, style)
        )
    ):
        return text

    lines = _strings.do_split_description(text, indentation, wrap_length, style)

    return indentation + "\n".join(lines).strip()


def do_close_description(
    text: str,
    text_idx: int,
    indentation: str,
) -> List[str]:
    """Wrap any description following the last URL or field list.

    Parameters
    ----------
    text : str
        The docstring text.
    text_idx : int
        The index of the last URL or field list match.
    indentation : str
        The indentation string to use with docstrings.

    Returns
    -------
    _split_lines : list
        The text input split into individual lines.
    """
    _split_lines = []
    with contextlib.suppress(IndexError):
        _split_lines = (
            text[text_idx + 1 :] if text[text_idx] == "\n" else text[text_idx:]
        ).splitlines()
        for _idx, _line in enumerate(_split_lines):
            if _line not in ["", "\n", f"{indentation}"]:
                _split_lines[_idx] = f"{indentation}{_line.strip()}"

    return _split_lines
