# pylint: skip-file
# type: ignore
#
#       tests.test_string_functions.py is part of the docformatter project
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
"""Module for testing functions that manipulate text.

This module contains tests for string functions.  String functions are
those:

    reindent()
    find_shortest_indentation()
    normalize_line()
    normalize_line_endings()
    normalize_summary()
    remove_section_headers()
    split_first_sentence()
    split_summary()
    split_summary_and_description()
    strip_leading_blank_lines()
    strip_quotes()
    strip_newlines()
"""

# Third Party Imports
import pytest

# docformatter Package Imports
import docformatter


class TestIndenters:
    """Class for testing the indentation related function.

    Includes tests for:

        - reindent()
        - find_shortest_indentation()
    """

    @pytest.mark.unit
    def test_reindent(self):
        """Should add four spaces to the beginning of each docstring line."""
        assert """\
    This should be dedented.

    1. This too.
    2. And this.
""" == docformatter.reindent(
            """\
                    This should be dedented.

                    1. This too.
                    2. And this.
                """,
            indentation="    ",
        )

    @pytest.mark.unit
    def test_reindent_should_expand_tabs_to_indentation(self):
        """Should convert tabs to indentation type (four spaces)."""
        assert """\
    This should be dedented.

    1. This too.
    2. And this.
""" == docformatter.reindent(
            """\
                This should be dedented.

                1. This too.
        \t2. And this.
            """,
            indentation="    ",
        )

    @pytest.mark.unit
    def test_reindent_with_no_indentation_expand_tabs(self):
        """Should convert tabs to indentation type (four spaces)."""
        assert """\
The below should be indented with spaces:

        1. This too.
        2. And this.
""" == docformatter.reindent(
            """\
The below should be indented with spaces:

\t1. This too.
\t2. And this.
            """,
            indentation="",
        )

    @pytest.mark.unit
    def test_reindent_should_maintain_indentation(self):
        """Should make no changes with existing indentation same as type."""
        description = """\
    Parameters:

        - a
        - b
"""
        assert description == docformatter.reindent(
            description,
            indentation="    ",
        )

    @pytest.mark.unit
    def test_reindent_tab_indentation(self):
        """Should maintain tabs for the indentation."""
        assert """\
\tThis should be indented with a tab.

\tSo should this.
""" == docformatter.reindent(
            """\
\tThis should be indented with a tab.

\tSo should this.
            """,
            indentation="\t",
        )

    @pytest.mark.unit
    def testfind_shortest_indentation(self):
        """Should find the shortest indentation to be one space."""
        assert " " == docformatter.find_shortest_indentation(
            ["    ", " b", "  a"],
        )


class TestNormalizers:
    """Class for testing the string normalizing functions.

    Includes tests for:

        - normalize_line()
        - normalize_line_endings()
        - normalize_summary()
    """

    @pytest.mark.unit
    def test_normalize_summary(self):
        """Add period and strip spaces to line."""
        assert "This is a sentence." == docformatter.normalize_summary(
            "This is a sentence "
        )

    @pytest.mark.unit
    def test_normalize_summary_multiline(self):
        """Add period to line even with line return character."""
        assert "This \n\t is\na sentence." == docformatter.normalize_summary(
            "This \n\t is\na sentence "
        )

    @pytest.mark.unit
    def test_normalize_summary_with_different_punctuation(self):
        """Do not add period for line ending in question mark."""
        summary = "This is a question?"
        assert summary == docformatter.normalize_summary(summary)

    @pytest.mark.unit
    def test_normalize_summary_formatted_as_title(self):
        """Do not add period for markup title (line begins with #).

        See issue #56.
        """
        summary = "# This is a title"
        assert summary == docformatter.normalize_summary(summary)

    @pytest.mark.unit
    def test_normalize_summary_capitalize_first_letter(self):
        """Capitalize the first letter of the summary.

        See issue #76. See requirement docformatter_4.5.1.
        """
        assert (
            "This is a summary that needs to be capped."
            == docformatter.normalize_summary(
                "this is a summary that needs to be capped"
            )
        )

        assert "Don't lower case I'm." == docformatter.normalize_summary(
            "don't lower case I'm"
        )

    @pytest.mark.unit
    def test_normalize_summary_capitalize_first_letter_with_period(self):
        """Capitalize the first letter of the summary even when ends in period.

        See issue #184. See requirement docformatter_4.5.1.
        """
        assert (
            "This is a summary that needs to be capped."
            == docformatter.normalize_summary(
                "this is a summary that needs to be capped."
            )
        )

    @pytest.mark.unit
    def test_normalize_summary_dont_capitalize_first_letter_if_variable(self):
        """Capitalize the first word unless it looks like a variable."""
        assert (
            "num_iterations should not be capitalized in this summary."
            == docformatter.normalize_summary(
                "num_iterations should not be capitalized in this summary"
            )
        )


class TestSplitters:
    """Class for testing the string splitting function.

    Includes tests for:

        - split_first_sentence()
        - split_summary_and_description()
    """

    @pytest.mark.unit
    def test_split_first_sentence(self):
        """"""
        assert (
            "This is a sentence.",
            " More stuff. And more stuff.   .!@#$%",
        ) == docformatter.split_first_sentence(
            "This is a sentence. More stuff. And more stuff.   .!@#$%"
        )

        assert (
            "This e.g. sentence.",
            " More stuff. And more stuff.   .!@#$%",
        ) == docformatter.split_first_sentence(
            "This e.g. sentence. More stuff. And more stuff.   .!@#$%"
        )

        assert (
            "This is the first:",
            "\none\ntwo",
        ) == docformatter.split_first_sentence("This is the first:\none\ntwo")

    @pytest.mark.unit
    def test_split_one_sentence_summary(self):
        """A single sentence summary should be returned as is.

        See issue #283.
        """
        assert [
            "This is a sentence.",
            "",
        ] == docformatter.split_summary(["This is a sentence.", ""])

        assert [
            "This e.g. a sentence.",
            "",
        ] == docformatter.split_summary(["This e.g. a sentence.", ""])

    @pytest.mark.unit
    def test_split_multi_sentence_summary(self):
        """A multi-sentence summary should return only the first as the summary.

        See issue #283.
        """
        assert [
            "This is a sentence.",
            "",
            "This is another.",
        ] == docformatter.split_summary(["This is a sentence. This is another.", ""])

        assert [
            "This e.g. a sentence.",
            "",
            "This is another.",
        ] == docformatter.split_summary(["This e.g. a sentence. This is another.", ""])

    @pytest.mark.unit
    def test_split_summary_and_description(self):
        """"""
        assert (
            "This is the first.",
            "This is the second. This is the third.",
        ) == docformatter.split_summary_and_description(
            "This is the first. This is the second. This is the third."
        )

    @pytest.mark.unit
    def test_split_summary_and_description_complex(self):
        """"""
        assert (
            "This is the first",
            "\nThis is the second. This is the third.",
        ) == docformatter.split_summary_and_description(
            "This is the first\n\nThis is the second. This is the third."
        )

    @pytest.mark.unit
    def test_split_summary_and_description_more_complex(self):
        """"""
        assert (
            "This is the first.",
            "This is the second. This is the third.",
        ) == docformatter.split_summary_and_description(
            "This is the first.\nThis is the second. This is the third."
        )

    @pytest.mark.unit
    def test_split_summary_and_description_with_list(self):
        """"""
        assert (
            "This is the first",
            "- one\n- two",
        ) == docformatter.split_summary_and_description(
            "This is the first\n- one\n- two"
        )

    @pytest.mark.unit
    def test_split_summary_and_description_with_list_of_parameters(self):
        """"""
        assert (
            "This is the first",
            "one - one\ntwo - two",
        ) == docformatter.split_summary_and_description(
            "This is the first\none - one\ntwo - two"
        )

    @pytest.mark.unit
    def test_split_summary_and_description_with_capital(self):
        """"""
        assert (
            "This is the first\nWashington",
            "",
        ) == docformatter.split_summary_and_description("This is the first\nWashington")

    @pytest.mark.unit
    def test_split_summary_and_description_with_list_on_other_line(self):
        """"""
        assert (
            "Test",
            "    test\n    @blah",
        ) == docformatter.split_summary_and_description(
            """\
    Test
    test
    @blah
"""
        )

    @pytest.mark.unit
    def test_split_summary_and_description_with_other_symbol(self):
        """"""
        assert (
            "This is the first",
            "@ one\n@ two",
        ) == docformatter.split_summary_and_description(
            "This is the first\n@ one\n@ two"
        )

    @pytest.mark.unit
    def test_split_summary_and_description_with_colon(self):
        """"""
        assert (
            "This is the first:",
            "one\ntwo",
        ) == docformatter.split_summary_and_description("This is the first:\none\ntwo")

    @pytest.mark.unit
    def test_split_summary_and_description_with_exclamation(self):
        """"""
        assert (
            "This is the first!",
            "one\ntwo",
        ) == docformatter.split_summary_and_description("This is the first!\none\ntwo")

    @pytest.mark.unit
    def test_split_summary_and_description_with_question_mark(self):
        """"""
        assert (
            "This is the first?",
            "one\ntwo",
        ) == docformatter.split_summary_and_description("This is the first?\none\ntwo")

    @pytest.mark.unit
    def test_split_summary_and_description_with_quote(self):
        """"""
        assert (
            'This is the first\n"one".',
            "",
        ) == docformatter.split_summary_and_description('This is the first\n"one".')

        assert (
            "This is the first\n'one'.",
            "",
        ) == docformatter.split_summary_and_description("This is the first\n'one'.")

        assert (
            "This is the first\n``one``.",
            "",
        ) == docformatter.split_summary_and_description("This is the first\n``one``.")

    @pytest.mark.unit
    def test_split_summary_and_description_with_punctuation(self):
        """"""
        assert (
            (
                """\
Try this and this and this and this and this and this and this at
    https://example.com/""",
                """
    Parameters
    ----------
    email : string""",
            )
            == docformatter.split_summary_and_description(
                """\
    Try this and this and this and this and this and this and this at
    https://example.com/

    Parameters
    ----------
    email : string
"""
            )
        )

    @pytest.mark.unit
    def test_split_summary_and_description_without_punctuation(self):
        """"""
        assert (
            (
                """\
Try this and this and this and this and this and this and this at
    this other line""",
                """
    Parameters
    ----------
    email : string""",
            )
            == docformatter.split_summary_and_description(
                """\
    Try this and this and this and this and this and this and this at
    this other line

    Parameters
    ----------
    email : string
"""
            )
        )

    @pytest.mark.unit
    def test_split_summary_and_description_with_abbreviation(self):
        """"""
        for text in [
            "Test e.g. now",
            "Test foo, bar, etc. now",
            "Test i.e. now",
            "Test Dr. now",
            "Test Mr. now",
            "Test Mrs. now",
            "Test Ms. now",
        ]:
            assert (text, "") == docformatter.split_summary_and_description(text)

    @pytest.mark.unit
    def test_split_summary_and_description_with_url(self):
        """Retain URL on second line with summary."""
        text = '''\
"""Sequence of package managers as defined by `XKCD #1654: Universal Install Script
<https://xkcd.com/1654/>`_.

See the corresponding :issue:`implementation rationale in issue #10 <10>`.
"""\
'''
        assert (
            '"""Sequence of package managers as defined by `XKCD #1654: Universal Install Script\n'
            "<https://xkcd.com/1654/>`_.",
            "\nSee the corresponding :issue:`implementation rationale in issue #10 <10>`."
            '\n"""',
        ) == docformatter.split_summary_and_description(text)


class TestStrippers:
    """Class for testing the string stripping functions.

    Includes tests for:

        - strip_leading_blank_lines()
        - strip_quotes()
        - strip_newlines()
        - strip_docstring()
    """

    @pytest.mark.unit
    def test_remove_section_header(self):
        """Remove section header directives."""
        assert "foo\nbar\n" == docformatter.remove_section_header("----\nfoo\nbar\n")

        line = "foo\nbar\n"
        assert line == docformatter.remove_section_header(line)

        line = "    \nfoo\nbar\n"
        assert line == docformatter.remove_section_header(line)
