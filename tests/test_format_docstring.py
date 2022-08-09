# pylint: skip-file
# type: ignore
#
#       tests.test_format_docstring.py is part of the docformatter project
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
"""Module for testing the format_docstring() function."""


# Standard Library Imports
import itertools
import random

# Third Party Imports
import pytest

# docformatter Package Imports
import docformatter

# docformatter Local Imports
from . import generate_random_docstring


class TestFormatDocstring:
    """Class for testing format_docstring() with no arguments."""

    @pytest.mark.unit
    def test_format_docstring(self):
        """Return one-line docstring."""
        assert '"""Hello."""' == docformatter.format_docstring(
            "    ",
            '''
"""

Hello.
"""
'''.strip(),
        )

    @pytest.mark.unit
    def test_format_docstring_with_summary_that_ends_in_quote(self):
        """Return one-line docstring with period after quote."""
        assert '''""""Hello"."""''' == docformatter.format_docstring(
            "    ",
            '''
"""

"Hello"
"""
'''.strip(),
        )

    @pytest.mark.unit
    def test_format_docstring_with_bad_indentation(self):
        """Add spaces to indentation when too few."""
        assert '''"""Hello.

    This should be indented but it is not. The
    next line should be indented too. And
    this too.
    """''' == docformatter.format_docstring(
            "    ",
            '''
"""Hello.

 This should be indented but it is not. The
 next line should be indented too. And
 this too.
    """
'''.strip(),
        )

    @pytest.mark.unit
    def test_format_docstring_with_too_much_indentation(self):
        """Remove spaces from indentation when too many."""
        assert '''"""Hello.

    This should be dedented.

    1. This too.
    2. And this.
    3. And this.
    """''' == docformatter.format_docstring(
            "    ",
            '''
"""Hello.

        This should be dedented.

        1. This too.
        2. And this.
        3. And this.

    """
'''.strip(),
        )

    @pytest.mark.unit
    def test_format_docstring_with_trailing_whitespace(self):
        """Remove trailing white space."""
        assert '''"""Hello.

    This should be not have trailing whitespace. The
    next line should not have trailing whitespace either.
    """''' == docformatter.format_docstring(
            "    ",
            '''
"""Hello.\t
\t
    This should be not have trailing whitespace. The\t\t\t
    next line should not have trailing whitespace either.\t
\t
    """
'''.strip(),
        )

    @pytest.mark.unit
    def test_format_docstring_with_empty_docstring(self):
        """Do nothing with empty docstring."""
        assert '""""""' == docformatter.format_docstring("    ", '""""""')

    @pytest.mark.unit
    def test_format_docstring_with_no_period(self):
        """Add period to end of one-line and summary line."""
        assert '"""Hello."""' == docformatter.format_docstring(
            "    ",
            '''
"""

Hello
"""
'''.strip(),
        )

    @pytest.mark.unit
    def test_format_docstring_with_single_quotes(self):
        """Replace single triple quotes with triple double quotes."""
        assert '"""Hello."""' == docformatter.format_docstring(
            "    ",
            """
'''

Hello.
'''
""".strip(),
        )

    @pytest.mark.unit
    def test_format_docstring_with_single_quotes_multi_line(self):
        """Replace single triple quotes with triple double quotes."""
        assert '''
    """Return x factorial.

    This uses math.factorial.
    """
'''.strip() == docformatter.format_docstring(
            "    ",
            """
    '''
    Return x factorial.

    This uses math.factorial.
    '''
""".strip(),
        )

    @pytest.mark.unit
    def test_format_docstring_leave_underlined_summaries_alone(self):
        docstring = '''"""
    Foo bar
    -------

    This is more.

    """'''
        assert docstring == docformatter.format_docstring("    ", docstring)


class TestFormatLists:
    """Class for testing format_docstring() with lists in the docstring."""

    @pytest.mark.unit
    def test_format_docstring_should_ignore_numbered_lists(self):
        """Ignore lists beginning with numbers."""
        docstring = '''"""Hello.

    1. This should be indented but it is not. The
    next line should be indented too. But
    this is okay.
    """'''
        assert docstring == docformatter.format_docstring(
            "    ", docstring, description_wrap_length=72
        )

    @pytest.mark.unit
    def test_format_docstring_should_ignore_parameter_lists(self):
        """Ignore lists beginning with <word> -."""
        docstring = '''"""Hello.

    foo - This is a foo. This is a foo. This is a foo. This is a foo. This is.
    bar - This is a bar. This is a bar. This is a bar. This is a bar. This is.
    """'''
        assert docstring == docformatter.format_docstring(
            "    ", docstring, description_wrap_length=72
        )

    @pytest.mark.unit
    def test_format_docstring_should_ignore_colon_parameter_lists(self):
        """Ignore lists beginning with <word>:"""
        docstring = '''"""Hello.

    foo: This is a foo. This is a foo. This is a foo. This is a foo. This is.
    bar: This is a bar. This is a bar. This is a bar. This is a bar. This is.
    """'''
        assert docstring == docformatter.format_docstring(
            "    ", docstring, description_wrap_length=72
        )

    @pytest.mark.unit
    def test_format_docstring_should_leave_list_alone(self):
        docstring = '''"""
    one
    two
    three
    four
    five
    six
    seven
    eight
    nine
    ten
    eleven
    """'''
        assert docstring == docformatter.format_docstring(
            "    ", docstring, strict=False
        )


class TestFormatWrap:
    """Class for testing format_docstring() when requesting line wrapping."""

    @pytest.mark.unit
    def test_unwrap_summary(self):
        """Remove newline and tab characters."""
        assert "This is a sentence." == docformatter.unwrap_summary(
            "This \n\tis\na sentence."
        )

    @pytest.mark.unit
    def test_format_docstring_with_wrap(self):
        """Wrap docstring."""
        # This function uses `random` so make sure each run of this test is
        # repeatable.
        random.seed(0)

        min_line_length = 50
        for max_length, num_indents in itertools.product(
            range(min_line_length, 100), range(20)
        ):
            indentation = " " * num_indents
            formatted_text = indentation + docformatter.format_docstring(
                indentation=indentation,
                docstring=generate_random_docstring(
                    max_word_length=min_line_length // 2
                ),
                summary_wrap_length=max_length,
            )

            for line in formatted_text.split("\n"):
                # It is not the formatter's fault if a word is too long to
                # wrap.
                if len(line.split()) > 1:
                    assert len(line) <= max_length

    @pytest.mark.unit
    def test_format_docstring_with_weird_indentation_and_punctuation(self):
        """"""
        assert '''
    """Creates and returns four was awakens to was created tracked ammonites
    was the fifty, arithmetical four was pyrotechnic to pyrotechnic physicists.

    `four' falsified x falsified ammonites
    to awakens to. `created' to ancestor was four to x dynamo to was
    four ancestor to physicists().
    """
        '''.strip() == docformatter.format_docstring(
            "    ",
            '''
            """Creates and returns four was awakens to was created tracked
               ammonites was the fifty, arithmetical four was pyrotechnic to
               pyrotechnic physicists. `four' falsified x falsified ammonites
               to awakens to. `created' to ancestor was four to x dynamo to was
               four ancestor to physicists().
            """
        '''.strip(),
            summary_wrap_length=79,
        )

    @pytest.mark.unit
    def test_format_docstring_with_description_wrapping(self):
        """Wrap description at 72 characters."""
        assert '''"""Hello.

    This should be indented but it is not. The next line should be
    indented too. But this is okay.
    """''' == docformatter.format_docstring(
            "    ",
            '''
"""Hello.

    This should be indented but it is not. The
    next line should be indented too. But
    this is okay.

    """
'''.strip(),
            description_wrap_length=72,
        )

    @pytest.mark.unit
    def test_format_docstring_should_ignore_multi_paragraph(self):
        """Ignore multiple paragraphs in elaborate description."""
        docstring = '''"""Hello.

    This should be indented but it is not. The
    next line should be indented too. But
    this is okay.

    This should be indented but it is not. The
    next line should be indented too. But
    this is okay.
    """'''
        assert docstring == docformatter.format_docstring(
            "    ", docstring, description_wrap_length=72
        )

    @pytest.mark.unit
    def test_format_docstring_should_ignore_doctests(self):
        """Leave doctests alone."""
        docstring = '''"""Hello.

    >>> 4
    4
    """'''
        assert docstring == docformatter.format_docstring(
            "    ", docstring, description_wrap_length=72
        )

    @pytest.mark.unit
    def test_format_docstring_should_ignore_doctests_in_summary(self):
        """Leave doctests alone if they're in the summary."""
        docstring = '''"""
    >>> 4
    4

    """'''
        assert docstring == docformatter.format_docstring(
            "    ", docstring, description_wrap_length=72
        )

    @pytest.mark.unit
    def test_format_docstring_should_maintain_indentation_of_doctest(self):
        """Don't change indentation of doctest lines."""
        assert '''"""Foo bar bing bang.

        >>> tests = DocTestFinder().find(_TestClass)
        >>> runner = DocTestRunner(verbose=False)
        >>> tests.sort(key = lambda test: test.name)
    """''' == docformatter.format_docstring(
            "    ",
            docstring='''"""Foo bar bing bang.

        >>> tests = DocTestFinder().find(_TestClass)
        >>> runner = DocTestRunner(verbose=False)
        >>> tests.sort(key = lambda test: test.name)

    """''',
            description_wrap_length=72,
        )

    @pytest.mark.unit
    def test_force_wrap(self):
        """Force even lists to be wrapped."""
        assert (
            (
                '''\
"""num_iterations is the number of updates -
    instead of a better definition of
    convergence."""\
'''
            )
            == docformatter.format_docstring(
                "    ",
                '''\
"""
num_iterations is the number of updates - instead of a better definition of convergence.
"""\
''',
                description_wrap_length=50,
                summary_wrap_length=50,
                force_wrap=True,
            )
        )

    @pytest.mark.xfail
    def test_format_docstring_with_summary_only_and_wrap_and_tab_indentation(
        self,
    ):
        """"Should account for length of tab when wrapping.

        See PR #69.
        """
        assert '''
\t\t"""Some summary x x x
\t\tx."""
'''.strip() == docformatter.format_docstring(
            "\t\t",
            '''
\t\t"""Some summary x x x x."""
'''.strip(),
            summary_wrap_length=30,
            tab_width=4,
        )


class TestFormatStyleOptions:
    """Class for testing format_docstring() when requesting style options."""

    @pytest.mark.unit
    def test_format_docstring_with_no_post_description_blank(self):
        """Remove blank lines before closing triple quotes."""
        assert '''"""Hello.

    Description.
    """''' == docformatter.format_docstring(
            "    ",
            '''
"""

Hello.

    Description.


    """
'''.strip(),
            post_description_blank=False,
        )

    @pytest.mark.unit
    def test_format_docstring_with_pre_summary_newline(self):
        """Remove blank line before summary."""
        assert '''"""
    Hello.

    Description.
    """''' == docformatter.format_docstring(
            "    ",
            '''
"""

Hello.

    Description.


    """
'''.strip(),
            pre_summary_newline=True,
        )

    @pytest.mark.unit
    def test_format_docstring_make_summary_multi_line(self):
        assert (
            (
                '''\
"""
    This one-line docstring will be multi-line.
    """\
'''
            )
            == docformatter.format_docstring(
                "    ",
                '''\
"""This one-line docstring will be multi-line"""\
''',
                make_summary_multi_line=True,
            )
        )

    @pytest.mark.unit
    def test_format_docstring_pre_summary_space(self):
        """"""
        assert (
            '''""" This one-line docstring will have a leading space."""'''
        ) == docformatter.format_docstring(
            "    ",
            '''\
"""This one-line docstring will have a leading space."""\
''',
            pre_summary_space=True,
        )
