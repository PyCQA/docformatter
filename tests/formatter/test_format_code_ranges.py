# pylint: skip-file
# type: ignore
#
#       tests.test_format_code_ranges.py is part of the docformatter project
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
"""Module for testing the Formattor._format_code() method with ranges and lengths."""

# Standard Library Imports
import contextlib
import sys

with contextlib.suppress(ImportError):
    if sys.version_info >= (3, 11):
        # Standard Library Imports
        import tomllib
    else:
        # Third Party Imports
        import tomli as tomllib

# Third Party Imports
import pytest

# docformatter Package Imports
from docformatter import Formatter


class TestFormatCodeRanges:
    """Class for testing _format_code() with the line_range or length_range
    arguments."""

    with open("tests/_data/string_files/format_code_ranges.toml", "rb") as f:
        TEST_STRINGS = tomllib.load(f)

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [["--range", "1", "1", ""]])
    def test_format_code_range_miss(self, test_args, args):
        """Should leave docstrings outside line range as is."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["range_miss"]["instring"]
        outstring = self.TEST_STRINGS["range_miss"]["outstring"]

        assert outstring == uut._format_code(
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [["--range", "1", "2", ""]])
    def test_format_code_range_hit(self, test_args, args):
        """Should format docstrings within line_range."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["range_hit"]["instring"]
        outstring = self.TEST_STRINGS["range_hit"]["outstring"]

        assert outstring == uut._format_code(
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [["--docstring-length", "1", "1", ""]])
    def test_format_code_docstring_length(self, test_args, args):
        """Should leave docstrings outside length_range as is."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["length_ignore"]["instring"]
        outstring = self.TEST_STRINGS["length_ignore"]["outstring"]

        assert outstring == uut._format_code(
            instring,
        )
