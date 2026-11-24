"""Keep blank lines after docstrings that --docstring-length skips."""

# Standard Library Imports
import io

# Third Party Imports
import pytest

# docformatter Package Imports
from docformatter import Configurater, Formatter


def format_source(source, *args):
    configuration = Configurater(["docformatter", *args, "-"])
    configuration.do_parse_arguments()
    formatter = Formatter(
        configuration.args, io.StringIO(), io.StringIO(), io.StringIO()
    )
    return formatter._do_format_code(source)


SKIPPED_CLASS = '''\
class Foo:
    """
    Class docstring.
    """

    # comment
    x = 1
'''

SKIPPED_FUNCTION = '''\
def outer():
    """
    Function docstring.
    """

    def inner():
        pass

    return inner
'''

SKIPPED_MODULE = '''\
"""
Module docstring.
"""

import os
'''

SKIPPED_BLANK_LINES = '''\
class Foo:
    """
    Class docstring.
    """



    x = 1
'''


@pytest.mark.integration
@pytest.mark.parametrize(
    "source",
    [SKIPPED_CLASS, SKIPPED_FUNCTION, SKIPPED_MODULE, SKIPPED_BLANK_LINES],
)
def test_skipped_docstring_keeps_following_blank_lines(source):
    """A docstring outside the --docstring-length range is left untouched.

    The blank lines after it are part of that and must not be removed.
    """
    formatted = format_source(source, "--docstring-length", "1", "1")
    assert formatted == source
    assert format_source(formatted, "--docstring-length", "1", "1") == formatted
