# pylint: skip-file
# type: ignore
#
#       tests.test_format_sphinx.py is part of the docformatter project
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


class TestFormatWrapSphinx:
    """Class for testing _do_format_docstring() with line wrapping and Sphinx lists."""

    with open("tests/_data/string_files/format_sphinx.toml", "rb") as f:
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
                "sphinx",
                "",
            ]
        ],
    )
    def test_format_docstring_sphinx_style(
        self,
        test_args,
        args,
    ):
        """Wrap sphinx style parameter lists.

        See requirement docformatter_10.4.2 and issue #230.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["sphinx"]["instring"]
        outstring = self.TEST_STRINGS["sphinx"]["outstring"]

        assert outstring == uut._do_format_docstring(
            INDENTATION,
            instring,
        )

        # Issue #230 required adding parenthesis to the SPHINX_REGEX.
        instring = self.TEST_STRINGS["issue_230"]["instring"]
        outstring = self.TEST_STRINGS["issue_230"]["outstring"]

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
    def test_format_docstring_non_sphinx_style(
        self,
        test_args,
        args,
    ):
        """Ignore wrapping sphinx style parameter lists when not using sphinx style.

        See requirement docformatter_10.4.1
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["sphinx"]["numpy"]["instring"]
        outstring = self.TEST_STRINGS["sphinx"]["numpy"]["outstring"]

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
                "",
            ]
        ],
    )
    def test_format_docstring_sphinx_style_remove_excess_whitespace(
        self,
        test_args,
        args,
    ):
        """Should remove unneeded whitespace.

        See issue #217 and #222
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["issue_217_222"]["instring"]
        outstring = self.TEST_STRINGS["issue_217_222"]["outstring"]

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
                "",
            ]
        ],
    )
    def test_format_docstring_sphinx_style_two_directives_in_row(
        self,
        test_args,
        args,
    ):
        """Should remove unneeded whitespace.

        See issue #215.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["issue_215"]["instring"]
        outstring = self.TEST_STRINGS["issue_215"]["outstring"]

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
                "",
            ]
        ],
    )
    def test_format_docstring_sphinx_style_field_body_is_blank(
        self,
        test_args,
        args,
    ):
        """Retain newline after the field list when it's in the original docstring.

        Also do not return a field body that is just whitespace.

        See docformatter_10.4.3.2, issue #224, and issue #239.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["issue_224"]["instring"]
        outstring = self.TEST_STRINGS["issue_224"]["outstring"]

        assert outstring == uut._do_format_docstring(
            INDENTATION,
            instring,
        )

        instring = self.TEST_STRINGS["issue_239"]["instring"]
        outstring = self.TEST_STRINGS["issue_239"]["outstring"]

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
                "",
            ]
        ],
    )
    def test_format_docstring_sphinx_style_field_name_included_wrap_length(
        self,
        test_args,
        args,
    ):
        """Should consider field name, not just field body, when wrapping.

        See issue #228.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["issue_228"]["instring"]
        outstring = self.TEST_STRINGS["issue_228"]["outstring"]

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
                "",
            ]
        ],
    )
    def test_format_docstring_sphinx_style_field_body_is_a_link(
        self,
        test_args,
        args,
    ):
        """Should not add a space after the field name when the body is a link.

        See docformatter_10.4.3.1, issue #229, issue #234, and issue #235.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["issue_229"]["instring"]
        outstring = self.TEST_STRINGS["issue_229"]["outstring"]

        assert outstring == uut._do_format_docstring(
            INDENTATION,
            instring,
        )

        instring = self.TEST_STRINGS["issue_229_2"]["instring"]
        outstring = self.TEST_STRINGS["issue_229_2"]["outstring"]

        assert outstring == uut._do_format_docstring(
            INDENTATION,
            instring,
        )

        instring = self.TEST_STRINGS["issue_234"]["instring"]
        outstring = self.TEST_STRINGS["issue_234"]["outstring"]

        assert outstring == uut._do_format_docstring(
            INDENTATION,
            instring,
        )

        instring = self.TEST_STRINGS["issue_235"]["instring"]
        outstring = self.TEST_STRINGS["issue_235"]["outstring"]

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
                "",
            ]
        ],
    )
    def test_format_docstring_sphinx_style_field_name_has_periods(
        self,
        test_args,
        args,
    ):
        """Should format sphinx field names containing a period.

        See issue #245.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["issue_245"]["instring"]
        outstring = self.TEST_STRINGS["issue_245"]["outstring"]

        assert outstring == uut._do_format_docstring(
            INDENTATION,
            instring,
        )
