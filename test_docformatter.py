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
