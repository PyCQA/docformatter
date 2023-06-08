# pylint: skip-file
# type: ignore
#
#       tests.test_format_docstring.py is part of the docformatter project
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
import itertools
import random
import sys

# Third Party Imports
import pytest

# docformatter Package Imports
import docformatter
from docformatter import Formatter

# docformatter Local Imports
from . import generate_random_docstring

INDENTATION = "    "


class TestFormatDocstring:
    """Class for testing _do_format_docstring() with no arguments."""

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_docstring(self, test_args, args):
        """Return one-line docstring."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        assert '"""Hello."""' == uut._do_format_docstring(
            INDENTATION,
            '''
"""

Hello.
"""
'''.strip(),
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_docstring_with_summary_that_ends_in_quote(self, test_args, args):
        """Return one-line docstring with period after quote."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        assert '''""""Hello"."""''' == uut._do_format_docstring(
            INDENTATION,
            '''
"""

"Hello"
"""
'''.strip(),
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [["--wrap-descriptions", "44", ""]])
    def test_format_docstring_with_bad_indentation(self, test_args, args):
        """Add spaces to indentation when too few."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        assert '''"""Hello.

    This should be indented but it is not.
    The next line should be indented too.
    And this too.
    """''' == uut._do_format_docstring(
            INDENTATION,
            '''
"""Hello.

 This should be indented but it is not. The
 next line should be indented too. And
 this too.
    """
'''.strip(),
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_docstring_with_too_much_indentation(self, test_args, args):
        """Remove spaces from indentation when too many."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        assert '''"""Hello.

    This should be dedented.

    1. This too.
    2. And this.
    3. And this.
    """''' == uut._do_format_docstring(
            INDENTATION,
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
    @pytest.mark.parametrize("args", [["--wrap-descriptions", "52", ""]])
    def test_format_docstring_with_trailing_whitespace(self, test_args, args):
        """Remove trailing white space."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        assert '''"""Hello.

    This should be not have trailing whitespace. The
    next line should not have trailing whitespace
    either.
    """''' == uut._do_format_docstring(
            INDENTATION,
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
    @pytest.mark.parametrize("args", [[""]])
    def test_format_docstring_with_empty_docstring(self, test_args, args):
        """Do nothing with empty docstring."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        assert '""""""' == uut._do_format_docstring(INDENTATION, '""""""')

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_docstring_with_no_period(self, test_args, args):
        """Add period to end of one-line and summary line."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        assert '"""Hello."""' == uut._do_format_docstring(
            INDENTATION,
            '''
"""

Hello
"""
'''.strip(),
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [["--non-cap", "eBay", "iPad", "-c", ""]])
    def test_format_docstring_with_non_cap_words(self, test_args, args):
        """Capitalize words not found in the non_cap list.

        See issue #193.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        assert '"""eBay kinda suss."""' == uut._do_format_docstring(
            INDENTATION,
            '''\
"""
eBay kinda suss
"""
''',
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_docstring_with_single_quotes(self, test_args, args):
        """Replace single triple quotes with triple double quotes."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        assert '"""Hello."""' == uut._do_format_docstring(
            INDENTATION,
            """
'''

Hello.
'''
""".strip(),
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_docstring_with_single_quotes_multi_line(self, test_args, args):
        """Replace single triple quotes with triple double quotes."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        assert '''
    """Return x factorial.

    This uses math.factorial.
    """
'''.strip() == uut._do_format_docstring(
            INDENTATION,
            """
    '''
    Return x factorial.

    This uses math.factorial.
    '''
""".strip(),
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_docstring_leave_underlined_summaries_alone(self, test_args, args):
        """Leave underlined summary lines as is."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        docstring = '''"""
    Foo bar
    -------

    This is more.

    """'''
        assert docstring == uut._do_format_docstring(INDENTATION, docstring)

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_docstring_leave_directive_alone(self, test_args, args):
        """Leave docstrings that have a reST directive in the summary alone."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        docstring = '''
    """.. code-block:: shell-session

    ► apm --version
    apm  2.6.2
    npm  6.14.13
    node 12.14.1 x64
    atom 1.58.0
    python 2.7.16
    git 2.33.0
    """'''
        assert docstring == uut._do_format_docstring(INDENTATION, docstring)

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_docstring_leave_link_only_docstring_alone(self, test_args, args):
        """Leave docstrings that consist of only a link alone."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        docstring = '''"""
    `Source of this snippet
    <https://www.freecodecamp.org/news/how-to-flatten-a-dictionary-in-python-in-4-different-ways/>`_.
    """'''
        assert docstring == uut._do_format_docstring(INDENTATION, docstring)

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_docstring_leave_blank_line_after_variable_def(
        self,
        test_args,
        args,
    ):
        """Leave blank lines after any variable beginning with 'def'.

        See issue #156.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        docstring = '\
class AcceptHeader(ExtendedSchemaNode): \
    # ok to use name in this case because target key in the mapping must \
    # be that specific value but cannot have a field named with this format \
    name = "Accept" \
    schema_type = String \
    missing = drop \
    default = ContentType.APP_JSON  # defaults to JSON for easy use within browsers \
\
\
class AcceptLanguageHeader(ExtendedSchemaNode): \
    # ok to use name in this case because target key in the mapping must \
    # be that specific value but cannot have a field named with this format \
    name = "Accept-Language" \
    schema_type = String \
    missing = drop \
    default = AcceptLanguage.EN_CA \
    # FIXME: oneOf validator for supported languages (?)'
        assert docstring == uut._do_format_code(docstring)

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_docstring_leave_blank_line_after_comment(
        self,
        test_args,
        args,
    ):
        """Leave blank lines after docstring followed by a comment.

        See issue #176.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        docstring = '''\
def Class1:
    """Class.""" #noqa

    attribute
    """Attr."""


def Class2:
    """Class."""

    attribute
    """Attr."""


def Class3:
    """Class docstring.

    With long description.
    """    #noqa

    attribute
    """Attr."""
'''
        assert docstring == uut._do_format_code(docstring)

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_docstring_no_summary_sphinx_style(
        self,
        test_args,
        args,
    ):
        """Leave docstring alone if it only contains Sphinx style directives.

        See issue #232.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        docstring = '''\
def function:
    """
    :param x: X
    :param y: Y
    """
'''
        assert docstring == uut._do_format_code(docstring)


class TestFormatLists:
    """Class for testing format_docstring() with lists in the docstring."""

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [["--wrap-descriptions", "72", ""]])
    def test_format_docstring_should_ignore_numbered_lists(self, test_args, args):
        """Ignore lists beginning with numbers."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        docstring = '''"""Hello.

    1. This should be indented but it is not. The
    next line should be indented too. But
    this is okay.
    """'''
        assert docstring == uut._do_format_docstring(
            INDENTATION,
            docstring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [["--wrap-descriptions", "72", ""]])
    def test_format_docstring_should_ignore_parameter_lists(self, test_args, args):
        """Ignore lists beginning with <word> -."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        docstring = '''"""Hello.

    foo - This is a foo. This is a foo. This is a foo. This is a foo. This is.
    bar - This is a bar. This is a bar. This is a bar. This is a bar. This is.
    """'''
        assert docstring == uut._do_format_docstring(
            INDENTATION,
            docstring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize(
        "args", [["--wrap-descriptions", "72", "--style", "numpy", ""]]
    )
    def test_format_docstring_should_ignore_colon_parameter_lists(
        self, test_args, args
    ):
        """Ignore lists beginning with <word>:"""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        docstring = '''"""Hello.

    foo: This is a foo. This is a foo. This is a foo. This is a foo. This is.
    bar: This is a bar. This is a bar. This is a bar. This is a bar. This is.
    """'''
        assert docstring == uut._do_format_docstring(
            INDENTATION,
            docstring,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_docstring_should_leave_list_alone(self, test_args, args):
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

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
        assert docstring == uut._do_format_docstring(
            INDENTATION,
            docstring,
        )


class TestFormatWrap:
    """Class for testing _do_format_docstring() with line wrapping."""

    @pytest.mark.unit
    def test_unwrap_summary(self):
        """Remove newline and tab characters."""
        assert "This is a sentence." == docformatter.unwrap_summary(
            "This \n\tis\na sentence."
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

        assert '''\
"""My awesome function.

    This line is quite long. In fact is it longer than one hundred and twenty characters so it should be wrapped but it
    is not.

    It doesn\'t wrap because of this line and the blank line in between! Delete them and it will wrap.
    """''' == uut._do_format_docstring(
            INDENTATION,
            '''"""My awesome function.

    This line is quite long. In fact is it longer than one hundred and twenty characters so it should be wrapped but it is not.

    It doesn't wrap because of this line and the blank line in between! Delete them and it will wrap.
    """'''.strip(),
        )

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

        assert '''
    """Creates and returns four was awakens to was created tracked ammonites
    was the fifty, arithmetical four was pyrotechnic to pyrotechnic physicists.

    `four' falsified x falsified ammonites to awakens to. `created' to
    ancestor was four to x dynamo to was four ancestor to physicists().
    """
        '''.strip() == uut._do_format_docstring(
            INDENTATION,
            '''
            """Creates and returns four was awakens to was created tracked
               ammonites was the fifty, arithmetical four was pyrotechnic to
               pyrotechnic physicists. `four' falsified x falsified ammonites
               to awakens to. `created' to ancestor was four to x dynamo to was
               four ancestor to physicists().
            """
        '''.strip(),
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

        assert '''"""Hello.

    This should be indented but it is not. The next line should be
    indented too. But this is okay.
    """''' == uut._do_format_docstring(
            INDENTATION,
            '''
"""Hello.

    This should be indented but it is not. The
    next line should be indented too. But
    this is okay.

    """
'''.strip(),
        )

    @pytest.mark.xfail
    @pytest.mark.parametrize("args", [["--wrap-descriptions", "72", ""]])
    def test_format_docstring_should_ignore_multi_paragraph(
        self,
        test_args,
        args,
    ):
        """Ignore multiple paragraphs in elaborate description.

        Multiple description paragraphs is supported since v1.5.0.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        docstring = '''"""Hello.

    This should be indented but it is not. The
    next line should be indented too. But
    this is okay.

    This should be indented but it is not. The
    next line should be indented too. But
    this is okay.
    """'''
        assert docstring == uut._do_format_docstring(
            INDENTATION,
            docstring,
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

        docstring = '''"""Hello.

    >>> 4
    4
    """'''
        assert docstring == uut._do_format_docstring(
            INDENTATION,
            docstring,
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

        docstring = '''"""
    >>> 4
    4

    """'''
        assert docstring == uut._do_format_docstring(
            INDENTATION,
            docstring,
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

        assert '''"""Foo bar bing bang.

        >>> tests = DocTestFinder().find(_TestClass)
        >>> runner = DocTestRunner(verbose=False)
        >>> tests.sort(key = lambda test: test.name)
    """''' == uut._do_format_docstring(
            INDENTATION,
            docstring='''"""Foo bar bing bang.

        >>> tests = DocTestFinder().find(_TestClass)
        >>> runner = DocTestRunner(verbose=False)
        >>> tests.sort(key = lambda test: test.name)

    """''',
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

        assert (
            (
                '''\
"""num_iterations is the number of updates -
    instead of a better definition of
    convergence."""\
'''
            )
            == uut._do_format_docstring(
                INDENTATION,
                '''\
"""
num_iterations is the number of updates - instead of a better definition of convergence.
"""\
''',
            )
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

        assert '''
\t\t"""Some summary x x x
\t\tx."""
'''.strip() == uut._do_format_docstring(
            "\t\t",
            '''
\t\t"""Some summary x x x x."""
'''.strip(),
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

        assert (
            (
                '''\
"""This one-line docstring will be multi-line because it's quite
    long.
    """\
'''
            )
            == uut._do_format_docstring(
                INDENTATION,
                '''\
"""This one-line docstring will be multi-line because it's quite long."""\
''',
            )
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

        assert (
            (
                '''\
"""This one-line docstring will not be wrapped and quotes will be in-line."""\
'''
            )
            == uut._do_format_docstring(
                INDENTATION,
                '''\
"""This one-line docstring will not be wrapped and quotes will be in-line."""\
''',
            )
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

        docstring = '''\
class TestClass:
    """This is a class docstring."""

    test_int = 1
    """This is a very, very, very long docstring that should really be
    reformatted nicely by docformatter."""
'''
        assert docstring == uut._do_format_code(
            '''\
class TestClass:
    """This is a class docstring."""

    test_int = 1
    """This is a very, very, very long docstring that should really be reformatted nicely by docformatter."""
'''
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

        docstring = '''\
def function2():
    """Hello yeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeet
    -v."""
'''
        assert docstring == uut._do_format_code(docstring)


class TestFormatWrapURL:
    """Class for testing _do_format_docstring() with line wrapping and URLs."""

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

        See issue #75. See requirement docformatter_10.1.3.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        docstring = '''\
"""This is a docstring with a link.

    Here is an elaborate description containing a link.
    `Area Under the Receiver Operating Characteristic Curve (ROC AUC)
        <https://en.wikipedia.org/wiki/Receiver_operating_characteristic#Further_interpretations>`_.
    """\
'''

        assert '''\
"""This is a docstring with a link.

    Here is an elaborate description containing a link. `Area Under the
    Receiver Operating Characteristic Curve (ROC AUC)
    <https://en.wikipedia.org/wiki/Receiver_operating_characteristic#Further_interpretations>`_.
    """\
''' == uut._do_format_docstring(
            INDENTATION, docstring.strip()
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

        See issue #140. See requirement docformatter_10.1.3.1.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        docstring = '''\
"""This is yanf with a short link.

    See `the link <https://www.link.com>`_ for more details.
    """\
'''

        assert '''\
"""This is yanf with a short link.

    See `the link <https://www.link.com>`_ for more details.
    """\
''' == uut._do_format_docstring(
            INDENTATION, docstring.strip()
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

        docstring = '''\
    """Helpful docstring.

    A larger description that starts here.  https://github.com/apache/kafka/blob/2.5/clients/src/main/java/org/apache/kafka/common/requests/DescribeConfigsResponse.java
    A larger description that ends here.
    """\
'''

        assert '''\
"""Helpful docstring.

    A larger description that starts here.
    https://github.com/apache/kafka/blob/2.5/clients/src/main/java/org/apache/kafka/common/requests/DescribeConfigsResponse.java
    A larger description that ends here.
    """\
''' == uut._do_format_docstring(
            INDENTATION, docstring.strip()
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

        docstring = '''\
"""This is a docstring with a link that causes a wrap.

    See `the link <https://www.link.com/a/long/link/that/causes/line/break>`_ for more details.
    """\
'''

        assert '''\
"""This is a docstring with a link that causes a wrap.

    See
    `the link <https://www.link.com/a/long/link/that/causes/line/break>`_
    for more details.
    """\
''' == uut._do_format_docstring(
            INDENTATION, docstring.strip()
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

        See issue #75. See requirement docformatter_10.1.3.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        docstring = '''\
"""This is another docstring with `a link`_.

    .. a link: http://www.reliqual.com/wiki/how_to_use_ramstk/verification_and_validation_module/index.html.
    """\
'''

        assert '''\
"""This is another docstring with `a link`_.

    .. a link: http://www.reliqual.com/wiki/how_to_use_ramstk/verification_and_validation_module/index.html.
    """\
''' == uut._do_format_docstring(
            INDENTATION, docstring.strip()
        )

        docstring = '''\
"""<Short decription>

    .. _linspace API: https://numpy.org/doc/stable/reference/generated/numpy.linspace.html
    .. _arange API: https://numpy.org/doc/stable/reference/generated/numpy.arange.html
    .. _logspace API: https://numpy.org/doc/stable/reference/generated/numpy.logspace.html
    """\
'''
        assert '''\
"""<Short decription>

    .. _linspace API: https://numpy.org/doc/stable/reference/generated/numpy.linspace.html
    .. _arange API: https://numpy.org/doc/stable/reference/generated/numpy.arange.html
    .. _logspace API: https://numpy.org/doc/stable/reference/generated/numpy.logspace.html
    """\
''' == uut._do_format_docstring(
            INDENTATION, docstring.strip()
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

        See issue #75. See requirement docformatter_10.1.3.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        docstring = '''\
"""This is another docstring with a link.

    See http://www.reliqual.com/wiki/how_to_use_ramstk/verification_and_validation_module/index.html for additional information.
    """\
'''

        assert '''\
"""This is another docstring with a link.

    See
    http://www.reliqual.com/wiki/how_to_use_ramstk/verification_and_validation_module/index.html
    for additional information.
    """\
''' == uut._do_format_docstring(
            INDENTATION, docstring.strip()
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

        docstring = '''\
    """Get the Python type of a Click parameter.

    See the list of `custom types provided by Click
    <https://click.palletsprojects.com/en/8.1.x/api/?highlight=intrange#types>`_.
    """\
    '''

        assert '''\
"""Get the Python type of a Click parameter.

    See the list of
    `custom types provided by Click <https://click.palletsprojects.com/en/8.1.x/api/?highlight=intrange#types>`_.
    """\
''' == uut._do_format_docstring(
            INDENTATION, docstring.strip()
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

        docstring = '''\
"""Fetch parameters values from configuration file and merge them with the
    defaults.

    User configuration is `merged to the context default_map as Click does
    <https://click.palletsprojects.com/en/8.1.x/commands/#context-defaults>`_.

    This allow user's config to only overrides defaults. Values sets from direct
    command line parameters, environment variables or interactive prompts, takes
    precedence over any values from the config file.
"""\
'''

        assert '''\
"""Fetch parameters values from configuration file and merge them with the
    defaults.

    User configuration is
    `merged to the context default_map as Click does <https://click.palletsprojects.com/en/8.1.x/commands/#context-defaults>`_.

    This allow user\'s config to only overrides defaults. Values sets from direct
    command line parameters, environment variables or interactive prompts, takes
    precedence over any values from the config file.
    """\
''' == uut._do_format_docstring(
            INDENTATION, docstring.strip()
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

        See issue #75. See requirement docformatter_10.1.3.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        docstring = '''\
"""This is yanf with a short link.

    See http://www.reliaqual.com for examples.
    """\
'''

        assert '''\
"""This is yanf with a short link.

    See http://www.reliaqual.com for examples.
    """\
''' == uut._do_format_docstring(
            INDENTATION, docstring.strip()
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

        docstring = '''\
    """This method doesn't do anything.

    https://example.com/this-is-just-a-long-url/designed-to-trigger/the-wrapping-of-the-description
    """
'''

        assert '''\
"""This method doesn\'t do anything.

    https://example.com/this-is-just-a-long-url/designed-to-trigger/the-wrapping-of-the-description
    """\
''' == uut._do_format_docstring(
            INDENTATION, docstring.strip()
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

        docstring = '''\
"""Django settings for webapp project.

    Generated by 'django-admin startproject' using Django 4.1.1.

    For more information on this file, see
    https://docs.djangoproject.com/en/4.1/topics/settings/

    For the full list of settings and their values, see
    https://docs.djangoproject.com/en/4.1/ref/settings/
    """\
'''

        assert '''\
"""Django settings for webapp project.

    Generated by 'django-admin startproject' using Django 4.1.1.

    For more information on this file, see
    https://docs.djangoproject.com/en/4.1/topics/settings/

    For the full list of settings and their values, see
    https://docs.djangoproject.com/en/4.1/ref/settings/
    """\
''' == uut._do_format_docstring(
            INDENTATION, docstring.strip()
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_docstring_with_short_anonymous_link(self, test_args, args):
        """Anonymous link references should not be wrapped into the link.

        See issue #210.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        docstring = '''\
"""Short description.

This graphics format generates terminal escape codes that transfer PNG
data to a TTY using the `kitty graphics protocol`__.

__ https://sw.kovidgoyal.net/kitty/graphics-protocol/
"""
'''
        assert docstring == uut._do_format_code(
            '''\
"""Short description.

This graphics format generates terminal escape codes that transfer
PNG data to a TTY using the `kitty graphics protocol`__.

__ https://sw.kovidgoyal.net/kitty/graphics-protocol/
"""
'''
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_docstring_with_quoted_link(self, test_args, args):
        """Anonymous link references should not be wrapped into the link.

        See issue #218.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        docstring = '''\
"""Construct a candidate project URL from the bundle and app name.

It's not a perfect guess, but it's better than having
"https://example.com".

:param bundle: The bundle identifier.
:param app_name: The app name.
:returns: The candidate project URL
"""
'''
        assert docstring == uut._do_format_code(
            '''\
"""Construct a candidate project URL from the bundle and app name.

It's not a perfect guess, but it's better than having "https://example.com".

:param bundle: The bundle identifier.
:param app_name: The app name.
:returns: The candidate project URL
"""
'''
        )


class TestFormatWrapBlack:
    """Class for testing _do_format_docstring() with line wrapping and black option."""

    @pytest.mark.unit
    @pytest.mark.parametrize(
        "args",
        [
            [
                "--black",
                "",
            ]
        ],
    )
    def test_format_docstring_black(
        self,
        test_args,
        args,
    ):
        """Format with black options when --black specified.

        Add a space between the opening quotes and the summary if content starts with a
        quote.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        assert (
            '''"""This one-line docstring will not have a leading space."""'''
        ) == uut._do_format_docstring(
            INDENTATION,
            '''\
"""   This one-line docstring will not have a leading space."""\
''',
        )
        assert (
            '''""" "This" quote starting one-line docstring will have a leading space."""'''
        ) == uut._do_format_docstring(
            INDENTATION,
            '''\
""""This" quote starting one-line docstring will have a leading space."""\
''',
        )
        assert (
            (
                '''\
""" "This" quote starting one-line docstring will have a leading space.

    This long description will be wrapped at 88 characters because we
    passed the --black option and 88 characters is the default wrap
    length.
    """\
'''
            )
            == uut._do_format_docstring(
                INDENTATION,
                '''\
""""This" quote starting one-line docstring will have a leading space.

This long description will be wrapped at 88 characters because we passed the --black option and 88 characters is the default wrap length.
"""\
''',
            )
        )


class TestFormatWrapEpytext:
    """Class for testing _do_format_docstring() with line wrapping and Epytext lists."""

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

        assert (
            (
                '''\
"""Return line-wrapped description text.

    We only wrap simple descriptions. We leave doctests, multi-paragraph text, and
    bulleted lists alone.  See
    http://www.docformatter.com/.

    @param text: the text argument.
    @param indentation: the super long description for the indentation argument that
        will require docformatter to wrap this line.
    @param wrap_length: the wrap_length argument
    @param force_wrap: the force_warp argument.
    @return: really long description text wrapped at n characters and a very long
        description of the return value so we can wrap this line abcd efgh ijkl mnop
        qrst uvwx yz.
    """\
'''
            )
            == uut._do_format_docstring(
                INDENTATION,
                '''\
"""Return line-wrapped description text.

    We only wrap simple descriptions. We leave doctests, multi-paragraph text,
    and bulleted lists alone.  See http://www.docformatter.com/.

    @param text: the text argument.
    @param indentation: the super long description for the indentation argument that will require docformatter to wrap this line.
    @param wrap_length: the wrap_length argument
    @param force_wrap: the force_warp argument.
    @return: really long description text wrapped at n characters and a very long description of the return value so we can wrap this line abcd efgh ijkl mnop qrst uvwx yz.
"""\
''',
            )
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

        assert (
            (
                '''\
"""Return line-wrapped description text.

    We only wrap simple descriptions. We leave doctests, multi-paragraph text, and
    bulleted lists alone.  See
    http://www.docformatter.com/.

    @param text: the text argument.
    @param indentation: the super long description for the indentation argument that will require docformatter to wrap this line.
    @param wrap_length: the wrap_length argument
    @param force_wrap: the force_warp argument.
    @return: really long description text wrapped at n characters and a very long description of the return value so we can wrap this line abcd efgh ijkl mnop qrst uvwx yz.
    """\
'''
            )
            == uut._do_format_docstring(
                INDENTATION,
                '''\
"""Return line-wrapped description text.

    We only wrap simple descriptions. We leave doctests, multi-paragraph text,
    and bulleted lists alone.  See http://www.docformatter.com/.

    @param text: the text argument.
    @param indentation: the super long description for the indentation argument that will require docformatter to wrap this line.
    @param wrap_length: the wrap_length argument
    @param force_wrap: the force_warp argument.
    @return: really long description text wrapped at n characters and a very long description of the return value so we can wrap this line abcd efgh ijkl mnop qrst uvwx yz.
"""\
''',
            )
        )


class TestFormatWrapSphinx:
    """Class for testing _do_format_docstring() with line wrapping and Sphinx lists."""

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

        assert (
            (
                '''\
"""Return line-wrapped description text.

    We only wrap simple descriptions. We leave doctests, multi-paragraph text, and
    bulleted lists alone.  See
    http://www.docformatter.com/.

    :param str text: the text argument.
    :param str indentation: the super long description for the indentation argument that
        will require docformatter to wrap this line.
    :param int wrap_length: the wrap_length argument
    :param bool force_wrap: the force_warp argument.
    :return: really long description text wrapped at n characters and a very long
        description of the return value so we can wrap this line abcd efgh ijkl mnop
        qrst uvwx yz.
    :rtype: str
    """\
'''
            )
            == uut._do_format_docstring(
                INDENTATION,
                '''\
"""Return line-wrapped description text.

    We only wrap simple descriptions. We leave doctests, multi-paragraph text, and bulleted lists alone.  See http://www.docformatter.com/.

    :param str text: the text argument.
    :param str indentation: the super long description for the indentation argument that will require docformatter to wrap this line.
    :param int wrap_length: the wrap_length argument
    :param bool force_wrap: the force_warp argument.
    :return: really long description text wrapped at n characters and a very long description of the return value so we can wrap this line abcd efgh ijkl mnop qrst uvwx yz.
    :rtype: str
"""\
''',
            )
        )

        # Issue #230 required adding parenthesis to the SPHINX_REGEX.
        assert (
            (
                '''\
"""CC.

    :math:`-`
    :param d: blabla
    :param list(str) l: more blabla.
    """\
'''
            )
            == uut._do_format_docstring(
                INDENTATION,
                '''\
"""CC.

    :math:`-`
    :param d: blabla
    :param list(str) l: more blabla.
    """\
''',
            )
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

        assert (
            (
                '''\
"""Return line-wrapped description text.

    We only wrap simple descriptions. We leave doctests, multi-paragraph text, and
    bulleted lists alone.  See
    http://www.docformatter.com/.

    :param str text: the text argument.
    :param str indentation: the super long description for the indentation argument that will require docformatter to wrap this line.
    :param int wrap_length: the wrap_length argument
    :param bool force_wrap: the force_warp argument.
    :return: really long description text wrapped at n characters and a very long description of the return value so we can wrap this line abcd efgh ijkl mnop qrst uvwx yz.
    :rtype: str
    """\
'''
            )
            == uut._do_format_docstring(
                INDENTATION,
                '''\
"""Return line-wrapped description text.

    We only wrap simple descriptions. We leave doctests, multi-paragraph text, and bulleted lists alone.  See http://www.docformatter.com/.

    :param str text: the text argument.
    :param str indentation: the super long description for the indentation argument that will require docformatter to wrap this line.
    :param int wrap_length: the wrap_length argument
    :param bool force_wrap: the force_warp argument.
    :return: really long description text wrapped at n characters and a very long description of the return value so we can wrap this line abcd efgh ijkl mnop qrst uvwx yz.
    :rtype: str
"""\
''',
            )
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

        assert (
            (
                '''\
"""Base for all Commands.

    :param logger: Logger for console and logfile.
    :param console: Facilitates console interaction and input solicitation.
    :param tools: Cache of tools populated by Commands as they are required.
    :param apps: Dictionary of project's Apps keyed by app name.
    :param base_path: Base directory for Briefcase project.
    :param data_path: Base directory for Briefcase tools, support packages, etc.
    :param is_clone: Flag that Command was triggered by the user's requested Command;
        for instance, RunCommand can invoke UpdateCommand and/or BuildCommand.
    """\
'''
            )
            == uut._do_format_docstring(
                INDENTATION,
                '''\
"""Base for all Commands.

:param logger: Logger for console and logfile.
:param console: Facilitates console interaction and input solicitation.
:param tools: Cache of tools populated by Commands as they are required.
:param apps: Dictionary of project's Apps keyed by app name.
:param base_path: Base directory for Briefcase project.
:param data_path: Base directory for Briefcase tools, support packages, etc.
:param is_clone: Flag that Command was triggered by the user's requested Command;
    for instance, RunCommand can invoke UpdateCommand and/or BuildCommand.
"""\
''',
            )
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

        assert (
            (
                '''\
"""Create or return existing HTTP session.

    :return: Requests :class:`~requests.Session` object
    """\
'''
            )
            == uut._do_format_docstring(
                INDENTATION,
                '''\
"""Create or return existing HTTP session.

    :return: Requests :class:`~requests.Session` object
    """\
''',
            )
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

        assert (
            (
                '''\
"""Configure application requirements by writing a requirements.txt file.

    :param app: The app configuration
    :param requires: The full list of requirements
    :param requirements_path: The full path to a requirements.txt file that will be
        written.
    """\
'''
            )
            == uut._do_format_docstring(
                INDENTATION,
                '''\
"""Configure application requirements by writing a requirements.txt file.

    :param app: The app configuration
    :param requires: The full list of requirements
    :param requirements_path: The full path to a requirements.txt file that
        will be written.
    """\
''',
            )
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

        See docformatter_10.4.3.1, issue #229, and issue #230.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        assert (
            (
                '''\
"""CC.

    :meth:`!X`
    """\
'''
            )
            == uut._do_format_docstring(
                INDENTATION,
                '''\
"""CC.

    :meth:`!X`
    """\
''',
            )
        )

        assert (
            (
                '''\
"""CC.

    :math:`-`
    """\
'''
            )
            == uut._do_format_docstring(
                INDENTATION,
                '''\
"""CC.

    :math: `-`
    """\
''',
            )
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
        """Should not add a space after the field name when the body is blank.

        See docformatter_10.4.3.2 and issue #224.
        """
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        assert (
            (
                '''\
"""Add trackers to a torrent.

    :raises NotFound404Error:

    :param torrent_hash: hash for torrent
    :param urls: tracker URLs to add to torrent
    :return: None
    """\
'''
            )
            == uut._do_format_docstring(
                INDENTATION,
                '''\
"""
Add trackers to a torrent.

:raises NotFound404Error:

:param torrent_hash: hash for torrent
:param urls: tracker URLs to add to torrent
:return: None
"""\
''',
            )
        )


class TestFormatStyleOptions:
    """Class for testing format_docstring() when requesting style options."""

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [[""]])
    def test_format_docstring_with_no_post_description_blank(
        self,
        test_args,
        args,
    ):
        """Remove blank lines before closing triple quotes."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        assert '''"""Hello.

    Description.
    """''' == uut._do_format_docstring(
            INDENTATION,
            '''
"""

Hello.

    Description.


    """
'''.strip(),
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [["--pre-summary-newline", ""]])
    def test_format_docstring_with_pre_summary_newline(
        self,
        test_args,
        args,
    ):
        """Remove blank line before summary."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        assert '''"""
    Hello.

    Description.
    """''' == uut._do_format_docstring(
            INDENTATION,
            '''
"""

Hello.

    Description.


    """
'''.strip(),
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [["--make-summary-multi-line", ""]])
    def test_format_docstring_make_summary_multi_line(
        self,
        test_args,
        args,
    ):
        """Place the one-line docstring between triple quotes."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        assert (
            (
                '''\
"""
    This one-line docstring will be multi-line.
    """\
'''
            )
            == uut._do_format_docstring(
                INDENTATION,
                '''\
"""This one-line docstring will be multi-line"""\
''',
            )
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("args", [["--pre-summary-space", ""]])
    def test_format_docstring_pre_summary_space(
        self,
        test_args,
        args,
    ):
        """Place a space between the opening quotes and the summary."""
        uut = Formatter(
            test_args,
            sys.stderr,
            sys.stdin,
            sys.stdout,
        )

        assert (
            '''""" This one-line docstring will have a leading space."""'''
        ) == uut._do_format_docstring(
            INDENTATION,
            '''\
"""This one-line docstring will have a leading space."""\
''',
        )


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
