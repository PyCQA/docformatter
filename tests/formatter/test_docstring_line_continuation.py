"""Leave docstrings that use a backslash line continuation alone."""

import ast
import io

import pytest

from docformatter import Configurater, Formatter


def format_source(source):
    configuration = Configurater(["docformatter", "-"])
    configuration.do_parse_arguments()
    formatter = Formatter(
        configuration.args, io.StringIO(), io.StringIO(), io.StringIO()
    )
    return formatter._do_format_code(source)


@pytest.mark.integration
@pytest.mark.parametrize(
    "source",
    [
        '"""\\\nThis module provides sockets.\nOn Unix, it supports IP.\n"""\n',
        'def foo():\n    """\\\n    Return a thing.\n\n    More text here.\n    """\n',
        'def foo():\n    """Return a thing.\n\n    Some text that goes on \\\n    and continues here.\n    """\n',
        'def foo():\n    r"""\\\n    Return a thing.\n\n    More text here.\n    """\n',
    ],
)
def test_backslash_continuation_is_not_rewrapped(source):
    """A trailing backslash must not become a literal backslash in the docstring."""
    formatted = format_source(source)
    assert formatted == source
    assert ast.dump(ast.parse(formatted)) == ast.dump(ast.parse(source))
