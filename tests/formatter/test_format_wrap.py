# pylint: skip-file
# type: ignore
#
#       tests.test_format_wrap.py is part of the docformatter project
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
"""Module for testing the Formatter class with the --wrap options."""


# Standard Library Imports
import contextlib
import itertools
import random
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
import docformatter
from docformatter import Formatter

# docformatter Local Imports
from .. import generate_random_docstring

INDENTATION = "    "


class TestFormatWrap:
    """Class for testing _do_format_docstring() with line wrapping."""

    with open("tests/_data/string_files/format_wrap.toml", "rb") as f:
        TEST_STRINGS = tomllib.load(f)

    @pytest.mark.unit
    def test_unwrap_summary(self):
        """Remove newline and tab characters."""

        instring = self.TEST_STRINGS["unwrap"]["instring"]
        outstring = self.TEST_STRINGS["unwrap"]["outstring"]

        assert outstring == docformatter.unwrap_summary(
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_docstring_with_wrap(
        self,
        test_args,
        args,
    ):
        """Wrap the docstring."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        # This function uses `random` so make sure each run of this test is
        # repeatable.
        random.seed(0)

        min_line_length = 50
        for max_length, num_indents in itertools.product(
            range(min_line_length, 100), range(20)
        ):
            indentation = " " * num_indents
            uut.args.wrap_summaries = max_length
            formatted_text = indentation + uut._do_format_docstring(
                indentation=indentation,
                docstring=generate_random_docstring(
                    max_word_length=min_line_length // 2
                ),
            )
            for line in formatted_text.split("\n"):
                # It is not the formatter's fault if a word is too long to
                # wrap.
                if len(line.split()) > 1:
                    assert len(line) <= max_length

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [["--wrap-summaries", "79", ""]])
    def test_format_docstring_with_weird_indentation_and_punctuation(
        self,
        test_args,
        args,
    ):
        """Wrap and dedent docstring."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["weird_punctuation"]["instring"]
        outstring = self.TEST_STRINGS["weird_punctuation"]["outstring"]

        assert outstring == uut._do_format_docstring(
            INDENTATION,
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [["--wrap-descriptions", "72", ""]])
    def test_format_docstring_with_description_wrapping(
        self,
        test_args,
        args,
    ):
        """Wrap description at 72 characters."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["description_wrap"]["instring"]
        outstring = self.TEST_STRINGS["description_wrap"]["outstring"]

        assert outstring == uut._do_format_docstring(
            INDENTATION,
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [["--wrap-descriptions", "72", ""]])
    def test_format_docstring_should_ignore_doctests(
        self,
        test_args,
        args,
    ):
        """Leave doctests alone."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["ignore_doctest"]["instring"]
        outstring = self.TEST_STRINGS["ignore_doctest"]["outstring"]

        assert outstring == uut._do_format_docstring(
            INDENTATION,
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [["--wrap-descriptions", "72", ""]])
    def test_format_docstring_should_ignore_doctests_in_summary(
        self,
        test_args,
        args,
    ):
        """Leave doctests alone if they're in the summary."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["ignore_summary_doctest"]["instring"]
        outstring = self.TEST_STRINGS["ignore_summary_doctest"]["outstring"]

        assert outstring == uut._do_format_docstring(
            INDENTATION,
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [["--wrap-descriptions", "72", ""]])
    def test_format_docstring_should_maintain_indentation_of_doctest(
        self,
        test_args,
        args,
    ):
        """Don't change indentation of doctest lines."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["same_indentation_doctest"]["instring"]
        outstring = self.TEST_STRINGS["same_indentation_doctest"]["outstring"]

        assert outstring == uut._do_format_docstring(
            INDENTATION,
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize(
        "args",
        [
            [
                "--wrap-descriptions",
                "72",
                "--wrap-summaries",
                "50",
                "--force-wrap",
                "",
            ]
        ],
    )
    def test_force_wrap(
        self,
        test_args,
        args,
    ):
        """Force even lists to be wrapped."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["force_wrap"]["instring"]
        outstring = self.TEST_STRINGS["force_wrap"]["outstring"]

        assert outstring == uut._do_format_docstring(
            INDENTATION,
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize(
        "args",
        [["--wrap-summaries", "30", "--tab-width", "4", ""]],
    )
    def test_format_docstring_with_summary_only_and_wrap_and_tab_indentation(
        self,
        test_args,
        args,
    ):
        """Should account for length of tab when wrapping.

        See PR #69.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["summary_wrap_tab"]["instring"]
        outstring = self.TEST_STRINGS["summary_wrap_tab"]["outstring"]

        assert outstring == uut._do_format_docstring(
            "\t\t",
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize(
        "args",
        [["--wrap-summaries", "69", "--close-quotes-on-newline", ""]],
    )
    def test_format_docstring_for_multi_line_summary_alone(
        self,
        test_args,
        args,
    ):
        """Place closing quotes on newline when wrapping one-liner."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["one_line_wrap_newline"]["instring"]
        outstring = self.TEST_STRINGS["one_line_wrap_newline"]["outstring"]

        assert outstring == uut._do_format_docstring(
            INDENTATION,
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize(
        "args",
        [["--wrap-summaries", "88", "--close-quotes-on-newline", ""]],
    )
    def test_format_docstring_for_one_line_summary_alone_but_too_long(
        self,
        test_args,
        args,
    ):
        """"""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["one_line_no_wrap"]["instring"]
        outstring = self.TEST_STRINGS["one_line_no_wrap"]["outstring"]

        assert outstring == uut._do_format_docstring(
            INDENTATION,
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_docstring_with_class_attributes(self, test_args, args):
        """Wrap long class attribute docstrings."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["class_attribute_wrap"]["instring"]
        outstring = self.TEST_STRINGS["class_attribute_wrap"]["outstring"]

        assert outstring == uut._do_format_code(
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_docstring_no_newline_in_summary_with_symbol(self, test_args, args):
        """Wrap summary with symbol should not add newline.

        See issue #79.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["issue_79"]["instring"]
        outstring = self.TEST_STRINGS["issue_79"]["outstring"]

        assert outstring == uut._do_format_code(
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize(
        "args", [["--wrap-descriptions", "120", "--wrap-summaries", "120", ""]]
    )
    def test_format_docstring_with_multi_paragraph_description(
        self,
        test_args,
        args,
    ):
        """Wrap each paragraph in the long description separately.

        See issue #127.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["issue_127"]["instring"]
        outstring = self.TEST_STRINGS["issue_127"]["outstring"]

        assert outstring == uut._do_format_docstring(
            INDENTATION,
            instring,
        )
