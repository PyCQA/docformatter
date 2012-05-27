"""Test suite for docformatter."""

import docformatter
import unittest
import contextlib


class TestUnits(unittest.TestCase):

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

    def test_format_docstring(self):
        self.assertEqual('"""Hello."""',
                         docformatter.format_docstring('    ', '''
"""

Hello.
"""
'''.strip()))

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

    def test_format_code_with_multiple_sentences_multiline_summary(self):
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
    """Hello foo.

    This is a docstring.

    More stuff.

    """
''',
                docformatter.format_code(
'''\
def foo():
    """
    Hello
    foo. This is a docstring.

    More stuff.
    """
'''))

    def test_format_code_with_trailing_whitespace(self):
        self.assertEqual(
'''\
def foo():
    """Hello foo.

    This is a docstring.

    More stuff.

    """
''',
                docformatter.format_code(
'''\
def foo():
    """
    Hello
    foo. This is a docstring.\t

    More stuff.\t
    """
'''))

    def test_format_code_with_no_docstring(self):
        line = '''\
def foo():
    "Just a regular string"
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
    """Hello foo.

    This is a docstring.

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
    foo. This is a docstring.

    More stuff.
    """
    x = """My non-docstring
    This should not touched."""

    """More stuff
    that should not be
    touched\t"""
'''))

    def test_split_summary_and_description(self):
        self.assertEqual(('This is the first.',
                          'This is the second. This is the third.'),
                         docformatter.split_summary_and_description(
'This is the first. This is the second. This is the third.'))

    def test_split_summary_and_description_complex(self):
        self.assertEqual(('This is the first',
                          'This is the second. This is the third.'),
                         docformatter.split_summary_and_description(
'This is the first\n\nThis is the second. This is the third.'))

    def test_split_summary_and_description_more_complex(self):
        self.assertEqual(('This is the first.',
                          'This is the second. This is the third.'),
                         docformatter.split_summary_and_description(
'This is the first.\nThis is the second. This is the third.'))


def py27_and_above(func):
    import sys
    if sys.version_info < (2, 7):
        return None
    else:
        return func


@contextlib.contextmanager
def temporary_file(contents):
    """Write contents to temporary file and yield it."""
    import tempfile
    f = tempfile.NamedTemporaryFile(suffix='.py', delete=False)
    try:
        f.write(contents.encode('utf8'))
        f.close()
        yield f.name
    finally:
        import os
        os.remove(f.name)


class TestSystem(unittest.TestCase):

    @py27_and_above
    def test_diff(self):
        with temporary_file('''\
def foo():
    """
    
    Hello world
    
    """
''') as filename:
            import subprocess
            p = subprocess.Popen(['./docformatter', filename],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            (output, error) = p.communicate()
            self.assertFalse(error)
            self.assertEqual('''\
@@ -1,7 +1,3 @@
 def foo():
-    """
-    
-    Hello world
-    
-    """
+    """Hello world."""
 
''', '\n'.join(output.decode('utf8').split('\n')[2:]))


if __name__ == '__main__':
    unittest.main()
