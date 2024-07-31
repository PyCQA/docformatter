# pylint: skip-file
# type: ignore
#
#       tests.test_syntax_functions.py is part of the docformatter project
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
"""Module for testing functions that deal with syntax.

This module contains tests for syntax functions.  Syntax functions are
those:

    do_clean_link()
    do_find_directives()
    do_find_links()
    do_skip_link()
"""
import textwrap

# Third Party Imports
import pytest

# docformatter Package Imports
import docformatter
from docformatter import do_split_description


class TestURLHandlers:
    """Class for testing the URL handling functions.

    Includes tests for:

        - do_clean_link()
        - do_find_links()
        - do_skip_link()
    """

    @pytest.mark.unit
    def test_find_in_line_link(self):
        """Should find link pattern in a text block."""
        assert [(53, 162)] == docformatter.do_find_links(
            "The text file can be retrieved via the Chrome plugin `Get \
Cookies.txt <https://chrome.google.com/webstore/detail/get-\
cookiestxt/bgaddhkoddajcdgocldbbfleckgcbcid>` while browsing."
        )
        assert [(95, 106), (110, 123)] == docformatter.do_find_links(
            "``pattern`` is considered as an URL only if it is parseable as such\
            and starts with ``http://`` or ``https://``."
        )

    @pytest.mark.unit
    def test_skip_link_with_manual_wrap(self):
        """Should skip a link that has been manually wrapped by the user."""
        assert docformatter.do_skip_link(
            "``pattern`` is considered as an URL only if it is parseable as such\
            and starts with ``http://`` or ``https://``.",
            (95, 106),
        )
        assert docformatter.do_skip_link(
            "``pattern`` is considered as an URL only if it is parseable as such\
            and starts with ``http://`` or ``https://``.",
            (110, 123),
        )

    @pytest.mark.unit
    def test_do_clean_link(self):
        """Should remove line breaks from links."""
        assert (
            "    `Get Cookies.txt <https://chrome.google.com/webstore/detail/get-cookiestxt/bgaddhkoddajcdgocldbbfleckgcbcid>`"
        ) == docformatter.do_clean_url(
            "`Get \
Cookies.txt <https://chrome.google.com/webstore/detail/get-\
cookiestxt/bgaddhkoddajcdgocldbbfleckgcbcid>`",
            "    ",
        )

        assert (
            "    `custom types provided by Click        <https://click.palletsprojects.com/en/8.1.x/api/?highlight=intrange#types>`_."
        ) == docformatter.do_clean_url(
            "`custom types provided by Click\
        <https://click.palletsprojects.com/en/8.1.x/api/?highlight=intrange#types>`_.",
            "    ",
        )


class TestreSTHandlers:
    """Class for testing the reST directive handling functions.

    Includes tests for:

        - do_find_directives()
    """

    @pytest.mark.unit
    def test_find_in_line_directives(self):
        """Should find reST directieves in a text block."""
        assert docformatter.do_find_directives(
            "These are some reST directives that need  to be retained even if it means not wrapping the line they are found on.\
         Constructs and returns a :class:`QuadraticCurveTo <QuadraticCurveTo>`.\
         Register ``..click:example::`` and ``.. click:run::`` directives, augmented with ANSI coloring."
        )

    @pytest.mark.unit
    def test_find_double_dot_directives(self):
        """Should find reST directives preceeded by .."""
        assert docformatter.do_find_directives(
            ".. _linspace API: https://numpy.org/doc/stable/reference/generated/numpy.linspace.html\
             .. _arange API: https://numpy.org/doc/stable/reference/generated/numpy.arange.html\
             .. _logspace API: https://numpy.org/doc/stable/reference/generated/numpy.logspace.html"
        )

        assert docformatter.do_find_directives(
            "``pattern`` is considered as an URL only if it is parseable as such"
            "and starts with ``http://`` or ``https://``."
            ""
            ".. important::"
            ""
            "This is a straight `copy of the functools.cache implementation"
            "<https://github.com/python/cpython/blob/55a26de6ba938962dc23f2495723cf0f4f3ab7c6/Lib/functools.py#L647-L653>`_,"
            "hich is only `available in the standard library starting with Python v3.9"
            "<https://docs.python.org/3/library/functools.html?highlight=caching#functools.cache>`."
        )

    @pytest.mark.unit
    def test_find_double_backtick_directives(self):
        """Should find reST directives preceeded by ``."""
        assert docformatter.do_find_directives(
            "By default we choose to exclude:"
            ""
            "``Cc``"
            "   Since ``mailman`` apparently `sometimes trims list members"
            "   <https://mail.python.org/pipermail/mailman-developers/2002-September/013233.html>`_"
            "   from the ``Cc`` header to avoid sending duplicates. Which means that copies of mail"
            "   reflected back from the list server will have a different ``Cc`` to the copy saved by"
            "   the MUA at send-time."
            ""
            "``Bcc``"
            "    Because copies of the mail saved by the MUA at send-time will have ``Bcc``, but copies"
            "    reflected back from the list server won't."
            ""
            "``Reply-To``"
            "    Since a mail could be ``Cc``'d to two lists with different ``Reply-To`` munging"
            "options set."
        )


class TestSplitDescription:
    """Class for testing the function to process the description

    Includes tests for:
        - do_split_description()

    """
    med_str = "m"*40  # long enough that 2 won't fit on a line
    indent = "    "

    def do_test(self, text):
        return do_split_description(textwrap.dedent(text), self.indent, 72, "sphinx")

    def indent_all(self, strs):
        return [self.indent + s for s in strs]

    @pytest.mark.unit
    def test_split_description_url_outside_param(self):
        assert self.do_test(
            f"""\
            {self.med_str} https://{self.med_str}
            :param a: {self.med_str}
            """
        ) == self.indent_all([
            self.med_str,
            f"https://{self.med_str}",
            f":param a: {self.med_str}",
        ])

    @pytest.mark.unit
    def test_split_description_single_url_in_param(self):
        assert self.do_test(
            f"""\
            {self.med_str}
            :param a: {self.med_str} https://{self.med_str}a
            """
        ) == self.indent_all([
            self.med_str,
            f":param a: {self.med_str}",
            self.indent + f"https://{self.med_str}a",
        ])

    @pytest.mark.unit
    def test_split_description_single_url_in_multiple_params(self):
        assert self.do_test(
            f"""\
            {self.med_str}
            :param a: {self.med_str} https://{self.med_str}a
            :param b: {self.med_str} https://{self.med_str}b
            """
        ) == self.indent_all([
            self.med_str,
            f":param a: {self.med_str}",
            self.indent + f"https://{self.med_str}a",
            f":param b: {self.med_str}",
            self.indent + f"https://{self.med_str}b",
        ])

    @pytest.mark.unit
    def test_split_description_multiple_urls_in_param(self):
        assert self.do_test(
            f"""\
            {self.med_str}
            :param a: {self.med_str} https://{self.med_str}0 https://{self.med_str}1
            """
        ) == self.indent_all([
            self.med_str,
            f":param a: {self.med_str}",
            self.indent + f"https://{self.med_str}0",
            self.indent + f"https://{self.med_str}1",
        ])
