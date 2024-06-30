# pylint: skip-file
# type: ignore
#
#       tests.test_format_docstring.py is part of the docformatter project
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


class TestFormatDocstring:
    """Class for testing _do_format_docstring() with no arguments."""

    with open("tests/_data/string_files/do_format_docstrings.toml", "rb") as f:
        TEST_STRINGS = tomllib.load(f)

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_one_line_docstring(self, test_args, args):
        """Return one-line docstring."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["one_line"]["instring"]
        outstring = self.TEST_STRINGS["one_line"]["outstring"]

        assert outstring == uut._do_format_docstring(
            INDENTATION,
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_docstring_with_summary_that_ends_in_quote(self, test_args, args):
        """Return one-line docstring with period after quote."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["summary_end_quote"]["instring"]
        outstring = self.TEST_STRINGS["summary_end_quote"]["outstring"]

        assert outstring == uut._do_format_docstring(
            INDENTATION,
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [["--wrap-descriptions", "44", ""]])
    def test_format_docstring_with_bad_indentation(self, test_args, args):
        """Add spaces to indentation when too few."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["bad_indentation"]["instring"]
        outstring = self.TEST_STRINGS["bad_indentation"]["outstring"]

        assert outstring == uut._do_format_docstring(
            INDENTATION,
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_docstring_with_too_much_indentation(self, test_args, args):
        """Remove spaces from indentation when too many."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["too_much_indentation"]["instring"]
        outstring = self.TEST_STRINGS["too_much_indentation"]["outstring"]

        assert outstring == uut._do_format_docstring(
            INDENTATION,
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [["--wrap-descriptions", "52", ""]])
    def test_format_docstring_with_trailing_whitespace(self, test_args, args):
        """Remove trailing white space."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["trailing_whitespace"]["instring"]
        outstring = self.TEST_STRINGS["trailing_whitespace"]["outstring"]

        assert outstring == uut._do_format_docstring(
            INDENTATION,
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_docstring_with_empty_docstring(self, test_args, args):
        """Do nothing with empty docstring."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["empty_docstring"]["instring"]
        outstring = self.TEST_STRINGS["empty_docstring"]["outstring"]

        assert outstring == uut._do_format_docstring(
            INDENTATION,
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_docstring_with_no_period(self, test_args, args):
        """Add period to end of one-line and summary line."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["no_summary_period"]["instring"]
        outstring = self.TEST_STRINGS["no_summary_period"]["outstring"]

        assert outstring == uut._do_format_docstring(
            INDENTATION,
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_docstring_with_single_quotes(self, test_args, args):
        """Replace single triple quotes with triple double quotes."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["single_quotes"]["instring"]
        outstring = self.TEST_STRINGS["single_quotes"]["outstring"]

        assert outstring == uut._do_format_docstring(
            INDENTATION,
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_docstring_with_single_quotes_multi_line(self, test_args, args):
        """Replace single triple quotes with triple double quotes."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["single_quotes_multiline"]["instring"]
        outstring = self.TEST_STRINGS["single_quotes_multiline"]["outstring"]

        assert outstring == uut._do_format_docstring(
            INDENTATION,
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_docstring_leave_underlined_summaries_alone(self, test_args, args):
        """Leave underlined summary lines as is."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["skip_underlined_summary"]["instring"]
        outstring = self.TEST_STRINGS["skip_underlined_summary"]["outstring"]

        assert outstring == uut._do_format_docstring(
            INDENTATION,
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_docstring_leave_blank_line_after_variable_def(
        self,
        test_args,
        args,
    ):
        """Leave blank lines after any variable beginning with 'def'.

        See issue #156.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["issue_156"]["instring"]
        outstring = self.TEST_STRINGS["issue_156"]["outstring"]

        assert outstring == uut._do_format_code(
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_docstring_leave_directive_alone(self, test_args, args):
        """Leave docstrings that have a reST directive in the summary alone.

        See issue #157.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["issue_157"]["instring"]
        outstring = self.TEST_STRINGS["issue_157"]["outstring"]

        assert outstring == uut._do_format_docstring(
            INDENTATION,
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_docstring_leave_blank_line_after_comment(
        self,
        test_args,
        args,
    ):
        """Leave blank lines after docstring followed by a comment.

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

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [["--non-cap", "eBay", "iPad", "-c", ""]])
    def test_format_docstring_with_non_cap_words(self, test_args, args):
        """Capitalize words not found in the non_cap list.

        See issue #193.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["issue_193"]["instring"]
        outstring = self.TEST_STRINGS["issue_193"]["outstring"]

        assert outstring == uut._do_format_docstring(
            INDENTATION,
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [["--style", "sphinx", ""], ["--style", "epytext", ""]])
    def test_do_not_double_process_urls(self, test_args, args):
        """Do not double-process urls in fields

        See issue #263
        """
        style = args[1]

        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["issue_263"][style]["instring"]
        outstring = self.TEST_STRINGS["issue_263"][style]["outstring"]

        assert outstring == uut._do_format_docstring(INDENTATION, instring, )
