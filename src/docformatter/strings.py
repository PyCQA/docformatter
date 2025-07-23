#!/usr/bin/env python
#
#       docformatter.strings.py is part of the docformatter project
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
"""This module provides docformatter string manipulation functions."""


# Standard Library Imports
import contextlib
import re
import textwrap
from typing import Iterable, List, Optional, Tuple, Union

# docformatter Package Imports
import docformatter.patterns as _patterns
import docformatter.util as _util
import docformatter.wrappers as _wrappers
from docformatter.constants import (
    ABBREVIATIONS,
    QUOTE_TYPES,
    RAW_QUOTE_TYPES,
    UCODE_QUOTE_TYPES,
)


def description_to_list(
    description: str,
    indentation: str,
    wrap_length: int,
) -> List[str]:
    """Convert the description to a list of wrap length lines.

    Parameters
    ----------
    description : str
        The docstring description.
    indentation : str
        The indentation (number of spaces or tabs) to place in front of each
        line.
    wrap_length : int
        The column to wrap each line at.

    Returns
    -------
    _wrapped_lines : list
          A list containing each line of the description wrapped at wrap_length.
    """
    # This is a description containing only one paragraph.
    if len(re.findall(r"\n\n", description)) <= 0:
        return textwrap.wrap(
            textwrap.dedent(description),
            width=wrap_length,
            initial_indent=indentation,
            subsequent_indent=indentation,
        )

    # This is a description containing multiple paragraphs.
    _wrapped_lines = []
    for _line in description.split("\n\n"):
        _wrapped_line = textwrap.wrap(
            textwrap.dedent(_line),
            width=wrap_length,
            initial_indent=indentation,
            subsequent_indent=indentation,
        )

        if _wrapped_line:
            _wrapped_lines.extend(_wrapped_line)
        _wrapped_lines.append("")

        with contextlib.suppress(IndexError):
            if not _wrapped_lines[-1] and not _wrapped_lines[-2]:
                _wrapped_lines.pop(-1)

    if (
        description[-len(indentation) - 1 : -len(indentation)] == "\n"
        and description[-len(indentation) - 2 : -len(indentation)] != "\n\n"
    ):
        _wrapped_lines.pop(-1)

    return _wrapped_lines


def do_clean_excess_whitespace(text: str, indentation: str) -> str:
    r"""Strip newlines and multiple whitespace from a string.

    This function deals with situations such as:

    `Get\n     Cookies.txt <https://chrome.google.com/webstore/detail/get-

    by returning:
    `Get Cookies.txt <https://chrome.google.com/webstore/detail/get-

    Parameters
    ----------
    text : str
        The text that needs to be processed.
    indentation : str
       The indentation pattern used.
    Returns
    -------
    text : str
       The text with internal newlines removed and excess whitespace removed.
    """
    _lines = text.splitlines()

    for _idx, _line in enumerate(_lines):
        if indentation and _line[: len(indentation)] == indentation:
            _lines[_idx] = f" {_line.strip()}"

    return f'{indentation}{"".join(list(_lines))}'


def do_find_shortest_indentation(lines: List[str]) -> str:
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


def do_normalize_line(line: str, newline: str) -> str:
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


def do_normalize_line_endings(lines, newline):
    """Return fixed line endings.

    All lines will be modified to use the most common line ending.
    """
    return "".join([do_normalize_line(line, newline) for line in lines])


def do_normalize_summary(summary: str, noncap: Optional[List[str]] = None) -> str:
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


def do_reindent(text, indentation):
    """Return reindented text that matches indentation."""
    if "\t" not in indentation:
        text = text.expandtabs()

    text = textwrap.dedent(text)

    return (
        "\n".join(
            [(indentation + line).rstrip() for line in text.splitlines()]
        ).rstrip()
        + "\n"
    )


def do_split_description(
    text: str,
    indentation: str,
    wrap_length: int,
    style: str,
) -> Union[List[str], Iterable]:
    """Split the description into a list of lines.

    Parameters
    ----------
    text : str
        The docstring description.
    indentation : str
        The indentation (number of spaces or tabs) to place in front of each
        line.
    wrap_length : int
        The column to wrap each line at.
    style : str
        The docstring style to use for dealing with parameter lists.

    Returns
    -------
    _lines : list
        A list containing each line of the description with any links put
        back together.
    """
    _lines: List[str] = []
    _text_idx = 0

    # Check if the description contains any URLs.
    _url_idx = _patterns.do_find_links(text)

    # Check if the description contains any field lists.
    _field_idx, _wrap_fields = _patterns.do_find_field_lists(
        text,
        style,
    )

    # Field list wrapping takes precedence over URL wrapping.
    _url_idx = _util.prefer_field_over_url(
        _field_idx,
        _url_idx,
    )

    if not _url_idx and not (_field_idx and _wrap_fields):
        return description_to_list(
            text,
            indentation,
            wrap_length,
        )

    if _url_idx:
        _lines, _text_idx = _wrappers.do_wrap_urls(
            text,
            _url_idx,
            0,
            indentation,
            wrap_length,
        )

    if _field_idx:
        _lines, _text_idx = _wrappers.do_wrap_field_lists(
            text,
            _field_idx,
            _lines,
            _text_idx,
            indentation,
            wrap_length,
        )
    else:
        # Finally, add everything after the last URL or field list directive.
        _lines += _wrappers.do_close_description(text, _text_idx, indentation)

    return _lines


def do_split_first_sentence(text):
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

        if sentence.endswith(ABBREVIATIONS):
            # Ignore false end of sentence.
            pass
        elif sentence.endswith((".", "?", "!")):
            break
        elif sentence.endswith(":") and delimiter == "\n":
            # Break on colon if it ends the line. This is a heuristic to detect
            # the beginning of some parameter list after wards.
            break

        previous_delimiter = delimiter
        delimiter = ""

    return sentence, delimiter + rest


def do_split_summary(lines) -> List[str]:
    """Split multi-sentence summary into the first sentence and the rest."""
    if not lines or not lines[0].strip():
        return lines

    text = lines[0].strip()

    tokens = re.split(r"(\s+)", text)  # Keep whitespace for accurate rejoining
    sentence = []
    i = 0

    while i < len(tokens):
        token = tokens[i]
        sentence.append(token)

        if token.endswith(".") and not any(
            "".join(sentence).strip().endswith(abbr) for abbr in ABBREVIATIONS
        ):
            i += 1
            break

        i += 1

    rest = tokens[i:]
    first_sentence = "".join(sentence).strip()
    rest_text = "".join(rest).strip()

    lines[0] = first_sentence
    if rest_text:
        lines.insert(2, rest_text)

    return lines


def do_split_summary_and_description(contents):
    """Split docstring into summary and description.

    Return tuple (summary, description).
    """
    split_lines = contents.rstrip().splitlines()
    split_lines = do_split_summary(split_lines)

    for index in range(1, len(split_lines)):
        # Empty line separation would indicate the rest is the description or
        # symbol on second line probably is a description with a list.
        if not split_lines[index].strip() or (
            index + 1 < len(split_lines)
            and _patterns.is_probably_beginning_of_sentence(split_lines[index + 1])
        ):
            return (
                "\n".join(split_lines[:index]).strip(),
                "\n".join(split_lines[index:]).rstrip(),
            )

    # Break on first sentence.
    split = do_split_first_sentence(contents)
    if split[0].strip() and split[1].strip():
        return (
            split[0].strip(),
            do_find_shortest_indentation(split[1].splitlines()[1:]) + split[1].strip(),
        )

    return contents, ""


def do_strip_docstring(docstring: str) -> Tuple[str, str]:
    """Return contents of docstring and opening quote type.

    Strips the docstring of its triple quotes, trailing white space,
    and line returns.  Determine the type of docstring quote (either string,
    raw, or Unicode) and returns the opening quotes, including the type
    identifier, with single quotes replaced by double quotes.

    Parameters
    ----------
    docstring: str
        The docstring, including the opening and closing triple quotes.

    Returns
    -------
    (docstring, open_quote) : tuple
        The docstring with the triple quotes removed.
        The opening quote type with single quotes replaced by double
        quotes.
    """
    docstring = docstring.strip()

    for quote in QUOTE_TYPES:
        if quote in RAW_QUOTE_TYPES + UCODE_QUOTE_TYPES and (
            docstring.startswith(quote) and docstring.endswith(quote[1:])
        ):
            return docstring.split(quote, 1)[1].rsplit(quote[1:], 1)[
                0
            ].strip(), quote.replace("'", '"')
        elif docstring.startswith(quote) and docstring.endswith(quote):
            return docstring.split(quote, 1)[1].rsplit(quote, 1)[
                0
            ].strip(), quote.replace("'", '"')

    raise ValueError(
        "docformatter only handles triple-quoted (single or double) strings"
    )


def do_strip_leading_blank_lines(text):
    """Return text with leading blank lines removed."""
    split = text.splitlines()

    found = next((index for index, line in enumerate(split) if line.strip()), 0)

    return "\n".join(split[found:])
