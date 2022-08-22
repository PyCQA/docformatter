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
        argb = [
            "/path/to/docformatter",
            "",
        ]

        uut = Configurator(argb)
        uut.do_parse_arguments()

        assert uut.args_lst == argb
        assert uut.config_file == "./pyproject.toml"

    @pytest.mark.unit
    def test_initialize_configurator_with_pyproject_toml(self):
        """Return a Configurator() instance loaded from a pyproject.toml."""
        argb = [
            "/path/to/docformatter",
            "-c",
            "--config",
            "./tests/_data/pyproject.toml",
            "",
        ]

        uut = Configurator(argb)
        uut.do_parse_arguments()

        assert uut.args.check
        assert not uut.args.in_place
        assert uut.args_lst == argb
        assert uut.config_file == "./tests/_data/pyproject.toml"
        assert uut.configuration_file_lst == [
            "pyproject.toml",
            "setup.cfg",
            "tox.ini",
        ]
        assert uut.flargs_dct == {
            "recursive": "True",
            "wrap-summaries": "82",
        }

    @pytest.mark.unit
    def test_initialize_configurator_with_setup_cfg(self):
        """Return docformatter configuration loaded from a setup.cfg file."""
        argb = [
            "/path/to/docformatter",
            "-c",
            "--config",
            "./tests/_data/setup.cfg",
            "",
        ]

        uut = Configurator(argb)
        uut.do_parse_arguments()

        assert uut.config_file == "./tests/_data/setup.cfg"
        assert uut.flargs_dct == {
            "blank": "False",
            "wrap-summaries": "79",
            "wrap-descriptions": "72",
        }

    @pytest.mark.unit
    def test_initialize_configurator_with_tox_ini(self):
        """Return docformatter configuration loaded from a tox.ini file."""
        argb = [
            "/path/to/docformatter",
            "-c",
            "--config",
            "./tests/_data/tox.ini",
            "",
        ]

        uut = Configurator(argb)
        uut.do_parse_arguments()

        assert uut.config_file == "./tests/_data/tox.ini"
        assert uut.flargs_dct == {
            "blank": "False",
            "wrap-summaries": "79",
            "wrap-descriptions": "72",
        }

    @pytest.mark.unit
    def test_unsupported_config_file(self):
        """Return empty configuration dict when file is unsupported."""
        argb = [
            "/path/to/docformatter",
            "-c",
            "--config",
            "./tests/conf.py",
            "",
        ]

        uut = Configurator(argb)
        uut.do_parse_arguments()

        assert uut.config_file == "./tests/conf.py"
        assert uut.flargs_dct == {}

    @pytest.mark.unit
    def test_cli_override_config_file(self):
        """Command line arguments override configuration file options."""
        argb = [
            "/path/to/docformatter",
            "-c",
            "--config",
            "./tests/_data/tox.ini",
            "--make-summary-multi-line",
            "--blank",
            "--wrap-summaries",
            "88",
            "",
        ]

        uut = Configurator(argb)
        uut.do_parse_arguments()

        assert uut.config_file == "./tests/_data/tox.ini"
        assert uut.flargs_dct == {
            "blank": "False",
            "wrap-descriptions": "72",
            "wrap-summaries": "79",
        }
        assert not uut.args.in_place
        assert uut.args.check
        assert not uut.args.recursive
        assert uut.args.exclude is None
        assert uut.args.wrap_summaries == 88
        assert uut.args.wrap_descriptions == 72
        assert uut.args.post_description_blank
        assert not uut.args.pre_summary_newline
        assert not uut.args.pre_summary_space
        assert uut.args.make_summary_multi_line
        assert not uut.args.force_wrap
        assert uut.args.line_range is None
        assert uut.args.length_range is None
        assert not uut.args.non_strict

    @pytest.mark.unit
    def test_only_format_in_line_range(self, capsys):
        """Only format docstrings in line range."""
        argb = [
            "/path/to/docformatter",
            "-c",
            "--range",
            "1",
            "3",
            "",
        ]

        uut = Configurator(argb)
        uut.do_parse_arguments()

        assert uut.args.line_range == [1, 3]

    @pytest.mark.unit
    def test_low_line_range_is_zero(self, capsys):
        """Raise parser error if the first value for the range is zero."""
        argb = [
            "/path/to/docformatter",
            "-c",
            "--range",
            "0",
            "10",
            "",
        ]

        uut = Configurator(argb)
        with pytest.raises(SystemExit):
            uut.do_parse_arguments()

        out, err = capsys.readouterr()
        assert out == ""
        assert "--range must be positive numbers" in err

    @pytest.mark.unit
    def test_low_line_range_greater_than_high_line_range(self, capsys):
        """Raise parser error if the first value for the range is greater than
        the second."""
        argb = [
            "/path/to/docformatter",
            "-c",
            "--range",
            "10",
            "1",
            "",
        ]

        uut = Configurator(argb)
        with pytest.raises(SystemExit):
            uut.do_parse_arguments()

        out, err = capsys.readouterr()
        assert out == ""
        assert (
            "First value of --range should be less than or equal to the second"
            in err
        )

    @pytest.mark.unit
    def test_only_format_in_length_range(self, capsys):
        """Only format docstrings in length range."""
        argb = [
            "/path/to/docformatter",
            "-c",
            "--docstring-length",
            "25",
            "55",
            "",
        ]

        uut = Configurator(argb)
        uut.do_parse_arguments()

        assert uut.args.length_range == [25, 55]

    @pytest.mark.unit
    def test_low_length_range_is_zero(self, capsys):
        """Raise parser error if the first value for the length range is
        zero."""
        argb = [
            "/path/to/docformatter",
            "-c",
            "--docstring-length",
            "0",
            "10",
            "",
        ]

        uut = Configurator(argb)
        with pytest.raises(SystemExit):
            uut.do_parse_arguments()

        out, err = capsys.readouterr()
        assert out == ""
        assert "--docstring-length must be positive numbers" in err

    @pytest.mark.unit
    def test_low_length_range_greater_than_high_length_range(self, capsys):
        """Raise parser error if the first value for the range is greater than
        the second."""
        argb = [
            "/path/to/docformatter",
            "-c",
            "--docstring-length",
            "55",
            "25",
            "",
        ]

        uut = Configurator(argb)
        with pytest.raises(SystemExit):
            uut.do_parse_arguments()

        out, err = capsys.readouterr()
        assert out == ""
        assert (
            "First value of --docstring-length should be less than or equal "
            "to the second" in err
        )
