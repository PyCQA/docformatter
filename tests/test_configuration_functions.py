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
from docformatter import Configurator


class TestConfigurator:
    """Class for testing configuration functions."""

    @pytest.mark.unit
    def test_initialize_configurator_with_default(self):
        """Return a Configurator() instance using default pyproject.toml."""
        unit_under_test = Configurator([])

        assert unit_under_test.config_file == "./pyproject.toml"

    @pytest.mark.unit
    def test_initialize_configurator_with_pyproject_toml(self):
        """Return a Configurator() instance loaded from a pyproject.toml."""
        argb = [
            "--config",
            "./tests/_data/pyproject.toml",
        ]

        unit_under_test = Configurator(argb)

        assert unit_under_test.args is None
        assert unit_under_test.flargs_dct == {
            "recursive": "True",
            "wrap-summaries": "82",
        }
        assert unit_under_test.configuration_file_lst == [
            "pyproject.toml",
            "setup.cfg",
            "tox.ini",
        ]
        assert unit_under_test.args_lst == argb
        assert unit_under_test.config_file == "./tests/_data/pyproject.toml"

    @pytest.mark.unit
    def test_initialize_configurator_with_setup_cfg(self):
        """Return docformatter configuration loaded from a setup.cfg file."""
        argb = [
            "--config",
            "./tests/_data/setup.cfg",
        ]

        unit_under_test = Configurator(argb)
        unit_under_test.do_parse_arguments()

        assert unit_under_test.flargs_dct == {
            "blank": "False",
            "wrap-summaries": "79",
            "wrap-descriptions": "72",
        }

    @pytest.mark.unit
    def test_initialize_configurator_with_tox_ini(self):
        """Return docformatter configuration loaded from a tox.ini file."""
        argb = [
            "--config",
            "./tests/_data/tox.ini",
        ]

        unit_under_test = Configurator(argb)
        unit_under_test.do_parse_arguments()

        assert unit_under_test.flargs_dct == {
            "blank": "False",
            "wrap-summaries": "79",
            "wrap-descriptions": "72",
        }

    @pytest.mark.unit
    def test_unsupported_config_file(self):
        """Return empty configuration dict when file is unsupported."""
        argb = [
            "--config",
            "./tests/conf.py",
        ]

        unit_under_test = Configurator(argb)
        unit_under_test.do_parse_arguments()

        assert unit_under_test.flargs_dct == {}

    @pytest.mark.unit
    def test_cli_override_config_file(self):
        """Command line arguments override configuration file options."""
        argb = [
            "--config",
            "./tests/_data/tox.ini",
            "--make-summary-multi-line",
            "--blank",
            "--wrap-summaries",
            "88",
        ]

        unit_under_test = Configurator(argb)
        unit_under_test.do_parse_arguments()

        assert unit_under_test.flargs_dct == {
            "blank": "False",
            "wrap-descriptions": "72",
            "wrap-summaries": "79",
        }
        assert not unit_under_test.args.in_place
        assert not unit_under_test.args.check
        assert not unit_under_test.args.recursive
        assert unit_under_test.args.exclude is None
        assert unit_under_test.args.wrap_summaries == 88
        assert unit_under_test.args.wrap_descriptions == 72
        assert unit_under_test.args.post_description_blank
        assert not unit_under_test.args.pre_summary_newline
        assert not unit_under_test.args.pre_summary_space
        assert unit_under_test.args.make_summary_multi_line
        assert not unit_under_test.args.force_wrap
        assert unit_under_test.args.line_range is None
        assert unit_under_test.args.length_range is None
        assert not unit_under_test.args.non_strict
