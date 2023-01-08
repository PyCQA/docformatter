#!/usr/bin/env python
#
# Copyright (C) 2012-2022 Steven Myint
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
from typing import List

HEURISTIC_MIN_LIST_ASPECT_RATIO = 0.4


def description_to_list(
    text: str, indentation: str, wrap_length: int
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
    lines : list
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
    lines = []
    for _line in text.splitlines():
        _text = textwrap.wrap(
            textwrap.dedent(_line),
            width=wrap_length,
            initial_indent=indentation,
            subsequent_indent=indentation,
        )
        if _text:
            lines.extend(_text)
        else:
            lines.append("")
    return lines


def do_preserve_links(
    text: str,
    indentation: str,
    wrap_length: int,
) -> List[str]:
    """Rebuild links in docstring.

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
    lines = description_to_list(text, indentation, wrap_length)

    # There is nothing to do if the input wasn't wrapped.
    if len(lines) < 2:
        return lines

    url = is_some_sort_of_link(lines)

    if url != "":
        url_idx = lines.index(url)

        # Is this an in-line link (i.e., enclosed in <>)?  We want to keep
        # the '<' and '>' part of the link.
        if re.search(r"<", url):
            if len(url.split(sep="<")[0].strip()) > 0:
                lines[url_idx] = (
                    f"{indentation}" + url.split(sep="<")[0].strip()
                )

            url = f"{indentation}<" + url.split(sep="<")[1]
            if len(url.split(sep=">")) < 2:
                url = url + lines[url_idx + 1].strip()
                lines[url_idx + 1] = url

        # Is this a link target definition (i.e., .. a link: https://)?  We
        # want to keep the .. a link: on the same line as the url.
        elif re.search(r"(\.\. )", url):
            url = url + lines[url_idx + 1].strip()
            lines[url_idx] = url
            lines.pop(url_idx + 1)

        # Is this a simple link (i.e., just a link in the text) that should
        # be unwrapped?  We want to break the url out from the rest of the
        # text.
        elif len(lines[url_idx]) >= wrap_length:
            lines[url_idx] = (
                f"{indentation}" + url.strip().split(sep=" ")[0].strip()
            )
            url = f"{indentation}" + url.strip().split(sep=" ")[1].strip()
            url = url + lines[url_idx + 1].strip().split(sep=" ")[0].strip()
            lines.append(
                indentation
                + " ".join(lines[url_idx + 1].strip().split(sep=" ")[1:])
            )
            lines[url_idx + 1] = url

        with contextlib.suppress(IndexError):
            if lines[url_idx + 2].strip() in [".", "?", "!", ";"] or re.search(
                r">", lines[url_idx + 2]
            ):
                url = url + lines[url_idx + 2].strip()
                lines[url_idx + 1] = url
                lines.pop(url_idx + 2)

    return lines


def is_some_sort_of_link(lines: List[str]) -> str:
    """Determine if docstring line contains a link.

    URL patterns based on table at
    <https://en.wikipedia.org/wiki/List_of_URI_schemes>

    Parameters
    ----------
    lines: str
        the list of docstring lines to check for a link pattern.

    Returns
    -------
    url: str
        the line with the url pattern.
    """
    url_patterns = (
        "("
        "afp://|"
        "apt:|"
        "bitcoin:|"
        "chrome://|"
        "cvs://|"
        "dav://|"
        "dns:|"
        "file://|"
        "finger://|"
        "fish://|"
        "ftp://|"
        "ftps://|"
        "git://|"
        "http://|"
        "https://|"
        "imap://|"
        "ipp://|"
        "ipps://|"
        "irc://|"
        "irc6://|"
        "ircs://|"
        "jar:|"
        "ldap://|"
        "ldaps://|"
        "mailto:|"
        "news:|"
        "nfs://|"
        "nntp://|"
        "pop://|"
        "rsync://|"
        "s3://|"
        "sftp://|"
        "shttp://|"
        "sip:|"
        "sips:|"
        "smb://|"
        "sms:|"
        "snmp://|"
        "ssh://|"
        "svn://|"
        "telnet://|"
        "vnc://|"
        "xmpp:|"
        "xri://"
        ")"
    )

    return next(
        (line for line in lines if re.search(rf"<?{url_patterns}", line)),
        "",
    )


# pylint: disable=line-too-long
def is_some_sort_of_list(text, strict) -> bool:
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
            # re.match(r"\s*$", line)
            # or
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
        len(word) > 50
        and not re.match(r"<{0,1}(http:|https:|ftp:|sftp:)", word)
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
        and (is_some_sort_of_code(text) or is_some_sort_of_list(text, strict))
    ):
        return text

    text = do_preserve_links(text, indentation, wrap_length)

    return indentation + "\n".join(text).strip()
