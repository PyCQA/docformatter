# pylint: skip-file
# type: ignore
#
#       tests.test_strip_docstring.py is part of the docformatter project
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
"""Module for testing the _do_strip_docstring() method."""


# Standard Library Imports
import sys

# Third Party Imports
import pytest

# docformatter Package Imports
from docformatter import Formatter

INDENTATION = "    "


class TestStripDocstring:
    """Class for testing _do_strip_docstring()."""

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_strip_docstring(
        self,
        test_args,
        args,
    ):
        """Strip triple double quotes from docstring."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        docstring, open_quote = uut._do_strip_docstring(
            '''
    """Hello.

    """

    '''
        )
        assert docstring == "Hello."
        assert open_quote == '"""'

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_strip_docstring_with_triple_single_quotes(
        self,
        test_args,
        args,
    ):
        """Strip triple single quotes from docstring."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        docstring, open_quote = uut._do_strip_docstring(
            """
    '''Hello.

    '''

    """
        )
        assert docstring == "Hello."
        assert open_quote == '"""'

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_strip_docstring_with_empty_string(
        self,
        test_args,
        args,
    ):
        """Return series of six double quotes when passed empty string."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        docstring, open_quote = uut._do_strip_docstring('""""""')
        assert not docstring
        assert open_quote == '"""'

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_strip_docstring_with_raw_string(
        self,
        test_args,
        args,
    ):
        """Return docstring and raw open quote."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        docstring, open_quote = uut._do_strip_docstring('r"""foo"""')
        assert docstring == "foo"
        assert open_quote == 'r"""'

        docstring, open_quote = uut._do_strip_docstring("R'''foo'''")
        assert docstring == "foo"
        assert open_quote == 'R"""'

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_strip_docstring_with_unicode_string(
        self,
        test_args,
        args,
    ):
        """Return docstring and unicode open quote."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        docstring, open_quote = uut._do_strip_docstring("u'''foo'''")
        assert docstring == "foo"
        assert open_quote == 'u"""'

        docstring, open_quote = uut._do_strip_docstring('U"""foo"""')
        assert docstring == "foo"
        assert open_quote == 'U"""'

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_strip_docstring_with_unknown(
        self,
        test_args,
        args,
    ):
        """Raise ValueError with single quotes."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        with pytest.raises(ValueError):
            uut._do_strip_docstring("foo")

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_strip_docstring_with_single_quotes(
        self,
        test_args,
        args,
    ):
        """Raise ValueError when strings begin with single single quotes.

        See requirement PEP_257_1.  See issue #66 for example of docformatter breaking
        code when encountering single quote.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        with pytest.raises(ValueError):
            uut._do_strip_docstring("'hello\\''")

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_strip_docstring_with_double_quotes(
        self,
        test_args,
        args,
    ):
        """Raise ValueError when strings begin with single double quotes.

        See requirement PEP_257_1.  See issue #66 for example of docformatter breaking
        code when encountering single quote.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        with pytest.raises(ValueError):
            uut._do_strip_docstring('"hello\\""')
