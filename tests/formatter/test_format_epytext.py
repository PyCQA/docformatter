# pylint: skip-file
# type: ignore
#
#       tests.test_format_epytext.py is part of the docformatter project
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


class TestFormatWrapEpytext:
    """Class for testing _do_format_docstring() with line wrapping and Epytext lists."""

    with open("tests/_data/string_files/format_epytext.toml", "rb") as f:
        TEST_STRINGS = tomllib.load(f)

    @pytest.mark.unit
    @pytest.mark.parametrize(
        "args",
        [
            [
                "--wrap-descriptions",
                "88",
                "--wrap-summaries",
                "88",
                "--style",
                "epytext",
                "",
            ]
        ],
    )
    def test_format_docstring_epytext_style(
        self,
        test_args,
        args,
    ):
        """Wrap epytext style parameter lists.

        See requirement docformatter_10.6.2
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["epytext"]["instring"]
        outstring = self.TEST_STRINGS["epytext"]["outstring"]

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
                "88",
                "--wrap-summaries",
                "88",
                "--style",
                "numpy",
                "",
            ]
        ],
    )
    def test_format_docstring_non_epytext_style(
        self,
        test_args,
        args,
    ):
        """Ignore wrapping epytext style parameter lists when not using epytext style.

        See requirement docformatter_10.6.1
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["epytext"]["numpy"]["instring"]
        outstring = self.TEST_STRINGS["epytext"]["numpy"]["outstring"]

        assert outstring == uut._do_format_docstring(
            INDENTATION,
            instring,
        )
