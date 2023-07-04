# pylint: skip-file
# type: ignore
#
#       tests.test_format_urls.py is part of the docformatter project
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


class TestFormatWrapURL:
    """Class for testing _do_format_docstring() with line wrapping and URLs."""

    with open("tests/_data/string_files/format_urls.toml", "rb") as f:
        TEST_STRINGS = tomllib.load(f)

    @pytest.mark.unit
    @pytest.mark.parametrize(
        "args",
        [["--wrap-descriptions", "72", ""]],
    )
    def test_format_docstring_with_inline_links(
        self,
        test_args,
        args,
    ):
        """Preserve links instead of wrapping them.

        See requirement docformatter_10.1.3.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["inline"]["instring"]
        outstring = self.TEST_STRINGS["inline"]["outstring"]

        assert outstring == uut._do_format_docstring(
            INDENTATION,
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize(
        "args",
        [["--wrap-descriptions", "72", ""]],
    )
    def test_format_docstring_with_short_inline_link(
        self,
        test_args,
        args,
    ):
        """Short in-line links will remain untouched.

        See requirement docformatter_10.1.3.1.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["inline"]["short"]["instring"]
        outstring = self.TEST_STRINGS["inline"]["short"]["outstring"]

        assert outstring == uut._do_format_docstring(
            INDENTATION,
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize(
        "args",
        [["--wrap-descriptions", "72", ""]],
    )
    def test_format_docstring_with_long_inline_link(
        self,
        test_args,
        args,
    ):
        """Should move long in-line links to line by themselves."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["inline"]["long"]["instring"]
        outstring = self.TEST_STRINGS["inline"]["long"]["outstring"]

        assert outstring == uut._do_format_docstring(
            INDENTATION,
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize(
        "args",
        [["--wrap-descriptions", "72", ""]],
    )
    def test_format_docstring_with_only_link(
        self,
        test_args,
        args,
    ):
        """Should format docstring containing only a link."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["only"]["link"]["instring"]
        outstring = self.TEST_STRINGS["only"]["link"]["outstring"]

        assert outstring == uut._do_format_docstring(
            INDENTATION,
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize(
        "args",
        [["--wrap-descriptions", "72", ""]],
    )
    def test_format_docstring_with_target_links(
        self,
        test_args,
        args,
    ):
        """Preserve links instead of wrapping them.

        See requirement docformatter_10.1.3, issue #75, issue #145.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["issue_75"]["instring"]
        outstring = self.TEST_STRINGS["issue_75"]["outstring"]

        assert outstring == uut._do_format_docstring(
            INDENTATION,
            instring,
        )

        instring = self.TEST_STRINGS["issue_145"]["instring"]
        outstring = self.TEST_STRINGS["issue_145"]["outstring"]

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
                "",
            ]
        ],
    )
    def test_format_docstring_with_simple_link(
        self,
        test_args,
        args,
    ):
        """Preserve links instead of wrapping them.

        See requirement docformatter_10.1.3, issue #75.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["issue_75_2"]["instring"]
        outstring = self.TEST_STRINGS["issue_75_2"]["outstring"]

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
                "",
            ]
        ],
    )
    def test_format_docstring_with_short_link(
        self,
        test_args,
        args,
    ):
        """Short links will remain untouched.

        See requirement docformatter_10.1.3, issue #75.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["issue_75_3"]["instring"]
        outstring = self.TEST_STRINGS["issue_75_3"]["outstring"]

        assert outstring == uut._do_format_docstring(
            INDENTATION,
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize(
        "args",
        [["--wrap-descriptions", "72", ""]],
    )
    def test_format_docstring_with_inline_link_retain_spaces(
        self,
        test_args,
        args,
    ):
        """In-line links shouldn't remove blank spaces between words.

        See issue #140.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["issue_140"]["instring"]
        outstring = self.TEST_STRINGS["issue_140"]["outstring"]

        assert outstring == uut._do_format_docstring(
            INDENTATION,
            instring,
        )

        instring = self.TEST_STRINGS["issue_140_2"]["instring"]
        outstring = self.TEST_STRINGS["issue_140_2"]["outstring"]

        assert outstring == uut._do_format_docstring(
            INDENTATION,
            instring,
        )

        instring = self.TEST_STRINGS["issue_140_3"]["instring"]
        outstring = self.TEST_STRINGS["issue_140_3"]["outstring"]

        assert outstring == uut._do_format_docstring(
            INDENTATION,
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize(
        "args",
        [["--wrap-descriptions", "72", ""]],
    )
    def test_format_docstring_link_after_colon(
        self,
        test_args,
        args,
    ):
        """In-line links shouldn't be put on next line when following a colon.

        See issue #150.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["issue_150"]["instring"]
        outstring = self.TEST_STRINGS["issue_150"]["outstring"]

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
                "",
            ]
        ],
    )
    def test_format_docstring_keep_inline_link_together(
        self,
        test_args,
        args,
    ):
        """Keep in-line links together with the display text.

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
    @pytest.mark.parametrize(
        "args",
        [
            [
                "--wrap-descriptions",
                "88",
                "",
            ]
        ],
    )
    def test_format_docstring_keep_inline_link_together_two_paragraphs(
        self,
        test_args,
        args,
    ):
        """Keep in-line links together with the display text.

        If there is another paragraph following the in-line link, don't strip the
        newline in between.

        See issue #157.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["issue_157_2"]["instring"]
        outstring = self.TEST_STRINGS["issue_157_2"]["outstring"]

        assert outstring == uut._do_format_docstring(
            INDENTATION,
            instring,
        )

        instring = self.TEST_STRINGS["issue_157_3"]["instring"]
        outstring = self.TEST_STRINGS["issue_157_3"]["outstring"]

        assert outstring == uut._do_format_docstring(
            INDENTATION,
            instring,
        )

        instring = self.TEST_STRINGS["issue_157_4"]["instring"]
        outstring = self.TEST_STRINGS["issue_157_4"]["outstring"]

        assert outstring == uut._do_format_docstring(
            INDENTATION,
            instring,
        )

        instring = self.TEST_STRINGS["issue_157_5"]["instring"]
        outstring = self.TEST_STRINGS["issue_157_5"]["outstring"]

        assert outstring == uut._do_format_docstring(
            INDENTATION,
            instring,
        )

        instring = self.TEST_STRINGS["issue_157_6"]["instring"]
        outstring = self.TEST_STRINGS["issue_157_6"]["outstring"]

        assert outstring == uut._do_format_docstring(
            INDENTATION,
            instring,
        )

        instring = self.TEST_STRINGS["issue_157_7"]["instring"]
        outstring = self.TEST_STRINGS["issue_157_7"]["outstring"]

        assert outstring == uut._do_format_code(
            instring,
        )

        instring = self.TEST_STRINGS["issue_157_8"]["instring"]
        outstring = self.TEST_STRINGS["issue_157_8"]["outstring"]

        assert outstring == uut._do_format_code(
            instring,
        )

        instring = self.TEST_STRINGS["issue_157_9"]["instring"]
        outstring = self.TEST_STRINGS["issue_157_9"]["outstring"]

        assert outstring == uut._do_format_code(
            instring,
        )

        instring = self.TEST_STRINGS["issue_157_10"]["instring"]
        outstring = self.TEST_STRINGS["issue_157_10"]["outstring"]

        assert outstring == uut._do_format_code(
            instring,
        )

        instring = self.TEST_STRINGS["issue_157_11"]["instring"]
        outstring = self.TEST_STRINGS["issue_157_11"]["outstring"]

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
    def test_format_docstring_link_no_delete_words(
        self,
        test_args,
        args,
    ):
        """Should not delete words when wrapping a URL.

        See issue #159.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["issue_159"]["instring"]
        outstring = self.TEST_STRINGS["issue_159"]["outstring"]

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
    def test_format_docstring_link_no_newline_after_link(
        self,
        test_args,
        args,
    ):
        """Links should have no newline before or after them.

        See issue #180.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["issue_180"]["instring"]
        outstring = self.TEST_STRINGS["issue_180"]["outstring"]

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
                "",
            ]
        ],
    )
    def test_format_docstring_with_only_link_in_description(
        self,
        test_args,
        args,
    ):
        """No index error when only link in long description.

        See issue #189.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["issue_189"]["instring"]
        outstring = self.TEST_STRINGS["issue_189"]["outstring"]

        assert outstring == uut._do_format_docstring(
            INDENTATION,
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_docstring_no_indent_string_on_newline(
        self,
        test_args,
        args,
    ):
        """Should not add the indentation string to a newline.

        See issue #199.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["issue_199"]["instring"]
        outstring = self.TEST_STRINGS["issue_199"]["outstring"]

        assert outstring == uut._do_format_docstring(
            INDENTATION,
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_docstring_with_short_anonymous_link(
        self,
        test_args,
        args,
    ):
        """Anonymous link references should not be wrapped into the link.

        See issue #210.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["issue_210"]["instring"]
        outstring = self.TEST_STRINGS["issue_210"]["outstring"]

        assert outstring == uut._do_format_docstring(
            INDENTATION,
            instring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_docstring_with_quoted_link(
        self,
        test_args,
        args,
    ):
        """Anonymous link references should not be wrapped into the link.

        See issue #218.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        instring = self.TEST_STRINGS["issue_218"]["instring"]
        outstring = self.TEST_STRINGS["issue_218"]["outstring"]

        assert outstring == uut._do_format_docstring(
            INDENTATION,
            instring,
        )
