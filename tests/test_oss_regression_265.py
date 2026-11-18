"""Regression for a summary sentence split across short source lines."""

import sys

import pytest

from docformatter.format import Formatter


@pytest.mark.integration
@pytest.mark.parametrize("args", [[""]])
@pytest.mark.parametrize("continuation_indent", ["", "    "])
def test_wrapped_summary_sentence(test_args, continuation_indent):
    source = (
        "def launch_rocket():\n"
        '    """Launch\n'
        f"{continuation_indent}the\n"
        f'{continuation_indent}rocket. Go colonize space."""\n'
    )
    expected = (
        "def launch_rocket():\n"
        '    """Launch the rocket.\n'
        "\n"
        "    Go colonize space.\n"
        '    """\n'
    )
    formatter = Formatter(test_args, sys.stderr, sys.stdin, sys.stdout)

    formatted = formatter._do_format_code(source)

    assert formatted == expected
    assert formatter._do_format_code(formatted) == expected
