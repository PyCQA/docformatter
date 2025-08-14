#!/usr/bin/env python
#
#       docformatter.wrappers.summary.py is part of the docformatter project
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
"""This module provides docformatter's summary wrapper functions."""


# Standard Library Imports
import re
import textwrap


def do_unwrap_summary(summary: str) -> str:
    r"""Return summary with newlines removed in preparation for wrapping.

    Parameters
    ----------
    summary : str
        The summary text from the docstring.

    Returns
    -------
    str
        The summary text with newline (\n) characters replaced by a single space.
    """
    return re.sub(r"\s*\n\s*", " ", summary)


def do_wrap_summary(
    summary: str,
    initial_indent: str,
    subsequent_indent: str,
    wrap_length: int,
) -> str:
    """Return line-wrapped summary text.

    If the wrap_length is any value less than or equal to zero, the raw, unwrapped
    summary text will be returned.

    Parameters
    ----------
    summary : str
        The summary text from the docstring.
    initial_indent : str
        The indentation string for the first line of the summary.
    subsequent_indent : str
        The indentation string for all the other lines of the summary.
    wrap_length : int
        The column position to wrap the summary lines.

    Returns
    -------
    str
        The summary text from the docstring wrapped at wrap_length columns.
    """
    if wrap_length > 0:
        return textwrap.fill(
            do_unwrap_summary(summary),
            width=wrap_length,
            initial_indent=initial_indent,
            subsequent_indent=subsequent_indent,
        ).strip()
    else:
        return summary
