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

# Standard Library Imports
import subprocess
import sys

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
class TestMissingTomlSupport:
    """Class for testing behaviour when no TOML parser is installed.

    On Python < 3.11 the tomli backport is an optional extra, so a plain
    ``pip install docformatter`` leaves docformatter unable to read
    pyproject.toml.  Issue #268 is that this happens without a word.
    """

    @pytest.mark.unit
    def test_says_so_when_toml_support_is_missing(self, tmp_path, capsys):
        """Warn on stderr instead of silently dropping the settings."""
        # Third Party Imports
        import docformatter.configuration as configuration

        config_file = tmp_path / "pyproject.toml"
        config_file.write_text(
            '[tool.docformatter]\nwrap-summaries = "120"\n', encoding="utf-8"
        )

        saved = configuration.tomllib
        configuration.tomllib = None
        try:
            uut = Configurater(
                ["/path/to/docformatter", "--config", str(config_file), ""]
            )
            uut.do_parse_arguments()
        finally:
            configuration.tomllib = saved

        stderr = capsys.readouterr().err
        assert str(config_file) in stderr
        assert "tomli" in stderr
        # The settings are still dropped; that part is by design (#368).
        assert uut.args.wrap_summaries == 79

    @pytest.mark.unit
    def test_stays_quiet_when_toml_support_is_present(self, tmp_path, capsys):
        """Say nothing on the happy path."""
        config_file = tmp_path / "pyproject.toml"
        config_file.write_text(
            '[tool.docformatter]\nwrap-summaries = "120"\n', encoding="utf-8"
        )

        uut = Configurater(["/path/to/docformatter", "--config", str(config_file), ""])
        uut.do_parse_arguments()

        assert capsys.readouterr().err == ""
        assert uut.args.wrap_summaries == 120
DEFAULT_ADORNS = r"[!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~]{4,}"


def _write_pyproject(directory, body):
    """Write a pyproject.toml holding a [tool.docformatter] section."""
    config_file = directory / "pyproject.toml"
    config_file.write_text("[tool.docformatter]\n" + body, encoding="utf-8")
    return str(config_file)


class TestRestSectionAdornsConfigKey:
    """Class for testing the rest-section-adorns configuration file key.

    The command line option is --rest-section-adorns and every other option
    is read from the configuration file under its hyphenated command line
    name.  docs/source/configuration.rst tells the user to set the
    ``rest-section-adorns`` option in the configuration file, so that
    spelling has to be the one that is honored.
    """

    @pytest.mark.unit
    def test_hyphenated_key_is_honored(self, tmp_path):
        """Read the documented, hyphenated key from pyproject.toml."""
        config_file = _write_pyproject(tmp_path, 'rest-section-adorns = "[!]{4,}"\n')

        uut = Configurater(["/path/to/docformatter", "--config", config_file, ""])
        uut.do_parse_arguments()

        assert uut.flargs["rest-section-adorns"] == "[!]{4,}"
        assert uut.args.rest_section_adorns == "[!]{4,}"

    @pytest.mark.unit
    def test_underscored_key_is_still_honored(self, tmp_path):
        """Keep reading the undocumented, underscored key."""
        config_file = _write_pyproject(tmp_path, 'rest_section_adorns = "[@]{4,}"\n')

        uut = Configurater(["/path/to/docformatter", "--config", config_file, ""])
        uut.do_parse_arguments()

        assert uut.args.rest_section_adorns == "[@]{4,}"

    @pytest.mark.unit
    def test_hyphenated_key_wins_over_underscored_key(self, tmp_path):
        """Prefer the documented spelling when a file carries both."""
        config_file = _write_pyproject(
            tmp_path,
            'rest-section-adorns = "[!]{4,}"\nrest_section_adorns = "[@]{4,}"\n',
        )

        uut = Configurater(["/path/to/docformatter", "--config", config_file, ""])
        uut.do_parse_arguments()

        assert uut.args.rest_section_adorns == "[!]{4,}"

    @pytest.mark.unit
    def test_default_is_used_when_key_is_absent(self, tmp_path):
        """Fall back to the default adornment regex."""
        config_file = _write_pyproject(tmp_path, 'wrap-summaries = "79"\n')

        uut = Configurater(["/path/to/docformatter", "--config", config_file, ""])
        uut.do_parse_arguments()

        assert uut.args.rest_section_adorns == DEFAULT_ADORNS

    @pytest.mark.unit
    def test_command_line_overrides_the_configuration_file(self, tmp_path):
        """Let --rest-section-adorns beat the configuration file."""
        config_file = _write_pyproject(tmp_path, 'rest-section-adorns = "[!]{4,}"\n')

        uut = Configurater(
            [
                "/path/to/docformatter",
                "--config",
                config_file,
                "--rest-section-adorns",
                "[~]{4,}",
                "",
            ]
        )
        uut.do_parse_arguments()

        assert uut.args.rest_section_adorns == "[~]{4,}"


# filename, configuration body, and the flargs each file type produces.
CONFIG_FILE_TYPES = [
    ("pyproject.toml", "[tool.docformatter]\n{options}\n", {"blank": "True"}),
    ("setup.cfg", "[docformatter]\n{options}\n", {"blank": "true"}),
    ("tox.ini", "[docformatter]\n{options}\n", {"blank": "true"}),
]

CONFIG_CASES = pytest.mark.parametrize(
    "filename,body,expected", CONFIG_FILE_TYPES, ids=["pyproject", "setup-cfg", "tox"]
)

CONFIG_ARGUMENTS = pytest.mark.parametrize(
    "config_arguments",
    [lambda path: ["--config", path], lambda path: [f"--config={path}"]],
    ids=["separate", "equals"],
)

SOURCE = 'def f():\n    """Summary.\n\n    Description text.\n    """\n    return 1\n'
BLANK_SOURCE = (
    'def f():\n    """Summary.\n\n    Description text.\n\n    """\n    return 1\n'
)


def _run_docformatter(arguments, directory):
    """Run docformatter in a subprocess and return the completed process."""
    return subprocess.run(
        [sys.executable, "-m", "docformatter", *arguments],
        cwd=str(directory),
        capture_output=True,
        text=True,
    )


class TestConfigArgument:
    """Class for testing the two --config spellings accepted by argparse."""

    @pytest.mark.unit
    @CONFIG_CASES
    @CONFIG_ARGUMENTS
    def test_supported_file_is_read(
        self, tmp_path, filename, body, expected, config_arguments
    ):
        """Read a supported file given as --config PATH or --config=PATH."""
        config_file = tmp_path / filename
        config_file.write_text(body.format(options="blank = true"), encoding="utf-8")

        uut = Configurater(
            ["/path/to/docformatter", *config_arguments(str(config_file)), ""]
        )
        uut.do_parse_arguments()

        assert uut.config_file == str(config_file)
        assert uut.flargs == expected
        assert uut.args.post_description_blank

    @pytest.mark.unit
    @CONFIG_ARGUMENTS
    def test_explicit_path_wins_over_autodiscovery(self, tmp_path, config_arguments):
        """Use the requested file when the directory holds a different one."""
        (tmp_path / "setup.cfg").write_text(
            "[docformatter]\nwrap-summaries = 120\n", encoding="utf-8"
        )
        requested = tmp_path / "requested" / "pyproject.toml"
        requested.parent.mkdir()
        requested.write_text(
            "[tool.docformatter]\nwrap-summaries = 70\n", encoding="utf-8"
        )
        # Autodiscovery in the working directory would pick this file instead.
        (tmp_path / "pyproject.toml").write_text(
            "[tool.docformatter]\nwrap-summaries = 120\n", encoding="utf-8"
        )

        uut = Configurater(
            [
                "/path/to/docformatter",
                *config_arguments(str(requested)),
                "",
            ]
        )
        uut.do_parse_arguments()

        assert uut.config_file == str(requested)
        assert uut.args.wrap_summaries == 70

    @pytest.mark.unit
    @CONFIG_ARGUMENTS
    def test_unsupported_file_is_still_ignored(self, tmp_path, config_arguments):
        """Keep ignoring files outside the documented set of names."""
        config_file = tmp_path / "custom.toml"
        config_file.write_text("[tool.docformatter]\nblank = true\n", encoding="utf-8")

        uut = Configurater(
            ["/path/to/docformatter", *config_arguments(str(config_file)), ""]
        )
        uut.do_parse_arguments()

        assert uut.config_file == str(config_file)
        assert uut.flargs == {}
        assert not uut.args.post_description_blank

    @pytest.mark.unit
    def test_mixed_repeated_config_uses_the_last_value(self, tmp_path):
        """Load the same file argparse reports when --config is repeated."""
        first = tmp_path / "first" / "pyproject.toml"
        first.parent.mkdir()
        first.write_text("[tool.docformatter]\nwrap-summaries = 40\n", encoding="utf-8")
        second = tmp_path / "second" / "pyproject.toml"
        second.parent.mkdir()
        second.write_text("[tool.docformatter]\nblank = true\n", encoding="utf-8")

        uut = Configurater(
            [
                "/path/to/docformatter",
                f"--config={first}",
                "--config",
                str(second),
                "",
            ]
        )
        uut.do_parse_arguments()

        assert uut.args.config == str(second)
        assert uut.config_file == str(second)
        assert uut.flargs == {"blank": "True"}

    @pytest.mark.unit
    def test_stops_at_end_of_options(self, tmp_path):
        """Ignore --config looking tokens that argparse treats as file names."""
        requested = tmp_path / "pyproject.toml"
        requested.write_text("[tool.docformatter]\nblank = true\n", encoding="utf-8")
        decoy = tmp_path / "--config=decoy.toml"
        decoy.write_text("[tool.docformatter]\nwrap-summaries = 40\n", encoding="utf-8")

        uut = Configurater(
            [
                "/path/to/docformatter",
                f"--config={requested}",
                "--",
                "--config=decoy.toml",
            ]
        )
        uut.do_parse_arguments()

        assert uut.config_file == str(requested)
        assert uut.flargs == {"blank": "True"}

    @pytest.mark.unit
    def test_program_name_is_not_read_as_the_argument(self, tmp_path):
        """Start scanning after the program name argparse would ignore."""
        uut = Configurater(["--config=sample.toml", "file.py"])
        uut.do_parse_arguments()

        assert uut.config_file == "./pyproject.toml"

    @pytest.mark.system
    @CONFIG_CASES
    @CONFIG_ARGUMENTS
    def test_supported_file_is_applied_by_the_command(
        self, tmp_path, filename, body, expected, config_arguments
    ):
        """Apply the settings through the real command line."""
        (tmp_path / filename).write_text(
            body.format(options="blank = true"), encoding="utf-8"
        )
        (tmp_path / "target.py").write_text(SOURCE, encoding="utf-8")

        result = _run_docformatter(
            [*config_arguments(filename), "--in-place", "target.py"], tmp_path
        )

        assert result.returncode == 3, result.stderr
        assert (tmp_path / "target.py").read_text(encoding="utf-8") == BLANK_SOURCE

    @pytest.mark.system
    def test_explicit_path_beats_directory_file_on_the_command_line(self, tmp_path):
        """Prefer the requested file over the directory one end to end."""
        (tmp_path / "pyproject.toml").write_text(
            "[tool.docformatter]\nblank = false\n", encoding="utf-8"
        )
        requested = tmp_path / "requested" / "pyproject.toml"
        requested.parent.mkdir()
        requested.write_text("[tool.docformatter]\nblank = true\n", encoding="utf-8")
        (tmp_path / "target.py").write_text(SOURCE, encoding="utf-8")

        result = _run_docformatter(
            [f"--config={requested}", "--in-place", "target.py"], tmp_path
        )

        assert result.returncode == 3, result.stderr
        assert (tmp_path / "target.py").read_text(encoding="utf-8") == BLANK_SOURCE
