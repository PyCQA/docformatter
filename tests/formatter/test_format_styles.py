# pylint: skip-file
# type: ignore
#
#       tests.test_format_styles.py is part of the docformatter project
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
"""Module for testing the Formatter class with various style options."""


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


class TestFormatStyleOptions:
    """Class for testing format_docstring() when requesting style options."""

    with open("tests/_data/string_files/format_style_options.toml", "rb") as f:
        TEST_STRINGS = tomllib.load(f)

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_docstring_with_no_post_description_blank(
        self,
        test_args,
        args,
    ):
        """Remove blank lines before closing triple quotes."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["no_blank"]["instring"]
        outstring = self.TEST_STRINGS["no_blank"]["outstring"]

        assert outstring == uut._do_format_docstring(
            INDENTATION,
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [["--pre-summary-newline", ""]])
    def test_format_docstring_with_pre_summary_newline(
        self,
        test_args,
        args,
    ):
        """Remove blank line before summary."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["presummary_newline"]["instring"]
        outstring = self.TEST_STRINGS["presummary_newline"]["outstring"]

        assert outstring == uut._do_format_docstring(
            INDENTATION,
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [["--make-summary-multi-line", ""]])
    def test_format_docstring_make_summary_multi_line(
        self,
        test_args,
        args,
    ):
        """Place the one-line docstring between triple quotes."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["summary_multiline"]["instring"]
        outstring = self.TEST_STRINGS["summary_multiline"]["outstring"]

        assert outstring == uut._do_format_docstring(
            INDENTATION,
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [["--pre-summary-space", ""]])
    def test_format_docstring_pre_summary_space(
        self,
        test_args,
        args,
    ):
        """Place a space between the opening quotes and the summary."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["presummary_space"]["instring"]
        outstring = self.TEST_STRINGS["presummary_space"]["outstring"]

        assert outstring == uut._do_format_docstring(
            INDENTATION,
            instring,
        )
