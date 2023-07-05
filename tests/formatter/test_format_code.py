# pylint: skip-file
# type: ignore
#
#       tests.test_format_code.py is part of the docformatter project
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
"""Module for testing the Formattor._format_code() method."""

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


class TestFormatCode:
    """Class for testing _format_code() with no arguments."""

    with open("tests/_data/string_files/format_code.toml", "rb") as f:
        TEST_STRINGS = tomllib.load(f)

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_code_should_ignore_non_docstring(self, test_args, args):
        """Should ignore triple quoted strings that are assigned values."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["non_docstring"]["instring"]
        outstring = self.TEST_STRINGS["non_docstring"]["outstring"]

        assert outstring == uut._format_code(
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_code_with_empty_string(self, test_args, args):
        """Should do nothing with an empty string."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        assert not uut._format_code("")
        assert not uut._format_code("")

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_code_with_tabs(self, test_args, args):
        """Should retain tabbed indentation."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["tabbed_indentation"]["instring"]
        outstring = self.TEST_STRINGS["tabbed_indentation"]["outstring"]

        assert outstring == uut._format_code(
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_code_with_mixed_tabs(self, test_args, args):
        """Should retain mixed tabbed and spaced indentation."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["mixed_indentation"]["instring"]
        outstring = self.TEST_STRINGS["mixed_indentation"]["outstring"]

        assert outstring == uut._format_code(
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_code_with_escaped_newlines(self, test_args, args):
        """Should leave escaped newlines in code untouched."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["escaped_newlines"]["instring"]
        outstring = self.TEST_STRINGS["escaped_newlines"]["outstring"]

        assert outstring == uut._format_code(
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_code_with_comments(self, test_args, args):
        """Should leave comments as is."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["code_comments"]["instring"]
        outstring = self.TEST_STRINGS["code_comments"]["outstring"]

        assert outstring == uut._format_code(
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_code_with_escaped_newline_in_inline_comment(self, test_args, args):
        """Should leave code with inline comment as is."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["inline_comment"]["instring"]
        outstring = self.TEST_STRINGS["inline_comment"]["outstring"]

        assert outstring == uut._format_code(
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_code_raw_docstring_double_quotes(self, test_args, args):
        """Should format raw docstrings with triple double quotes.

        See requirement PEP_257_2.  See issue #54 for request to handle raw docstrings.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["raw_lowercase"]["instring"]
        outstring = self.TEST_STRINGS["raw_lowercase"]["outstring"]

        assert outstring == uut._format_code(
            instring,
        )

        instring = self.TEST_STRINGS["raw_uppercase"]["instring"]
        outstring = self.TEST_STRINGS["raw_uppercase"]["outstring"]

        assert outstring == uut._format_code(
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_code_raw_docstring_single_quotes(self, test_args, args):
        """Should format raw docstrings with triple single quotes.

        See requirement PEP_257_2.  See issue #54 for request to handle raw docstrings.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["raw_lowercase_single"]["instring"]
        outstring = self.TEST_STRINGS["raw_lowercase_single"]["outstring"]

        assert outstring == uut._format_code(
            instring,
        )

        instring = self.TEST_STRINGS["raw_uppercase_single"]["instring"]
        outstring = self.TEST_STRINGS["raw_uppercase_single"]["outstring"]

        assert outstring == uut._format_code(
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_code_unicode_docstring_double_quotes(self, test_args, args):
        """Should format unicode docstrings with triple double quotes.

        See requirement PEP_257_3.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["unicode_lowercase"]["instring"]
        outstring = self.TEST_STRINGS["unicode_lowercase"]["outstring"]

        assert outstring == uut._format_code(
            instring,
        )

        instring = self.TEST_STRINGS["unicode_uppercase"]["instring"]
        outstring = self.TEST_STRINGS["unicode_uppercase"]["outstring"]

        assert outstring == uut._format_code(
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_code_unicode_docstring_single_quotes(self, test_args, args):
        """Should format unicode docstrings with triple single quotes.

        See requirement PEP_257_3.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["unicode_lowercase_single"]["instring"]
        outstring = self.TEST_STRINGS["unicode_lowercase_single"]["outstring"]

        assert outstring == uut._format_code(
            instring,
        )

        instring = self.TEST_STRINGS["unicode_uppercase_single"]["instring"]
        outstring = self.TEST_STRINGS["unicode_uppercase_single"]["outstring"]

        assert outstring == uut._format_code(
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_code_skip_nested(self, test_args, args):
        """Should ignore nested triple quotes."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["nested_triple"]["instring"]
        outstring = self.TEST_STRINGS["nested_triple"]["outstring"]

        assert outstring == uut._format_code(
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_code_with_multiple_sentences(self, test_args, args):
        """Should create multi-line docstring from multiple sentences."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["multiple_sentences"]["instring"]
        outstring = self.TEST_STRINGS["multiple_sentences"]["outstring"]

        assert outstring == uut._format_code(
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_code_with_multiple_sentences_same_line(self, test_args, args):
        """Should create multi-line docstring from multiple sentences."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["multiple_sentences_same_line"]["instring"]
        outstring = self.TEST_STRINGS["multiple_sentences_same_line"]["outstring"]

        assert outstring == uut._format_code(
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_code_with_multiple_sentences_multi_line_summary(
        self, test_args, args
    ):
        """Should put summary line on a single line."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["multiline_summary"]["instring"]
        outstring = self.TEST_STRINGS["multiline_summary"]["outstring"]

        assert outstring == uut._format_code(
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_code_with_empty_lines(self, test_args, args):
        """Summary line on one line when wrapped, followed by empty line."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["empty_lines"]["instring"]
        outstring = self.TEST_STRINGS["empty_lines"]["outstring"]

        assert outstring == uut._format_code(
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_code_with_empty_lines_class_docstring(self, test_args, args):
        """No blank lines before a class's docstring."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["class_empty_lines"]["instring"]
        outstring = self.TEST_STRINGS["class_empty_lines"]["outstring"]

        assert outstring == uut._format_code(
            instring,
        )

        instring = self.TEST_STRINGS["class_empty_lines"]["instring_2"]
        outstring = self.TEST_STRINGS["class_empty_lines"]["outstring_2"]

        assert outstring == uut._format_code(
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_code_with_empty_lines_method_docstring(self, test_args, args):
        """No blank lines before a method's docstring."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["method_empty_lines"]["instring"]
        outstring = self.TEST_STRINGS["method_empty_lines"]["outstring"]

        assert outstring == uut._format_code(
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_code_with_trailing_whitespace(self, test_args, args):
        """Should strip trailing whitespace."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["trailing_whitespace"]["instring"]
        outstring = self.TEST_STRINGS["trailing_whitespace"]["outstring"]

        assert outstring == uut._format_code(
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_code_with_parameters_list(self, test_args, args):
        """Should treat parameters list as elaborate description."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["parameter_list"]["instring"]
        outstring = self.TEST_STRINGS["parameter_list"]["outstring"]

        assert outstring == uut._format_code(
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_ignore_code_with_single_quote(self, test_args, args):
        """Single single quote on first line of code should remain untouched.

        See requirement PEP_257_1.  See issue #66 for example of docformatter breaking
        code when encountering single quote.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["single_quote"]["instring"]
        outstring = self.TEST_STRINGS["single_quote"]["outstring"]

        assert outstring == uut._format_code(
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_ignore_code_with_double_quote(self, test_args, args):
        """Single double quotes on first line of code should remain untouched.

        See requirement PEP_257_1.  See issue #66 for example of docformatter breaking
        code when encountering single quote.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["double_quote"]["instring"]
        outstring = self.TEST_STRINGS["double_quote"]["outstring"]

        assert outstring == uut._format_code(
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_code_should_skip_nested_triple_quotes(self, test_args, args):
        """Should ignore triple quotes nested in a string."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["nested_triple_quote"]["instring"]
        outstring = self.TEST_STRINGS["nested_triple_quote"]["outstring"]

        assert outstring == uut._format_code(
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_code_with_assignment_on_first_line(self, test_args, args):
        """Should ignore triple quotes in variable assignment."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["first_line_assignment"]["instring"]
        outstring = self.TEST_STRINGS["first_line_assignment"]["outstring"]

        assert outstring == uut._format_code(
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_code_with_regular_strings_too(self, test_args, args):
        """Should ignore triple quoted strings after the docstring."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["regular_strings"]["instring"]
        outstring = self.TEST_STRINGS["regular_strings"]["outstring"]

        assert outstring == uut._format_code(
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_code_with_syntax_error(self, test_args, args):
        """Should ignore single set of triple quotes followed by newline."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["syntax_error"]["instring"]
        outstring = self.TEST_STRINGS["syntax_error"]["outstring"]

        assert outstring == uut._format_code(
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_code_with_syntax_error_case_slash_r(self, test_args, args):
        """Should ignore single set of triple quotes followed by return."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["slash_r"]["instring"]
        outstring = self.TEST_STRINGS["slash_r"]["outstring"]

        assert outstring == uut._format_code(
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_code_with_syntax_error_case_slash_r_slash_n(self, test_args, args):
        """Should ignore single triple quote followed by return, newline."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["slash_r_slash_n"]["instring"]
        outstring = self.TEST_STRINGS["slash_r_slash_n"]["outstring"]

        assert outstring == uut._format_code(
            instring,
        )
