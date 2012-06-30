"""Test suite for docformatter."""

import docformatter
import contextlib

try:
    from StringIO import StringIO
except ImportError:
    # Python 3
    from io import StringIO

try:
    # Python 2.6
    import unittest2 as unittest
except:
    import unittest


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

    def test_format_docstring_with_bad_indentation(self):
        self.assertEqual('''"""Hello.

    This should be indented but it is not. The
    next line should be indented too. But
    this is okay.

    """''',
                         docformatter.format_docstring('    ', '''
"""Hello.

This should be indented but it is not. The
next line should be indented too. But
    this is okay.
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

    def test_format_docstring_with_single_quotes_multiline(self):
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

    def test_split_summary_and_description_with_list(self):
        self.assertEqual(('This is the first',
                          '- one\n- two'),
                         docformatter.split_summary_and_description(
'This is the first\n- one\n- two'))

    def test_split_summary_and_description_with_other_symbol(self):
        self.assertEqual(('This is the first',
                          '@ one\n@ two'),
                         docformatter.split_summary_and_description(
'This is the first\n@ one\n@ two'))

    def test_normalize_summary(self):
        self.assertEqual(
                'This is a sentence.',
                docformatter.normalize_summary('This \n\t is\na sentence'))

    def test_normalize_summary_with_different_punctuation(self):
        summary = 'This is a question?'
        self.assertEqual(
                summary,
                docformatter.normalize_summary(summary))


@contextlib.contextmanager
def temporary_file(contents):
    """Write contents to temporary file and yield it."""
    import tempfile
    f = tempfile.NamedTemporaryFile(suffix='.py', delete=False, dir='.')
    try:
        f.write(contents.encode('utf8'))
        f.close()
        yield f.name
    finally:
        import os
        os.remove(f.name)


class TestSystem(unittest.TestCase):

    def test_diff(self):
        with temporary_file('''\
def foo():
    """
    Hello world
    """
''') as filename:
            output_file = StringIO()
            docformatter.main(argv=['my_fake_program', filename],
                              standard_out=output_file)
            self.assertEqual('''\
@@ -1,4 +1,2 @@
 def foo():
-    """
-    Hello world
-    """
+    """Hello world."""
''', '\n'.join(output_file.getvalue().split('\n')[2:]))

    def test_in_place(self):
        with temporary_file('''\
def foo():
    """
    Hello world
    """
''') as filename:
            output_file = StringIO()
            try:
                docformatter.main(argv=['my_fake_program', '--in-place', filename],
                                  standard_out=output_file)
                with open(filename) as f:
                    self.assertEqual('''\
def foo():
    """Hello world."""
''', f.read())
            finally:
                # Clean up backup file
                import os
                os.remove(filename + '.backup')

    def test_end_to_end(self):
        with temporary_file('''\
def foo():
    """
    Hello world
    """
''') as filename:
            import subprocess
            process = subprocess.Popen(['./docformatter', filename],
                                       stdout=subprocess.PIPE)
            self.assertEqual('''\
@@ -1,4 +1,2 @@
 def foo():
-    """
-    Hello world
-    """
+    """Hello world."""
''', '\n'.join(process.communicate()[0].decode('utf-8').split('\n')[2:]))

    def test_end_to_end_with_wrapping(self):
        with temporary_file('''\
def foo():
    """
    Hello world this is a summary that will get wrapped
    """
''') as filename:
            import subprocess
            process = subprocess.Popen(['./docformatter',
                                        '--wrap-long-summaries=40',
                                        filename],
                                       stdout=subprocess.PIPE)
            self.assertEqual('''\
@@ -1,4 +1,3 @@
 def foo():
-    """
-    Hello world this is a summary that will get wrapped
-    """
+    """Hello world this is a summary
+    that will get wrapped."""
''', '\n'.join(process.communicate()[0].decode('utf-8').split('\n')[2:]))

    def test_end_to_end_all_options(self):
        with temporary_file('''\
def foo():
    """Hello world is a long sentence that will be wrapped at 40 characters because I'm using that option
    - My list item
    - My list item


    """
''') as filename:
            import subprocess
            process = subprocess.Popen(['./docformatter',
                                        '--wrap-long-summaries=40',
                                        '--pre-summary-newline',
                                        '--no-blank',
                                        filename],
                                       stdout=subprocess.PIPE)
            self.assertEqual('''\
@@ -1,7 +1,9 @@
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
-
     """
''', '\n'.join(process.communicate()[0].decode('utf-8').split('\n')[2:]))

    def test_no_arguments(self):
        import subprocess
        process = subprocess.Popen(['./docformatter'],
                                   stderr=subprocess.PIPE)
        self.assertIn('too few arguments',
                      process.communicate()[1].decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
