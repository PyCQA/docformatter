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

    def test_format_code_raw_docstring_double_quotes(self):
        """Should format raw docstrings with triple double quotes.

        See requirement #2.  See issue #54 for request to handle raw
        docstrings.
        """
        self.assertEqual(
            '''\
def foo():
    r"""Hello foo."""
''',
            docformatter.format_code(
                '''\
def foo():
    r"""
    Hello foo.
    """
'''))

        self.assertEqual(
        '''\
def foo():
    R"""Hello foo."""
''',
            docformatter.format_code(
            '''\
def foo():
    R"""
    Hello foo.
    """
'''))

    def test_format_code_raw_docstring_single_quotes(self):
        """Should format raw docstrings with triple single quotes.

        See requirement #2.  See issue #54 for request to handle raw
        docstrings.
        """
        self.assertEqual(
            '''\
def foo():
    r"""Hello foo."""
''',
            docformatter.format_code(
                """\
def foo():
    r'''
    Hello foo.
    '''
"""))

        self.assertEqual(
        '''\
def foo():
    R"""Hello foo."""
''',
           docformatter.format_code(
            """\
def foo():
    R'''
    Hello foo.
    '''
"""))

    def test_format_code_unicode_docstring_double_quotes(self):
        """Should format unicode docstrings with triple double quotes.

        See requirement #3.  See issue #54 for request to handle raw
        docstrings.
        """
        self.assertEqual(
            '''\
def foo():
    u"""Hello foo."""
''',
            docformatter.format_code(
                '''\
def foo():
    u"""
    Hello foo.
    """
'''))

        self.assertEqual(
            '''\
def foo():
    U"""Hello foo."""
''',
            docformatter.format_code(
                '''\
def foo():
    U"""
    Hello foo.
    """
'''))

    def test_format_code_unicode_docstring_single_quotes(self):
        """Should format unicode docstrings with triple single quotes.

        See requirement #3.  See issue #54 for request to handle raw
        docstrings.
        """
        self.assertEqual(
            '''\
def foo():
    u"""Hello foo."""
''',
            docformatter.format_code(
                """\
def foo():
    u'''
    Hello foo.
    '''
"""))

        self.assertEqual(
            '''\
def foo():
    U"""Hello foo."""
''',
            docformatter.format_code(
                """\
def foo():
    U'''
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

    def test_ignore_code_with_single_quote(self):
        """Single single quote on first line of code should remain untouched.

        See requirement 1, always use triple double quotes.
        See issue #66 for example of docformatter breaking code when encountering
        single quote.
        """
        self.assertEqual(
                '''\
def foo():
    'Just a regular string'
''',
            docformatter.format_code(
                '''\
def foo():
    'Just a regular string'
'''))

    def test_ignore_code_with_double_quote(self):
        """Single double quotes on first line of code should remain untouched.

        See requirement 1, always use triple double quotes.
        See issue #66 for example of docformatter breaking code when encountering
        single quote.
        """
        self.assertEqual(
                '''\
def foo():
    "Just a regular string"
''',
            docformatter.format_code(
                '''\
def foo():
    "Just a regular string"
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

    def test_format_code_additional_empty_line_before_doc(self):
        args = {'summary_wrap_length': 79,
                'description_wrap_length': 72,
                'pre_summary_newline': False,
                'make_summary_multi_line': False,
                'post_description_blank': False,
                'force_wrap': False,
                'line_range': None}
        self.assertEqual('\n\n\ndef my_func():\n"""Summary of my function."""\npass',
                         docformatter._format_code('\n\n\ndef my_func():\n\n"""Summary of my function."""\npass', args))

    def test_format_code_extra_newline_following_comment(self):
        args = {'summary_wrap_length': 79,
                'description_wrap_length': 72,
                'pre_summary_newline': False,
                'pre_summary_space': False,
                'make_summary_multi_line': False,
                'post_description_blank': False,
                'force_wrap': False,
                'line_range': None}

        docstring = ('''\
def crash_rocket(location):    # pragma: no cover

    """This is a docstring following an in-line comment."""
    return location''')
        self.assertEqual('''\
def crash_rocket(location):    # pragma: no cover
    """This is a docstring following an in-line comment."""
    return location''',
                         docformatter._format_code(docstring))

    def test_format_code_no_docstring(self):
        args = {'summary_wrap_length': 79,
                'description_wrap_length': 72,
                'pre_summary_newline': False,
                'pre_summary_space': False,
                'make_summary_multi_line': False,
                'post_description_blank': False,
                'force_wrap': False,
                'line_range': None}
        docstring = ("def pytest_addoption(parser: pytest.Parser) -> "
        "None:\n    register_toggle.pytest_addoption(parser)\n")
        self.assertEqual(docstring,
                         docformatter._format_code(docstring, args))

        docstring = ("def pytest_addoption(parser: pytest.Parser) -> "
                     "None:    # pragma: no cover\n    "
                     "register_toggle.pytest_addoption(parser)\n")
        self.assertEqual(docstring,
                         docformatter._format_code(docstring, args))

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
''', '\n'.join(process.communicate()[0].decode().replace("\r", "").split(
                '\n')[2:]))

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
''', '\n'.join(process.communicate()[0].decode().replace("\r", "").split(
                '\n')[2:]))

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
                '\n'.join(process.communicate()[0].decode().replace("\r", "").split('\n')[2:]))

    def test_end_to_end_with_no_wrapping_2(self):
        with temporary_file('''\
def foo():
    """Hello world is a long sentence that will not
    be wrapped because I turned wrapping off.

    Hello world is a long sentence that will not
    be wrapped because I turned wrapping off.
    """
''') as filename:
            process = run_docformatter(['--wrap-summaries=0',
                                        '--wrap-description=0',
                                        filename])
            self.assertEqual(
                '',
                '\n'.join(process.communicate()[0].decode().replace("\r", "").split('\n')[2:]))

    def test_end_to_end_no_wrapping_period(self):
        with temporary_file('''\
def foo():
    """Wrapping is off, but it will still add
    the trailing period  """
''') as filename:
            process = run_docformatter(['--wrap-summaries=0',
                                        filename])
            self.assertEqual('''\
@@ -1,3 +1,3 @@
 def foo():
     """Wrapping is off, but it will still add
-    the trailing period  """
+    the trailing period."""
''', '\n'.join(process.communicate()[0].decode().replace("\r", "").split(
                '\n')[2:]))


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
''', '\n'.join(process.communicate()[0].decode().replace("\r", "").split(
                '\n')[2:]))

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
'''.encode())[0].decode().replace("\r", "")

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
