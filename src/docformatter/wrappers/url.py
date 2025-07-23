#!/usr/bin/env python
#
#       docformatter.wrappers.url.py is part of the docformatter project
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
"""This module provides docformatter's URL wrapper functions."""


# Standard Library Imports
import contextlib
from typing import Iterable, List, Tuple

# docformatter Package Imports
import docformatter.patterns as _patterns
import docformatter.strings as _strings


def do_wrap_urls(
    text: str,
    url_idx: Iterable,
    text_idx: int,
    indentation: str,
    wrap_length: int,
) -> Tuple[List[str], int]:
    """Wrap URLs in the long description.

    Parameters
    ----------
    text : str
        The long description text.
    url_idx : list
        The list of URL indices found in the description text.
    text_idx : int
        The index in the description of the end of the last URL.
    indentation : str
        The string to use to indent each line in the long description.
    wrap_length : int
         The line length at which to wrap long lines in the description.

    Returns
    -------
    _lines, _text_idx : tuple
        A list of the long description lines and the index in the long
        description where the last URL ended.
    """
    _lines = []
    for _url in url_idx:
        # Skip URL if it is simply a quoted pattern.
        if _patterns.do_skip_link(text, _url):
            continue

        # If the text including the URL is longer than the wrap length,
        # we need to split the description before the URL, wrap the pre-URL
        # text, and add the URL as a separate line.
        if len(text[text_idx : _url[1]]) > (wrap_length - len(indentation)):
            # Wrap everything in the description before the first URL.
            _lines.extend(
                _strings.description_to_list(
                    text[text_idx : _url[0]],
                    indentation,
                    wrap_length,
                )
            )

            with contextlib.suppress(IndexError):
                if text[_url[0] - len(indentation) - 2] != "\n" and not _lines[-1]:
                    _lines.pop(-1)

            # Add the URL making sure that the leading quote is kept with a quoted URL.
            _text = f"{text[_url[0]: _url[1]]}"
            with contextlib.suppress(IndexError):
                if _lines[0][-1] == '"':
                    _lines[0] = _lines[0][:-2]
                    _text = f'"{text[_url[0] : _url[1]]}'

            _lines.append(f"{_strings.do_clean_excess_whitespace(_text, indentation)}")

            text_idx = _url[1]

    return _lines, text_idx
