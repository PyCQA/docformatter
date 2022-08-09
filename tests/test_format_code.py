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
"""Module for testing the format_code() function."""

# Third Party Imports
import pytest

# docformatter Package Imports
import docformatter


class TestFormatCode:
    """Class for testing format_code() with no arguments."""

    @pytest.mark.unit
    def test_format_code(self):
        """Should place one-liner on single line."""
        assert '''\
def foo():
    """Hello foo."""
''' == docformatter.format_code(
            '''\
def foo():
    """
    Hello foo.
    """
'''
        )

    @pytest.mark.unit
    def test_format_code_with_module_docstring(self):
        """Should format module docstrings."""
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
''' == docformatter.format_code(
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

    @pytest.mark.unit
    def test_format_code_should_ignore_non_docstring(self):
        """Shoud ignore triple quoted strings that are assigned values."""
        source = '''\
x = """This
is
not."""
'''
        assert source == docformatter.format_code(source)

    @pytest.mark.unit
    def test_format_code_with_empty_string(self):
        """Should do nothing with an empty string."""
        assert "" == docformatter.format_code("")
        assert "" == docformatter.format_code("")

    @pytest.mark.unit
    def test_format_code_with_tabs(self):
        """Should retain tabbed indentation."""
        assert '''\
def foo():
\t"""Hello foo."""
\tif True:
\t\tx = 1
''' == docformatter.format_code(
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
    def test_format_code_with_mixed_tabs(self):
        """Should retain mixed tabbed and spaced indentation."""
        assert '''\
def foo():
\t"""Hello foo."""
\tif True:
\t    x = 1
''' == docformatter.format_code(
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
    def test_format_code_with_escaped_newlines(self):
        """Should leave escaped newlines in code untouched."""
        assert r'''def foo():
    """Hello foo."""
    x = \
            1
''' == docformatter.format_code(
            r'''def foo():
    """
    Hello foo.
    """
    x = \
            1
'''
        )

    @pytest.mark.unit
    def test_format_code_with_comments(self):
        """Should leave comments as is."""
        assert r'''
def foo():
    """Hello foo."""
    # My comment
    # My comment with escape \
    123
'''.lstrip() == docformatter.format_code(
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
    def test_format_code_with_escaped_newline_in_inline_comment(self):
        """Should leave code with inline comment as is."""
        assert r'''
def foo():
    """Hello foo."""
    def test_method_no_chr_92(): the501(92) # \
'''.lstrip() == docformatter.format_code(
            r'''
def foo():
    """
    Hello foo.
    """
    def test_method_no_chr_92(): the501(92) # \
'''.lstrip()
        )

    @pytest.mark.unit
    def test_format_code_raw_docstring_double_quotes(self):
        """Should format raw docstrings with triple double quotes.

        See requirement PEP_257_2.  See issue #54 for request to handle
        raw docstrings.
        """
        assert '''\
def foo():
    r"""Hello raw foo."""
''' == docformatter.format_code(
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
''' == docformatter.format_code(
            '''\
def foo():
    R"""
    Hello Raw foo.
    """
'''
        )

    @pytest.mark.unit
    def test_format_code_raw_docstring_single_quotes(self):
        """Should format raw docstrings with triple single quotes.

        See requirement PEP_257_2.  See issue #54 for request to handle
        raw docstrings.
        """
        assert '''\
def foo():
    r"""Hello raw foo."""
''' == docformatter.format_code(
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
''' == docformatter.format_code(
            """\
def foo():
    R'''
    Hello Raw foo.
    '''
"""
        )

    @pytest.mark.unit
    def test_format_code_unicode_docstring_double_quotes(self):
        """Should format unicode docstrings with triple double quotes.

        See requirement PEP_257_3.  See issue #54 for request to handle
        raw docstrings.
        """
        assert '''\
def foo():
    u"""Hello unicode foo."""
''' == docformatter.format_code(
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
''' == docformatter.format_code(
            '''\
def foo():
    U"""
    Hello Unicode foo.
    """
'''
        )

    @pytest.mark.unit
    def test_format_code_unicode_docstring_single_quotes(self):
        """Should format unicode docstrings with triple single quotes.

        See requirement PEP_257_3.  See issue #54 for request to handle
        raw docstrings.
        """
        assert '''\
def foo():
    u"""Hello unicode foo."""
''' == docformatter.format_code(
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
''' == docformatter.format_code(
            """\
def foo():
    U'''
    Hello Unicode foo.
    '''
"""
        )

    @pytest.mark.unit
    def test_format_code_skip_nested(self):
        """Should ignore nested triple quotes."""
        code = """\
def foo():
    '''Hello foo. \"\"\"abc\"\"\"
    '''
"""
        assert code == docformatter.format_code(code)

    @pytest.mark.unit
    def test_format_code_with_multiple_sentences(self):
        """Should create multi-line docstring from multiple sentences."""
        assert '''\
def foo():
    """Hello foo.

    This is a docstring.
    """
''' == docformatter.format_code(
            '''\
def foo():
    """
    Hello foo.
    This is a docstring.
    """
'''
        )

    @pytest.mark.unit
    def test_format_code_with_multiple_sentences_same_line(self):
        """Should create multi-line docstring from multiple sentences."""
        assert '''\
def foo():
    """Hello foo.

    This is a docstring.
    """
''' == docformatter.format_code(
            '''\
def foo():
    """
    Hello foo. This is a docstring.
    """
'''
        )

    @pytest.mark.unit
    def test_format_code_with_multiple_sentences_multi_line_summary(self):
        """Should put summary line on a single line."""
        assert '''\
def foo():
    """Hello foo.

    This is a docstring.
    """
''' == docformatter.format_code(
            '''\
def foo():
    """
    Hello
    foo. This is a docstring.
    """
'''
        )

    @pytest.mark.unit
    def test_format_code_with_empty_lines(self):
        """Summary line on one line when wrapped, followed by empty line."""
        assert '''\
def foo():
    """Hello foo and this is a docstring.

    More stuff.
    """
''' == docformatter.format_code(
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
    def test_format_code_with_trailing_whitespace(self):
        """Should strip trailing whitespace."""
        assert '''\
def foo():
    """Hello foo and this is a docstring.

    More stuff.
    """
''' == docformatter.format_code(
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
    def test_format_code_with_parameters_list(self):
        """Should treat parameters list as elaborate description."""
        assert '''\
def foo():
    """Test.

    one - first
    two - second
    """
''' == docformatter.format_code(
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
    def test_ignore_code_with_single_quote(self):
        """Single single quote on first line of code should remain untouched.

        See requirement PEP_257_1.  See issue #66 for example of
        docformatter breaking code when encountering single quote.
        """
        assert """\
def foo():
    'Just a regular string'
""" == docformatter.format_code(
            """\
def foo():
    'Just a regular string'
"""
        )

    @pytest.mark.unit
    def test_ignore_code_with_double_quote(self):
        """Single double quotes on first line of code should remain untouched.

        See requirement PEP_257_1.  See issue #66 for example of
        docformatter breaking code when encountering single quote.
        """
        assert """\
def foo():
    "Just a regular string"
""" == docformatter.format_code(
            """\
def foo():
    "Just a regular string"
"""
        )

    @pytest.mark.unit
    def test_format_code_should_skip_nested_triple_quotes(self):
        """Should ignore triple quotes nested in a string."""
        line = '''\
def foo():
    'Just a """foo""" string'
'''
        assert line == docformatter.format_code(line)

    @pytest.mark.unit
    def test_format_code_with_assignment_on_first_line(self):
        """Should ignore triple quotes in variable assignment."""
        assert '''\
def foo():
    x = """Just a regular string. Alpha."""
''' == docformatter.format_code(
            '''\
def foo():
    x = """Just a regular string. Alpha."""
'''
        )

    @pytest.mark.unit
    def test_format_code_with_regular_strings_too(self):
        """Should ignore triple quoted strings after the docstring."""
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
''' == docformatter.format_code(
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
    def test_format_code_with_syntax_error(self):
        """Should ignore single set of triple quotes followed by newline."""
        assert '"""\n' == docformatter.format_code('"""\n')

    @pytest.mark.unit
    def test_format_code_with_syntax_error_case_slash_r(self):
        """Should ignore single set of triple quotes followed by return."""
        assert '"""\r' == docformatter.format_code('"""\r')

    @pytest.mark.unit
    def test_format_code_with_syntax_error_case_slash_r_slash_n(self):
        """Should ignore single triple quote followed by return, newline."""
        assert '"""\r\n' == docformatter.format_code('"""\r\n')

    @pytest.mark.unit
    def test_format_code_dominant_line_ending_style_preserved(self):
        """Should retain carriage return line endings."""
        goes_in = '''\
def foo():\r
    """\r
    Hello\r
    foo. This is a docstring.\r
    """\r
'''
        assert docformatter.CRLF == docformatter.find_newline(
            goes_in.splitlines(True)
        )
        assert '''\
def foo():\r
    """Hello foo.\r
\r
    This is a docstring.\r
    """\r
''' == docformatter.format_code(
            goes_in
        )

    @pytest.mark.unit
    def test_format_code_additional_empty_line_before_doc(self):
        """Should remove empty line between function def and docstring.

        See issue #51.
        """
        assert (
            '\n\n\ndef my_func():\n"""Summary of my function."""\npass'
            == docformatter._format_code(
                '\n\n\ndef my_func():\n\n"""Summary of my function."""\npass'
            )
        )

    @pytest.mark.unit
    def test_format_code_extra_newline_following_comment(self):
        """Should remove extra newline following in-line comment.

        See issue #51.
        """
        docstring = '''\
def crash_rocket(location):    # pragma: no cover

    """This is a docstring following an in-line comment."""
    return location'''

        assert '''\
def crash_rocket(location):    # pragma: no cover
    """This is a docstring following an in-line comment."""
    return location''' == docformatter._format_code(
            docstring
        )

    @pytest.mark.unit
    def test_format_code_no_docstring(self):
        """Should leave code as is if there is no docstring.

        See issue #97.
        """
        docstring = (
            "def pytest_addoption(parser: pytest.Parser) -> "
            "None:\n    register_toggle.pytest_addoption(parser)\n"
        )
        assert docstring == docformatter._format_code(docstring)

        docstring = (
            "def pytest_addoption(parser: pytest.Parser) -> "
            "None:    # pragma: no cover\n    "
            "register_toggle.pytest_addoption(parser)\n"
        )
        assert docstring == docformatter._format_code(docstring)

class TestFormatCodeRanges:
    """Class for testing format_code() with the line_range or
    length_range arguments."""

    @pytest.mark.unit
    def test_format_code_range_miss(self):
        """Should leave docstrings outside line range as is."""
        assert '''\
    def f(x):
        """  This is a docstring. That should be on more lines"""
        pass
    def g(x):
        """  Badly indented docstring"""
        pass''' == docformatter.format_code('''\
    def f(x):
        """  This is a docstring. That should be on more lines"""
        pass
    def g(x):
        """  Badly indented docstring"""
        pass''', line_range=[1, 1])

    @pytest.mark.unit
    def test_format_code_range_hit(self):
        """Should format docstrings within line_range."""
        assert '''\
def f(x):
    """This is a docstring.

    That should be on more lines
    """
    pass
def g(x):
    """  Badly indented docstring"""
    pass''' == docformatter.format_code('''\
def f(x):
    """  This is a docstring. That should be on more lines"""
    pass
def g(x):
    """  Badly indented docstring"""
    pass''', line_range=[1, 2])

    @pytest.mark.unit
    def test_format_code_docstring_length(self):
        """Should leave docstrings outside length_range as is."""
        assert '''\
def f(x):
    """This is a docstring.


    That should be on less lines
    """
    pass
def g(x):
    """Badly indented docstring."""
    pass''' == docformatter.format_code('''\
def f(x):
    """This is a docstring.


    That should be on less lines
    """
    pass
def g(x):
    """  Badly indented docstring"""
    pass''', length_range=[1, 1])
