# pylint: skip-file
# type: ignore
#
#       tests.test_utility_functions.py is part of the docformatter project
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
"""Module for testing utility functions used when processing docstrings.

This module contains tests for utility functions.  Utility functions are:

    - find_py_files()
    - has_correct_length()
    - is_in_range()
    - is_probably_beginning_of_sentence()
    - is_some_sort_of_list()
    - is_some_sort_of_code()
"""

# Third Party Imports
import pytest
from mock import patch

# docformatter Package Imports
import docformatter


class TestFindPyFiles:
    """Class for testing the find_py_files() Function."""

    @pytest.mark.unit
    def test_is_hidden(self):
        """Skip files that are .hidden."""

        assert docformatter.find_py_files("not_hidden", ".hidden_file.py")

    @pytest.mark.xfail(
        reason="function only checks for python files in recursive mode."
    )
    def test_non_recursive_ignore_non_py_files(self):
        """Only process python (*.py) files."""

        sources = ["one.py", "two.py", "three.toml"]

        test_only_py = list(docformatter.find_py_files(sources, False))
        assert test_only_py == ["one.py", "two.py"]

    @pytest.mark.unit
    def test_recursive_ignore_non_py_files(self):
        """Only process python (*.py) files when recursing directories."""

        sources = {"/root"}
        patch_data = [
            ("/root", [], ["one.py", "two.py", "three.toml"]),
        ]

        with patch("os.walk", return_value=patch_data), patch(
            "os.path.isdir", return_value=True
        ):
            test_only_py = list(docformatter.find_py_files(sources, True))
            assert test_only_py == ["/root/one.py", "/root/two.py"]

    @pytest.mark.unit
    def test_is_excluded(self):
        """Skip excluded *.py files."""

        sources = {"/root"}
        patch_data = [
            ("/root", ["folder_one", "folder_two"], []),
            ("/root/folder_one", ["folder_three"], ["one.py"]),
            ("/root/folder_one/folder_three", [], ["three.py"]),
            ("/root/folder_two", [], ["two.py"]),
        ]

        with patch("os.walk", return_value=patch_data), patch(
            "os.path.isdir", return_value=True
        ):
            test_exclude_one = list(
                docformatter.find_py_files(sources, True, ["folder_one"])
            )
            assert test_exclude_one == ["/root/folder_two/two.py"]
            test_exclude_two = list(
                docformatter.find_py_files(sources, True, ["folder_two"])
            )
            assert test_exclude_two == [
                "/root/folder_one/one.py",
                "/root/folder_one/folder_three/three.py",
            ]
            test_exclude_three = list(
                docformatter.find_py_files(sources, True, ["folder_three"])
            )
            assert test_exclude_three == [
                "/root/folder_one/one.py",
                "/root/folder_two/two.py",
            ]
            test_exclude_py = list(
                docformatter.find_py_files(sources, True, ".py")
            )
            assert not test_exclude_py
            test_exclude_two_and_three = list(
                docformatter.find_py_files(
                    sources, True, ["folder_two", "folder_three"]
                )
            )
            assert test_exclude_two_and_three == ["/root/folder_one/one.py"]
            test_exclude_files = list(
                docformatter.find_py_files(sources, True, ["one.py", "two.py"])
            )
            assert test_exclude_files == [
                "/root/folder_one/folder_three/three.py"
            ]

    @pytest.mark.unit
    def test_nothing_is_excluded(self):
        """Include all *.py files found."""
        sources = {"/root"}
        patch_data = [
            ("/root", ["folder_one", "folder_two"], []),
            ("/root/folder_one", ["folder_three"], ["one.py"]),
            ("/root/folder_one/folder_three", [], ["three.py"]),
            ("/root/folder_two", [], ["two.py"]),
        ]

        with patch("os.walk", return_value=patch_data), patch(
            "os.path.isdir", return_value=True
        ):
            test_exclude_nothing = list(
                docformatter.find_py_files(sources, True, [])
            )
            assert test_exclude_nothing == [
                "/root/folder_one/one.py",
                "/root/folder_one/folder_three/three.py",
                "/root/folder_two/two.py",
            ]
            test_exclude_nothing = list(
                docformatter.find_py_files(sources, True)
            )
            assert test_exclude_nothing == [
                "/root/folder_one/one.py",
                "/root/folder_one/folder_three/three.py",
                "/root/folder_two/two.py",
            ]


class TestHasCorrectLength:
    """Class for testing the has_correct_length() function."""

    @pytest.mark.unit
    def test_has_correct_length(self):
        """Return True when passed line_length=None."""
        assert docformatter.has_correct_length(None, 1, 9)

    @pytest.mark.unit
    def test_has_correct_length(self):
        """Return True if the line is within the line_length."""
        assert docformatter.has_correct_length([1, 3], 3, 5)
        assert docformatter.has_correct_length([1, 1], 1, 1)
        assert docformatter.has_correct_length([1, 10], 5, 10)

    @pytest.mark.unit
    def test_not_correct_length(self):
        """Return False if the line is outside the line_length."""
        assert not docformatter.has_correct_length([1, 1], 2, 9)
        assert not docformatter.has_correct_length([10, 20], 2, 9)


class TestIsInRange:
    """Class for testing the is_in_range() function."""

    @pytest.mark.unit
    def test_is_in_range_none(self):
        """Return True when passed line_range=None."""
        assert docformatter.is_in_range(None, 1, 9)

    @pytest.mark.unit
    def test_is_in_range(self):
        """Return True if the line is within the line_range."""
        assert docformatter.is_in_range([1, 4], 3, 5)
        assert docformatter.is_in_range([1, 4], 4, 10)
        assert docformatter.is_in_range([2, 10], 1, 2)

    @pytest.mark.unit
    def test_not_in_range(self):
        """Return False if the line outside the line_range."""
        assert not docformatter.is_in_range([1, 1], 2, 9)
        assert not docformatter.is_in_range([10, 20], 1, 9)


class TestIsProbablySentence:
    """Class for testing the is_probably_beginning_of_senstence() function."""

    @pytest.mark.unit
    def test_is_probably_beginning_of_sentence(self):
        """Ignore special characters as sentence starters."""
        assert docformatter.is_probably_beginning_of_sentence(
            "- This is part of a list."
        )

        assert not docformatter.is_probably_beginning_of_sentence(
            "(this just continues an existing sentence)."
        )

    @pytest.mark.unit
    def test_is_probably_beginning_of_sentence_pydoc_ref(self):
        """Ignore colon as sentence starter."""
        assert not docformatter.is_probably_beginning_of_sentence(
            ":see:MyClass This is not the start of a sentence."
        )


class TestIsSomeSortdOfList:
    """Class for testing the is_some_sort_of_list() function."""

    @pytest.mark.unit
    def test_is_some_sort_of_list(self):
        """Identify @ character as list item directive."""
        assert docformatter.is_some_sort_of_list(
            """\
        @param
        @param
        @param
    """
        )

    @pytest.mark.unit
    def test_is_some_sort_of_list_with_dashes(self):
        """Identify dash (-) as a list item directive."""
        assert docformatter.is_some_sort_of_list(
            """\
        Keyword arguments:
        real -- the real part (default 0.0)
        imag -- the imaginary part (default 0.0)
    """
        )

    @pytest.mark.unit
    def test_is_some_sort_of_list_without_special_symbol(self):
        """Identify indented items following color (:) as list."""
        assert docformatter.is_some_sort_of_list(
            """\
        Example:
          release-1.1/
          release-1.2/
          release-1.3/
          release-1.4/
          release-1.4.1/
          release-1.5/
    """
        )

    @pytest.mark.unit
    def test_is_some_sort_of_list_of_parameter_list_with_newline(self):
        """Identify Google syntax as start of list."""
        assert docformatter.is_some_sort_of_list(
            """\
    Args:
        stream (BinaryIO): Binary stream (usually a file object).
    """
        )


class TestIsSomeSortOfCode:
    """Class for testing the is_some_sort_of_code() function."""

    @pytest.mark.unit
    def test_is_some_sort_of_code(self):
        """Identify single word>50 as code."""
        assert docformatter.is_some_sort_of_code(
            """\
                __________=__________(__________,__________,__________,
                __________[
                          '___'],__________,__________,__________,
                          __________,______________=__________)
    """
        )
