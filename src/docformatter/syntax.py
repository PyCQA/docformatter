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
"""This module provides docformatter's Syntaxor class."""


# Standard Library Imports
import contextlib
import re
import textwrap
from typing import Iterable, List, Tuple, Union

REST_REGEX = r"(\.{2}|``) ?[\w-]+(:{1,2}|``)?"
"""The regular expression to use for finding reST directives."""

URL_PATTERNS = (
    "afp|"
    "apt|"
    "bitcoin|"
    "chrome|"
    "cvs|"
    "dav|"
    "dns|"
    "file|"
    "finger|"
    "fish|"
    "ftp|"
    "ftps|"
    "git|"
    "http|"
    "https|"
    "imap|"
    "ipp|"
    "ipps|"
    "irc|"
    "irc6|"
    "ircs|"
    "jar|"
    "ldap|"
    "ldaps|"
    "mailto|"
    "news|"
    "nfs|"
    "nntp|"
    "pop|"
    "rsync|"
    "s3|"
    "sftp|"
    "shttp|"
    "sip|"
    "sips|"
    "smb|"
    "sms|"
    "snmp|"
    "ssh|"
    "svn|"
    "telnet|"
    "vnc|"
    "xmpp|"
    "xri"
)
"""The URL patterns to look for when finding links.

Based on the table at
<https://en.wikipedia.org/wiki/List_of_URI_schemes>
"""

# This is the regex used to find URL links:
#
# (`{{2}}|`\w[\w. :\n]*|\.\. _?[\w. :]+|')? is used to find in-line links that
# should remain on a single line even if it exceeds the wrap length.
#   `{{2}} is used to find two back-tick characters.
#   This finds patterns like: ``http://www.example.com``
#
#   `\w[\w. :#\n]* matches the back-tick character immediately followed by one
#   letter, then followed by any number of letters, periods, spaces, colons,
#   hash marks or newlines.
#   This finds patterns like: `Link text <https://domain.invalid/>`_
#
#   \.\. _?[\w. :]+ matches the pattern .. followed one space, then by zero or
#   one underscore, then any number of letters, periods, spaces, or colons.
#   This finds patterns like: .. _a link: https://domain.invalid/
#
#   ' matches a single quote.
#   This finds patterns like: 'http://www.example.com'
#
#   ? matches the previous pattern between zero or one times.
#
# <?({URL_PATTERNS}):(//)?(\S*)>? is used to find the actual link.
#   <? matches the character < between zero and one times.
#   ({URL_PATTERNS}) matches one of the strings in the variable
#   URL_PATTERNS
#   : matches a colon.
#   (//)? matches two forward slashes zero or one time.
#   (\S*) matches any non-whitespace character between zero and infinity times.
#   >? matches the character > between zero and one times.
URL_REGEX = rf"(`{{2}}|`\w[\w. :#\n]*|\.\. _?[\w. :]+|')?<?({URL_PATTERNS}):(\
//)?(\S*)>?"

URL_SKIP_REGEX = rf"({URL_PATTERNS}):(/){{0,2}}(``|')"
"""The regex used to ignore found hyperlinks.

URLs that don't actually contain a domain, but only the URL pattern should
be treated like simple text. This will ignore URLs like ``http://`` or 'ftp:`.

({URL_PATTERNS}) matches one of the URL patterns.
:(/){{0,2}} matches a colon followed by up to two forward slashes.
(``|') matches a double back-tick or single quote.
"""

HEURISTIC_MIN_LIST_ASPECT_RATIO = 0.4


def description_to_list(
    text: str,
    indentation: str,
    wrap_length: int,
) -> List[str]:
    """Convert the description to a list of wrap length lines.

    Parameters
    ----------
    text : str
        The docstring description.
    indentation : str
        The indentation (number of spaces or tabs) to place in front of each
        line.
    wrap_length : int
        The column to wrap each line at.

    Returns
    -------
    _lines : list
        A list containing each line of the description with any links put
        back together.
    """
    # This is a description containing only one paragraph.
    if len(re.findall(r"\n\n", text)) <= 0:
        return textwrap.wrap(
            textwrap.dedent(text),
            width=wrap_length,
            initial_indent=indentation,
            subsequent_indent=indentation,
        )

    # This is a description containing multiple paragraphs.
    _lines = []
    for _line in text.split("\n\n"):
        _text = textwrap.wrap(
            textwrap.dedent(_line),
            width=wrap_length,
            initial_indent=indentation,
            subsequent_indent=indentation,
        )
        if _text:
            _lines.extend(_text)
        _lines.append("")

    return _lines


def do_clean_url(url: str, indentation: str) -> str:
    r"""Strip newlines and multiple whitespace from URL string.

    This function deals with situations such as:

    `Get\n
        Cookies.txt <https://chrome.google.com/webstore/detail/get-

    by returning:

    `Get Cookies.txt <https://chrome.google.com/webstore/detail/get-

    Parameters
    ----------
    url : str
        The URL that was found by the do_find_links() function and needs to be
        processed.
    indentation : str
        The indentation pattern used.

    Returns
    -------
    url : str
        The URL with internal newlines removed and excess whitespace removed.
    """
    _lines = url.splitlines()
    for _idx, _line in enumerate(_lines):
        if indentation != "" and _line[: len(indentation)] == indentation:
            _lines[_idx] = f" {_line.strip()}"

    return f'{indentation}{"".join(list(_lines))}'


def do_find_directives(text: str) -> bool:
    """Determine if docstring contains any reST directives.

    .. todo::

        Currently this function only returns True/False to indicate whether a
        reST directive was found.  Should return a list of tuples containing
        the start and end position of each reST directive found similar to the
        function do_find_links().

    Parameters
    ----------
    text : str
        The docstring text to test.

    Returns
    -------
    is_directive : bool
        Whether the docstring is a reST directive.
    """
    _rest_iter = re.finditer(REST_REGEX, text)
    return bool([(rest.start(0), rest.end(0)) for rest in _rest_iter])


def do_find_links(text: str) -> List[Tuple[int, int]]:
    r"""Determine if docstring contains any links.

    Parameters
    ----------
    text : str
        the docstring description to check for a link patterns.

    Returns
    -------
    url_index : list
        a list of tuples with each tuple containing the starting and ending
        position of each URL found in the passed description.
    """
    _url_iter = re.finditer(URL_REGEX, text)
    return [(_url.start(0), _url.end(0)) for _url in _url_iter]


def do_skip_link(text: str, index: Tuple[int, int]) -> bool:
    """Check if the identified URL is something other than a complete link.

    Is the identified link simply:
        1. The URL scheme pattern such as 's3://' or 'file://' or 'dns:'.
        2. The beginning of a URL link that has been wrapped by the user.

    Arguments
    ---------
    text : str
        The description text containing the link.
    index : tuple
        The index in the text of the starting and ending position of the
        identified link.

    Returns
    -------
    _do_skip : bool
        Whether to skip this link and simply treat it as a standard text word.
    """
    _do_skip = re.search(URL_SKIP_REGEX, text[index[0] : index[1]]) is not None

    with contextlib.suppress(IndexError):
        _do_skip = _do_skip or (
            text[index[0]] == "<" and text[index[1]] != ">"
        )

    return _do_skip


def do_split_description(
    text: str,
    indentation: str,
    wrap_length: int,
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

    Returns
    -------
    lines : list
        A list containing each line of the description with any links put
        back together.
    """
    # Check if the description contains any URLs.
    _url_idx = do_find_links(text)
    if not _url_idx:
        return description_to_list(
            text,
            indentation,
            wrap_length,
        )
    _lines = []
    _text_idx = 0
    for _idx in _url_idx:
        # Skip URL if it is simply a quoted pattern.
        if do_skip_link(text, _idx):
            continue

        # If the text including the URL is longer than the wrap length,
        # we need to split the description before the URL, wrap the pre-URL
        # text, and add the URL as a separate line.
        if len(text[_text_idx : _idx[1]]) > (wrap_length - len(indentation)):
            # Wrap everything in the description before the first URL.
            _lines.extend(
                description_to_list(
                    text[_text_idx : _idx[0]],
                    indentation,
                    wrap_length,
                )
            )

            # Add the URL.
            _lines.append(
                f"{do_clean_url(text[_idx[0] : _idx[1]], indentation)}"
            )

            _text_idx = _idx[1]

    # Finally, add everything after the last URL.
    with contextlib.suppress(IndexError):
        _stripped_text = (
            text[_text_idx + 1 :].strip(indentation)
            if text[_text_idx] == "\n"
            else text[_text_idx:].strip()
        )
        _lines.append(f"{indentation}{_stripped_text}")
    return _lines


# pylint: disable=line-too-long
def is_some_sort_of_list(text: str, strict: bool) -> bool:
    """Determine if docstring is a reST list.

    Notes
    -----
    There are five types of lists in reST/docutils that need to be handled.

    * `Bullets lists
    <https://docutils.sourceforge.io/docs/user/rst/quickref.html#bullet-lists>`_
    * `Enumerated lists
     <https://docutils.sourceforge.io/docs/user/rst/quickref.html#enumerated-lists>`_
    * `Definition lists
     <https://docutils.sourceforge.io/docs/user/rst/quickref.html#definition-lists>`_
    * `Field lists
     <https://docutils.sourceforge.io/docs/user/rst/quickref.html#field-lists>`_
    * `Option lists
     <https://docutils.sourceforge.io/docs/user/rst/quickref.html#option-lists>`_
    """
    split_lines = text.rstrip().splitlines()

    # TODO: Find a better way of doing this.
    # Very large number of lines but short columns probably means a list of
    # items.
    if (
        len(split_lines)
        / max([len(line.strip()) for line in split_lines] + [1])
        > HEURISTIC_MIN_LIST_ASPECT_RATIO
    ) and not strict:
        return True

    return any(
        (
            # "1. item"
            re.match(r"\s*\d\.", line)
            or
            # "@parameter"
            re.match(r"\s*[\-*:=@]", line)
            or
            # "parameter - description"
            re.match(r".*\s+[\-*:=@]\s+", line)
            or
            # "parameter: description"
            re.match(r"\s*\S+[\-*:=@]\s+", line)
            or
            # "parameter:\n    description"
            re.match(r"\s*\S+:\s*$", line)
            or
            # "parameter -- description"
            re.match(r"\s*\S+\s+--\s+", line)
        )
        for line in split_lines
    )


def is_some_sort_of_code(text: str) -> bool:
    """Return True if text looks like code."""
    return any(
        len(word) > 50 and not re.match(URL_REGEX, word)
        for word in text.split()
    )


def reindent(text, indentation):
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


def remove_section_header(text):
    r"""Return text with section header removed.

    >>> remove_section_header('----\nfoo\nbar\n')
    'foo\nbar\n'

    >>> remove_section_header('===\nfoo\nbar\n')
    'foo\nbar\n'
    """
    stripped = text.lstrip()
    if not stripped:
        return text

    first = stripped[0]
    return (
        text
        if (
            first.isalnum()
            or first.isspace()
            or stripped.splitlines()[0].strip(first).strip()
        )
        else stripped.lstrip(first).lstrip()
    )


def strip_leading_blank_lines(text):
    """Return text with leading blank lines removed."""
    split = text.splitlines()

    found = next(
        (index for index, line in enumerate(split) if line.strip()), 0
    )

    return "\n".join(split[found:])


def unwrap_summary(summary):
    """Return summary with newlines removed in preparation for wrapping."""
    return re.sub(r"\s*\n\s*", " ", summary)


def wrap_summary(summary, initial_indent, subsequent_indent, wrap_length):
    """Return line-wrapped summary text."""
    if wrap_length > 0:
        return textwrap.fill(
            unwrap_summary(summary),
            width=wrap_length,
            initial_indent=initial_indent,
            subsequent_indent=subsequent_indent,
        ).strip()
    else:
        return summary


def wrap_description(text, indentation, wrap_length, force_wrap, strict):
    """Return line-wrapped description text.

    We only wrap simple descriptions. We leave doctests, multi-paragraph
    text, and bulleted lists alone.
    """
    text = strip_leading_blank_lines(text)

    # Do not modify doctests at all.
    if ">>>" in text:
        return text

    text = reindent(text, indentation).rstrip()

    # Ignore possibly complicated cases.
    if wrap_length <= 0 or (
        not force_wrap
        and (
            is_some_sort_of_code(text)
            or do_find_directives(text)
            or is_some_sort_of_list(text, strict)
        )
    ):
        return text

    lines = do_split_description(text, indentation, wrap_length)

    return indentation + "\n".join(lines).strip()
