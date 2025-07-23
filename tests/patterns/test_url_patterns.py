# pylint: skip-file
# type: ignore
#
#       tests.patterns.test_url_patterns.py is part of the docformatter project
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
"""Module for testing the URL pattern detection functions."""

# Standard Library Imports
import contextlib
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
from docformatter.patterns import do_find_links, do_skip_link

with open("tests/_data/string_files/url_patterns.toml", "rb") as f:
    TEST_STRINGS = tomllib.load(f)


@pytest.mark.unit
@pytest.mark.parametrize(
    "test_key",
    [
        "apple_filing_protocol",
        "network_filing_system",
        "samba_filing_system",
        "apt",
        "bitcoin",
        "chrome",
        "java_compressed_archive",
        "concurrent_version_system",
        "git",
        "subversion",
        "domain_name_system",
        "file_transfer_protocol",
        "secure_file_transfer_protocol",
        "ssh_file_transfer_protocol",
        "finger",
        "rsync",
        "telnet",
        "virtual_network_computing",
        "extensible_resource_identifier",
        "fish",
        "ssh",
        "webdav_transfer_protocol",
        "hypertext_transfer_protocol",
        "secure_hypertext_transfer_protocol",
        "obsolete_secure_hypertext_transfer_protocol",
        "imap",
        "smtp",
        "pop",
        "internet_printing_protocol",
        "secure_internet_printing_protocol",
        "internet_relay_chat",
        "internet_relay_chat_v6",
        "secure_internet_relay_chat",
        "short_message_service",
        "extensible_messaging_and_presence_protocol",
        "ldap",
        "secure_ldap",
        "amazon_s3",
        "usenet",
        "nntp",
        "session_initiation_protocol",
        "secure_session_initiation_protocol",
        "simple_network_management_protocol",
    ],
)
def test_do_find_links(test_key):
    source = TEST_STRINGS[test_key]["instring"]
    expected = TEST_STRINGS[test_key]["expected"]

    result = do_find_links(source)
    assert (
        result[0][0] == expected[0]
    ), f"\nFailed {test_key}\nExpected {expected[0]}\nGot {result[0][0]}"
    assert (
        result[0][1] == expected[1]
    ), f"\nFailed {test_key}\nExpected {expected[0]}\nGot {result[0][1]}"


@pytest.mark.unit
@pytest.mark.parametrize(
    "test_key, index",
    [
        ("only_link_patterns", (70, 76)),
        ("only_link_patterns", (137, 145)),
        ("already_wrapped_url", (70, 117)),
    ],
)
def test_do_skip_link(test_key, index):
    source = TEST_STRINGS[test_key]["instring"]
    expected = TEST_STRINGS[test_key]["expected"]

    result = do_skip_link(source, index)
    assert result == expected, f"\nFailed {test_key}\nExpected {expected}\nGot {result}"
