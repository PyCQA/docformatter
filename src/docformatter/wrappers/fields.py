#!/usr/bin/env python
#
#       docformatter.wrappers.fields.py is part of the docformatter project
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
"""This module provides docformatter's field list wrapper functions."""

# Standard Library Imports
import re
import textwrap
from typing import List, Optional, Tuple

# docformatter Package Imports
import docformatter.patterns as _patterns
import docformatter.strings as _strings
from docformatter.constants import DEFAULT_INDENT, GOOGLE_WRAPPABLE_SECTIONS


def do_wrap_field_lists(  # noqa: PLR0913
    text: str,
    field_idx: List[Tuple[int, int]],
    lines: List[str],
    text_idx: int,
    indentation: str,
    wrap_length: int,
) -> Tuple[List[str], int]:
    """Wrap field lists in the long description.

    Parameters
    ----------
    text : str
        The long description text.
    field_idx : list
        The list of field list indices found in the description text.
    lines : list
        The list of formatted lines in the description that come before the
        first parameter list item.
    text_idx : int
        The index in the description of the end of the last parameter list
        item.
    indentation : str
        The string to use to indent each line in the long description.
    wrap_length : int
         The line length at which to wrap long lines in the description.

    Returns
    -------
    lines, text_idx : tuple
         A list of the long description lines and the index in the long
        description where the last parameter list item ended.
    """
    lines.extend(
        _strings.description_to_list(
            text[text_idx : field_idx[0][0]],
            indentation,
            wrap_length,
        )
    )

    for _idx, _field_idx in enumerate(field_idx):
        _field_name = text[_field_idx[0] : _field_idx[1]]
        _field_body = _do_join_field_body(
            text,
            field_idx,
            _idx,
        )

        if len(f"{_field_name}{_field_body}") <= (wrap_length - len(indentation)):
            _field = f"{_field_name}{_field_body}"
            lines.append(f"{indentation}{_field}")
        else:
            lines.extend(
                _do_wrap_field(_field_name, _field_body, indentation, wrap_length)
            )

        text_idx = _field_idx[1]

    return lines, text_idx


def _do_join_field_body(text: str, field_idx: list[tuple[int, int]], idx: int) -> str:
    """Join the filed body lines into a single line that can be wrapped.

    Parameters
    ----------
    text : str
        The docstring long description text that contains field lists.
    field_idx : list
        The list of tuples containing the found field list start and end position.
    idx : int
        The index of the tuple in the field_idx list to extract the field body.

    Returns
    -------
    _field_body : str
        The field body collapsed into a single line.
    """
    try:
        _field_body = text[field_idx[idx][1] : field_idx[idx + 1][0]].strip()
    except IndexError:
        _field_body = text[field_idx[idx][1] :].strip()

    _field_body = " ".join(
        [_line.strip() for _line in _field_body.splitlines()]
    ).strip()

    # Add a space before the field body unless the field body is a link.
    if not _field_body.startswith("`") and _field_body:
        _field_body = f" {_field_body}"

    # Is there a blank line between field lists?  Keep it if so.
    if text[field_idx[idx][1] : field_idx[idx][1] + 2] == "\n\n":
        _field_body = "\n"

    return _field_body


def _do_wrap_field(field_name, field_body, indentation, wrap_length):
    """Wrap complete field at wrap_length characters.

    Parameters
    ----------
    field_name : str
        The name text of the field.
    field_body : str
        The body text of the field.
    indentation : str
        The string to use for indentation of the first line in the field.
    wrap_length : int
        The number of characters at which to wrap the field.

    Returns
    -------
    _wrapped_field : str
        The field wrapped at wrap_length characters.
    """
    if len(indentation) > DEFAULT_INDENT:
        _subsequent = indentation + int(0.5 * len(indentation)) * " "
    else:
        _subsequent = 2 * indentation

    _wrapped_field = textwrap.wrap(
        textwrap.dedent(f"{field_name}{field_body}"),
        width=wrap_length,
        initial_indent=indentation,
        subsequent_indent=_subsequent,
    )

    for _idx, _field in enumerate(_wrapped_field):
        _indent = indentation if _idx == 0 else _subsequent
        _wrapped_field[_idx] = f"{_indent}{re.sub(' +', ' ', _field.strip())}"

    return _wrapped_field


def do_wrap_google_description(
    text: str,
    indentation: str,
    wrap_length: int,
) -> List[str]:
    """Wrap prose and Google-style Args/Returns entries independently.

    Parameters
    ----------
    text : str
        The description text, already reindented to ``indentation``.
    indentation : str
        The indentation to place in front of each description line.
    wrap_length : int
        The column at which to wrap long lines.

    Returns
    -------
    list[str]
        The wrapped description lines, each including ``indentation``.
    """
    _headers = _patterns.do_find_google_section_headers(text)
    if not _headers:
        return _strings.description_to_list(text, indentation, wrap_length)

    _lines: List[str] = []
    _first_start = _headers[0][0]
    _prose = text[:_first_start]
    if _prose.strip():
        _lines = _strings.description_to_list(
            _prose,
            indentation,
            wrap_length,
        )
        while _lines and not _lines[-1]:
            _lines.pop()

    for _idx, (_start, _body_start, _name) in enumerate(_headers):
        _section_end = _headers[_idx + 1][0] if _idx + 1 < len(_headers) else len(text)
        _body = text[_body_start:_section_end]

        if _lines:
            _lines.append("")
        _header_line = text[_start:_body_start].splitlines()[0].rstrip()
        _lines.append(_header_line)

        if _name.lower() in GOOGLE_WRAPPABLE_SECTIONS:
            _lines.extend(
                _do_wrap_google_section_body(
                    _body,
                    indentation,
                    wrap_length,
                )
            )
        else:
            _lines.extend(_do_preserve_section_body(_body))

    while _lines and not _lines[-1]:
        _lines.pop()

    return _lines


def _do_wrap_google_section_body(
    body: str,
    indentation: str,
    wrap_length: int,
) -> List[str]:
    """Wrap each parsed Google section entry at wrap_length."""
    _lines: List[str] = []
    for _name, _type_hint, _description in _patterns.do_parse_google_entries(body):
        _lines.extend(
            _do_wrap_google_entry(
                _name,
                _type_hint,
                _description,
                indentation,
                wrap_length,
            )
        )
    return _lines


def _do_wrap_google_entry(  # noqa: PLR0913
    name: Optional[str],
    type_hint: Optional[str],
    description: str,
    indentation: str,
    wrap_length: int,
) -> List[str]:
    """Wrap one Google Args/Returns entry with hanging continuation indent."""
    _entry_indent = indentation + DEFAULT_INDENT * " "

    if name is None:
        if not description:
            return []
        return textwrap.wrap(
            description,
            width=wrap_length,
            initial_indent=_entry_indent,
            subsequent_indent=_entry_indent,
        )

    _type_part = f" ({type_hint})" if type_hint else ""
    _prefix = f"{name}{_type_part}: "
    _text = f"{_prefix}{description}".rstrip()
    _continuation = indentation + (2 * DEFAULT_INDENT) * " "

    _wrapped = textwrap.wrap(
        _text,
        width=wrap_length,
        initial_indent=_entry_indent,
        subsequent_indent=_continuation,
    )
    return _wrapped or [f"{_entry_indent}{_text}"]


def _do_preserve_section_body(body: str) -> List[str]:
    """Return a non-wrappable Google section body with original lines."""
    _lines: List[str] = []
    for _line in body.splitlines():
        if _line.strip():
            _lines.append(_line.rstrip())
        elif _lines and _lines[-1]:
            _lines.append("")
    while _lines and not _lines[-1]:
        _lines.pop()
    return _lines
