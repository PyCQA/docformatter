# pylint: skip-file
# type: ignore
#
#       tests.test_configuration_functions.py is part of the docformatter
#       project
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
"""Module for testing docformatter's Configurater class."""

# Standard Library Imports
import io
import sys

# Third Party Imports
import pytest

# docformatter Package Imports
from docformatter import Configurater


class TestConfigurater:
    """Class for testing configuration functions."""

    @pytest.mark.unit
    def test_initialize_configurator_with_default(self):
        """Return a Configurater() instance using default pyproject.toml."""
        argb = [
            "/path/to/docformatter",
            "",
        ]

        uut = Configurater(argb)
        uut.do_parse_arguments()

        assert uut.args_lst == argb
        assert uut.config_file == "./pyproject.toml"

    @pytest.mark.unit
    def test_initialize_configurator_with_pyproject_toml(self):
        """Return a Configurater() instance loaded from a pyproject.toml."""
        argb = [
            "/path/to/docformatter",
            "-c",
            "--config",
            "./tests/_data/pyproject.toml",
            "",
        ]

        uut = Configurater(argb)
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

        uut = Configurater(argb)
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

        uut = Configurater(argb)
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

        uut = Configurater(argb)
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

        uut = Configurater(argb)
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
        assert not uut.args.black
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

        uut = Configurater(argb)
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

        uut = Configurater(argb)
        with pytest.raises(SystemExit):
            uut.do_parse_arguments()

        out, err = capsys.readouterr()
        assert out == ""
        assert "--range must be positive numbers" in err

    @pytest.mark.unit
    def test_low_line_range_greater_than_high_line_range(self, capsys):
        """Raise parser error if first value for range > than second."""
        argb = [
            "/path/to/docformatter",
            "-c",
            "--range",
            "10",
            "1",
            "",
        ]

        uut = Configurater(argb)
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

        uut = Configurater(argb)
        uut.do_parse_arguments()

        assert uut.args.length_range == [25, 55]

    @pytest.mark.unit
    def test_low_length_range_is_zero(self, capsys):
        """Raise parser error if the first value for the length range = 0."""
        argb = [
            "/path/to/docformatter",
            "-c",
            "--docstring-length",
            "0",
            "10",
            "",
        ]

        uut = Configurater(argb)
        with pytest.raises(SystemExit):
            uut.do_parse_arguments()

        out, err = capsys.readouterr()
        assert out == ""
        assert "--docstring-length must be positive numbers" in err

    @pytest.mark.unit
    def test_low_length_range_greater_than_high_length_range(self, capsys):
        """Raise parser error if first value for range > second value."""
        argb = [
            "/path/to/docformatter",
            "-c",
            "--docstring-length",
            "55",
            "25",
            "",
        ]

        uut = Configurater(argb)
        with pytest.raises(SystemExit):
            uut.do_parse_arguments()

        out, err = capsys.readouterr()
        assert out == ""
        assert (
            "First value of --docstring-length should be less than or equal "
            "to the second" in err
        )

    @pytest.mark.unit
    def test_black_line_length_defaults(self, capsys):
        argb = [
            "/path/to/docformatter",
            "-c",
            "--black",
            "",
        ]
        uut = Configurater(argb)
        uut.do_parse_arguments()
        assert uut.args.black
        assert not uut.args.pre_summary_space
        assert uut.args.wrap_summaries == 88
        assert uut.args.wrap_descriptions == 88

    @pytest.mark.unit
    @pytest.mark.parametrize(
        "config",
        [
            """\
[tool.docformatter]
check = true
diff = true
recursive = true
exclude = ["src/", "tests/"]
"""
        ],
    )
    def test_exclude_from_pyproject_toml(self,temporary_pyproject_toml,config,):
        """Read exclude list from pyproject.toml.

        See issue #120.
        """
        argb = [
            "/path/to/docformatter",
            "-c",
            "--config",
            "/tmp/pyproject.toml",
            "",
        ]

        uut = Configurater(argb)
        uut.do_parse_arguments()

        assert uut.args.check
        assert not uut.args.in_place
        assert uut.args_lst == argb
        assert uut.config_file == "/tmp/pyproject.toml"
        assert uut.flargs_dct == {
            "recursive": "True",
            "check": "True",
            "diff": "True",
            "exclude": ["src/", "tests/"]
        }

    @pytest.mark.unit
    @pytest.mark.parametrize(
        "config",
        [
            """\
[docformatter]
check = true
diff = true
recursive = true
exclude = ["src/", "tests/"]
"""
        ],
    )
    def test_exclude_from_setup_cfg(self,temporary_setup_cfg,config,):
        """Read exclude list from setup.cfg.

        See issue #120.
        """
        argb = [
            "/path/to/docformatter",
            "-c",
            "--config",
            "/tmp/setup.cfg",
            "",
        ]

        uut = Configurater(argb)
        uut.do_parse_arguments()

        assert uut.args.check
        assert not uut.args.in_place
        assert uut.args_lst == argb
        assert uut.config_file == "/tmp/setup.cfg"
        assert uut.flargs_dct == {
            "recursive": "true",
            "check": "true",
            "diff": "true",
            "exclude": '["src/", "tests/"]'
        }