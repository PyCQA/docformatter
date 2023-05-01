# pylint: skip-file
# type: ignore
#
#       tests.conftest.py is part of the docformatter project
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
"""docformatter test suite configuration file."""

# Standard Library Imports
import argparse
import os
import shutil
import subprocess
import sys
import tempfile

# Third Party Imports
import pytest

# Root directory is up one because we're in tests/.
ROOT_DIRECTORY = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


@pytest.fixture(scope="function")
def temporary_directory(directory=".", prefix=""):
    """Create temporary directory and yield its path."""
    temp_directory = tempfile.mkdtemp(prefix=prefix, dir=directory)
    try:
        yield temp_directory
    finally:
        shutil.rmtree(temp_directory)


@pytest.fixture(scope="function")
def temporary_file(contents, file_directory=".", file_prefix=""):
    """Write contents to temporary file and yield it."""
    f = tempfile.NamedTemporaryFile(
        suffix=".py", prefix=file_prefix, delete=False, dir=file_directory
    )
    try:
        f.write(contents.encode())
        f.close()
        yield f.name
    finally:
        os.remove(f.name)

@pytest.fixture(scope="function")
def temporary_pyproject_toml(config, config_file_directory="/tmp",):
    """Write contents to temporary configuration and yield it."""
    f = open(f"{config_file_directory}/pyproject.toml", "wb")
    try:
        f.write(config.encode())
        f.close()
        yield f.name
    finally:
        os.remove(f.name)

@pytest.fixture(scope="function")
def temporary_setup_cfg(config, config_file_directory="/tmp",):
    """Write contents to temporary configuration and yield it."""
    f = open(f"{config_file_directory}/setup.cfg", "wb")
    try:
        f.write(config.encode())
        f.close()
        yield f.name
    finally:
        os.remove(f.name)

@pytest.fixture(scope="function")
def run_docformatter(arguments, temporary_file):
    """Run subprocess with same Python path as parent.

    Return subprocess object.
    """
    if "DOCFORMATTER_COVERAGE" in os.environ and int(
            os.environ["DOCFORMATTER_COVERAGE"]
    ):
        DOCFORMATTER_COMMAND = [
            "coverage",
            "run",
            "--branch",
            "--parallel",
            "--omit=*/site-packages/*",
            os.environ["VIRTUAL_ENV"] + "/bin/docformatter",
        ]
    else:
        DOCFORMATTER_COMMAND = [
            os.environ["VIRTUAL_ENV"] + "/bin/docformatter",
        ]  # pragma: no cover

    if "-" not in arguments:
        arguments.append(temporary_file)
    environ = os.environ.copy()
    environ["PYTHONPATH"] = os.pathsep.join(sys.path)
    return subprocess.Popen(
        DOCFORMATTER_COMMAND + arguments,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE,
        env=environ,
    )


@pytest.fixture(scope="function")
def test_args(args):
    """Create a set of arguments to use with tests.

    To pass no arguments, just an empty file name:
        @pytest.mark.parametrize("args", [[""]])

    To pass an argument AND empty file name:
        @pytest.mark.parametrize("args", [["--wrap-summaries", "79", ""]])
    """
    parser = argparse.ArgumentParser(
        description="parser object for docformatter tests",
        prog="docformatter",
    )

    changes = parser.add_mutually_exclusive_group()
    changes.add_argument(
        "-i",
        "--in-place",
        action="store_true",
    )
    changes.add_argument(
        "-c",
        "--check",
        action="store_true",
    )
    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-e",
        "--exclude",
        nargs="*",
    )
    parser.add_argument(
        "-n",
        "--non-cap",
        nargs="*",
    )
    parser.add_argument(
        "-s",
        "--style",
        default="sphinx",
    )
    parser.add_argument(
        "--wrap-summaries",
        default=79,
        type=int,
        metavar="length",
    )
    parser.add_argument(
        "--wrap-descriptions",
        default=72,
        type=int,
        metavar="length",
    )
    parser.add_argument(
        "--force-wrap",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--tab-width",
        type=int,
        dest="tab_width",
        metavar="width",
        default=1,
    )
    parser.add_argument(
        "--blank",
        dest="post_description_blank",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--pre-summary-newline",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--pre-summary-space",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--black",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--make-summary-multi-line",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--close-quotes-on-newline",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--range",
        metavar="line",
        dest="line_range",
        default=None,
        type=int,
        nargs=2,
    )
    parser.add_argument(
        "--docstring-length",
        metavar="length",
        dest="length_range",
        default=None,
        type=int,
        nargs=2,
    )
    parser.add_argument(
        "--non-strict",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--config",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="test version",
    )
    parser.add_argument(
        "files",
        nargs="+",
    )

    yield parser.parse_args(args)
