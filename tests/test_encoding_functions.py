# pylint: skip-file
# type: ignore
#
#       tests.test_encoding_functions.py is part of the docformatter project
#
# Copyright (C) 2012-2019 Steven Myint
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
"""Module for testing functions used determine file encodings.

Encoding functions are:

    - detect_encoding()
    - find_newline()
    - open_with_encoding()
"""

# Standard Library Imports
import io
import sys

# Third Party Imports
import pytest

# docformatter Package Imports
from docformatter import Encoder

SYSTEM_ENCODING = sys.getdefaultencoding()


@pytest.mark.usefixtures("temporary_file")
class TestDetectEncoding:
    """Class for testing the detect_encoding() function."""

    @pytest.mark.unit
    @pytest.mark.parametrize("contents", ["# -*- coding: utf-8 -*-\n"])
    def test_detect_encoding_with_explicit_utf_8(
        self, temporary_file, contents
    ):
        """Return utf-8 when explicitly set in file."""
        uut = Encoder()
        uut.do_detect_encoding(temporary_file)

        assert "utf_8" == uut.encoding

    @pytest.mark.unit
    @pytest.mark.parametrize(
        "contents", ["# Wow!  docformatter is super-cool.\n"]
    )
    def test_detect_encoding_with_non_explicit_setting(
        self, temporary_file, contents
    ):
        """Return default system encoding when encoding not explicitly set."""
        uut = Encoder()
        uut.do_detect_encoding(temporary_file)

        assert "ascii" == uut.encoding

    @pytest.mark.unit
    @pytest.mark.parametrize("contents", ["# -*- coding: blah -*-"])
    def test_detect_encoding_with_bad_encoding(self, temporary_file, contents):
        """Default to latin-1 when unknown encoding detected."""
        uut = Encoder()
        uut.do_detect_encoding(temporary_file)

        assert "ascii" == uut.encoding


class TestFindNewline:
    """Class for testing the find_newline() function."""

    @pytest.mark.unit
    def test_find_newline_only_cr(self):
        """Return carriage return as newline type."""
        uut = Encoder()
        source = ["print 1\r", "print 2\r", "print3\r"]

        assert uut.CR == uut.do_find_newline(source)

    @pytest.mark.unit
    def test_find_newline_only_lf(self):
        """Return line feed as newline type."""
        uut = Encoder()
        source = ["print 1\n", "print 2\n", "print3\n"]

        assert uut.LF == uut.do_find_newline(source)

    @pytest.mark.unit
    def test_find_newline_only_crlf(self):
        """Return carriage return, line feed as newline type."""
        uut = Encoder()
        source = ["print 1\r\n", "print 2\r\n", "print3\r\n"]

        assert uut.CRLF == uut.do_find_newline(source)

    @pytest.mark.unit
    def test_find_newline_cr1_and_lf2(self):
        """Favor line feed over carriage return when both are found."""
        uut = Encoder()
        source = ["print 1\n", "print 2\r", "print3\n"]

        assert uut.LF == uut.do_find_newline(source)

    @pytest.mark.unit
    def test_find_newline_cr1_and_crlf2(self):
        """Favor carriage return, line feed when mix of newline types."""
        uut = Encoder()
        source = ["print 1\r\n", "print 2\r", "print3\r\n"]

        assert uut.CRLF == uut.do_find_newline(source)

    @pytest.mark.unit
    def test_find_newline_should_default_to_lf(self):
        """Default to line feed when no newline type found."""
        uut = Encoder()

        assert uut.LF == uut.do_find_newline([])
        assert uut.LF == uut.do_find_newline(["", ""])

    @pytest.mark.unit
    def test_find_dominant_newline(self):
        """Should detect carriage return as the dominant line endings."""
        uut = Encoder()

        goes_in = '''\
def foo():\r
    """\r
    Hello\r
    foo. This is a docstring.\r
    """\r
'''
        assert uut.CRLF == uut.do_find_newline(goes_in.splitlines(True))


@pytest.mark.usefixtures("temporary_file")
class TestOpenWithEncoding:
    """Class for testing the open_with_encoding() function."""

    @pytest.mark.unit
    @pytest.mark.parametrize("contents", ["# -*- coding: utf-8 -*-\n"])
    def test_open_with_utf_8_encoding(self, temporary_file, contents):
        """Return TextIOWrapper object when opening file with encoding."""
        uut = Encoder()
        uut.do_detect_encoding(temporary_file)

        assert isinstance(
            uut.do_open_with_encoding(temporary_file),
            io.TextIOWrapper,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("contents", ["# -*- coding: utf-8 -*-\n"])
    def test_open_with_wrong_encoding(self, temporary_file, contents):
        """Raise LookupError when passed unknown encoding."""
        uut = Encoder()
        uut.encoding = "cr1252"

        with pytest.raises(LookupError):
            uut.do_open_with_encoding(temporary_file)
