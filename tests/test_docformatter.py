# pylint: skip-file
# type: ignore
#
#       tests.test_docformatter.py is part of the docformatter project
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
"""Module for testing docformatter end-to-end."""

# Standard Library Imports
import io
import os

# Third Party Imports
import pytest

# docformatter Package Imports
from docformatter import __main__ as main


class TestMain:
    """Class for testing the _main() function."""

    @pytest.mark.system
    @pytest.mark.parametrize(
        "contents",
        [
            '''\
    def foo():
        """
        Hello world
        """
'''
        ],
    )
    def test_diff(self, temporary_file, contents):
        """Should produce diff showing changes."""
        output_file = io.StringIO()
        main._main(
            argv=["my_fake_program", temporary_file],
            standard_out=output_file,
            standard_error=None,
            standard_in=None,
        )

        assert '''\
@@ -1,4 +1,2 @@
     def foo():
-        """
-        Hello world
-        """
+        """Hello world."""
''' == "\n".join(
            output_file.getvalue().split("\n")[2:]
        )

    @pytest.mark.system
    def test_diff_with_nonexistent_file(self):
        """Should return error message when file doesn't exist."""
        output_file = io.StringIO()
        main._main(
            argv=["my_fake_program", "nonexistent_file"],
            standard_out=output_file,
            standard_error=output_file,
            standard_in=None,
        )
        assert "no such file" in output_file.getvalue().lower()

    @pytest.mark.system
    @pytest.mark.parametrize(
        "contents",
        [
            '''\
def foo():
    """
    Hello world
    """
'''
        ],
    )
    @pytest.mark.parametrize(
        "diff", [True, False], ids=["show-diff", "no-diff"]
    )
    def test_in_place(self, temporary_file, contents, diff):
        """Should make changes and save back to file."""
        output_file = io.StringIO()
        args = ["my_fake_program", "--in-place", temporary_file]
        if diff:
            args.append("--diff")

        main._main(
            argv=args,
            standard_out=output_file,
            standard_error=None,
            standard_in=None,
        )
        with open(temporary_file) as f:
            assert (
                '''\
def foo():
    """Hello world."""
'''
                == f.read()
            )

        if diff:
            assert "def foo" in output_file.getvalue()
        else:
            assert "def foo" not in output_file

    @pytest.mark.system
    @pytest.mark.parametrize(
        "contents",
        [
            '''\
def foo():
    """
    Hello world
    """
'''
        ],
    )
    @pytest.mark.parametrize("file_directory", ["temporary_directory"])
    @pytest.mark.parametrize("directory", ["."])
    @pytest.mark.parametrize("prefix", ["."])
    def test_ignore_hidden_directories(
        self,
        temporary_file,
        temporary_directory,
        contents,
        file_directory,
        directory,
        prefix,
    ):
        """Ignore 'hidden' directories when recursing."""
        output_file = io.StringIO()
        main._main(
            argv=["my_fake_program", "--recursive", temporary_directory],
            standard_out=output_file,
            standard_error=None,
            standard_in=None,
        )
        assert "" == output_file.getvalue().strip()

    @pytest.mark.system
    def test_io_error_exit_code(self):
        """Return error code 1 when file does not exist."""
        stderr = io.StringIO()
        ret_code = main._main(
            argv=["my_fake_program", "this_file_should_not_exist_please"],
            standard_out=None,
            standard_error=stderr,
            standard_in=None,
        )

        assert ret_code == 1

    @pytest.mark.system
    @pytest.mark.parametrize(
        "contents",
        ["""Totally fine docstring, do not report anything."""],
    )
    @pytest.mark.parametrize(
        "diff", [True, False], ids=["show-diff", "no-diff"]
    )
    def test_check_mode_correct_docstring(
        self, temporary_file, contents, diff
    ):
        """"""
        stdout = io.StringIO()
        stderr = io.StringIO()
        args = ["my_fake_program", "--check", temporary_file]
        if diff:
            args.append("--diff")

        ret_code = main._main(
            argv=args,
            standard_out=stdout,
            standard_error=stderr,
            standard_in=None,
        )

        assert ret_code == 0  # FormatResult.ok
        assert stdout.getvalue() == ""
        assert stderr.getvalue() == ""

    @pytest.mark.system
    @pytest.mark.parametrize(
        "contents",
        [
            '''
    """
Print my path and return error code
"""
'''
        ],
    )
    @pytest.mark.parametrize(
        "diff", [True, False], ids=["show-diff", "no-diff"]
    )
    def test_check_mode_incorrect_docstring(
        self, temporary_file, contents, diff
    ):
        """"""
        stdout = io.StringIO()
        stderr = io.StringIO()
        args = ["my_fake_program", "--check", temporary_file]
        if diff:
            args.append("--diff")

        ret_code = main._main(
            argv=args,
            standard_out=stdout,
            standard_error=stderr,
            standard_in=None,
        )
        assert ret_code == 3  # FormatResult.check_failed
        if diff:
            assert "Print my path" in stdout.getvalue()
        else:
            assert stdout.getvalue() == ""
        assert stderr.getvalue().strip() == temporary_file


class TestEndToEnd:
    """Class to test docformatter by executing it from the command line."""

    @pytest.mark.system
    @pytest.mark.parametrize(
        "contents",
        [
            '''\
    def foo():
        """
        Hello world
        """
'''
        ],
    )
    @pytest.mark.parametrize("arguments", [[]])
    def test_end_to_end(
        self,
        temporary_file,
        contents,
        run_docformatter,
        arguments,
    ):
        """"""
        assert '''\
@@ -1,4 +1,2 @@
     def foo():
-        """
-        Hello world
-        """
+        """Hello world."""
''' == "\n".join(
            run_docformatter.communicate()[0]
            .decode()
            .replace("\r", "")
            .split("\n")[2:]
        )

    @pytest.mark.system
    @pytest.mark.parametrize(
        "contents",
        [
            '''\
def foo():
    """
    Hello world this is a summary that will get wrapped
    """
'''
        ],
    )
    @pytest.mark.parametrize("arguments", [["--wrap-summaries=40"]])
    def test_end_to_end_with_wrapping(
        self,
        run_docformatter,
        temporary_file,
        contents,
        arguments,
    ):
        """Wrap summary at --wrap-summaries number of columns."""
        assert '''\
@@ -1,4 +1,3 @@
 def foo():
-    """
-    Hello world this is a summary that will get wrapped
-    """
+    """Hello world this is a summary
+    that will get wrapped."""
''' == "\n".join(
            run_docformatter.communicate()[0]
            .decode()
            .replace("\r", "")
            .split("\n")[2:]
        )

    @pytest.mark.system
    @pytest.mark.parametrize(
        "contents",
        [
            '''\
def foo():
    """Hello world is a long sentence that will not be wrapped because I turned wrapping off.

    Hello world is a long sentence that will not be wrapped because I turned wrapping off.
    """
'''
        ],
    )
    @pytest.mark.parametrize(
        "arguments", [["--wrap-summaries=0", "--wrap-description=0"]]
    )
    def test_end_to_end_with_no_wrapping_long_sentences(
        self,
        run_docformatter,
        temporary_file,
        contents,
        arguments,
    ):
        """Long sentences remain long with wrapping turned off."""
        assert "" == "\n".join(
            run_docformatter.communicate()[0]
            .decode()
            .replace("\r", "")
            .split("\n")[2:]
        )

    @pytest.mark.system
    @pytest.mark.parametrize(
        "contents",
        [
            '''\
def foo():
    """Hello world is a long sentence that will not
    be wrapped because I turned wrapping off.

    Hello world is a long sentence that will not
    be wrapped because I turned wrapping off.
    """
'''
        ],
    )
    @pytest.mark.parametrize(
        "arguments", [["--wrap-summaries=0", "--wrap-description=0"]]
    )
    def test_end_to_end_with_no_wrapping_short_sentences(
        self,
        run_docformatter,
        temporary_file,
        arguments,
        contents,
    ):
        """Short sentences remain short with wrapping turned off."""
        assert "" == "\n".join(
            run_docformatter.communicate()[0]
            .decode()
            .replace("\r", "")
            .split("\n")[2:]
        )

    @pytest.mark.system
    @pytest.mark.parametrize(
        "contents",
        [
            '''\
def foo():
    """Wrapping is off, but it will still add
    the trailing period  """
'''
        ],
    )
    @pytest.mark.parametrize("arguments", [["--wrap-summaries=0"]])
    def test_end_to_end_no_wrapping_period(
        self,
        run_docformatter,
        temporary_file,
        arguments,
        contents,
    ):
        """Add period to end of summary even with wrapping off."""
        assert '''\
@@ -1,3 +1,3 @@
 def foo():
     """Wrapping is off, but it will still add
-    the trailing period  """
+    the trailing period."""
''' == "\n".join(
            run_docformatter.communicate()[0]
            .decode()
            .replace("\r", "")
            .split("\n")[2:]
        )

    @pytest.mark.system
    @pytest.mark.parametrize(
        "contents",
        [
            '''\
def foo():
    """Description from issue #145 that was being improperly wrapped.

    .. _linspace API: https://numpy.org/doc/stable/reference/generated/numpy.linspace.html
    .. _arange API: https://numpy.org/doc/stable/reference/generated/numpy.arange.html
    .. _logspace API: https://numpy.org/doc/stable/reference/generated/numpy.logspace.html
    """
'''
        ],
    )
    @pytest.mark.parametrize(
        "arguments",
        [
            [
                "--wrap-summaries=72",
                "--wrap-descriptions=78",
            ]
        ],
    )
    def test_end_to_end_keep_rest_link_one_line(
        self,
        run_docformatter,
        temporary_file,
        arguments,
        contents,
    ):
        """Keep reST in-line URL link on one line.

        See issue #145. See requirement docformatter_10.1.3.1.
        """
        assert "" == "\n".join(
            run_docformatter.communicate()[0]
            .decode()
            .replace("\r", "")
            .split("\n")[2:]
        )

    @pytest.mark.system
    @pytest.mark.parametrize(
        "contents",
        [
            '''\
def foo():
    """Description from issue #150 that was being improperly wrapped.

    The text file can be retrieved via the Chrome plugin `Get 
    Cookies.txt <https://chrome.google.com/webstore/detail/get-
    cookiestxt/bgaddhkoddajcdgocldbbfleckgcbcid>` while browsing."""
'''
        ],
    )
    @pytest.mark.parametrize(
        "arguments",
        [
            [
                "--wrap-summaries=72",
                "--wrap-descriptions=78",
            ]
        ],
    )
    def test_ignore_already_wrapped_link(
        self,
        run_docformatter,
        temporary_file,
        arguments,
        contents,
    ):
        """Ignore a URL link that was wrapped by the user.

        See issue #150.
        """
        assert '''\
@@ -1,6 +1,7 @@
 def foo():
     """Description from issue #150 that was being improperly wrapped.
 
-    The text file can be retrieved via the Chrome plugin `Get 
+    The text file can be retrieved via the Chrome plugin `Get
     Cookies.txt <https://chrome.google.com/webstore/detail/get-
-    cookiestxt/bgaddhkoddajcdgocldbbfleckgcbcid>` while browsing."""
+    cookiestxt/bgaddhkoddajcdgocldbbfleckgcbcid>` while browsing.
+    """
''' == "\n".join(
            run_docformatter.communicate()[0]
            .decode()
            .replace("\r", "")
            .split("\n")[2:]
        )

    @pytest.mark.system
    @pytest.mark.parametrize(
        "contents",
        [
            '''\
def foo():
    """Hello world is a long sentence that will be wrapped at 40 characters because I'm using that option
    - My list item
    - My list item


    """
'''
        ],
    )
    @pytest.mark.parametrize(
        "arguments",
        [
            [
                "--wrap-summaries=40",
                "--pre-summary-newline",
                "--blank",
            ]
        ],
    )
    def test_end_to_end_all_options(
        self,
        run_docformatter,
        temporary_file,
        arguments,
        contents,
    ):
        """"""
        assert '''\
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
''' == "\n".join(
            run_docformatter.communicate()[0]
            .decode()
            .replace("\r", "")
            .split("\n")[2:]
        )

    @pytest.mark.system
    @pytest.mark.parametrize("contents", [""])
    @pytest.mark.parametrize(
        "arguments",
        [
            ["--range", "0", "1", os.devnull],
            ["--range", "3", "1", os.devnull],
        ],
    )
    def test_invalid_range(
        self,
        run_docformatter,
        arguments,
        contents,
    ):
        """"""
        if arguments[1] == "0":
            assert (
                "must be positive"
                in run_docformatter.communicate()[1].decode()
            )
        if arguments[1] == "3":
            assert (
                "should be less than"
                in run_docformatter.communicate()[1].decode()
            )

    @pytest.mark.system
    @pytest.mark.parametrize("arguments", [[]])
    @pytest.mark.parametrize("contents", [""])
    def test_no_arguments(
        self,
        run_docformatter,
        arguments,
        contents,
    ):
        """"""
        assert "" == run_docformatter.communicate()[1].decode()

    @pytest.mark.system
    @pytest.mark.parametrize("arguments", [["-"]])
    @pytest.mark.parametrize("contents", [""])
    def test_standard_in(
        self,
        run_docformatter,
        arguments,
        contents,
    ):
        result = (
            run_docformatter.communicate(
                '''\
"""
Hello world"""
'''.encode()
            )[0]
            .decode()
            .replace("\r", "")
        )

        assert 0 == run_docformatter.returncode
        assert '''"""Hello world."""\n''' == result

    @pytest.mark.system
    @pytest.mark.parametrize(
        "arguments",
        [
            ["foo.py", "-"],
            ["--in-place", "-"],
            ["--recursive", "-"],
        ],
    )
    @pytest.mark.parametrize("contents", [""])
    def test_standard_in_with_invalid_options(
        self,
        run_docformatter,
        arguments,
        contents,
    ):
        """"""
        if arguments[0] == "foo.py":
            assert "cannot mix" in run_docformatter.communicate()[1].decode()

        if arguments[0] == "--in-place":
            assert (
                "cannot be used" in run_docformatter.communicate()[1].decode()
            )

        if arguments[0] == "--recursive":
            assert (
                "cannot be used" in run_docformatter.communicate()[1].decode()
            )


class TestEndToEndPyproject:
    """Class to test docformatter using pyproject.toml for options."""

    @pytest.mark.system
    @pytest.mark.parametrize(
        "contents",
        [
            '''\
            class TestFoo():
                """Docstring that should not have a pre-summary space."""
            '''
        ],
    )
    @pytest.mark.parametrize(
        "config",
        [
            """\
[tool.docformatter]
pre-summary-space = false
"""
        ],
    )
    @pytest.mark.parametrize(
        "arguments",
        [
            [
                "--config",
                "/tmp/pyproject.toml",
            ]
        ],
    )
    def test_no_pre_summary_space_using_pyproject(
        self,
        run_docformatter,
        temporary_pyproject_toml,
        temporary_file,
        arguments,
        contents,
        config,
    ):
        """No pre-summary space using configuration from pyproject.toml.

        See issue #119.
        """
        assert '''\
@@ -1,3 +1,2 @@
             class TestFoo():
                 """Docstring that should not have a pre-summary space."""
-            
''' == "\n".join(
            run_docformatter.communicate()[0]
            .decode()
            .replace("\r", "")
            .split("\n")[2:]
        )

    @pytest.mark.system
    @pytest.mark.parametrize(
        "contents",
        [
            '''\
                class TestFoo():
                    """Docstring that should have a pre-summary space."""
                '''
        ],
    )
    @pytest.mark.parametrize(
        "config",
        [
            """\
                [tool.docformatter]
                pre-summary-space = true
                """
        ],
    )
    @pytest.mark.parametrize(
        "arguments",
        [
            [
                "--config",
                "/tmp/pyproject.toml",
            ]
        ],
    )
    def test_pre_summary_space_using_pyproject(
        self,
        run_docformatter,
        temporary_pyproject_toml,
        temporary_file,
        arguments,
        contents,
        config,
    ):
        """Pre-summary space using configuration from pyproject.toml.

        See issue #119.
        """
        assert '''\
@@ -1,3 +1,2 @@
                 class TestFoo():
-                    """Docstring that should have a pre-summary space."""
-                
+                    """ Docstring that should have a pre-summary space."""
''' == "\n".join(
            run_docformatter.communicate()[0]
            .decode()
            .replace("\r", "")
            .split("\n")[2:]
        )

    @pytest.mark.system
    @pytest.mark.parametrize(
        "contents",
        [
            '''\
            class TestFoo():
                """Docstring that should not have a pre-summary newline.
                
                This is a multi-line docstring that should not have a 
                newline placed before the summary."""
            '''
        ],
    )
    @pytest.mark.parametrize(
        "config",
        [
            """\
                [tool.docformatter]
                pre-summary-newline = false
                """
        ],
    )
    @pytest.mark.parametrize(
        "arguments",
        [
            [
                "--config",
                "/tmp/pyproject.toml",
            ]
        ],
    )
    def test_no_pre_summary_newline_using_pyproject(
        self,
        run_docformatter,
        temporary_pyproject_toml,
        temporary_file,
        arguments,
        contents,
        config,
    ):
        """No pre-summary newline using configuration from pyproject.toml.

        See issue #119.
        """
        assert '''\
@@ -1,6 +1,6 @@
             class TestFoo():
                 """Docstring that should not have a pre-summary newline.
-                
-                This is a multi-line docstring that should not have a 
-                newline placed before the summary."""
-            
+
+                This is a multi-line docstring that should not have a
+                newline placed before the summary.
+                """
''' == "\n".join(
            run_docformatter.communicate()[0]
            .decode()
            .replace("\r", "")
            .split("\n")[2:]
        )

    @pytest.mark.system
    @pytest.mark.parametrize(
        "contents",
        [
            '''\
class TestFoo():
    """Docstring that should have a pre-summary newline.

    This is a multi-line docstring that should have a newline 
    placed before the summary."""
'''
        ],
    )
    @pytest.mark.parametrize(
        "config",
        [
            """\
                [tool.docformatter]
                pre-summary-newline = true
                """
        ],
    )
    @pytest.mark.parametrize(
        "arguments",
        [
            [
                "--config",
                "/tmp/pyproject.toml",
            ]
        ],
    )
    def test_pre_summary_newline_using_pyproject(
        self,
        run_docformatter,
        temporary_pyproject_toml,
        temporary_file,
        arguments,
        contents,
        config,
    ):
        """Pre-summary newline using configuration from pyproject.toml.

        See issue #119.
        """
        assert '''\
@@ -1,5 +1,7 @@
 class TestFoo():
-    """Docstring that should have a pre-summary newline.
+    """
+    Docstring that should have a pre-summary newline.
 
-    This is a multi-line docstring that should have a newline 
-    placed before the summary."""
+    This is a multi-line docstring that should have a newline placed
+    before the summary.
+    """
''' == "\n".join(
            run_docformatter.communicate()[0]
            .decode()
            .replace("\r", "")
            .split("\n")[2:]
        )

    @pytest.mark.system
    @pytest.mark.parametrize(
        "contents",
        [
            '''\
                class TestFoo():
                    """Really long summary docstring that should not be 
                    split into a multiline summary."""
                '''
        ],
    )
    @pytest.mark.parametrize(
        "config",
        [
            """\
                    [tool.docformatter]
                    pre-summary-multi-line = false
                    """
        ],
    )
    @pytest.mark.parametrize(
        "arguments",
        [
            [
                "--config",
                "/tmp/pyproject.toml",
            ]
        ],
    )
    def test_no_pre_summary_multiline_using_pyproject(
        self,
        run_docformatter,
        temporary_pyproject_toml,
        temporary_file,
        arguments,
        contents,
        config,
    ):
        """No pre-summary multi-line using configuration from pyproject.toml.

        See issue #119.
        """
        assert '''\
@@ -1,4 +1,3 @@
                 class TestFoo():
-                    """Really long summary docstring that should not be 
-                    split into a multiline summary."""
-                
+                    """Really long summary docstring that should not be split
+                    into a multiline summary."""
''' == "\n".join(
            run_docformatter.communicate()[0]
            .decode()
            .replace("\r", "")
            .split("\n")[2:]
        )

    @pytest.mark.system
    @pytest.mark.parametrize(
        "contents",
        [
            '''\
                    class TestFoo():
                        """Really long summary docstring that should be 
                        split into a multiline summary."""
                    '''
        ],
    )
    @pytest.mark.parametrize(
        "config",
        [
            """\
                        [tool.docformatter]
                        pre-summary-multi-line = true
                        """
        ],
    )
    @pytest.mark.parametrize(
        "arguments",
        [
            [
                "--config",
                "/tmp/pyproject.toml",
            ]
        ],
    )
    def test_pre_summary_multiline_using_pyproject(
        self,
        run_docformatter,
        temporary_pyproject_toml,
        temporary_file,
        arguments,
        contents,
        config,
    ):
        """Pre-summary multi-line using configuration from pyproject.toml.

        See issue #119.
        """
        assert '''\
@@ -1,4 +1,3 @@
                     class TestFoo():
-                        """Really long summary docstring that should be 
-                        split into a multiline summary."""
-                    
+                        """Really long summary docstring that should be split
+                        into a multiline summary."""
''' == "\n".join(
            run_docformatter.communicate()[0]
            .decode()
            .replace("\r", "")
            .split("\n")[2:]
        )

    @pytest.mark.system
    @pytest.mark.parametrize(
        "contents",
        [
            '''\
class TestFoo():
    """Summary docstring that is followed by a description.

    This is the description and it shouldn't have a blank line 
    inserted after it.
    """
'''
        ],
    )
    @pytest.mark.parametrize(
        "config",
        [
            """\
                        [tool.docformatter]
                        blank = false
                        """
        ],
    )
    @pytest.mark.parametrize(
        "arguments",
        [
            [
                "--config",
                "/tmp/pyproject.toml",
            ]
        ],
    )
    def test_no_blank_using_pyproject(
        self,
        run_docformatter,
        temporary_pyproject_toml,
        temporary_file,
        arguments,
        contents,
        config,
    ):
        """No blank after description using configuration from pyproject.toml.

        See issue #119.
        """
        assert '''\
@@ -1,6 +1,6 @@
 class TestFoo():
     """Summary docstring that is followed by a description.
 
-    This is the description and it shouldn\'t have a blank line 
-    inserted after it.
+    This is the description and it shouldn\'t have a blank line inserted
+    after it.
     """
''' == "\n".join(
            run_docformatter.communicate()[0]
            .decode()
            .replace("\r", "")
            .split("\n")[2:]
        )

    @pytest.mark.system
    @pytest.mark.parametrize(
        "contents",
        [
            '''\
class TestFoo():
    """Summary docstring that is followed by a description.

    This is the description and it should have a blank line 
    inserted after it.
    """
'''
        ],
    )
    @pytest.mark.parametrize(
        "config",
        [
            """\
            [tool.docformatter]
            blank = true
            """
        ],
    )
    @pytest.mark.parametrize(
        "arguments",
        [
            [
                "--config",
                "/tmp/pyproject.toml",
            ]
        ],
    )
    def test_blank_using_pyproject(
        self,
        run_docformatter,
        temporary_pyproject_toml,
        temporary_file,
        arguments,
        contents,
        config,
    ):
        """Blank after description using configuration from pyproject.toml.

        See issue #119.
        """
        assert '''\
@@ -1,6 +1,7 @@
 class TestFoo():
     """Summary docstring that is followed by a description.
 
-    This is the description and it should have a blank line 
-    inserted after it.
+    This is the description and it should have a blank line inserted
+    after it.
+
     """
''' == "\n".join(
            run_docformatter.communicate()[0]
            .decode()
            .replace("\r", "")
            .split("\n")[2:]
        )

    @pytest.mark.system
    @pytest.mark.parametrize(
        "contents",
        [
            '''\
class foo():
    """Hello world is a long sentence that will be wrapped at 12 
    characters because I\'m using that option in pyproject.toml."""
'''
        ],
    )
    @pytest.mark.parametrize(
        "config",
        [
            """\
                [tool.docformatter]
                wrap-summaries = 12
                """
        ],
    )
    @pytest.mark.parametrize(
        "arguments",
        [
            [
                "--config",
                "/tmp/pyproject.toml",
            ]
        ],
    )
    def test_format_wrap_using_pyproject(
        self,
        run_docformatter,
        temporary_pyproject_toml,
        temporary_file,
        arguments,
        contents,
        config,
    ):
        """Wrap docstring using configuration from pyproject.toml.

        See issue #119.
        """
        assert '''\
@@ -1,3 +1,18 @@
 class foo():
-    """Hello world is a long sentence that will be wrapped at 12 
-    characters because I\'m using that option in pyproject.toml."""
+    """Hello
+    world is
+    a long
+    sentence
+    that
+    will be
+    wrapped
+    at 12 ch
+    aracters
+    because
+    I\'m
+    using
+    that
+    option
+    in pypro
+    ject.tom
+    l."""
''' == "\n".join(
            run_docformatter.communicate()[0]
            .decode()
            .replace("\r", "")
            .split("\n")[2:]
        )


class TestEndToEndSetupcfg:
    """Class to test docformatter using setup.cfg for options."""

    @pytest.mark.system
    @pytest.mark.parametrize(
        "contents",
        [
            '''\
class TestFoo():
    """ Docstring that should not have a pre-summary space."""
'''
        ],
    )
    @pytest.mark.parametrize(
        "config",
        [
            """\
[docformatter]
pre-summary-space = false
"""
        ],
    )
    @pytest.mark.parametrize(
        "arguments",
        [
            [
                "--config",
                "/tmp/setup.cfg",
            ]
        ],
    )
    def test_no_pre_summary_space_using_setup_cfg(
        self,
        run_docformatter,
        temporary_setup_cfg,
        temporary_file,
        arguments,
        contents,
        config,
    ):
        """No pre-summary space using configuration from setup.cfg.

        See issue #119.
        """
        assert '''\
@@ -1,2 +1,2 @@
 class TestFoo():
-    """ Docstring that should not have a pre-summary space."""
+    """Docstring that should not have a pre-summary space."""
''' == "\n".join(
            run_docformatter.communicate()[0]
            .decode()
            .replace("\r", "")
            .split("\n")[2:]
        )

    @pytest.mark.system
    @pytest.mark.parametrize(
        "contents",
        [
            '''\
class TestFoo():
    """ Docstring that should not have a pre-summary space."""
'''
        ],
    )
    @pytest.mark.parametrize(
        "config",
        [
            """\
[docformatter]
in-place = true
check = false
diff = false
"""
        ],
    )
    @pytest.mark.parametrize(
        "arguments",
        [
            [
                "--config",
                "/tmp/setup.cfg",
            ]
        ],
    )
    def test_in_place_using_setup_cfg(
        self,
        run_docformatter,
        temporary_setup_cfg,
        temporary_file,
        arguments,
        contents,
        config,
    ):
        """Make changes in-place if set in setup.cfg.

        See issue #122.
        """
        assert "" == "\n".join(
            run_docformatter.communicate()[0]
            .decode()
            .replace("\r", "")
            .split("\n")[2:]
        )
        with open(temporary_file, "r") as f:
            assert (
                f.read()
                == '''\
class TestFoo():
    """Docstring that should not have a pre-summary space."""
'''
            )

    @pytest.mark.system
    @pytest.mark.parametrize(
        "contents",
        [
            '''\
class TestFoo():
    """ Docstring that should not have a pre-summary space."""
'''
        ],
    )
    @pytest.mark.parametrize(
        "config",
        [
            """\
[docformatter]
in-place = true
check = true
diff = false
"""
        ],
    )
    @pytest.mark.parametrize(
        "arguments",
        [
            [
                "--config",
                "/tmp/setup.cfg",
            ]
        ],
    )
    def test_check_using_setup_cfg(
        self,
        run_docformatter,
        temporary_setup_cfg,
        temporary_file,
        arguments,
        contents,
        config,
    ):
        """Just check for changes if set in setup.cfg.

        See issue #122.
        """
        _results = run_docformatter.communicate()
        assert "" == "\n".join(
            _results[0].decode().replace("\r", "").split("\n")[2:]
        )
        assert temporary_file == _results[1].decode().rstrip("\n")

    @pytest.mark.system
    @pytest.mark.parametrize(
        "contents",
        [
            '''\
class TestFoo():
    """ Docstring that should not have a pre-summary space."""
'''
        ],
    )
    @pytest.mark.parametrize(
        "config",
        [
            """\
[docformatter]
check = true
diff = true
"""
        ],
    )
    @pytest.mark.parametrize(
        "arguments",
        [
            [
                "--config",
                "/tmp/setup.cfg",
            ]
        ],
    )
    def test_check_with_diff_using_setup_cfg(
        self,
        run_docformatter,
        temporary_setup_cfg,
        temporary_file,
        arguments,
        contents,
        config,
    ):
        """Check for changes and print diff if set in setup.cfg.

        See issue #122.
        """
        assert '''\
@@ -1,2 +1,2 @@
 class TestFoo():
-    """ Docstring that should not have a pre-summary space."""
+    """Docstring that should not have a pre-summary space."""
''' == "\n".join(
            run_docformatter.communicate()[0]
            .decode()
            .replace("\r", "")
            .split("\n")[2:]
        )
