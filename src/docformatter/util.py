#!/usr/bin/env python
#
#       docformatter.util.py is part of the docformatter project
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
"""This module provides docformatter utility functions."""


# Standard Library Imports
import os
import re
import sysconfig
from typing import List, Tuple

unicode = str

_PYTHON_LIBS = set(sysconfig.get_paths().values())


def find_py_files(sources, recursive, exclude=None):
    """Find Python source files.

    Parameters
    ----------
    sources : list
        Paths to files and/or directories to search.
    recursive : bool
        Drill down directories if True.
    exclude : list
        Which directories and files are excluded.

    Returns
    -------
        list of files found.
    """

    def is_hidden(name):
        """Return True if file 'name' is .hidden."""
        return os.path.basename(os.path.abspath(name)).startswith(".")

    def is_excluded(name, excluded):
        """Return True if file 'name' is excluded."""
        return (
            any(re.search(re.escape(str(e)), name, re.IGNORECASE) for e in excluded)
            if excluded
            else False
        )

    for _name in sorted(sources):
        if recursive and os.path.isdir(_name):
            for root, dirs, children in os.walk(unicode(_name)):
                if is_excluded(root, exclude):
                    break

                files = sorted(
                    [
                        _file
                        for _file in children
                        if not is_hidden(_file)
                        and not is_excluded(_file, exclude)
                        and _file.endswith(".py")
                    ]
                )
                for filename in files:
                    yield os.path.join(root, filename)
        elif (
            _name.endswith(".py")
            and not is_hidden(_name)
            and not is_excluded(_name, exclude)
        ):
            yield _name


def has_correct_length(length_range, start, end):
    """Determine if the line under test is within the desired docstring length.

    This function is used with the --docstring-length min_rows max_rows
    argument.

    Parameters
    ----------
    length_range: list
        The file row range passed to the --docstring-length argument.
    start: int
        The row number where the line under test begins in the source file.
    end: int
        The row number where the line under tests ends in the source file.

    Returns
    -------
    correct_length: bool
        True if the docstring has the correct length or length range is None,
        otherwise False
    """
    if length_range is None:
        return True
    min_length, max_length = length_range

    docstring_length = end + 1 - start
    return min_length <= docstring_length <= max_length


def is_in_range(line_range, start, end):
    """Determine if ??? is within the desired range.

    This function is used with the --range start_row end_row argument.

    Parameters
    ----------
    line_range: list
        The line number range passed to the --range argument.
    start: int
        The row number where the line under test begins in the source file.
    end: int
        The row number where the line under tests ends in the source file.

    Returns
    -------
    in_range : bool
        True if in range or range is None, else False
    """
    if line_range is None:
        return True
    return any(
        line_range[0] <= line_no <= line_range[1] for line_no in range(start, end + 1)
    )


def prefer_field_over_url(
    field_idx: List[Tuple[int, int]],
    url_idx: List[Tuple[int, int]],
):
    """Remove URL indices that overlap with field list indices.

    Parameters
    ----------
    field_idx : list
        The list of field list index tuples.
    url_idx : list
        The list of URL index tuples.

    Returns
    -------
    url_idx : list
        The url_idx list with any tuples that have indices overlapping with field
        list indices removed.
    """
    if not field_idx:
        return url_idx

    nonoverlapping_urls = []

    any_param_start = min(e[0] for e in field_idx)
    for _key, _value in enumerate(url_idx):
        if _value[1] < any_param_start:
            nonoverlapping_urls.append(_value)
    return nonoverlapping_urls
