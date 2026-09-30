# pylint: skip-file
# type: ignore
#
#       tests.formatter.test_google_field_wrapping.py is part of the docformatter project
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
"""Tests for wrapping Google-style Args and Returns entries.

Each Args/Returns entry is wrapped independently.
Running the formatter twice must leave the source unchanged.
"""

# Standard Library Imports
import sys

# Third Party Imports
import pytest

# docformatter Package Imports
from docformatter.format import Formatter

NO_ARGS = [""]


def _formatter(test_args):
    return Formatter(
        test_args,
        sys.stderr,
        sys.stdin,
        sys.stdout,
    )


@pytest.mark.integration
@pytest.mark.order(7)
@pytest.mark.parametrize("args", [NO_ARGS])
def test_wraps_long_prose_before_google_args(test_args, args):
    """Prose before Args: is wrapped; short argument entries stay intact."""
    source = '''\
def split_audio():
    """Split audio at silences to keep under the size limit.

    It's important to split near the middle of a silent section to prevent splitting on a spoken word and causing issues with transcription and diarization.

    Args:
        silent_sections: list of silent sections in ms.
        duration: total length of audio in ms
        audio_size: total size of audio file in bytes
        max_file_size: maximum file size that may exist after splits

    Returns:
        List of points in ms to use to split the audio file into chunks.
    """
'''
    expected = '''\
def split_audio():
    """Split audio at silences to keep under the size limit.

    It's important to split near the middle of a silent section to
    prevent splitting on a spoken word and causing issues with
    transcription and diarization.

    Args:
        silent_sections: list of silent sections in ms.
        duration: total length of audio in ms
        audio_size: total size of audio file in bytes
        max_file_size: maximum file size that may exist after splits

    Returns:
        List of points in ms to use to split the audio file into chunks.
    """
'''
    uut = _formatter(test_args)
    assert uut._do_format_code(source) == expected


@pytest.mark.integration
@pytest.mark.order(7)
@pytest.mark.parametrize("args", [NO_ARGS])
def test_wrap_google_args_entry(test_args, args):
    """A long Args entry wraps under the parameter with hanging indent."""
    source = '''\
def foo(value):
    """Example.

    Args:
        value: A very long argument description that exceeds the configured line width and should wrap underneath this individual parameter.
    """
'''
    expected = '''\
def foo(value):
    """Example.

    Args:
        value: A very long argument description that exceeds the
            configured line width and should wrap underneath this
            individual parameter.
    """
'''
    uut = _formatter(test_args)
    assert uut._do_format_code(source) == expected


@pytest.mark.integration
@pytest.mark.order(7)
@pytest.mark.parametrize("args", [NO_ARGS])
def test_wrap_google_args_and_returns(test_args, args):
    """Args and Returns entries wrap independently without losing structure."""
    source = '''\
def connect(host, configuration):
    """Connect to the configured database.

    Args:
        host: Hostname used by the database connection.
        configuration: Configuration containing authentication information and connection parameters that will be used when establishing the database connection.

    Returns:
        A database connection that has been initialized using the requested configuration and is ready for queries.
    """
'''
    expected = '''\
def connect(host, configuration):
    """Connect to the configured database.

    Args:
        host: Hostname used by the database connection.
        configuration: Configuration containing authentication
            information and connection parameters that will be used when
            establishing the database connection.

    Returns:
        A database connection that has been initialized using the
        requested configuration and is ready for queries.
    """
'''
    uut = _formatter(test_args)
    assert uut._do_format_code(source) == expected


@pytest.mark.integration
@pytest.mark.order(7)
@pytest.mark.parametrize("args", [NO_ARGS])
def test_reflows_existing_manual_wrapping(test_args, args):
    """Already-wrapped Args entries are unwrapped then rewrapped at width."""
    source = '''\
def foo(value):
    """Example.

    Args:
        value: A very long argument description that exceeds
          the configured line width and should wrap underneath
          this individual parameter.
    """
'''
    expected = '''\
def foo(value):
    """Example.

    Args:
        value: A very long argument description that exceeds the
            configured line width and should wrap underneath this
            individual parameter.
    """
'''
    uut = _formatter(test_args)
    assert uut._do_format_code(source) == expected


@pytest.mark.integration
@pytest.mark.order(7)
@pytest.mark.parametrize("args", [NO_ARGS])
def test_google_args_wrapping_is_idempotent(test_args, args):
    """Running the formatter twice yields the same source."""
    source = '''\
def connect(host, configuration):
    """Connect to the configured database.

    Args:
        host: Hostname used by the database connection.
        configuration: Configuration containing authentication information and connection parameters that will be used when establishing the database connection.

    Returns:
        A database connection that has been initialized using the requested configuration and is ready for queries.
    """
'''
    uut = _formatter(test_args)
    once = uut._do_format_code(source)
    twice = uut._do_format_code(once)
    assert twice == once


@pytest.mark.integration
@pytest.mark.order(7)
@pytest.mark.parametrize("args", [NO_ARGS])
def test_already_correct_google_docstring_is_unchanged(test_args, args):
    """A docstring that is already wrapped at the configured width is stable."""
    source = '''\
def connect(host, configuration):
    """Connect to the configured database.

    Args:
        host: Hostname used by the database connection.
        configuration: Configuration containing authentication
            information and connection parameters that will be used when
            establishing the database connection.

    Returns:
        A database connection that has been initialized using the
        requested configuration and is ready for queries.
    """
'''
    uut = _formatter(test_args)
    assert uut._do_format_code(source) == source


@pytest.mark.integration
@pytest.mark.order(7)
@pytest.mark.parametrize("args", [NO_ARGS])
def test_wraps_google_entry_with_type_hint(test_args, args):
    """Type hints on Args entries are preserved while the description wraps."""
    source = '''\
def load(cfg, task):
    """Load a model from a configuration file.

    Args:
        cfg (str): Path to the model configuration file in YAML format that should be wrapped when the path description is long enough.
        task (str | None): The specific task for the model.
    """
'''
    expected = '''\
def load(cfg, task):
    """Load a model from a configuration file.

    Args:
        cfg (str): Path to the model configuration file in YAML format
            that should be wrapped when the path description is long
            enough.
        task (str | None): The specific task for the model.
    """
'''
    uut = _formatter(test_args)
    assert uut._do_format_code(source) == expected


@pytest.mark.integration
@pytest.mark.order(7)
@pytest.mark.parametrize("args", [NO_ARGS])
def test_wraps_method_docstring_google_args(test_args, args):
    """Method docstrings keep the extra indent while wrapping entries."""
    source = '''\
class Client:
    def connect(self, configuration):
        """Connect to the configured database.

        Args:
            configuration: Configuration containing authentication information and connection parameters that will be used when establishing the database connection.
        """
'''
    expected = '''\
class Client:
    def connect(self, configuration):
        """Connect to the configured database.

        Args:
            configuration: Configuration containing authentication
                information and connection parameters that will be used
                when establishing the database connection.
        """
'''
    uut = _formatter(test_args)
    assert uut._do_format_code(source) == expected


@pytest.mark.integration
@pytest.mark.order(7)
@pytest.mark.parametrize("args", [NO_ARGS])
def test_preserves_raises_section(test_args, args):
    """Non-Args/Returns Google sections are left unchanged."""
    source = '''\
def load(cfg):
    """Load a model from a configuration file.

    Args:
        cfg: Path to the model configuration file in YAML format that should be wrapped when the path description is long enough.

    Raises:
        ValueError: If the configuration file is invalid.
        ImportError: If the required dependencies are not installed.
    """
'''
    expected = '''\
def load(cfg):
    """Load a model from a configuration file.

    Args:
        cfg: Path to the model configuration file in YAML format that
            should be wrapped when the path description is long enough.

    Raises:
        ValueError: If the configuration file is invalid.
        ImportError: If the required dependencies are not installed.
    """
'''
    uut = _formatter(test_args)
    assert uut._do_format_code(source) == expected


@pytest.mark.integration
@pytest.mark.order(7)
@pytest.mark.parametrize("args", [NO_ARGS])
def test_leaves_url_in_prose_before_args(test_args, args):
    """A URL in the description before Args: does not destroy the section."""
    source = '''\
def fetch(url):
    """Fetch a remote resource.

    See https://example.com/docs/api/v1/resources for the full protocol description that explains how resources are addressed.

    Args:
        url: Resource locator passed to the client.
    """
'''
    uut = _formatter(test_args)
    result = uut._do_format_code(source)
    assert "    Args:\n        url: Resource locator passed to the client." in result
    assert uut._do_format_code(result) == result


@pytest.mark.integration
@pytest.mark.order(7)
@pytest.mark.parametrize("args", [NO_ARGS])
def test_leaves_doctest_docstring_unchanged(test_args, args):
    """Docstrings that contain doctests are not wrapped."""
    source = '''\
def add(left, right):
    """Add two numbers.

    Examples:
        >>> add(1, 2)
        3

    Args:
        left: The first operand that would otherwise wrap if this were ordinary prose of sufficient length to exceed the wrap width.
        right: The second operand.
    """
'''
    uut = _formatter(test_args)
    assert uut._do_format_code(source) == source
