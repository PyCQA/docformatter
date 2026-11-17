"""Preserve comments following docstrings excluded from formatting."""

import ast
import sys

import pytest

from docformatter import Formatter


@pytest.mark.integration
@pytest.mark.parametrize(
    "args",
    [
        ["--range", "20", "30", ""],
        ["--docstring-length", "20", "30", ""],
        ["--black", "--range", "20", "30", ""],
        ["--black", "--docstring-length", "20", "30", ""],
    ],
)
@pytest.mark.parametrize("newline", ["\n", "\r\n"])
@pytest.mark.parametrize("comment", ["", "  # noqa: D400", "\t# trailing", "# joined"])
@pytest.mark.parametrize(
    "source",
    [
        '"""leave this unformatted"""{comment}\n',
        '"""leave this unformatted\n\nmore detail\n"""{comment}\n',
        'def f():\n    """leave this unformatted"""{comment}\n    pass\n',
        'async def f():\n    """leave this unformatted"""{comment}\n    pass\n',
        'class C:\n    """leave this unformatted"""{comment}\n    pass\n',
        'class C:\n    def f(self):\n'
        '        """leave this unformatted"""{comment}\n        pass\n',
        'value = 1\n"""leave this unformatted"""{comment}\nother = 2\n',
        'def f():\n    """leave this unformatted\n\n'
        '    more detail\n    """{comment}\n    pass\n',
        'r"""leave this unformatted"""{comment}\n',
        '"""leave this unformatted"""{comment}\n# standalone comment\nvalue = 1\n',
    ],
)
def test_skipped_docstring_preserves_comment(source, comment, newline, test_args, args):
    """Excluded docstrings and their comments must remain unchanged."""
    source = source.replace("{comment}", comment).replace("\n", newline)
    formatter = Formatter(test_args, sys.stderr, sys.stdin, sys.stdout)

    formatted = formatter._do_format_code(source)

    assert formatted == source
    assert ast.dump(ast.parse(formatted)) == ast.dump(ast.parse(source))
    assert formatter._do_format_code(formatted) == formatted


@pytest.mark.integration
@pytest.mark.parametrize(
    "args",
    [
        ["--range", "20", "30", ""],
        ["--docstring-length", "20", "30", ""],
    ],
)
@pytest.mark.parametrize("newline", ["\n", "\r\n"])
@pytest.mark.parametrize("ending", ["", "\n"])
@pytest.mark.parametrize(
    "source",
    [
        '"""leave this unformatted"""  # noqa: D400',
        '"""leave this unformatted\n\nmore detail\n"""  # noqa: D400',
        'def f():\n    """leave this unformatted"""  # noqa: D400',
        'class C:\n    """leave this unformatted"""  # noqa: D400',
        'value = 1\n"""leave this unformatted"""  # noqa: D400',
    ],
)
def test_skipped_docstring_comment_at_eof(source, ending, newline, test_args, args):
    """Preserve whether a trailing comment has a final newline."""
    source = (source + ending).replace("\n", newline)
    formatter = Formatter(test_args, sys.stderr, sys.stdin, sys.stdout)

    formatted = formatter._do_format_code(source)

    assert formatted == source
    assert ast.dump(ast.parse(formatted)) == ast.dump(ast.parse(source))
    assert formatter._do_format_code(formatted) == formatted


@pytest.mark.integration
@pytest.mark.parametrize(
    "args",
    [
        ["--range", "5", "6", ""],
        ["--docstring-length", "2", "2", ""],
    ],
)
@pytest.mark.parametrize("newline", ["\n", "\r\n"])
def test_skipped_comment_does_not_prevent_selected_formatting(newline, test_args, args):
    """Preserve skipped content while formatting another selected docstring."""
    source = (
        '"""leave this unformatted"""  # noqa: D400\n\n\n'
        "def f():\n"
        '    """Selected docstring\n'
        '    """\n'
        "    return 1\n"
    )
    expected = (
        '"""leave this unformatted"""  # noqa: D400\n\n\n'
        "def f():\n"
        '    """Selected docstring."""\n'
        "    return 1\n"
    )
    source = source.replace("\n", newline)
    expected = expected.replace("\n", newline)
    formatter = Formatter(test_args, sys.stderr, sys.stdin, sys.stdout)

    formatted = formatter._do_format_code(source)

    assert formatted == expected
    assert formatter._do_format_code(formatted) == formatted
