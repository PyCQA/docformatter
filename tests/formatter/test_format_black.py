# pylint: skip-file
# type: ignore
#
#       tests.test_format_black.py is part of the docformatter project
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
"""Module for testing the Formatter class with the --black option."""


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


class TestFormatWrapBlack:
    """Class for testing _do_format_docstring() with line wrapping and black option."""

    with open("tests/_data/string_files/format_black.toml", "rb") as f:
        TEST_STRINGS = tomllib.load(f)

    @pytest.mark.unit
    @pytest.mark.parametrize(
        "args",
        [
            [
                "--black",
                "",
            ]
        ],
    )
    def test_format_docstring_black(
        self,
        test_args,
        args,
    ):
        """Format with black options when --black specified.

        Add a space between the opening quotes and the summary if content starts with a
        quote.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["quote_no_space"]["instring"]
        outstring = self.TEST_STRINGS["quote_no_space"]["outstring"]

        assert outstring == uut._do_format_docstring(
            INDENTATION,
            instring,
        )

        instring = self.TEST_STRINGS["quote_space"]["instring"]
        outstring = self.TEST_STRINGS["quote_space"]["outstring"]

        assert outstring == uut._do_format_docstring(
            INDENTATION,
            instring,
        )

        instring = self.TEST_STRINGS["quote_space_2"]["instring"]
        outstring = self.TEST_STRINGS["quote_space_2"]["outstring"]

        assert outstring == uut._do_format_docstring(
            INDENTATION,
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize(
        "args",
        [
            [
                "--black",
                "",
            ]
        ],
    )
    def test_format_code_strip_blank_lines(
        self,
        test_args,
        args,
    ):
        """Blank lines are stripped in black mode."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["strip_blank_lines"]["instring"]
        outstring = self.TEST_STRINGS["strip_blank_lines"]["outstring"]

        assert outstring == uut._do_format_code(
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize(
        "args",
        [
            [
                "--black",
                "",
            ]
        ],
    )
    def test_format_docstring_black_keep_newline_after_comment(
        self,
        test_args,
        args,
    ):
        """Retain the newline after a docstring with an inline comment.

        See issue #176.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["issue_176"]["instring"]
        outstring = self.TEST_STRINGS["issue_176"]["outstring"]

        assert outstring == uut._do_format_code(
            instring,
        )
