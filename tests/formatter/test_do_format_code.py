# pylint: skip-file
# type: ignore
#
#       tests.test_do_format_code.py is part of the docformatter project
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
"""Module for testing the Formattor._do_format_code() method."""

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


class TestDoFormatCode:
    """Class for testing _do_format_code() with no arguments."""

    with open("tests/_data/string_files/do_format_code.toml", "rb") as f:
        TEST_STRINGS = tomllib.load(f)

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_do_format_code(self, test_args, args):
        """Should place one-liner on single line."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["one_line"]["instring"]
        outstring = self.TEST_STRINGS["one_line"]["outstring"]

        assert outstring == uut._do_format_code(
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_do_format_code_with_module_docstring(self, test_args, args):
        """Should format module docstrings."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["module_docstring"]["instring"]
        outstring = self.TEST_STRINGS["module_docstring"]["outstring"]

        assert outstring == uut._do_format_code(
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_code_strip_blank_line_after_module_variable(
        self,
        test_args,
        args,
    ):
        """Strip newlines between module variable definition and docstring."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["newline_module_variable"]["instring"]
        outstring = self.TEST_STRINGS["newline_module_variable"]["outstring"]

        assert outstring == uut._do_format_code(
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_code_class_docstring(self, test_args, args):
        """Format class docstring."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["class_docstring"]["instring"]
        outstring = self.TEST_STRINGS["class_docstring"]["outstring"]

        assert outstring == uut._do_format_code(
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_code_strip_blank_line_after_class_variable(
        self,
        test_args,
        args,
    ):
        """Strip any newlines between a class variable definition and docstring.

        See requirement .
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["newline_class_variable"]["instring"]
        outstring = self.TEST_STRINGS["newline_class_variable"]["outstring"]

        assert outstring == uut._do_format_code(
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_do_format_code_keep_newlines_outside_docstring(self, test_args, args):
        """Should keep newlines in code following docstring."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["newline_outside_docstring"]["instring"]
        outstring = self.TEST_STRINGS["newline_outside_docstring"]["outstring"]

        assert outstring == uut._do_format_code(
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_code_dominant_line_ending_style_preserved(self, test_args, args):
        """Should retain carriage return line endings."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["preserve_line_ending"]["instring"]
        outstring = self.TEST_STRINGS["preserve_line_ending"]["outstring"]

        assert outstring == uut._do_format_code(
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_code_additional_empty_line_before_doc(self, test_args, args):
        """Should remove empty line between function def and docstring.

        See issue #51.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["issue_51"]["instring"]
        outstring = self.TEST_STRINGS["issue_51"]["outstring"]

        assert outstring == uut._do_format_code(
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_code_extra_newline_following_comment(self, test_args, args):
        """Should remove extra newline following in-line comment.

        See issue #51.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["issue_51_2"]["instring"]
        outstring = self.TEST_STRINGS["issue_51_2"]["outstring"]

        assert outstring == uut._do_format_code(
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_code_no_docstring(self, test_args, args):
        """Should leave code as is if there is no docstring.

        See issue #97.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["issue_97"]["instring"]
        outstring = self.TEST_STRINGS["issue_97"]["outstring"]

        assert outstring == uut._do_format_code(
            instring,
        )

        instring = self.TEST_STRINGS["issue_97_2"]["instring"]
        outstring = self.TEST_STRINGS["issue_97_2"]["outstring"]

        assert outstring == uut._do_format_code(
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_code_class_docstring_remove_blank_line(self, test_args, args):
        """Remove blank line before class docstring.

        See issue #139.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["issue_139"]["instring"]
        outstring = self.TEST_STRINGS["issue_139"]["outstring"]

        assert outstring == uut._do_format_code(
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_code_class_docstring_keep_blank_line(self, test_args, args):
        """Keep blank line after class definition if there is no docstring.

        See issue #139.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["issue_139_2"]["instring"]
        outstring = self.TEST_STRINGS["issue_139_2"]["outstring"]

        assert outstring == uut._do_format_code(
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_code_strip_blank_line_after_method_docstring(
        self,
        test_args,
        args,
    ):
        """Strip any newlines after a method docstring.

        See requirement PEP_257_4.4, issue #130.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["issue_130"]["instring"]
        outstring = self.TEST_STRINGS["issue_130"]["outstring"]

        assert outstring == uut._do_format_code(
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_code_do_not_touch_function_no_docstring(
        self,
        test_args,
        args,
    ):
        """Do not remove newlines in functions with no docstring.

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
    def test_do_format_code_keep_newline_for_stub_functions(self, test_args, args):
        """Should keep newline after docstring in stub functions.

        See issue #156 and issue #173.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["issue_156_173"]["instring"]
        outstring = self.TEST_STRINGS["issue_156_173"]["outstring"]

        assert outstring == uut._do_format_code(
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_code_keep_newline_after_shebang(
        self,
        test_args,
        args,
    ):
        """Do not remove newlines following the shebang.

        See issue #187.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["issue_187"]["instring"]
        outstring = self.TEST_STRINGS["issue_187"]["outstring"]

        assert outstring == uut._do_format_code(
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_code_keep_newline_after_import(
        self,
        test_args,
        args,
    ):
        """Do not remove newlines following the import section.

        See issue #203.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["issue_203"]["instring"]
        outstring = self.TEST_STRINGS["issue_203"]["outstring"]

        assert outstring == uut._do_format_code(
            instring,
        )
