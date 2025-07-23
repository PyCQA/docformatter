# pylint: skip-file
# type: ignore
#
#       tests.test_configuration_functions.py is part of the docformatter project
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
"""Module for testing docformatter's Configurater class."""

# Third Party Imports
import pytest

# docformatter Package Imports
from docformatter.configuration import Configurater

WRAP_72 = 72
WRAP_80 = 80
WRAP_88 = 88


@pytest.mark.unit
def test_do_read_toml_configuration():
    uut = Configurater([""])
    uut.config_file = "./tests/_data/pyproject.toml"
    expected = {
        "wrap-summaries": "79",
        "wrap-descriptions": "72",
        "blank": "False",
    }

    uut._do_read_toml_configuration()
    assert uut.flargs == expected, (
        f"\nFailed _do_read_toml_configuration:\n"
        f"Expected {expected}\n"
        f"Got {uut.flargs}"
    )


@pytest.mark.unit
@pytest.mark.parametrize(
    "config_file",
    [
        "./tests/_data/setup.cfg",
        "./tests/_data/tox.ini",
    ],
)
def test_do_read_parser_configuration(config_file):
    uut = Configurater([""])
    uut.config_file = config_file
    expected = {
        "blank": "False",
        "wrap-summaries": "79",
        "wrap-descriptions": "72",
    }

    uut._do_read_parser_configuration()
    assert uut.flargs == expected, (
        f"\nFailed _do_read_parser_configuration:\n"
        f"Expected {expected}\n"
        f"Got {uut.flargs}"
    )


@pytest.mark.integration
@pytest.mark.order(1)
@pytest.mark.parametrize(
    "config_file",
    [
        "./tests/_data/pyproject.toml",
        "./tests/_data/setup.cfg",
        "./tests/_data/tox.ini",
    ],
)
def test_do_read_configuration_file(config_file):
    uut = Configurater([""])
    uut.config_file = config_file
    if config_file == "./tests/_data/pyproject.toml":
        expected = {
            "wrap-summaries": "79",
            "wrap-descriptions": "72",
            "blank": "false",
        }
    else:
        expected = {
            "blank": "False",
            "wrap-summaries": "79",
            "wrap-descriptions": "72",
        }

    uut._do_read_parser_configuration()
    assert uut.flargs == expected, (
        f"\nFailed _do_read_configuration_file:\n"
        f"Expected {expected}\n"
        f"Got {uut.flargs}"
    )


class TestConfigurater:
    """Class for testing configuration functions."""

    @pytest.mark.integration
    @pytest.mark.order(0)
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

    @pytest.mark.integration
    @pytest.mark.order(0)
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
        assert uut.flargs == {
            "wrap-summaries": "79",
            "wrap-descriptions": "72",
            "blank": "False",
        }

    @pytest.mark.integration
    @pytest.mark.order(0)
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
        assert uut.flargs == {
            "blank": "False",
            "wrap-summaries": "79",
            "wrap-descriptions": "72",
        }

    @pytest.mark.integration
    @pytest.mark.order(0)
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
        assert uut.flargs == {
            "blank": "False",
            "wrap-summaries": "79",
            "wrap-descriptions": "72",
        }

    @pytest.mark.integration
    @pytest.mark.order(0)
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
        assert uut.flargs == {}

    @pytest.mark.integration
    @pytest.mark.order(0)
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
        assert uut.flargs == {
            "blank": "False",
            "wrap-summaries": "79",
            "wrap-descriptions": "72",
        }
        assert not uut.args.in_place
        assert uut.args.check
        assert not uut.args.recursive
        assert uut.args.exclude is None
        assert uut.args.wrap_summaries == WRAP_88
        assert uut.args.wrap_descriptions == WRAP_72
        assert not uut.args.black
        assert uut.args.post_description_blank
        assert not uut.args.pre_summary_newline
        assert not uut.args.pre_summary_space
        assert uut.args.make_summary_multi_line
        assert not uut.args.force_wrap
        assert uut.args.line_range is None
        assert uut.args.length_range is None
        assert not uut.args.non_strict

    @pytest.mark.integration
    @pytest.mark.order(1)
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

    @pytest.mark.integration
    @pytest.mark.order(1)
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

    @pytest.mark.integration
    @pytest.mark.order(1)
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
            "First value of --range should be less than or equal to the second" in err
        )

    @pytest.mark.integration
    @pytest.mark.order(1)
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

    @pytest.mark.integration
    @pytest.mark.order(1)
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

    @pytest.mark.integration
    @pytest.mark.order(1)
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

    @pytest.mark.integration
    @pytest.mark.order(1)
    @pytest.mark.parametrize(
        "config",
        [
            """\
[tool.docformatter]
"""
        ],
    )
    def test_black_defaults(
        self,
        temporary_pyproject_toml,
        config,
    ):
        """Black line length defaults to 88 and pre-summary-space to True."""
        argb = [
            "/path/to/docformatter",
            "-c",
            "--black",
            "--config",
            "/tmp/pyproject.toml",
            "",
        ]
        uut = Configurater(argb)
        uut.do_parse_arguments()
        assert uut.args.black
        assert uut.args.pre_summary_space
        assert uut.args.wrap_summaries == WRAP_88
        assert uut.args.wrap_descriptions == WRAP_88

    @pytest.mark.integration
    @pytest.mark.order(2)
    @pytest.mark.parametrize(
        "config",
        [
            """\
[tool.docformatter]
black = true
wrap-summaries = 80
    """
        ],
    )
    def test_black_from_pyproject(
        self,
        temporary_pyproject_toml,
        config,
    ):
        """Test black setting via pyproject.toml."""
        argb = [
            "/path/to/docformatter",
            "-c",
            "--config",
            "/tmp/pyproject.toml",
            "",
        ]

        uut = Configurater(argb)
        uut.do_parse_arguments()

        assert uut.args.black
        assert uut.args.pre_summary_space
        assert uut.args.wrap_summaries == WRAP_80
        assert uut.args.wrap_descriptions == WRAP_88
        assert uut.flargs == {
            "black": "True",
            "wrap-summaries": "80",
        }

    @pytest.mark.integration
    @pytest.mark.order(2)
    @pytest.mark.parametrize(
        "config",
        [
            """\
[docformatter]
black = True
wrap-descriptions = 80
"""
        ],
    )
    def test_black_from_setup_cfg(
        self,
        temporary_setup_cfg,
        config,
    ):
        """Read black config from setup.cfg."""
        argb = [
            "/path/to/docformatter",
            "-c",
            "--config",
            "/tmp/setup.cfg",
            "",
        ]

        uut = Configurater(argb)
        uut.do_parse_arguments()

        assert uut.args.black
        assert uut.args.pre_summary_space
        assert uut.args.wrap_summaries == WRAP_88
        assert uut.args.wrap_descriptions == WRAP_80
        assert uut.flargs == {
            "black": "True",
            "wrap-descriptions": "80",
        }

    @pytest.mark.integration
    @pytest.mark.order(2)
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
    def test_exclude_from_pyproject_toml(
        self,
        temporary_pyproject_toml,
        config,
    ):
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
        assert uut.flargs == {
            "recursive": "True",
            "check": "True",
            "diff": "True",
            "exclude": ["src/", "tests/"],
        }

    @pytest.mark.integration
    @pytest.mark.order(2)
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
    def test_exclude_from_setup_cfg(
        self,
        temporary_setup_cfg,
        config,
    ):
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
        assert uut.flargs == {
            "recursive": "true",
            "check": "true",
            "diff": "true",
            "exclude": '["src/", "tests/"]',
        }

    @pytest.mark.integration
    @pytest.mark.order(0)
    def test_non_capitalize_words(self, capsys):
        """Read list of words not to capitalize.

        See issue #193.
        """
        argb = [
            "/path/to/docformatter",
            "-n",
            "qBittorrent",
            "eBay",
            "iPad",
            "-c",
            "",
        ]

        uut = Configurater(argb)
        uut.do_parse_arguments()

        assert uut.args.non_cap == ["qBittorrent", "eBay", "iPad"]

    @pytest.mark.integration
    @pytest.mark.order(0)
    @pytest.mark.parametrize(
        "config",
        [
            """\
[tool.docformatter]
check = true
diff = true
recursive = true
non-cap = ["qBittorrent", "iPad", "iOS", "eBay"]
"""
        ],
    )
    def test_non_cap_from_pyproject_toml(
        self,
        temporary_pyproject_toml,
        config,
    ):
        """Read list of words not to capitalize from pyproject.toml.

        See issue #193.
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
        assert uut.flargs == {
            "recursive": "True",
            "check": "True",
            "diff": "True",
            "non-cap": ["qBittorrent", "iPad", "iOS", "eBay"],
        }

    @pytest.mark.integration
    @pytest.mark.order(0)
    @pytest.mark.parametrize(
        "config",
        [
            """\
[docformatter]
check = true
diff = true
recursive = true
non-cap = ["qBittorrent", "iPad", "iOS", "eBay"]
"""
        ],
    )
    def test_non_cap_from_setup_cfg(
        self,
        temporary_setup_cfg,
        config,
    ):
        """Read list of words not to capitalize from setup.cfg.

        See issue #193.
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
        assert uut.flargs == {
            "recursive": "true",
            "check": "true",
            "diff": "true",
            "non-cap": '["qBittorrent", "iPad", "iOS", "eBay"]',
        }
