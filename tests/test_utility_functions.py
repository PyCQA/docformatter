# pylint: skip-file
# type: ignore
#
#       tests.test_utility_functions.py is part of the docformatter project
#
# Copyright (C) 2012-2023 Steven Myint
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
    """Class for testing the find_py_files() function."""

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


class TestDoFindLinks:
    """Class for testing the do_find_links() function."""

    @pytest.mark.unit
    def test_do_find_file_system_link(self):
        """Identify afp://, nfs://, smb:// as a link."""
        text = "This is an Apple Filing Protocol URL pattern: afp://[<user@]<host>[:<port>][/[<path>]]"
        assert docformatter.do_find_links(text) == [(46, 86)]
        text = "This is an Network File System URL pattern: nfs://server<:port>/<path>"
        assert docformatter.do_find_links(text) == [(44, 70)]
        text = "This is an Samba URL pattern: smb://[<user>@]<host>[:<port>][/[<path>]][?<param1>=<value1>[;<param2>=<value2>]]"
        assert docformatter.do_find_links(text) == [(30, 111)]

    @pytest.mark.unit
    def test_do_find_miscellaneous_link(self):
        """Identify apt:, bitcoin:, chrome://, and jar: as a link."""
        text = "This is an apt URL pattern: apt:docformatter"
        assert docformatter.do_find_links(text) == [(28, 44)]
        text = "This is a bitcoin URL pattern: bitcoin:<address>[?[amount=<size>][&][label=<label>][&][message=<message>]]"
        assert docformatter.do_find_links(text) == [(31, 106)]
        text = (
            "This is a chrome URL pattern: chrome://<package>/<section>/<path>"
        )
        assert docformatter.do_find_links(text) == [(30, 65)]
        text = "This is a Java compressed archive URL pattern: jar:<url>!/[<entry>]"
        assert docformatter.do_find_links(text) == [(47, 67)]

    @pytest.mark.unit
    def test_do_find_version_control_link(self):
        """Identify cvs://, git://, or svn:// as a link."""
        text = "This is a Concurrent Versions System URL pattern: cvs://<method:logindetails>@<repository>/<modulepath>;[date=date to retrieve | tag=tag to retrieve]"
        assert docformatter.do_find_links(text) == [(50, 114)]
        text = "This is a Git URL pattern: git://github.com/PyCQA/docformatter.git"
        assert docformatter.do_find_links(text) == [(27, 66)]
        text = "This is a Subversion URL pattern: svn://<logindetails>@<repository><:port>/<modulepath>"
        assert docformatter.do_find_links(text) == [(34, 87)]

    @pytest.mark.unit
    def test_do_find_domain_name_system_link(self):
        """Identify dns: as a link."""
        text = "This is a Domain Name System URL pattern: dns:example?TYPE=A;CLASS=IN"
        assert docformatter.do_find_links(text) == [(42, 69)]

    @pytest.mark.unit
    def test_do_find_file_transfer_protocol_link(self):
        """Identify file://, ftp://, ftps://, and sftp:// as a link."""
        text = (
            "This is a URL pattern for addressing a file: file://[host]/path"
        )
        assert docformatter.do_find_links(text) == [(39, 44), (45, 63)]
        text = "This is a File Transfer Protocol URL pattern: ftp://[user[:password]@]host[:port]/url-path"
        assert docformatter.do_find_links(text) == [(46, 90)]
        text = "This is a Secure File Transfer Protocol URL pattern: ftps://[user[:password]@]host[:port]/url-path"
        assert docformatter.do_find_links(text) == [(53, 98)]
        text = "This is a SSH File Transfer Protocol URL pattern: sftp://[<user>[;fingerprint=<host-key fingerprint>]@]<host>[:<port>]/<path>/<file>"
        assert docformatter.do_find_links(text) == [(50, 87)]

    @pytest.mark.unit
    def test_do_find_network_command_link(self):
        """Identify finger://, rsync://, telnet://, and vnc:// as a link."""
        text = "This is a finger protocol URL pattern: finger://host[:port][/<request>]"
        assert docformatter.do_find_links(text) == [(39, 71)]
        text = "This is a remote synchronization URL pattern: rsync://<host>[:<port>]/<path>"
        assert docformatter.do_find_links(text) == [(46, 76)]
        text = "This is a telnet URL pattern: telnet://<user>:<password>@<host>[:<port>/]"
        assert docformatter.do_find_links(text) == [(30, 73)]
        text = "This is a Virtual Network Computing URL pattern: vnc://[<host>[:<port>]][?<params>]"
        assert docformatter.do_find_links(text) == [(49, 83)]
        text = "This is an eXtensible Resource Identifier URL pattern: xri://<authority>[/[<path>]][?<query>][#fragment]"
        assert docformatter.do_find_links(text) == [(55, 104)]

    @pytest.mark.unit
    def test_do_find_remote_shell_link(self):
        """Identify fish:// and ssh:// as a link."""
        text = "This is a fish URL pattern: fish://[<username>[:<password>]@]<hostname>[:<port>]"
        assert docformatter.do_find_links(text) == [(28, 80)]
        text = "This is a Secure Shell URL pattern: ssh://[<user>[;fingerprint=<host-key fingerprint>]@]<host>[:<port>]"
        assert docformatter.do_find_links(text) == [(36, 72)]

    @pytest.mark.unit
    def test_do_find_internet_transfer_protocol_link(self):
        """Identify dav:, http://, https://, and shttp:// as a link."""
        text = "This is a WebDAV Transfer Protocol URL pattern: dav://example.com/directory/subdirectory"
        assert docformatter.do_find_links(text) == [(48, 88)]
        text = "This is a Hypertext Transfer Protocol URL pattern: http://github.com/PyCQA/docformatter"
        assert docformatter.do_find_links(text) == [(51, 87)]
        text = "This is a Secure Hypertext Transfer Protocol URL pattern: https://github.com/PyCQA/docformatter"
        assert docformatter.do_find_links(text) == [(58, 95)]
        text = "This is an obsolete Secure Hypertext Transfer Protocol URL pattern: shttp://github.com/PyCQA/docformatter"
        assert docformatter.do_find_links(text) == [(68, 105)]

    @pytest.mark.unit
    def test_do_find_mail_link(self):
        """Identify imap://, mailto:, and pop:// as a link."""
        text = "This is a Internet Message Access Protocol URL pattern: imap://[<user>[;AUTH=<type>]@]<host>[:<port>]/<command>"
        assert docformatter.do_find_links(text) == [(56, 111)]
        text = "This is a Simple Mail Transfer Protocol URL pattern: mailto:<address>[?<header1>=<value1>[&<header2>=<value2>]]"
        assert docformatter.do_find_links(text) == [(53, 111)]
        text = "This is a Post Office Protocol URL pattern: pop://[<user>[;AUTH=<auth>]@]<host>[:<port>]"
        assert docformatter.do_find_links(text) == [(44, 88)]

    @pytest.mark.unit
    def test_do_find_printer_link(self):
        """Identify ipp:// and ipps:// as a link."""
        text = "This is a Internet Printing Protocol URL pattern: ipp://printer.example.com/ipp/print"
        assert docformatter.do_find_links(text) == [(50, 85)]
        text = "This is a Secure Internet Printing Protocol URL pattern: ipps://printer2.example.com:443/ipp/print"
        assert docformatter.do_find_links(text) == [(57, 98)]

    @pytest.mark.unit
    def test_do_find_messaging_link(self):
        """Identify irc://, irc6://, ircs://, sms://, and xmpp:// as a link."""
        text = "This is a Internet Relay Chat URL pattern: irc://<host>[:<port>]/[<channel>[?<password>]]"
        assert docformatter.do_find_links(text) == [(43, 89)]
        text = "This is a Internet Relay Chat v6 URL pattern: irc6://<host>[:<port>]/[<channel>[?<password>]]"
        assert docformatter.do_find_links(text) == [(46, 93)]
        text = "This is a Secure Internet Relay Chat URL pattern: ircs://<host>[:<port>]/[<channel>[?<password>]]"
        assert docformatter.do_find_links(text) == [(50, 97)]
        text = "This is a Short Message Service URL pattern: sms:+15558675309?body=hello%20there"
        assert docformatter.do_find_links(text) == [(45, 80)]
        text = "This is a Extensible Messaging and Presence Protocol URL pattern: xmpp:[<user>]@<host>[:<port>]/[<resource>][?<query>]"
        assert docformatter.do_find_links(text) == [(66, 118)]

    @pytest.mark.unit
    def test_do_find_directory_access_link(self):
        """Identify ldap://, ldaps://, and s3:// as a link."""
        text = "This is a Lightweight Directory Access Protocol URL pattern: ldap://[<host>[:<port>]][/<dn> [?[<attributes>][?[<scope>][?[<filter>][?<extensions>]]]]]"
        assert docformatter.do_find_links(text) == [(61, 91)]
        text = "This is a Secure Lightweight Directory Access Protocol URL pattern: ldaps://[<host>[:<port>]][/<dn> [?[<attributes>][?[<scope>][?[<filter>][?<extensions>]]]]]"
        assert docformatter.do_find_links(text) == [(68, 99)]
        text = (
            "This is an Amazon S3 bucket URL pattern: s3://mybucket/puppy.jpg"
        )
        assert docformatter.do_find_links(text) == [(41, 64)]

    @pytest.mark.unit
    def test_do_find_news_link(self):
        """Identify news: and nntp:// as a link."""
        text = "This is a Usenet newsgroup URL pattern: news:<newsgroupname>"
        assert docformatter.do_find_links(text) == [(40, 60)]
        text = "This is a Network News Transfer Protocol URL pattern: nntp://<host>:<port>/<newsgroup-name>/<article-number>"
        assert docformatter.do_find_links(text) == [(54, 108)]

    @pytest.mark.unit
    def test_do_find_initiation_link(self):
        """Identify sip:, sips:, and snmp:// as a link."""
        text = "This is a Session Initiation Protocol URL pattern: sip:<user>[:<password>]@<host>[:<port>][;<uri-parameters>][?<headers>]"
        assert docformatter.do_find_links(text) == [(51, 121)]
        text = "This is a Secure Session Initiation Protocol URL pattern: sips:<user>[:<password>]@<host>[:<port>][;<uri-parameters>][?<headers>]"
        assert docformatter.do_find_links(text) == [(58, 129)]
        text = "This is a Simple Network Management Protocol URL pattern: snmp://[user@]host[:port][/[<context>[;<contextEngineID>]][/<oid>]]"
        assert docformatter.do_find_links(text) == [(58, 125)]


class TestDoSkipLink:
    """Class for testing the do_skip_links() function."""

    @pytest.mark.unit
    def test_do_skip_only_link_pattern(self):
        """Don't treat things like 's3://' or 'file://' as links.

        See issue #150.
        """
        text = (
            "Directories are implicitly created.  The accepted URL can start "
            "with 's3://' to refer to files on s3.  Local files can be "
            "prefixed with 'file://' (but it is not needed!)"
        )
        assert docformatter.do_skip_link(text, (70, 76))
        assert docformatter.do_skip_link(text, (137, 145))

    @pytest.mark.unit
    def test_do_skip_already_wrapped_link(self):
        """Skip links that were already wrapped by the user.

        See issue #150.
        """
        text = (
            "The text file can be retrieved via the Chrome plugin `Get "
            "Cookies.txt <https://chrome.google.com/webstore/detail/get-"
            "cookiestxt/bgaddhkoddajcdgocldbbfleckgcbcid>` while browsing."
        )
        assert docformatter.do_skip_link(text, (70, 117))


class TestIsSomeSortOfList:
    """Class for testing the is_some_sort_of_list() function."""

    @pytest.mark.unit
    def test_is_some_sort_of_list(self):
        """Identify @ character as list item directive."""
        assert docformatter.is_some_sort_of_list(
            """\
        @param
        @param
        @param
    """,
            True,
        )

    @pytest.mark.unit
    def test_is_some_sort_of_list_with_dashes(self):
        """Identify dash (-) as a list item directive."""
        assert docformatter.is_some_sort_of_list(
            """\
        Keyword arguments:
        real -- the real part (default 0.0)
        imag -- the imaginary part (default 0.0)
    """,
            True,
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
    """,
            True,
        )

    @pytest.mark.unit
    def test_is_some_sort_of_list_of_parameter_list_with_newline(self):
        """Identify Google syntax as start of list."""
        assert docformatter.is_some_sort_of_list(
            """\
    Args:
        stream (BinaryIO): Binary stream (usually a file object).
    """,
            True,
        )

    @pytest.mark.unit
    def test_is_some_sort_of_list_strict_wrap(self):
        """Ignore many lines of short words as a list with strict set True.

        See issue #67.
        """
        assert not docformatter.is_some_sort_of_list(
            """\
        Launch
the
rocket.
    """,
            True,
        )

    @pytest.mark.unit
    def test_is_some_sort_of_list_non_strict_wrap(self):
        """Identify many lines of short words as a list with strict False.

        See issue #67.
        """
        assert docformatter.is_some_sort_of_list(
            """\
        Launch
the
rocket.
    """,
            False,
        )

    @pytest.mark.unit
    def test_is_some_sort_of_list_literal_block(self):
        """Identify literal blocks.

        See issue #199 and requirement docformatter_10.1.1.1.
        """
        assert docformatter.is_some_sort_of_list(
"""\
This is a description.

Example code::

    config(par=value)

Example code2::

    with config(par=value) as f:
        pass
""",
            False,
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
