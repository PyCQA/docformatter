#!/usr/bin/env python
#
#       docformatter.constants.py is part of the docformatter project
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
"""This module provides docformatter's constants."""


# TODO: Move these constants to the configuration file and/or command line.
ABBREVIATIONS = (
    "e.g.",
    "i.e.",
    "et. al.",
    "etc.",
    "Dr.",
    "Mr.",
    "Mrs.",
    "Ms.",
)

ALEMBIC_REGEX = r"^(Revision ID|Revises|Create Date): {0,}"
"""Regular expression to use for finding alembic headers."""

BULLET_REGEX = r"\s*[*\-+] [\S ]+"
"""Regular expression to use for finding bullet lists."""

CODE_PATTERN_REGEX = (
    r"^ {0,}(assert|async|await|break|class|continue|def|del|do|elif|else|except|"
    r"finally|for|global|if|import|lambda|pass|print|raise|return|super|try|while|"
    r"with|yield)"
)
"""Regular expression to use for finding code patterns."""

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

NUMPY_SECTION_REGEX = (
    r"^ *?(Parameters|Other Parameters|Returns|Raises|See "
    r"Also|Notes|Examples|References|Yields|Warns|Warnings|Receives)\n[- ]+"
)
"""Regular expression to use for finding Numpy section headers."""

OPTION_REGEX = r"^ {0,}-{1,2}[\S ]+ \w+"
"""Regular expression to use for finding option lists."""

REST_SECTION_REGEX = (
    r"(^ *[#\*=\-^\'\"\+_\~`\.\:]+\n)?[\w ]+\n *[#\*=\-^\'\"\+_\~`\.\:]+"
)
"""Regular expression to use for finding reST section headers."""

# Complete list:
# https://www.sphinx-doc.org/en/master/usage/domains/python.html#info-field-lists
SPHINX_FIELD_PATTERNS = (
    "arg|"
    "cvar|"
    "except|"
    "ivar|"
    "key|"
    "meta|"
    "param|"
    "raise|"
    "return|"
    "rtype|"
    "type|"
    "var|"
    "yield"
)

SPHINX_REGEX = rf":({SPHINX_FIELD_PATTERNS})[a-zA-Z0-9_\-.() ]*:"
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

Based on the table at
<https://en.wikipedia.org/wiki/List_of_URI_schemes>
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

# Keep these constants as constants.
MAX_PYTHON_VERSION = (3, 11)

DEFAULT_INDENT = 4
"""The default indentation for docformatter."""

HEURISTIC_MIN_LIST_ASPECT_RATIO = 0.4
"""The minimum aspect ratio to consider a list."""

STR_QUOTE_TYPES = (
    '"""',
    "'''",
)
RAW_QUOTE_TYPES = (
    'r"""',
    'R"""',
    "r'''",
    "R'''",
)
UCODE_QUOTE_TYPES = (
    'u"""',
    'U"""',
    "u'''",
    "U'''",
)
QUOTE_TYPES = STR_QUOTE_TYPES + RAW_QUOTE_TYPES + UCODE_QUOTE_TYPES
