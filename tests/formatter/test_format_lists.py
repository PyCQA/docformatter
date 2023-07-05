# pylint: skip-file
# type: ignore
#
#       tests.test_format_lists.py is part of the docformatter project
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
"""Module for testing the Formatter class."""


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

INDENTATION = "    "


class TestFormatLists:
    """Class for testing format_docstring() with lists in the docstring."""

    with open("tests/_data/string_files/format_lists.toml", "rb") as f:
        TEST_STRINGS = tomllib.load(f)

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [["--wrap-descriptions", "72", ""]])
    def test_format_docstring_should_ignore_numbered_lists(self, test_args, args):
        """Ignore lists beginning with numbers."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["numbered"]["instring"]
        outstring = self.TEST_STRINGS["numbered"]["outstring"]

        assert outstring == uut._do_format_docstring(
            INDENTATION,
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [["--wrap-descriptions", "72", ""]])
    def test_format_docstring_should_ignore_parameter_lists(self, test_args, args):
        """Ignore lists beginning with <word> -."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["parameter"]["dash"]["instring"]
        outstring = self.TEST_STRINGS["parameter"]["dash"]["outstring"]

        assert outstring == uut._do_format_docstring(
            INDENTATION,
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize(
        "args", [["--wrap-descriptions", "72", "--style", "numpy", ""]]
    )
    def test_format_docstring_should_ignore_colon_parameter_lists(
        self, test_args, args
    ):
        """Ignore lists beginning with <word>:"""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["parameter"]["colon"]["instring"]
        outstring = self.TEST_STRINGS["parameter"]["colon"]["outstring"]

        assert outstring == uut._do_format_docstring(
            INDENTATION,
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_docstring_should_leave_list_alone(self, test_args, args):
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["many"]["short"]["columns"]["instring"]
        outstring = self.TEST_STRINGS["many"]["short"]["columns"]["outstring"]

        assert outstring == uut._do_format_docstring(
            INDENTATION,
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_docstring_should_leave_list_alone_with_rest(self, test_args, args):
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["issue_239"]["instring"]
        outstring = self.TEST_STRINGS["issue_239"]["outstring"]

        assert outstring == uut._do_format_docstring(
            INDENTATION,
            instring,
        )
