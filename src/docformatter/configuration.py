#!/usr/bin/env python
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
"""This module provides docformatter's Configurater class."""


# Standard Library Imports
import argparse
import contextlib
import os
import sys
from configparser import ConfigParser
from typing import Dict, List, Union

TOMLLIB_INSTALLED = False
TOMLI_INSTALLED = False
with contextlib.suppress(ImportError):
    if sys.version_info >= (3, 11):
        # Standard Library Imports
        import tomllib

        TOMLLIB_INSTALLED = True
    else:
        # Third Party Imports
        import tomli

        TOMLI_INSTALLED = True

# docformatter Package Imports
from docformatter import __pkginfo__


class Configurater:
    """Read and store all the docformatter configuration information."""

    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    """Parser object."""

    flargs_dct: Dict[str, Union[bool, float, int, str]] = {}
    """Dictionary of configuration file arguments."""

    configuration_file_lst = [
        "pyproject.toml",
        "setup.cfg",
        "tox.ini",
    ]
    """List of supported configuration files."""

    args: argparse.Namespace = argparse.Namespace()

    def __init__(self, args: List[Union[bool, int, str]]) -> None:
        """Initialize a Configurater class instance.

        Parameters
        ----------
        args : list
            Any command line arguments passed during invocation.
        """
        self.args_lst = args
        self.config_file = ""
        self.parser = argparse.ArgumentParser(
            description=__doc__,
            prog="docformatter",
        )

        try:
            self.config_file = self.args_lst[self.args_lst.index("--config") + 1]
        except ValueError:
            for _configuration_file in self.configuration_file_lst:
                if os.path.isfile(_configuration_file):
                    self.config_file = f"./{_configuration_file}"
                    break

        if os.path.isfile(self.config_file):
            self._do_read_configuration_file()

    def do_parse_arguments(self) -> None:
        """Parse configuration file and command line arguments."""
        changes = self.parser.add_mutually_exclusive_group()
        changes.add_argument(
            "-i",
            "--in-place",
            action="store_true",
            default=self.flargs_dct.get("in-place", "false").lower() == "true",
            help="make changes to files instead of printing diffs",
        )
        changes.add_argument(
            "-c",
            "--check",
            action="store_true",
            default=self.flargs_dct.get("check", "false").lower() == "true",
            help="only check and report incorrectly formatted files",
        )
        self.parser.add_argument(
            "-d",
            "--diff",
            action="store_true",
            default=self.flargs_dct.get("diff", "false").lower() == "true",
            help="when used with `--check` or `--in-place`, also what changes "
            "would be made",
        )
        self.parser.add_argument(
            "-r",
            "--recursive",
            action="store_true",
            default=self.flargs_dct.get("recursive", "false").lower() == "true",
            help="drill down directories recursively",
        )
        self.parser.add_argument(
            "-e",
            "--exclude",
            nargs="*",
            default=self.flargs_dct.get("exclude", None),
            help="in recursive mode, exclude directories and files by names",
        )
        self.parser.add_argument(
            "-n",
            "--non-cap",
            action="store",
            nargs="*",
            default=self.flargs_dct.get("non-cap", None),
            help="list of words not to capitalize when they appear as the first word "
            "in the summary",
        )
        self.parser.add_argument(
            "--black",
            action="store_true",
            default=self.flargs_dct.get("black", "false").lower() == "true",
            help="make formatting compatible with standard black options "
            "(default: False)",
        )

        self.args = self.parser.parse_known_args(self.args_lst[1:])[0]

        # Default black line length is 88 so use this when not specified
        # otherwise use PEP-8 defaults
        if self.args.black:
            _default_wrap_summaries = 88
            _default_wrap_descriptions = 88
            _default_pre_summary_space = "true"
        else:
            _default_wrap_summaries = 79
            _default_wrap_descriptions = 72
            _default_pre_summary_space = "false"

        self.parser.add_argument(
            "-s",
            "--style",
            default=self.flargs_dct.get("style", "sphinx"),
            help="name of the docstring style to use when formatting "
            "parameter lists (default: sphinx)",
        )
        self.parser.add_argument(
            "--rest-section-adorns",
            type=str,
            dest="rest_section_adorns",
            default=self.flargs_dct.get(
                "rest_section_adorns", r"[!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~]{4,}"
            ),
            help="regex for identifying reST section header adornments",
        )
        self.parser.add_argument(
            "--wrap-summaries",
            default=int(self.flargs_dct.get("wrap-summaries", _default_wrap_summaries)),
            type=int,
            metavar="length",
            help="wrap long summary lines at this length; "
            "set to 0 to disable wrapping (default: 79, 88 with --black "
            "option)",
        )
        self.parser.add_argument(
            "--wrap-descriptions",
            default=int(
                self.flargs_dct.get("wrap-descriptions", _default_wrap_descriptions)
            ),
            type=int,
            metavar="length",
            help="wrap descriptions at this length; "
            "set to 0 to disable wrapping (default: 72, 88 with --black "
            "option)",
        )
        self.parser.add_argument(
            "--force-wrap",
            action="store_true",
            default=self.flargs_dct.get("force-wrap", "false").lower() == "true",
            help="force descriptions to be wrapped even if it may "
            "result in a mess (default: False)",
        )
        self.parser.add_argument(
            "--tab-width",
            type=int,
            dest="tab_width",
            metavar="width",
            default=int(self.flargs_dct.get("tab-width", 1)),
            help="tabs in indentation are this many characters when "
            "wrapping lines (default: 1)",
        )
        self.parser.add_argument(
            "--blank",
            dest="post_description_blank",
            action="store_true",
            default=self.flargs_dct.get("blank", "false").lower() == "true",
            help="add blank line after description (default: False)",
        )
        self.parser.add_argument(
            "--pre-summary-newline",
            action="store_true",
            default=self.flargs_dct.get("pre-summary-newline", "false").lower()
            == "true",
            help="add a newline before the summary of a multi-line docstring "
            "(default: False)",
        )
        self.parser.add_argument(
            "--pre-summary-space",
            action="store_true",
            default=self.flargs_dct.get(
                "pre-summary-space", _default_pre_summary_space
            ).lower()
            == "true",
            help="add a space after the opening triple quotes (default: False)",
        )
        self.parser.add_argument(
            "--make-summary-multi-line",
            action="store_true",
            default=self.flargs_dct.get("make-summary-multi-line", "false").lower()
            == "true",
            help="add a newline before and after the summary of a one-line "
            "docstring (default: False)",
        )
        self.parser.add_argument(
            "--close-quotes-on-newline",
            action="store_true",
            default=self.flargs_dct.get("close-quotes-on-newline", "false").lower()
            == "true",
            help="place closing triple quotes on a new-line when a "
            "one-line docstring wraps to two or more lines "
            "(default: False)",
        )
        self.parser.add_argument(
            "--range",
            metavar="line",
            dest="line_range",
            default=self.flargs_dct.get("range", None),
            type=int,
            nargs=2,
            help="apply docformatter to docstrings between these "
            "lines; line numbers are indexed at 1 (default: None)",
        )
        self.parser.add_argument(
            "--docstring-length",
            metavar="length",
            dest="length_range",
            default=self.flargs_dct.get("docstring-length", None),
            type=int,
            nargs=2,
            help="apply docformatter to docstrings of given length range "
            "(default: None)",
        )
        self.parser.add_argument(
            "--non-strict",
            action="store_true",
            default=self.flargs_dct.get("non-strict", "false").lower() == "true",
            help="don't strictly follow reST syntax to identify lists (see "
            "issue #67) (default: False)",
        )
        self.parser.add_argument(
            "--config",
            default=self.config_file,
            help="path to file containing docformatter options",
        )
        self.parser.add_argument(
            "--version",
            action="version",
            version=f"%(prog)s {__pkginfo__.__version__}",
        )
        self.parser.add_argument(
            "files",
            nargs="+",
            help="files to format or '-' for standard in",
        )

        self.args = self.parser.parse_args(self.args_lst[1:])

        if self.args.line_range:
            if self.args.line_range[0] <= 0:
                self.parser.error("--range must be positive numbers")
            if self.args.line_range[0] > self.args.line_range[1]:
                self.parser.error(
                    "First value of --range should be less than or equal "
                    "to the second"
                )

        if self.args.length_range:
            if self.args.length_range[0] <= 0:
                self.parser.error("--docstring-length must be positive numbers")
            if self.args.length_range[0] > self.args.length_range[1]:
                self.parser.error(
                    "First value of --docstring-length should be less "
                    "than or equal to the second"
                )

    def _do_read_configuration_file(self) -> None:
        """Read docformatter options from a configuration file."""
        argfile = os.path.basename(self.config_file)
        for f in self.configuration_file_lst:
            if argfile == f:
                break

        fullpath, ext = os.path.splitext(self.config_file)
        filename = os.path.basename(fullpath)

        if (
            ext == ".toml"
            and (TOMLI_INSTALLED or TOMLLIB_INSTALLED)
            and filename == "pyproject"
        ):
            self._do_read_toml_configuration()

        if (ext == ".cfg" and filename == "setup") or (
            ext == ".ini" and filename == "tox"
        ):
            self._do_read_parser_configuration()

    def _do_read_toml_configuration(self) -> None:
        """Load configuration information from a *.toml file."""
        with open(self.config_file, "rb") as f:
            if TOMLI_INSTALLED:
                config = tomli.load(f)
            elif TOMLLIB_INSTALLED:
                config = tomllib.load(f)

        result = config.get("tool", {}).get("docformatter", None)
        if result is not None:
            self.flargs_dct = {
                k: v if isinstance(v, list) else str(v) for k, v in result.items()
            }

    def _do_read_parser_configuration(self) -> None:
        """Load configuration information from a *.cfg or *.ini file."""
        config = ConfigParser()
        config.read(self.config_file)

        for _section in [
            "tool.docformatter",
            "tool:docformatter",
            "docformatter",
        ]:
            if _section in config.sections():
                self.flargs_dct = {
                    k: v if isinstance(v, list) else str(v)
                    for k, v in config[_section].items()
                }
