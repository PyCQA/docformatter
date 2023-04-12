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
"""This module provides docformatter's Encoder class."""

# Standard Library Imports
import collections
import io
import locale
import sys
from typing import Dict, List

# Third Party Imports
from charset_normalizer import from_path  # pylint: disable=import-error

unicode = str


class Encoder:
    """Encoding and decoding of files."""

    CR = "\r"
    LF = "\n"
    CRLF = "\r\n"

    def __init__(self):
        """Initialize an Encoder instance."""
        self.encoding = "latin-1"
        self.system_encoding = (
            locale.getpreferredencoding() or sys.getdefaultencoding()
        )

    def do_detect_encoding(self, filename: str) -> None:
        """Return the detected file encoding.

        Parameters
        ----------
        filename : str
            The full path name of the file whose encoding is to be detected.
        """
        try:
            self.encoding = from_path(filename).best().encoding

            # Check for correctness of encoding.
            with self.do_open_with_encoding(filename) as check_file:
                check_file.read()
        except (SyntaxError, LookupError, UnicodeDecodeError):
            self.encoding = "latin-1"

    def do_find_newline(self, source: List[str]) -> Dict[int, int]:
        """Return type of newline used in source.

        Parameters
        ----------
        source : list
            A list of lines.

        Returns
        -------
        counter : dict
            A dict with the count of new line types found.
        """
        assert not isinstance(source, unicode)

        counter = collections.defaultdict(int)
        for line in source:
            if line.endswith(self.CRLF):
                counter[self.CRLF] += 1
            elif line.endswith(self.CR):
                counter[self.CR] += 1
            elif line.endswith(self.LF):
                counter[self.LF] += 1

        return (sorted(counter, key=counter.get, reverse=True) or [self.LF])[0]

    def do_open_with_encoding(self, filename: str, mode: str = "r"):
        """Return opened file with a specific encoding.

        Parameters
        ----------
        filename : str
            The full path name of the file to open.
        mode : str
            The mode to open the file in.  Defaults to read-only.

        Returns
        -------
        contents : TextIO
            The contents of the file.
        """
        return io.open(
            filename, mode=mode, encoding=self.encoding, newline=""
        )  # Preserve line endings
