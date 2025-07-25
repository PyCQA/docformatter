# pylint: skip-file
# type: ignore
#
#       tests.test.encoding_functions.py is part of the docformatter project
#
# Copyright (C) 2012-2023 Steven Myint
# Copyright (C) 2023-2025 Doyle "weibullguy" Rowland
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
"""Module for testing functions used to determine file encodings."""

# Standard Library Imports
import contextlib
import io
import sys

with contextlib.suppress(ImportError):
    if sys.version_info >= (3, 11):
        # Standard Library Imports
        import tomllib
    else:
        # Third Party Imports
        import tomli as tomllib

# Third Party Imports
import pytest

# docformatter Package Imports
from docformatter import Encoder

with open("tests/_data/string_files/encoding_functions.toml", "rb") as f:
    TEST_STRINGS = tomllib.load(f)


@pytest.mark.unit
@pytest.mark.parametrize(
    "test_key",
    [
        "find_newline_only_cr",
        "find_newline_only_lf",
        "find_newline_only_crlf",
        "find_newline_cr1_and_lf2",
        "find_newline_cr1_and_crlf2",
        "find_newline_should_default_to_lf_empty",
        "find_newline_should_default_to_lf_blank",
        "find_dominant_newline",
    ],
)
def test_do_find_newline(test_key):
    uut = Encoder()

    source = TEST_STRINGS[test_key]["instring"]
    expected = TEST_STRINGS[test_key]["expected"]

    result = uut.do_find_newline(source)
    assert result == expected, f"\nFailed {test_key}\nExpected {expected}\nGot {result}"


@pytest.mark.usefixtures("temporary_file")
class TestDoOpenWithEncoding:
    """Class for testing the do_open_with_encoding function."""

    @pytest.mark.unit
    @pytest.mark.parametrize("contents", ["# -*- coding: utf-8 -*-\n"])
    def test_do_open_with_utf_8_encoding(self, temporary_file, contents):
        """Return TextIOWrapper object when opening file with encoding."""
        uut = Encoder()

        assert isinstance(
            uut.do_open_with_encoding(temporary_file),
            io.TextIOWrapper,
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("contents", ["# -*- coding: utf-8 -*-\n"])
    def test_do_open_with_wrong_encoding(self, temporary_file, contents):
        """Raise LookupError when passed unknown encoding."""
        uut = Encoder()
        uut.encoding = "cr1252"

        with pytest.raises(LookupError):
            uut.do_open_with_encoding(temporary_file)


@pytest.mark.usefixtures("temporary_file")
class TestDoDetectEncoding:
    """Class for testing the detect_encoding() function."""

    @pytest.mark.integration
    @pytest.mark.parametrize("contents", ["# -*- coding: utf-8 -*-\n"])
    def test_do_detect_encoding_with_explicit_utf_8(self, temporary_file, contents):
        """Return utf-8 when explicitly set in the file."""
        uut = Encoder()
        uut.do_detect_encoding(temporary_file)

        assert "utf_8" == uut.encoding

    @pytest.mark.integration
    @pytest.mark.parametrize("contents", ["# Wow!  docformatter is super-cool.\n"])
    def test_do_detect_encoding_with_non_explicit_setting(
        self, temporary_file, contents
    ):
        """Return default system encoding when encoding not explicitly set."""
        uut = Encoder()
        uut.do_detect_encoding(temporary_file)

        assert "ascii" == uut.encoding

    @pytest.mark.integration
    @pytest.mark.parametrize("contents", ["# -*- coding: blah -*-"])
    def test_do_detect_encoding_with_bad_encoding(self, temporary_file, contents):
        """Default to latin-1 when unknown encoding detected."""
        uut = Encoder()
        uut.do_detect_encoding(temporary_file)

        assert "ascii" == uut.encoding

    @pytest.mark.integration
    @pytest.mark.parametrize("contents", [""])
    def test_do_detect_encoding_with_undetectable_encoding(self, temporary_file):
        """Default to latin-1 when encoding detection fails."""
        uut = Encoder()

        # Simulate a file with undetectable encoding
        with open(temporary_file, "wb") as file:
            # Binary content unlikely to have a detectable encoding
            file.write(b"\xff\xfe\xfd\xfc\x00\x00\x00\x00")

        uut.do_detect_encoding(temporary_file)

        assert uut.encoding == uut.DEFAULT_ENCODING
