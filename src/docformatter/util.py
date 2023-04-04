#!/usr/bin/env python
#
# Copyright (C) 2012-2023 Steven Myint
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

unicode = str

_PYTHON_LIBS = set(sysconfig.get_paths().values())


def find_py_files(sources, recursive, exclude=None):
    """Find Python source files.

    Parameters
        - sources: iterable with paths as strings.
        - recursive: drill down directories if True.
        - exclude: string based on which directories and files are excluded.

    Return: yields paths to found files.
    """
    def not_hidden(name):
        """Return True if file 'name' isn't .hidden."""
        return not name.startswith(".")

    def is_excluded(name, exclude):
        """Return True if file 'name' is excluded."""
        return (
            any(
                re.search(re.escape(str(e)), name, re.IGNORECASE)
                for e in exclude
            )
            if exclude
            else False
        )

    for name in sorted(sources):
        if recursive and os.path.isdir(name):
            for root, dirs, children in os.walk(unicode(name)):
                dirs[:] = [
                    d
                    for d in dirs
                    if not_hidden(d) and not is_excluded(d, _PYTHON_LIBS)
                ]
                dirs[:] = sorted(
                    [d for d in dirs if not is_excluded(d, exclude)]
                )
                files = sorted(
                    [
                        f
                        for f in children
                        if not_hidden(f) and not is_excluded(f, exclude)
                    ]
                )
                for filename in files:
                    if filename.endswith(".py") and not is_excluded(
                        root, exclude
                    ):
                        yield os.path.join(root, filename)
        else:
            yield name


def has_correct_length(length_range, start, end):
    """Determine if the line under test is within desired docstring length.

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
        True if is correct length or length range is None, else False
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
        line_range[0] <= line_no <= line_range[1]
        for line_no in range(start, end + 1)
    )
