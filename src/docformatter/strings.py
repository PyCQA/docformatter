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
"""This module provides docformatter string functions."""


# Standard Library Imports
import contextlib
import re
from typing import List, Match, Optional, Union


def find_shortest_indentation(lines: List[str]) -> str:
    """Determine the shortest indentation in a list of lines.

    Parameters
    ----------
    lines : list
        A list of lines to check indentation.

    Returns
    -------
    indentation : str
        The shortest (smallest number of spaces) indentation in the list of
        lines.
    """
    assert not isinstance(lines, str)

    indentation = None

    for line in lines:
        if line.strip():
            non_whitespace_index = len(line) - len(line.lstrip())
            _indent = line[:non_whitespace_index]
            if indentation is None or len(_indent) < len(indentation):
                indentation = _indent

    return indentation or ""


def is_probably_beginning_of_sentence(line: str) -> Union[Match[str], None, bool]:
    """Determine if the line begins a sentence.

    Parameters
    ----------
    line : str
        The line to be tested.

    Returns
    -------
    is_beginning : bool
        True if this token is the beginning of a sentence.
    """
    # Check heuristically for a parameter list.
    for token in ["@", "-", r"\*"]:
        if re.search(rf"\s{token}\s", line):
            return True

    stripped_line = line.strip()
    is_beginning_of_sentence = re.match(r"^[-@\)]", stripped_line)
    is_pydoc_ref = re.match(r"^:\w+:", stripped_line)

    return is_beginning_of_sentence and not is_pydoc_ref


def normalize_line(line: str, newline: str) -> str:
    """Return line with fixed ending, if ending was present in line.

    Otherwise, does nothing.

    Parameters
    ----------
    line : str
        The line to normalize.
    newline : str
        The newline character to use for line endings.

    Returns
    -------
    normalized_line : str
        The supplied line with line endings replaced by the newline.
    """
    stripped = line.rstrip("\n\r")
    return stripped + newline if stripped != line else line


def normalize_line_endings(lines, newline):
    """Return fixed line endings.

    All lines will be modified to use the most common line ending.
    """
    return "".join([normalize_line(line, newline) for line in lines])


def normalize_summary(summary: str, noncap: Optional[List[str]] = None) -> str:
    """Return normalized docstring summary.

    A normalized docstring summary will have the first word capitalized and
    a period at the end.

    Parameters
    ----------
    summary : str
        The summary string.
    noncap : list
        A user-provided list of words not to capitalize when they appear as
        the first word in the summary.

    Returns
    -------
    summary : str
        The normalized summary string.
    """
    if noncap is None:
        noncap = []

    # Remove trailing whitespace
    summary = summary.rstrip()

    # Add period at end of sentence.
    if (
        summary
        and (summary[-1].isalnum() or summary[-1] in ['"', "'"])
        and (not summary.startswith("#"))
    ):
        summary += "."

    with contextlib.suppress(IndexError):
        # Look for underscores, periods in the first word, this would typically
        # indicate the first word is a variable name, file name, or some other
        # non-standard English word.  The search the list of user-defined
        # words not to capitalize.  If none of these exist capitalize the
        # first word of the summary.
        if (
            all(char not in summary.split(" ", 1)[0] for char in ["_", "."])
            and summary.split(" ", 1)[0] not in noncap
        ):
            summary = summary[0].upper() + summary[1:]

    return summary


def split_first_sentence(text):
    """Split text into first sentence and the rest.

    Return a tuple (sentence, rest).
    """
    sentence = ""
    rest = text
    delimiter = ""
    previous_delimiter = ""

    while rest:
        split = re.split(r"(\s)", rest, maxsplit=1)
        word = split[0]
        if len(split) == 3:  # noqa PLR2004
            delimiter = split[1]
            rest = split[2]
        else:
            assert len(split) == 1
            delimiter = ""
            rest = ""

        sentence += previous_delimiter + word

        if sentence.endswith(("e.g.", "i.e.", "Dr.", "Mr.", "Mrs.", "Ms.")):
            # Ignore false end of sentence.
            pass
        elif sentence.endswith((".", "?", "!")):
            break
        elif sentence.endswith(":") and delimiter == "\n":
            # Break on colon if it ends the line. This is a heuristic to detect
            # the beginning of some parameter list afterwards.
            break

        previous_delimiter = delimiter
        delimiter = ""

    return sentence, delimiter + rest


def split_summary_and_description(contents):
    """Split docstring into summary and description.

    Return tuple (summary, description).
    """
    split_lines = contents.rstrip().splitlines()

    for index in range(1, len(split_lines)):
        # Empty line separation would indicate the rest is the description or
        # symbol on second line probably is a description with a list.
        if not split_lines[index].strip() or (
            index + 1 < len(split_lines)
            and is_probably_beginning_of_sentence(split_lines[index + 1])
        ):
            return (
                "\n".join(split_lines[:index]).strip(),
                "\n".join(split_lines[index:]).rstrip(),
            )

    # Break on first sentence.
    split = split_first_sentence(contents)
    if split[0].strip() and split[1].strip():
        return (
            split[0].strip(),
            find_shortest_indentation(split[1].splitlines()[1:]) + split[1].strip(),
        )

    return contents, ""
