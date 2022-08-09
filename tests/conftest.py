# pylint: skip-file
# type: ignore
#
#       tests.conftest.py is part of the docformatter project
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
"""docformatter test suite configuration file."""

# Standard Library Imports
import os
import shutil
import subprocess
import sys
import tempfile

# Third Party Imports
import pytest

# Root directory is up one because we're in tests/.
ROOT_DIRECTORY = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

if "DOCFORMATTER_COVERAGE" in os.environ and int(
    os.environ["DOCFORMATTER_COVERAGE"]
):
    DOCFORMATTER_COMMAND = [
        "coverage",
        "run",
        "--branch",
        "--parallel",
        "--omit=*/site-packages/*",
        os.path.join(ROOT_DIRECTORY, "docformatter.py"),
    ]
else:
    # We need to specify the executable to make sure the correct Python
    # interpreter gets used.
    DOCFORMATTER_COMMAND = [
        sys.executable,
        os.path.join(ROOT_DIRECTORY, "docformatter.py"),
    ]  # pragma: no cover


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
def run_docformatter(arguments, temporary_file):
    """Run subprocess with same Python path as parent.

    Return subprocess object.
    """
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
