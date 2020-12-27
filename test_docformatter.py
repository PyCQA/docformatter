#!/usr/bin/env python

"""Test suite for docformatter."""

from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

import contextlib
import io
import os
import random
import shutil
import string
import subprocess
import sys
import tempfile
import unittest

if sys.version_info >= (3, 3):
    from unittest.mock import patch
else:
    from mock import patch

import docformatter


ROOT_DIRECTORY = os.path.abspath(os.path.dirname(__file__))


if (
    'DOCFORMATTER_COVERAGE' in os.environ and
    int(os.environ['DOCFORMATTER_COVERAGE'])
):
    DOCFORMATTER_COMMAND = ['coverage', 'run', '--branch', '--parallel',
                            '--omit=*/site-packages/*',
                            os.path.join(ROOT_DIRECTORY, 'docformatter.py')]
else:
    # We need to specify the executable to make sure the correct Python
    # interpreter gets used.
    DOCFORMATTER_COMMAND = [sys.executable,
                            os.path.join(
                                ROOT_DIRECTORY,
                                'docformatter.py')]  # pragma: no cover


class TestUnits(unittest.TestCase):

    def test_is_in_range(self):
        self.assertTrue(docformatter.is_in_range(None, 1, 9))
        self.assertTrue(docformatter.is_in_range([1, 4], 3, 5))
        self.assertTrue(docformatter.is_in_range([1, 4], 4, 10))
        self.assertTrue(docformatter.is_in_range([2, 10], 1, 2))
        self.assertFalse(docformatter.is_in_range([1, 1], 2, 9))
        self.assertFalse(docformatter.is_in_range([10, 20], 1, 9))

    def test_has_correct_length(self):
        self.assertTrue(docformatter.has_correct_length(None, 1, 9))
        self.assertTrue(docformatter.has_correct_length([1, 3], 3, 5))
        self.assertTrue(docformatter.has_correct_length([1, 1], 1, 1))
        self.assertTrue(docformatter.has_correct_length([1, 10], 5, 10))
        self.assertFalse(docformatter.has_correct_length([1, 1], 2, 9))
        self.assertFalse(docformatter.has_correct_length([10, 20], 2, 9))

    def test_strip_docstring(self):
        self.assertEqual(
            'Hello.',
            docformatter.strip_docstring('''
    """Hello.

    """

    '''))

    def test_strip_docstring_with_single_quotes(self):
        self.assertEqual(
            'Hello.',
            docformatter.strip_docstring("""
    '''Hello.

    '''

    """))

    def test_strip_docstring_with_empty_string(self):
        self.assertEqual('', docformatter.strip_docstring('""""""'))

    def test_strip_docstring_with_escaped_quotes(self):
        self.assertEqual("hello\\'",
                         docformatter.strip_docstring("'hello\\''"))

    def test_strip_docstring_with_escaped_double_quotes(self):
        self.assertEqual('hello\\"',
                         docformatter.strip_docstring('"hello\\""'))

    def test_strip_docstring_with_unhandled(self):
        with self.assertRaises(ValueError):
            docformatter.strip_docstring('r"""foo"""')

    def test_strip_docstring_with_unknown(self):
        with self.assertRaises(ValueError):
            docformatter.strip_docstring('foo')

    def test_format_docstring(self):
        self.assertEqual('"""Hello."""',
                         docformatter.format_docstring('    ', '''
"""

Hello.
"""
'''.strip()))

    def test_format_docstring_with_summary_that_ends_in_quote(self):
        self.assertEqual('''""""Hello"."""''',
                         docformatter.format_docstring('    ', '''
"""

"Hello"
"""
'''.strip()))

    def test_format_docstring_with_bad_indentation(self):
        self.assertEqual('''"""Hello.

    This should be indented but it is not. The
    next line should be indented too. And
    this too.
    """''',
                         docformatter.format_docstring('    ', '''
"""Hello.

 This should be indented but it is not. The
 next line should be indented too. And
 this too.
    """
'''.strip()))

    def test_format_docstring_with_too_much_indentation(self):
        self.assertEqual('''"""Hello.

    This should be dedented.

    1. This too.
    2. And this.
    3. And this.
    """''',
                         docformatter.format_docstring('    ', '''
"""Hello.

        This should be dedented.

        1. This too.
        2. And this.
        3. And this.

    """
'''.strip()))

    def test_format_docstring_with_description_wrapping(self):
        self.assertEqual('''"""Hello.

    This should be indented but it is not. The next line should be
    indented too. But this is okay.
    """''',
                         docformatter.format_docstring('    ', '''
"""Hello.

    This should be indented but it is not. The
    next line should be indented too. But
    this is okay.

    """
'''.strip(), description_wrap_length=72))

    def test_format_docstring_should_ignore_doctests(self):
        docstring = '''"""Hello.

    >>> 4
    4
    """'''
        self.assertEqual(
            docstring,
            docformatter.format_docstring('    ',
                                          docstring,
                                          description_wrap_length=72))

    def test_format_docstring_should_ignore_doctests_in_summary(self):
        docstring = '''"""
    >>> 4
    4

    """'''
        self.assertEqual(
            docstring,
            docformatter.format_docstring('    ',
                                          docstring,
                                          description_wrap_length=72))

    def test_format_docstring_should_maintain_indentation_of_doctest(self):
        self.assertEqual(
            '''"""Foo bar bing bang.

        >>> tests = DocTestFinder().find(_TestClass)
        >>> runner = DocTestRunner(verbose=False)
        >>> tests.sort(key = lambda test: test.name)
    """''',
            docformatter.format_docstring(
                '    ',
                docstring='''"""Foo bar
        bing bang.

        >>> tests = DocTestFinder().find(_TestClass)
        >>> runner = DocTestRunner(verbose=False)
        >>> tests.sort(key = lambda test: test.name)

    """''',
                description_wrap_length=72))

    def test_format_docstring_should_ignore_numbered_lists(self):
        docstring = '''"""Hello.

    1. This should be indented but it is not. The
    next line should be indented too. But
    this is okay.
    """'''
        self.assertEqual(
            docstring,
            docformatter.format_docstring('    ',
                                          docstring,
                                          description_wrap_length=72))

    def test_format_docstring_should_ignore_parameter_lists(self):
        docstring = '''"""Hello.

    foo - This is a foo. This is a foo. This is a foo. This is a foo. This is.
    bar - This is a bar. This is a bar. This is a bar. This is a bar. This is.
    """'''
        self.assertEqual(
            docstring,
            docformatter.format_docstring('    ',
                                          docstring,
                                          description_wrap_length=72))

    def test_format_docstring_should_ignore__colon_parameter_lists(self):
        docstring = '''"""Hello.

    foo: This is a foo. This is a foo. This is a foo. This is a foo. This is.
    bar: This is a bar. This is a bar. This is a bar. This is a bar. This is.
    """'''
        self.assertEqual(
            docstring,
            docformatter.format_docstring('    ',
                                          docstring,
                                          description_wrap_length=72))

    def test_format_docstring_should_ignore_multi_paragraph(self):
        docstring = '''"""Hello.

    This should be indented but it is not. The
    next line should be indented too. But
    this is okay.

    This should be indented but it is not. The
    next line should be indented too. But
    this is okay.
    """'''
        self.assertEqual(
            docstring,
            docformatter.format_docstring('    ',
                                          docstring,
                                          description_wrap_length=72))

    def test_format_docstring_with_trailing_whitespace(self):
        self.assertEqual('''"""Hello.

    This should be not have trailing whitespace. The
    next line should not have trailing whitespace either.
    """''',
                         docformatter.format_docstring('    ', '''
"""Hello.\t
\t
    This should be not have trailing whitespace. The\t\t\t
    next line should not have trailing whitespace either.\t
\t
    """
'''.strip()))

    def test_format_docstring_with_no_post_description_blank(self):
        self.assertEqual('''"""Hello.

    Description.
    """''',
                         docformatter.format_docstring('    ', '''
"""

Hello.

    Description.


    """
'''.strip(), post_description_blank=False))

    def test_format_docstring_with_pre_summary_newline(self):
        self.assertEqual('''"""
    Hello.

    Description.
    """''',
                         docformatter.format_docstring('    ', '''
"""

Hello.

    Description.


    """
'''.strip(), pre_summary_newline=True))

    def test_format_docstring_with_empty_docstring(self):
        self.assertEqual('""""""',
                         docformatter.format_docstring('    ', '""""""'))

    def test_format_docstring_with_no_period(self):
        self.assertEqual('"""Hello."""',
                         docformatter.format_docstring('    ', '''
"""

Hello
"""
'''.strip()))

    def test_format_docstring_with_single_quotes(self):
        self.assertEqual('"""Hello."""',
                         docformatter.format_docstring('    ', """
'''

Hello.
'''
""".strip()))

    def test_format_docstring_with_single_quotes_multi_line(self):
        self.assertEqual('''
    """Return x factorial.

    This uses math.factorial.
    """
'''.strip(),
            docformatter.format_docstring('    ', """
    '''
    Return x factorial.

    This uses math.factorial.
    '''
""".strip()))

    def test_format_docstring_with_wrap(self):
        # This function uses `random` so make sure each run of this test is
        # repeatable.
        random.seed(0)

        min_line_length = 50
        for max_length in range(min_line_length, 100):
            for num_indents in range(0, 20):
                indentation = ' ' * num_indents
                formatted_text = indentation + docformatter.format_docstring(
                    indentation=indentation,
                    docstring=generate_random_docstring(
                        max_word_length=min_line_length // 2),
                    summary_wrap_length=max_length)

                for line in formatted_text.split('\n'):
                    # It is not the formatter's fault if a word is too long to
                    # wrap.
                    if len(line.split()) > 1:
                        self.assertLessEqual(len(line), max_length)

    def test_format_docstring_with_weird_indentation_and_punctuation(self):
        self.assertEqual('''
    """Creates and returns four was awakens to was created tracked ammonites
    was the fifty, arithmetical four was pyrotechnic to pyrotechnic physicists.

    `four' falsified x falsified ammonites
    to awakens to. `created' to ancestor was four to x dynamo to was
    four ancestor to physicists().
    """
'''.strip(),
            docformatter.format_docstring('    ', '''
    """Creates and returns four was awakens to was created tracked
       ammonites was the fifty, arithmetical four was pyrotechnic to
       pyrotechnic physicists. `four' falsified x falsified ammonites
       to awakens to. `created' to ancestor was four to x dynamo to was
       four ancestor to physicists().
    """
'''.strip(), summary_wrap_length=79))

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
        self.assertEqual(
            docstring,
            docformatter.format_docstring('    ', docstring))

    def test_format_docstring_should_underlined_summaries_alone(self):
        docstring = '''"""
    Foo bar
    -------

    This is more.

    """'''
        self.assertEqual(
            docstring,
            docformatter.format_docstring('    ', docstring))

    def test_format_code(self):
        self.assertEqual(
            '''\
def foo():
    """Hello foo."""
''',
            docformatter.format_code(
                '''\
def foo():
    """
    Hello foo.
    """
'''))

    def test_format_code_range_miss(self):
        self.assertEqual('''\
def f(x):
    """  This is a docstring. That should be on more lines"""
    pass
def g(x):
    """  Badly indented docstring"""
    pass''',
                         docformatter.format_code('''\
def f(x):
    """  This is a docstring. That should be on more lines"""
    pass
def g(x):
    """  Badly indented docstring"""
    pass''', line_range=[1, 1]))

    def test_format_code_range_hit(self):
        self.assertEqual('''\
def f(x):
    """This is a docstring.

    That should be on more lines
    """
    pass
def g(x):
    """  Badly indented docstring"""
    pass''',
                         docformatter.format_code('''\
def f(x):
    """  This is a docstring. That should be on more lines"""
    pass
def g(x):
    """  Badly indented docstring"""
    pass''', line_range=[1, 2]))

    def test_format_code_docstring_length(self):
        self.assertEqual('''\
def f(x):
    """This is a docstring.


    That should be on less lines
    """
    pass
def g(x):
    """Badly indented docstring."""
    pass''',
                         docformatter.format_code('''\
def f(x):
    """This is a docstring.


    That should be on less lines
    """
    pass
def g(x):
    """  Badly indented docstring"""
    pass''', length_range=[1, 1]))

    def test_format_code_with_module_docstring(self):
        self.assertEqual(
            '''\
#!/usr/env/bin python
"""This is a module docstring.

1. One
2. Two
"""

"""But
this
is
not."""
''',
            docformatter.format_code(
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
'''))

    def test_format_code_should_ignore_non_docstring(self):
        source = '''\
x = """This
is
not."""
'''
        self.assertEqual(
            source,
            docformatter.format_code(source))

    def test_format_code_with_empty_string(self):
        self.assertEqual(
            '',
            docformatter.format_code(''))

    def test_format_code_with_tabs(self):
        self.assertEqual(
            '''\
def foo():
\t"""Hello foo."""
\tif True:
\t\tx = 1
''',
            docformatter.format_code(
                '''\
def foo():
\t"""
\tHello foo.
\t"""
\tif True:
\t\tx = 1
'''))

    def test_format_code_with_mixed_tabs(self):
        self.assertEqual(
            '''\
def foo():
\t"""Hello foo."""
\tif True:
\t    x = 1
''',
            docformatter.format_code(
                '''\
def foo():
\t"""
\tHello foo.
\t"""
\tif True:
\t    x = 1
'''))

    def test_format_code_with_escaped_newlines(self):
        self.assertEqual(
            r'''def foo():
    """Hello foo."""
    x = \
            1
''',
            docformatter.format_code(
                r'''def foo():
    """
    Hello foo.
    """
    x = \
            1
'''))

    def test_format_code_with_comments(self):
        self.assertEqual(
            r'''
def foo():
    """Hello foo."""
    # My comment
    # My comment with escape \
    123
'''.lstrip(),
            docformatter.format_code(
                r'''
def foo():
    """
    Hello foo.
    """
    # My comment
    # My comment with escape \
    123
'''.lstrip()))

    def test_format_code_with_escaped_newline_in_inline_comment(self):
        self.assertEqual(
            r'''
def foo():
    """Hello foo."""
    def test_method_no_chr_92(): the501(92) # \
'''.lstrip(),
            docformatter.format_code(
                r'''
def foo():
    """
    Hello foo.
    """
    def test_method_no_chr_92(): the501(92) # \
'''.lstrip()))

    def test_format_code_skip_complex(self):
        """We do not handle r/u/b prefixed strings."""
        self.assertEqual(
            '''\
def foo():
    r"""
    Hello foo.
    """
''',
            docformatter.format_code(
                '''\
def foo():
    r"""
    Hello foo.
    """
'''))

    def test_format_code_skip_complex_single(self):
        """We do not handle r/u/b prefixed strings."""
        self.assertEqual(
            """\
def foo():
    r'''
    Hello foo.
    '''
""",
            docformatter.format_code(
                """\
def foo():
    r'''
    Hello foo.
    '''
"""))

    def test_format_code_skip_nested(self):
        code = """\
def foo():
    '''Hello foo. \"\"\"abc\"\"\"
    '''
"""
        self.assertEqual(code, docformatter.format_code(code))

    def test_format_code_with_multiple_sentences(self):
        self.assertEqual(
            '''\
def foo():
    """Hello foo.

    This is a docstring.
    """
''',
            docformatter.format_code(
                '''\
def foo():
    """
    Hello foo.
    This is a docstring.
    """
'''))

    def test_format_code_with_multiple_sentences_same_line(self):
        self.assertEqual(
            '''\
def foo():
    """Hello foo.

    This is a docstring.
    """
''',
            docformatter.format_code(
                '''\
def foo():
    """
    Hello foo. This is a docstring.
    """
'''))

    def test_format_code_with_multiple_sentences_multi_line_summary(self):
        self.assertEqual(
            '''\
def foo():
    """Hello foo.

    This is a docstring.
    """
''',
            docformatter.format_code(
                '''\
def foo():
    """
    Hello
    foo. This is a docstring.
    """
'''))

    def test_format_code_with_empty_lines(self):
        self.assertEqual(
            '''\
def foo():
    """Hello foo and this is a docstring.

    More stuff.
    """
''',
            docformatter.format_code(
                '''\
def foo():
    """
    Hello
    foo and this is a docstring.

    More stuff.
    """
'''))

    def test_format_code_with_trailing_whitespace(self):
        self.assertEqual(
            '''\
def foo():
    """Hello foo and this is a docstring.

    More stuff.
    """
''',
            docformatter.format_code(
                ('''\
def foo():
    """
    Hello
    foo and this is a docstring.\t

    More stuff.\t
    """
''')))

    def test_format_code_with_parameters_list(self):
        self.assertEqual(
            '''\
def foo():
    """Test.

    one - first
    two - second
    """
''',
            docformatter.format_code(
                ('''\
def foo():
    """Test
    one - first
    two - second
    """
''')))

    def test_format_code_with_double_quote(self):
        self.assertEqual(
            '''\
def foo():
    """Just a regular string."""
''',
            docformatter.format_code(
                '''\
def foo():
    "Just a regular string"
'''))

    def test_format_code_with_single_quote(self):
        self.assertEqual(
            '''\
def foo():
    """Just a regular string."""
''',
            docformatter.format_code(
                '''\
def foo():
    'Just a regular string'
'''))

    def test_format_code_with_should_skip_nested_triple_quotes(self):
        line = '''\
def foo():
    'Just a """foo""" string'
'''
        self.assertEqual(line, docformatter.format_code(line))

    def test_format_code_with_assignment_on_first_line(self):
        self.assertEqual(
            '''\
def foo():
    x = """Just a regular string. Alpha."""
''',
            docformatter.format_code(
                '''\
def foo():
    x = """Just a regular string. Alpha."""
'''))

    def test_format_code_with_regular_strings_too(self):
        self.assertEqual(
            '''\
def foo():
    """Hello foo and this is a docstring.

    More stuff.
    """
    x = """My non-docstring
    This should not touched."""

    """More stuff
    that should not be
    touched\t"""
''',
            docformatter.format_code(
                '''\
def foo():
    """
    Hello
    foo and this is a docstring.

    More stuff.
    """
    x = """My non-docstring
    This should not touched."""

    """More stuff
    that should not be
    touched\t"""
'''))

    def test_format_code_with_syntax_error(self):
        self.assertEqual('"""\n',
                         docformatter.format_code('"""\n'))

    def test_format_code_with_syntax_error_case_slash_r(self):
        self.assertEqual('"""\r',
                         docformatter.format_code('"""\r'))

    def test_format_code_with_syntax_error_case_slash_r_slash_n(self):
        self.assertEqual('"""\r\n',
                         docformatter.format_code('"""\r\n'))

    def test_find_newline_only_cr(self):
        source = ['print 1\r', 'print 2\r', 'print3\r']
        self.assertEqual(docformatter.CR, docformatter.find_newline(source))

    def test_find_newline_only_lf(self):
        source = ['print 1\n', 'print 2\n', 'print3\n']
        self.assertEqual(docformatter.LF, docformatter.find_newline(source))

    def test_find_newline_only_crlf(self):
        source = ['print 1\r\n', 'print 2\r\n', 'print3\r\n']
        self.assertEqual(docformatter.CRLF, docformatter.find_newline(source))

    def test_find_newline_cr1_and_lf2(self):
        source = ['print 1\n', 'print 2\r', 'print3\n']
        self.assertEqual(docformatter.LF, docformatter.find_newline(source))

    def test_find_newline_cr1_and_crlf2(self):
        source = ['print 1\r\n', 'print 2\r', 'print3\r\n']
        self.assertEqual(docformatter.CRLF, docformatter.find_newline(source))

    def test_find_newline_should_default_to_lf(self):
        self.assertEqual(docformatter.LF, docformatter.find_newline([]))
        self.assertEqual(docformatter.LF, docformatter.find_newline(['', '']))

    def test_format_code_dominant_line_ending_style_preserved(self):
        input = '''\
def foo():\r
    """\r
    Hello\r
    foo. This is a docstring.\r
    """\r
'''
        self.assertEqual(docformatter.CRLF, docformatter.find_newline(input.splitlines(True)))
        self.assertEqual(
            '''\
def foo():\r
    """Hello foo.\r
\r
    This is a docstring.\r
    """\r
''',
            docformatter.format_code(input))

    def test_split_summary_and_description(self):
        self.assertEqual(
            ('This is the first.',
             'This is the second. This is the third.'),
            docformatter.split_summary_and_description(
                'This is the first. This is the second. This is the third.'))

    def test_split_summary_and_description_complex(self):
        self.assertEqual(
            ('This is the first',
             '\nThis is the second. This is the third.'),
            docformatter.split_summary_and_description(
                'This is the first\n\nThis is the second. This is the third.'))

    def test_split_summary_and_description_more_complex(self):
        self.assertEqual(
            ('This is the first.',
             'This is the second. This is the third.'),
            docformatter.split_summary_and_description(
                'This is the first.\nThis is the second. This is the third.'))

    def test_split_summary_and_description_with_list(self):
        self.assertEqual(('This is the first',
                          '- one\n- two'),
                         docformatter.split_summary_and_description(
                             'This is the first\n- one\n- two'))

    def test_split_summary_and_description_with_list_of_parameters(self):
        self.assertEqual(('This is the first',
                          'one - one\ntwo - two'),
                         docformatter.split_summary_and_description(
                             'This is the first\none - one\ntwo - two'))

    def test_split_summary_and_description_with_capital(self):
        self.assertEqual(('This is the first\nWashington', ''),
                         docformatter.split_summary_and_description(
                             'This is the first\nWashington'))

    def test_split_summary_and_description_with_list_on_other_line(self):
        self.assertEqual(('Test\n    test', '    @blah'),
                         docformatter.split_summary_and_description('''\
    Test
    test
    @blah
'''))

    def test_split_summary_and_description_with_other_symbol(self):
        self.assertEqual(('This is the first',
                          '@ one\n@ two'),
                         docformatter.split_summary_and_description(
                             'This is the first\n@ one\n@ two'))

    def test_split_summary_and_description_with_colon(self):
        self.assertEqual(('This is the first:',
                          'one\ntwo'),
                         docformatter.split_summary_and_description(
                             'This is the first:\none\ntwo'))

    def test_split_summary_and_description_with_exclamation(self):
        self.assertEqual(('This is the first!',
                          'one\ntwo'),
                         docformatter.split_summary_and_description(
                             'This is the first!\none\ntwo'))

    def test_split_summary_and_description_with_question_mark(self):
        self.assertEqual(('This is the first?',
                          'one\ntwo'),
                         docformatter.split_summary_and_description(
                             'This is the first?\none\ntwo'))

    def test_split_summary_and_description_with_quote(self):
        self.assertEqual(('This is the first\n"one".', ''),
                         docformatter.split_summary_and_description(
                             'This is the first\n"one".'))

        self.assertEqual(("This is the first\n'one'.", ''),
                         docformatter.split_summary_and_description(
                             "This is the first\n'one'."))

        self.assertEqual(('This is the first\n``one``.', ''),
                         docformatter.split_summary_and_description(
                             'This is the first\n``one``.'))

    def test_split_summary_and_description_with_late__punctuation(self):
        self.assertEqual(
            ("""\
Try this and this and this and this and this and this and this at
    http://example.com/""",
             """
    Parameters
    ----------
    email : string"""),
            docformatter.split_summary_and_description('''\
    Try this and this and this and this and this and this and this at
    http://example.com/

    Parameters
    ----------
    email : string
'''))

    def test_split_summary_and_description_without__punctuation(self):
        self.assertEqual(
            ("""\
Try this and this and this and this and this and this and this at
    this other line""",
             """
    Parameters
    ----------
    email : string"""),
            docformatter.split_summary_and_description('''\
    Try this and this and this and this and this and this and this at
    this other line

    Parameters
    ----------
    email : string
'''))

    def test_split_summary_and_description_with_abbreviation(self):
        for text in ['Test e.g. now'
                     'Test i.e. now',
                     'Test Dr. now',
                     'Test Mr. now',
                     'Test Mrs. now',
                     'Test Ms. now']:
            self.assertEqual(
                (text, ''),
                docformatter.split_summary_and_description(text))

    def test_normalize_summary(self):
        self.assertEqual(
            'This is a sentence.',
            docformatter.normalize_summary('This \n\t is\na sentence'))

    def test_normalize_summary_with_different_punctuation(self):
        summary = 'This is a question?'
        self.assertEqual(
            summary,
            docformatter.normalize_summary(summary))
        
    def test_normalize_summary_formatted_as_title(self):
        summary = '# This is a title'
        self.assertEqual(
            summary,
            docformatter.normalize_summary(summary))    

    def test_detect_encoding_with_bad_encoding(self):
        with temporary_file('# -*- coding: blah -*-\n') as filename:
            self.assertEqual('latin-1',
                             docformatter.detect_encoding(filename))

    def test_reindent(self):
        self.assertEqual(
            """\
    This should be dedented.

    1. This too.
    2. And this.
""",
            docformatter.reindent("""\
                This should be dedented.

                1. This too.
                2. And this.
            """, indentation='    ')
        )

    def test_reindent_should_expand_tabs_to_indentation(self):
        self.assertEqual(
            """\
    This should be dedented.

    1. This too.
    2. And this.
""",
            docformatter.reindent("""\
                This should be dedented.

                1. This too.
        \t2. And this.
            """, indentation='    ')
        )

    def test_reindent_with_no_indentation_expand_tabs(self):
        self.assertEqual(
            """\
The below should be indented with spaces:

        1. This too.
        2. And this.
""",
            docformatter.reindent("""\
The below should be indented with spaces:

\t1. This too.
\t2. And this.
            """, indentation='')
        )

    def test_reindent_should_maintain_indentation(self):
        description = """\
    Parameters:

        - a
        - b
"""
        self.assertEqual(
            description,
            docformatter.reindent(description, indentation='    ')
        )

    def test_find_shortest_indentation(self):
        self.assertEqual(
            ' ',
            docformatter._find_shortest_indentation(['    ', ' b', '  a']))

    def test_split_first_sentence(self):
        self.assertEqual(
            ('This is a sentence.', ' More stuff. And more stuff.   .!@#$%'),
            docformatter.split_first_sentence(
                'This is a sentence. More stuff. And more stuff.   .!@#$%'))

        self.assertEqual(
            ('This e.g. sentence.', ' More stuff. And more stuff.   .!@#$%'),
            docformatter.split_first_sentence(
                'This e.g. sentence. More stuff. And more stuff.   .!@#$%'))

        self.assertEqual(
            ('This is the first:', '\none\ntwo'),
            docformatter.split_first_sentence(
                'This is the first:\none\ntwo'))

    def test_is_some_sort_of_list(self):
        self.assertTrue(docformatter.is_some_sort_of_list("""\
    @param
    @param
    @param
"""))

    def test_is_some_sort_of_list_with_dashes(self):
        self.assertTrue(docformatter.is_some_sort_of_list("""\
    Keyword arguments:
    real -- the real part (default 0.0)
    imag -- the imaginary part (default 0.0)
"""))

    def test_is_some_sort_of_list_without_special_symbol(self):
        self.assertTrue(docformatter.is_some_sort_of_list("""\
    Example:
      release-1.1/
      release-1.2/
      release-1.3/
      release-1.4/
      release-1.4.1/
      release-1.5/
"""))

    def test_is_some_sort_of_list_of_parameter_list_with_newline(self):
        self.assertTrue(docformatter.is_some_sort_of_list("""\
Args:
    stream (BinaryIO): Binary stream (usually a file object).
"""))

    def test_is_some_sort_of_code(self):
        self.assertTrue(docformatter.is_some_sort_of_code("""\
            __________=__________(__________,__________,__________,__________[
                      '___'],__________,__________,__________,__________,______________=__________)
"""))

    def test_force_wrap(self):
        self.assertEqual(('''\
"""num_iterations is the number of updates -
    instead of a better definition of
    convergence."""\
'''),
                         docformatter.format_docstring('    ', '''\
"""
num_iterations is the number of updates - instead of a better definition of convergence.
"""\
''', description_wrap_length=50, summary_wrap_length=50, force_wrap=True))

    def test_remove_section_header(self):
        self.assertEqual(
            'foo\nbar\n',
            docformatter.remove_section_header('----\nfoo\nbar\n')
        )

        line = 'foo\nbar\n'
        self.assertEqual(line, docformatter.remove_section_header(line))

        line = '    \nfoo\nbar\n'
        self.assertEqual(line, docformatter.remove_section_header(line))

    def test_is_probably_beginning_of_sentence(self):
        self.assertTrue(docformatter.is_probably_beginning_of_sentence(
            '- This is part of a list.'))

        self.assertFalse(docformatter.is_probably_beginning_of_sentence(
            '(this just continues an existing sentence).'))

    def test_is_probably_beginning_of_sentence_pydoc_ref(self):
        self.assertFalse(docformatter.is_probably_beginning_of_sentence(
            ':see:MyClass This is not the start of a sentence.'))

    def test_format_docstring_make_summary_multi_line(self):
        self.assertEqual(('''\
"""
    This one-line docstring will be multi-line.
    """\
'''),
                         docformatter.format_docstring('    ', '''\
"""This one-line docstring will be multi-line"""\
''', make_summary_multi_line=True))

    def test_exclude(self):
        sources = {"/root"}
        patch_data = [
            ("/root", ['folder_one', 'folder_two'], []),
            ("/root/folder_one", ['folder_three'], ["one.py"]),
            ("/root/folder_one/folder_three", [], ["three.py"]),
            ("/root/folder_two", [], ["two.py"]),
        ]
        with patch("os.walk", return_value=patch_data), patch("os.path.isdir", return_value=True):
            test_exclude_one = list(docformatter.find_py_files(sources, True, ["folder_one"]))
            self.assertEqual(test_exclude_one, ['/root/folder_two/two.py'])
            test_exclude_two = list(docformatter.find_py_files(sources, True, ["folder_two"]))
            self.assertEqual(test_exclude_two, ['/root/folder_one/one.py', '/root/folder_one/folder_three/three.py'])
            test_exclude_three = list(docformatter.find_py_files(sources, True, ["folder_three"]))
            self.assertEqual(test_exclude_three, ['/root/folder_one/one.py', '/root/folder_two/two.py'])
            test_exclude_py = list(docformatter.find_py_files(sources, True, ".py"))
            self.assertFalse(test_exclude_py)
            test_exclude_two_and_three = list(docformatter.find_py_files(sources, True, ["folder_two", "folder_three"]))
            self.assertEqual(test_exclude_two_and_three, ['/root/folder_one/one.py'])
            test_exclude_files = list(docformatter.find_py_files(sources, True, ["one.py", "two.py"]))
            self.assertEqual(test_exclude_files, ['/root/folder_one/folder_three/three.py'])

    def test_exclude_nothing(self):
        sources = {"/root"}
        patch_data = [
            ("/root", ['folder_one', 'folder_two'], []),
            ("/root/folder_one", ['folder_three'], ["one.py"]),
            ("/root/folder_one/folder_three", [], ["three.py"]),
            ("/root/folder_two", [], ["two.py"]),
        ]
        with patch("os.walk", return_value=patch_data), patch("os.path.isdir", return_value=True):
            test_exclude_nothing = list(docformatter.find_py_files(sources, True, []))
            self.assertEqual(test_exclude_nothing, ['/root/folder_one/one.py', '/root/folder_one/folder_three/three.py',
                                                    '/root/folder_two/two.py'])
            test_exclude_nothing = list(docformatter.find_py_files(sources, True))
            self.assertEqual(test_exclude_nothing, ['/root/folder_one/one.py', '/root/folder_one/folder_three/three.py',
                                                    '/root/folder_two/two.py'])

class TestSystem(unittest.TestCase):

    def test_diff(self):
        with temporary_file('''\
def foo():
    """
    Hello world
    """
''') as filename:
            output_file = io.StringIO()
            docformatter._main(argv=['my_fake_program', filename],
                               standard_out=output_file,
                               standard_error=None,
                               standard_in=None)
            self.assertEqual('''\
@@ -1,4 +1,2 @@
 def foo():
-    """
-    Hello world
-    """
+    """Hello world."""
''', '\n'.join(output_file.getvalue().split('\n')[2:]))

    def test_diff_with_nonexistent_file(self):
        output_file = io.StringIO()
        docformatter._main(argv=['my_fake_program', 'nonexistent_file'],
                           standard_out=output_file,
                           standard_error=output_file,
                           standard_in=None)
        self.assertIn('no such file', output_file.getvalue().lower())

    def test_in_place(self):
        with temporary_file('''\
def foo():
    """
    Hello world
    """
''') as filename:
            output_file = io.StringIO()
            docformatter._main(
                argv=['my_fake_program', '--in-place', filename],
                standard_out=output_file,
                standard_error=None,
                standard_in=None)
            with open(filename) as f:
                self.assertEqual('''\
def foo():
    """Hello world."""
''', f.read())

    def test_ignore_hidden_directories(self):
        with temporary_directory() as directory:
            with temporary_directory(prefix='.',
                                     directory=directory) as inner_directory:

                with temporary_file('''\
def foo():
    """
    Hello world
    """
''', directory=inner_directory):

                    output_file = io.StringIO()
                    docformatter._main(argv=['my_fake_program', '--recursive',
                                             directory],
                                       standard_out=output_file,
                                       standard_error=None,
                                       standard_in=None)
                    self.assertEqual(
                        '',
                        output_file.getvalue().strip())

    def test_end_to_end(self):
        with temporary_file('''\
def foo():
    """
    Hello world
    """
''') as filename:
            process = run_docformatter([filename])
            self.assertEqual('''\
@@ -1,4 +1,2 @@
 def foo():
-    """
-    Hello world
-    """
+    """Hello world."""
''', '\n'.join(process.communicate()[0].decode().split('\n')[2:]))

    def test_end_to_end_with_wrapping(self):
        with temporary_file('''\
def foo():
    """
    Hello world this is a summary that will get wrapped
    """
''') as filename:
            process = run_docformatter(['--wrap-summaries=40',
                                        filename])
            self.assertEqual('''\
@@ -1,4 +1,3 @@
 def foo():
-    """
-    Hello world this is a summary that will get wrapped
-    """
+    """Hello world this is a summary
+    that will get wrapped."""
''', '\n'.join(process.communicate()[0].decode().split('\n')[2:]))

    def test_end_to_end_with_no_wrapping(self):
        with temporary_file('''\
def foo():
    """Hello world is a long sentence that will not be wrapped because I turned wrapping off.

    Hello world is a long sentence that will not be wrapped because I turned wrapping off.
    """
''') as filename:
            process = run_docformatter(['--wrap-summaries=0',
                                        '--wrap-description=0',
                                        filename])
            self.assertEqual(
                '',
                '\n'.join(process.communicate()[0].decode().split('\n')[2:]))

    def test_end_to_end_all_options(self):
        with temporary_file('''\
def foo():
    """Hello world is a long sentence that will be wrapped at 40 characters because I'm using that option
    - My list item
    - My list item


    """
''') as filename:
            process = run_docformatter(['--wrap-summaries=40',
                                        '--wrap-summaries=40',
                                        '--pre-summary-newline',
                                        '--blank',
                                        filename])
            self.assertEqual('''\
@@ -1,7 +1,10 @@
 def foo():
-    """Hello world is a long sentence that will be wrapped at 40 characters because I'm using that option
+    """
+    Hello world is a long sentence that
+    will be wrapped at 40 characters
+    because I'm using that option.
+
     - My list item
     - My list item
 
-
     """
''', '\n'.join(process.communicate()[0].decode().split('\n')[2:]))

    def test_invalid_range(self):
        process = run_docformatter(['--range', '0', '1', os.devnull])
        self.assertIn('must be positive',
                      process.communicate()[1].decode())

        process = run_docformatter(['--range', '3', '1', os.devnull])
        self.assertIn('should be less than',
                      process.communicate()[1].decode())

    def test_no_arguments(self):
        process = run_docformatter([])
        self.assertIn('arguments',
                      process.communicate()[1].decode())

    def test_standard_in(self):
        process = run_docformatter(['-'])

        result = process.communicate('''\
"""
Hello world"""
'''.encode())[0].decode()

        self.assertEqual(0, process.returncode)

        self.assertEqual(
            '''"""Hello world."""\n''',
            result)

    def test_standard_in_with_invalid_options(self):
        process = run_docformatter(['foo.py', '-'])
        self.assertIn('cannot mix',
                      process.communicate()[1].decode())

        process = run_docformatter(['--in-place', '-'])
        self.assertIn('cannot be used',
                      process.communicate()[1].decode())

        process = run_docformatter(['--recursive', '-'])
        self.assertIn('cannot be used',
                      process.communicate()[1].decode())

    def test_io_error_exit_code(self):
        stderr = io.StringIO()
        ret_code = docformatter._main(
            argv=['my_fake_program', 'this_file_should_not_exist_please'],
            standard_out=None, standard_error=stderr, standard_in=None)
        self.assertEqual(ret_code, 1)

    def test_check_mode_correct_docstring(self):
        with temporary_file('''
"""Totally fine docstring, do not report anything."""
''') as filename:
            stdout = io.StringIO()
            stderr = io.StringIO()
            ret_code = docformatter._main(
                argv=['my_fake_program', '--check', filename],
                standard_out=stdout, standard_error=stderr, standard_in=None)
            self.assertEqual(ret_code, 0,
                             msg='Exit code should be 0')  # FormatResult.ok
            self.assertEqual(stdout.getvalue(), '',
                             msg='Do not write to stdout')
            self.assertEqual(stderr.getvalue(), '',
                             msg='Do not write to stderr')

    def test_check_mode_incorrect_docstring(self):
        with temporary_file('''
"""
Print my path and return error code
""" ''') as filename:
            stdout = io.StringIO()
            stderr = io.StringIO()
            ret_code = docformatter._main(
                argv=['my_fake_program', '--check', filename],
                standard_out=stdout, standard_error=stderr, standard_in=None)
            self.assertEqual(ret_code, 3,
                             msg='Exit code should be 3')  # FormatResult.check_failed
            self.assertEqual(stdout.getvalue(), '',
                             msg='Do not write to stdout')
            self.assertEqual(stderr.getvalue().strip(), filename,
                             msg='Changed file should be reported')


def generate_random_docstring(max_indentation_length=32,
                              max_word_length=20,
                              max_words=50):
    """Generate single-line docstring."""
    if random.randint(0, 1):
        words = []
    else:
        words = [generate_random_word(random.randint(0, max_word_length))
                 for _ in range(random.randint(0, max_words))]

    indentation = random.randint(0, max_indentation_length) * ' '
    quote = '"""' if random.randint(0, 1) else "'''"
    return (quote + indentation +
            ' '.join(words) +
            quote)


def generate_random_word(word_length):
    return ''.join(random.sample(string.ascii_letters, word_length))


@contextlib.contextmanager
def temporary_file(contents, directory='.', prefix=''):
    """Write contents to temporary file and yield it."""
    f = tempfile.NamedTemporaryFile(suffix='.py', prefix=prefix,
                                    delete=False, dir=directory)
    try:
        f.write(contents.encode())
        f.close()
        yield f.name
    finally:
        os.remove(f.name)


@contextlib.contextmanager
def temporary_directory(directory='.', prefix=''):
    """Create temporary directory and yield its path."""
    temp_directory = tempfile.mkdtemp(prefix=prefix, dir=directory)
    try:
        yield temp_directory
    finally:
        shutil.rmtree(temp_directory)


def run_docformatter(arguments):
    """Run subprocess with same Python path as parent.

    Return subprocess object.

    This is necessary for testing under "./setup.py test" without installing
    "untokenize".
    """
    environ = os.environ.copy()
    environ['PYTHONPATH'] = os.pathsep.join(sys.path)
    return subprocess.Popen(DOCFORMATTER_COMMAND + arguments,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE,
                            env=environ)


if __name__ == '__main__':
    unittest.main()
