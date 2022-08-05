# pylint: skip-file
# type: ignore
#
#       tests.test_configuration_functions.py is part of the docformatter
#       project
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
"""Module for testing functions used to control docformatter configuration.

Configuration functions are:

    - find_config_file()
    - read_configuration_file()
"""

# Standard Library Imports
import io
import sys

# Third Party Imports
import pytest

# docformatter Package Imports
import docformatter


class TestConfigurater:
    """Class for testing configuration functions."""

    @pytest.mark.unit
    def test_read_config_file(self):
        """Return docformatter configuration from pyproject.toml file."""
        assert docformatter.find_config_file(
            [
                "--config",
                "./tests/_data/pyproject.toml",
            ]
        ) == {
            "recursive": "True",
            "wrap-summaries": "82",
        }

    @pytest.mark.unit
    def test_missing_config_file(self):
        """Return empty configuration when file is missing."""
        assert (
            docformatter.find_config_file(
                [
                    "--config",
                    "../../pyproject.toml",
                ]
            )
            == {}
        )

    @pytest.mark.unit
    def test_unsupported_config_file(self):
        """Return empty configuration dict when file is unsupported."""
        assert docformatter.find_config_file(["--config", "tox.ini"]) == {}

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
        "arguments",
        [
            [
                "--wrap-summaries=79",
                "--config ./tests/_data/pyproject.toml",
            ]
        ],
    )
    def test_cli_override_config_file(
        self, temporary_file, contents, run_docformatter, arguments
    ):
        """Command line arguments override configuration file options."""
        process = run_docformatter
        assert '''\
@@ -1,4 +1,2 @@
 def foo():
-    """
-    Hello world
-    """
+    """Hello world."""
''' == "\n".join(
            process.communicate()[0].decode().split("\n")[2:]
        )
