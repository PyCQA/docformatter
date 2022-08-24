# pylint: skip-file
# type: ignore
#
#       tests.test_format_code.py is part of the docformatter project
#
# Copyright (C) 2012-2019 Steven Myint
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
"""Module for testing the Formattor._do_format_code() function."""

# Standard Library Imports
import sys

# Third Party Imports
import pytest

# docformatter Package Imports
import docformatter
from docformatter import Formatter


class TestFormatCode:
    """Class for testing _format_code() with no arguments."""

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

        source = '''\
x = """This
is
not a
docstring."""
'''
        assert source == uut._format_code(source)

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

        assert "" == uut._format_code("")
        assert "" == uut._format_code("")

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

        assert '''\
def foo():
\t"""Hello foo."""
\tif True:
\t\tx = 1
''' == uut._format_code(
            '''\
def foo():
\t"""
\tHello foo.
\t"""
\tif True:
\t\tx = 1
'''
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

        assert '''\
def foo():
\t"""Hello foo."""
\tif True:
\t    x = 1
''' == uut._format_code(
            '''\
def foo():
\t"""
\tHello foo.
\t"""
\tif True:
\t    x = 1
'''
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

        assert r'''def foo():
    """Hello foo."""
    x = \
            1
''' == uut._format_code(
            r'''def foo():
    """
    Hello foo.
    """
    x = \
            1
'''
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

        assert r'''
def foo():
    """Hello foo."""
    # My comment
    # My comment with escape \
    123
'''.lstrip() == uut._format_code(
            r'''
def foo():
    """
    Hello foo.
    """
    # My comment
    # My comment with escape \
    123
'''.lstrip()
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_code_with_escaped_newline_in_inline_comment(
        self, test_args, args
    ):
        """Should leave code with inline comment as is."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        assert r'''
def foo():
    """Hello foo."""
    def test_method_no_chr_92(): the501(92) # \
'''.lstrip() == uut._format_code(
            r'''
def foo():
    """
    Hello foo.
    """
    def test_method_no_chr_92(): the501(92) # \
'''.lstrip()
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_code_raw_docstring_double_quotes(self, test_args, args):
        """Should format raw docstrings with triple double quotes.

        See requirement PEP_257_2.  See issue #54 for request to handle
        raw docstrings.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        assert '''\
def foo():
    r"""Hello raw foo."""
''' == uut._format_code(
            '''\
def foo():
    r"""
    Hello raw foo.
    """
'''
        )

        assert '''\
def foo():
    R"""Hello Raw foo."""
''' == uut._format_code(
            '''\
def foo():
    R"""
    Hello Raw foo.
    """
'''
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_code_raw_docstring_single_quotes(self, test_args, args):
        """Should format raw docstrings with triple single quotes.

        See requirement PEP_257_2.  See issue #54 for request to handle
        raw docstrings.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        assert '''\
def foo():
    r"""Hello raw foo."""
''' == uut._format_code(
            """\
def foo():
    r'''
    Hello raw foo.
    '''
"""
        )

        assert '''\
def foo():
    R"""Hello Raw foo."""
''' == uut._format_code(
            """\
def foo():
    R'''
    Hello Raw foo.
    '''
"""
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_code_unicode_docstring_double_quotes(
        self, test_args, args
    ):
        """Should format unicode docstrings with triple double quotes.

        See requirement PEP_257_3.  See issue #54 for request to handle
        raw docstrings.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        assert '''\
def foo():
    u"""Hello unicode foo."""
''' == uut._format_code(
            '''\
def foo():
    u"""
    Hello unicode foo.
    """
'''
        )

        assert '''\
def foo():
    U"""Hello Unicode foo."""
''' == uut._format_code(
            '''\
def foo():
    U"""
    Hello Unicode foo.
    """
'''
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_code_unicode_docstring_single_quotes(
        self, test_args, args
    ):
        """Should format unicode docstrings with triple single quotes.

        See requirement PEP_257_3.  See issue #54 for request to handle
        raw docstrings.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        assert '''\
def foo():
    u"""Hello unicode foo."""
''' == uut._format_code(
            """\
def foo():
    u'''
    Hello unicode foo.
    '''
"""
        )

        assert '''\
def foo():
    U"""Hello Unicode foo."""
''' == uut._format_code(
            """\
def foo():
    U'''
    Hello Unicode foo.
    '''
"""
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

        code = """\
def foo():
    '''Hello foo. \"\"\"abc\"\"\"
    '''
"""
        assert code == uut._format_code(code)

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

        assert '''\
def foo():
    """Hello foo.

    This is a docstring.
    """
''' == uut._format_code(
            '''\
def foo():
    """
    Hello foo.
    This is a docstring.
    """
'''
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_code_with_multiple_sentences_same_line(
        self, test_args, args
    ):
        """Should create multi-line docstring from multiple sentences."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        assert '''\
def foo():
    """Hello foo.

    This is a docstring.
    """
''' == uut._format_code(
            '''\
def foo():
    """
    Hello foo. This is a docstring.
    """
'''
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

        assert '''\
def foo():
    """Hello foo.

    This is a docstring.
    """
''' == uut._format_code(
            '''\
def foo():
    """
    Hello
    foo. This is a docstring.
    """
'''
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

        assert '''\
def foo():
    """Hello foo and this is a docstring.

    More stuff.
    """
''' == uut._format_code(
            '''\
def foo():
    """
    Hello
    foo and this is a docstring.

    More stuff.
    """
'''
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

        assert '''\
def foo():
    """Hello foo and this is a docstring.

    More stuff.
    """
''' == uut._format_code(
            (
                '''\
def foo():
    """
    Hello
    foo and this is a docstring.\t

    More stuff.\t
    """
'''
            )
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

        assert '''\
def foo():
    """Test.

    one - first
    two - second
    """
''' == uut._format_code(
            (
                '''\
def foo():
    """Test
    one - first
    two - second
    """
'''
            )
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_ignore_code_with_single_quote(self, test_args, args):
        """Single single quote on first line of code should remain untouched.

        See requirement PEP_257_1.  See issue #66 for example of
        docformatter breaking code when encountering single quote.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        assert """\
def foo():
    'Just a regular string'
""" == uut._format_code(
            """\
def foo():
    'Just a regular string'
"""
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_ignore_code_with_double_quote(self, test_args, args):
        """Single double quotes on first line of code should remain untouched.

        See requirement PEP_257_1.  See issue #66 for example of
        docformatter breaking code when encountering single quote.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        assert """\
def foo():
    "Just a regular string"
""" == uut._format_code(
            """\
def foo():
    "Just a regular string"
"""
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_code_should_skip_nested_triple_quotes(
        self, test_args, args
    ):
        """Should ignore triple quotes nested in a string."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        line = '''\
def foo():
    'Just a """foo""" string'
'''
        assert line == uut._format_code(line)

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

        assert '''\
def foo():
    x = """Just a regular string. Alpha."""
''' == uut._format_code(
            '''\
def foo():
    x = """Just a regular string. Alpha."""
'''
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

        assert '''\
def foo():
    """Hello foo and this is a docstring.

    More stuff.
    """
    x = """My non-docstring
    This should not be touched."""

    """More stuff
    that should not be
    touched\t"""
''' == uut._format_code(
            '''\
def foo():
    """
    Hello
    foo and this is a docstring.

    More stuff.
    """
    x = """My non-docstring
    This should not be touched."""

    """More stuff
    that should not be
    touched\t"""
'''
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

        assert '"""\n' == uut._format_code('"""\n')

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

        assert '"""\r' == uut._format_code('"""\r')

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_code_with_syntax_error_case_slash_r_slash_n(
        self, test_args, args
    ):
        """Should ignore single triple quote followed by return, newline."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        assert '"""\r\n' == uut._format_code('"""\r\n')

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_code_dominant_line_ending_style_preserved(
        self, test_args, args
    ):
        """Should retain carriage return line endings."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        goes_in = '''\
def foo():\r
    """\r
    Hello\r
    foo. This is a docstring.\r
    """\r
'''
        assert '''\
def foo():\r
    """Hello foo.\r
\r
    This is a docstring.\r
    """\r
''' == uut._do_format_code(
            goes_in
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_code_additional_empty_line_before_doc(
        self, test_args, args
    ):
        """Should remove empty line between function def and docstring.

        See issue #51.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        assert (
            '\n\n\ndef my_func():\n"""Summary of my function."""\npass'
            == uut._do_format_code(
                '\n\n\ndef my_func():\n\n"""Summary of my function."""\npass'
            )
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_code_extra_newline_following_comment(
        self, test_args, args
    ):
        """Should remove extra newline following in-line comment.

        See issue #51.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        docstring = '''\
def crash_rocket(location):    # pragma: no cover

    """This is a docstring following an in-line comment."""
    return location'''

        assert '''\
def crash_rocket(location):    # pragma: no cover
    """This is a docstring following an in-line comment."""
    return location''' == uut._do_format_code(
            docstring
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

        docstring = (
            "def pytest_addoption(parser: pytest.Parser) -> "
            "None:\n    register_toggle.pytest_addoption(parser)\n"
        )
        assert docstring == uut._do_format_code(docstring)

        docstring = (
            "def pytest_addoption(parser: pytest.Parser) -> "
            "None:    # pragma: no cover\n    "
            "register_toggle.pytest_addoption(parser)\n"
        )
        assert docstring == uut._do_format_code(docstring)

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

        docstring = '''\
class TestClass:
    """This is a class docstring.

    :cvar test_int: a class attribute.
    ..py.method: big_method()
    """
'''
        assert docstring == uut._do_format_code('''\
class TestClass:
    """This is a class docstring.
    :cvar test_int: a class attribute.
    ..py.method: big_method()
    """
''')


class TestFormatCodeRanges:
    """Class for testing _format_code() with the line_range or length_range
    arguments."""

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [["--range", "1", "1", ""]])
    def test_format_code_range_miss(self, test_args, args):
        """Should leave docstrings outside line range as is."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        assert '''\
    def f(x):
        """  This is a docstring. That should be on more lines"""
        pass
    def g(x):
        """  Badly indented docstring"""
        pass''' == uut._format_code(
            '''\
    def f(x):
        """  This is a docstring. That should be on more lines"""
        pass
    def g(x):
        """  Badly indented docstring"""
        pass'''
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [["--range", "1", "2", ""]])
    def test_format_code_range_hit(self, test_args, args):
        """Should format docstrings within line_range."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        assert '''\
def f(x):
    """This is a docstring.

    That should be on more lines
    """
    pass
def g(x):
    """  Badly indented docstring"""
    pass''' == uut._format_code(
            '''\
def f(x):
    """  This is a docstring. That should be on more lines"""
    pass
def g(x):
    """  Badly indented docstring"""
    pass'''
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [["--docstring-length", "1", "1", ""]])
    def test_format_code_docstring_length(self, test_args, args):
        """Should leave docstrings outside length_range as is."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        assert '''\
def f(x):
    """This is a docstring.


    That should be on less lines
    """
    pass
def g(x):
    """Badly indented docstring."""
    pass''' == uut._format_code(
            '''\
def f(x):
    """This is a docstring.


    That should be on less lines
    """
    pass
def g(x):
    """  Badly indented docstring"""
    pass'''
        )


class TestDoFormatCode:
    """Class for testing _do_format_code() with no arguments."""

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

        assert '''\
def foo():
    """Hello foo."""
''' == uut._do_format_code(
            '''\
def foo():
    """
    Hello foo.
    """
'''
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

        assert '''\
#!/usr/env/bin python
"""This is a module docstring.

1. One
2. Two
"""

"""But
this
is
not."""
''' == uut._do_format_code(
            '''\
#!/usr/env/bin python
"""This is
a module
docstring.

1. One
2. Two
"""

"""But
this
is
not."""
'''
        )
