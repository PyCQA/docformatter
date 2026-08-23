# pylint: skip-file
# type: ignore
#
#       tests.patterns.test_google_sections.py is part of the docformatter project
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
"""Unit tests for Google-style section parsing."""

# Third Party Imports
import pytest

# docformatter Package Imports
from docformatter.patterns.fields import (
    do_find_google_section_headers,
    do_parse_google_entries,
)


@pytest.mark.unit
def test_find_args_and_returns_headers():
    text = (
        "Connect to the database.\n"
        "\n"
        "    Args:\n"
        "        host: Hostname.\n"
        "\n"
        "    Returns:\n"
        "        A connection.\n"
    )
    headers = do_find_google_section_headers(text)
    names = [name for _, _, name in headers]
    assert names == ["Args", "Returns"]


@pytest.mark.unit
def test_parse_named_args_entries_joins_continuations():
    body = (
        "        host: Hostname used by the database.\n"
        "        configuration: Configuration containing authentication\n"
        "            information and connection parameters.\n"
    )
    entries = do_parse_google_entries(body)
    assert entries[0][0] == "host"
    assert entries[0][2] == "Hostname used by the database."
    assert entries[1][0] == "configuration"
    assert (
        entries[1][2]
        == "Configuration containing authentication information and connection "
        "parameters."
    )


@pytest.mark.unit
def test_parse_unnamed_returns_paragraph():
    body = (
        "        A database connection that has been initialized using the\n"
        "        requested configuration.\n"
    )
    entries = do_parse_google_entries(body)
    assert len(entries) == 1
    assert entries[0][0] is None
    assert (
        entries[0][2] == "A database connection that has been initialized using "
        "the requested configuration."
    )


@pytest.mark.unit
def test_parse_entry_with_type_hint():
    body = "        cfg (str): Path to the model configuration file.\n"
    entries = do_parse_google_entries(body)
    assert entries == [
        ("cfg", "str", "Path to the model configuration file."),
    ]
