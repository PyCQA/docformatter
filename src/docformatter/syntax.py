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
"""This module provides docformatter's syntax functions."""


# Standard Library Imports
import contextlib
import re
import textwrap
from typing import Iterable, List, Tuple, Union

DEFAULT_INDENT = 4

ALEMBIC_REGEX = r"^ *[a-zA-Z0-9_\- ]*: "
"""Regular expression to use for finding alembic headers."""

BULLET_REGEX = r"\s*[*\-+] [\S ]+"
"""Regular expression to use for finding bullet lists."""

ENUM_REGEX = r"\s*\d\."
"""Regular expression to use for finding enumerated lists."""

EPYTEXT_REGEX = r"@[a-zA-Z0-9_\-\s]+:"
"""Regular expression to use for finding Epytext-style field lists."""

GOOGLE_REGEX = r"^ *[a-zA-Z0-9_\- ]*:$"
"""Regular expression to use for finding Google-style field lists."""

LITERAL_REGEX = r"[\S ]*::"
"""Regular expression to use for finding literal blocks."""

NUMPY_REGEX = r"^\s[a-zA-Z0-9_\- ]+ ?: [\S ]+"
"""Regular expression to use for finding Numpy-style field lists."""

OPTION_REGEX = r"^-{1,2}[\S ]+ {2}\S+"
"""Regular expression to use for finding option lists."""

REST_REGEX = r"((\.{2}|`{2}) ?[\w.~-]+(:{2}|`{2})?[\w ]*?|`[\w.~]+`)"
"""Regular expression to use for finding reST directives."""

SPHINX_REGEX = r":(param|raises|return|rtype|type|yield)[a-zA-Z0-9_\-.() ]*:"
"""Regular expression to use for finding Sphinx-style field lists."""

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

Based on the table at <https://en.wikipedia.org/wiki/List_of_URI_schemes>
"""

# This is the regex used to find URL links:
#
# (__ |`{{2}}|`\w[\w. :\n]*|\.\. _?[\w. :]+|')? is used to find in-line links that
# should remain on a single line even if it exceeds the wrap length.
#   __ is used to find to underscores followed by a single space.
#   This finds patterns like: __ https://sw.kovidgoyal.net/kitty/graphics-protocol/
#
#   `{{2}} is used to find two back-tick characters.
#   This finds patterns like: ``http://www.example.com``
#
#   `\w[a-zA-Z0-9. :#\n]* matches the back-tick character immediately followed by one
#   letter, then followed by any number of letters, numbers, periods, spaces, colons,
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
URL_REGEX = (
    rf"(__ |`{{2}}|`\w[\w :#\n]*[.|\.\. _?[\w. :]+|')?<?"
    rf"({URL_PATTERNS}):(\//)?(\S*)>?"
)

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


def do_clean_url(url: str, indentation: str) -> str:
    r"""Strip newlines and multiple whitespace from URL string.

    This function deals with situations such as:

    `Get\n     Cookies.txt <https://chrome.google.com/webstore/detail/get-

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
        if indentation and _line[: len(indentation)] == indentation:
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
    return bool([(_rest.start(0), _rest.end(0)) for _rest in _rest_iter])


def do_find_field_lists(
    text: str,
    style: str,
):
    r"""Determine if docstring contains any field lists.

    Parameters
    ----------
    text : str
        The docstring description to check for field list patterns.
    style : str
        The field list style used.

    Returns
    -------
    _field_idx, _wrap_parameters : tuple
        A list of tuples with each tuple containing the starting and ending
        position of each field list found in the passed description.
        A boolean indicating whether long field list lines should be wrapped.
    """
    _field_idx = []
    _wrap_parameters = False

    if style == "epytext":
        _field_idx = [
            (_field.start(0), _field.end(0))
            for _field in re.finditer(EPYTEXT_REGEX, text)
        ]
        _wrap_parameters = True
    elif style == "sphinx":
        _field_idx = [
            (_field.start(0), _field.end(0))
            for _field in re.finditer(SPHINX_REGEX, text)
        ]
        _wrap_parameters = True

    return _field_idx, _wrap_parameters


def do_find_links(text: str) -> List[Tuple[int, int]]:
    r"""Determine if docstring contains any links.

    Parameters
    ----------
    text : str
        The docstring description to check for link patterns.

    Returns
    -------
    url_index : list
        A list of tuples with each tuple containing the starting and ending
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
        _do_skip = _do_skip or (text[index[0]] == "<" and text[index[1]] != ">")

    return _do_skip


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
    _url_idx = do_find_links(text)

    # Check if the description contains any field lists.
    _field_idx, _wrap_fields = do_find_field_lists(
        text,
        style,
    )

    # Field list wrapping takes precedence over URL wrapping.
    _url_idx = _field_over_url(
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
        _lines, _text_idx = do_wrap_urls(
            text,
            _url_idx,
            0,
            indentation,
            wrap_length,
        )

    if _field_idx:
        _lines, _text_idx = do_wrap_field_lists(
            text,
            _field_idx,
            _lines,
            _text_idx,
            indentation,
            wrap_length,
        )
    else:
        # Finally, add everything after the last URL or field list directive.
        _lines += _do_close_description(text, _text_idx, indentation)

    return _lines


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
        description_to_list(
            text[text_idx : field_idx[0][0]],
            indentation,
            wrap_length,
        )
    )

    for _idx, __ in enumerate(field_idx):
        _field_name = text[field_idx[_idx][0] : field_idx[_idx][1]]
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

        text_idx = field_idx[_idx][1]

    return lines, text_idx


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
        if do_skip_link(text, _url):
            continue

        # If the text including the URL is longer than the wrap length,
        # we need to split the description before the URL, wrap the pre-URL
        # text, and add the URL as a separate line.
        if len(text[text_idx : _url[1]]) > (wrap_length - len(indentation)):
            # Wrap everything in the description before the first URL.
            _lines.extend(
                description_to_list(
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

            _lines.append(f"{do_clean_url(_text, indentation)}")

            text_idx = _url[1]

    return _lines, text_idx


def is_some_sort_of_field_list(
    text: str,
    style: str,
) -> bool:
    """Determine if docstring contains field lists.

    Parameters
    ----------
    text : str
        The docstring text.
    style : str
        The field list style to use.

    Returns
    -------
    is_field_list : bool
        Whether the field list pattern for style was found in the docstring.
    """
    split_lines = text.rstrip().splitlines()

    if style == "epytext":
        return any(
            (
                # "@param x:" <-- Epytext style
                # "@type x:" <-- Epytext style
                re.match(EPYTEXT_REGEX, line)
            )
            for line in split_lines
        )
    elif style == "sphinx":
        return any(
            (
                # ":parameter: description" <-- Sphinx style
                re.match(SPHINX_REGEX, line)
            )
            for line in split_lines
        )

    return False


# pylint: disable=line-too-long
def is_some_sort_of_list(
    text: str,
    strict: bool,
    rest_sections: str,
    style: str,
) -> bool:
    """Determine if docstring is a reST list.

    Notes
    -----
    There are five types of lists in reST/docutils that need to be handled.

    * `Bullet lists
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
        len(split_lines) / max([len(line.strip()) for line in split_lines] + [1])
        > HEURISTIC_MIN_LIST_ASPECT_RATIO
    ) and not strict:
        return True

    if is_some_sort_of_field_list(text, style):
        return False

    return any(
        (
            # "* parameter" <-- Bullet list
            # "- parameter" <-- Bullet list
            # "+ parameter" <-- Bullet list
            re.match(BULLET_REGEX, line)
            or
            # "1. item" <-- Enumerated list
            re.match(ENUM_REGEX, line)
            or
            # "====\ndescription\n====" <-- reST section
            # "----\ndescription\n----" <-- reST section
            # "description\n----" <-- reST section
            re.match(rest_sections, line)
            or
            # "-a  description" <-- Option list
            # "--long  description" <-- Option list
            re.match(OPTION_REGEX, line)
            or
            # "@param x:" <-- Epytext style
            # "@type x:" <-- Epytext style
            re.match(EPYTEXT_REGEX, line)
            or
            # ":parameter: description" <-- Sphinx style
            re.match(SPHINX_REGEX, line)
            or
            # "parameter : description" <-- Numpy style
            re.match(NUMPY_REGEX, line)
            or
            # "word\n----" <-- Numpy headings
            re.match(r"^\s*-+", line)
            or
            # "Args:" <-- Google style
            # "parameter:" <-- Google style
            re.match(GOOGLE_REGEX, line)
            or
            # "parameter - description"
            re.match(r"[\S ]+ - \S+", line)
            or
            # "parameter -- description"
            re.match(r"\s*\S+\s+--\s+", line)
            or
            # Literal block
            re.match(LITERAL_REGEX, line)
            or
            # "@parameter"
            re.match(r"^ *@[a-zA-Z0-9_\- ]*(?:(?!:).)*$", line)
            or
            # "    c :math:`[0, `]`.
            re.match(r" *\w *:[a-zA-Z0-9_\- ]*:", line)
            or
            # "Revision ID: <some id>>"
            # "Revises: <some other id>"
            # "Create Date: 2023-01-06 10:13:28.156709"
            re.match(ALEMBIC_REGEX, line)
        )
        for line in split_lines
    )


def is_some_sort_of_code(text: str) -> bool:
    """Return True if text looks like code."""
    return any(
        len(word) > 50 and not re.match(URL_REGEX, word)  # noqa: PLR2004
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

    found = next((index for index, line in enumerate(split) if line.strip()), 0)

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


def wrap_description(  # noqa: PLR0913
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
    description : str
        The description wrapped at wrap_length characters.
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
            or is_some_sort_of_list(text, strict, rest_sections, style)
        )
    ):
        return text

    lines = do_split_description(text, indentation, wrap_length, style)

    return indentation + "\n".join(lines).strip()


def _do_close_description(
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
    _split_lines : str
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


def _do_join_field_body(text, field_idx, idx):
    """Join the filed body lines into a single line that can be wrapped.

    Parameters
    ----------
    text : str
        The docstring long description text that contains field lists.
    field_idx : list
        The list of tuples containing the found field list start and end position.

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


def _field_over_url(
    field_idx: List[Tuple[int, int]],
    url_idx: List[Tuple[int, int]],
):
    """Remove URL indices that overlap with filed list indices.

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
    for _fieldl, _fieldu in field_idx:
        for _key, _value in enumerate(url_idx):
            if (
                _value[0] == _fieldl
                or _value[0] == _fieldu
                or _value[1] == _fieldl
                or _value[1] == _fieldu
            ):
                url_idx.pop(_key)

    return url_idx
