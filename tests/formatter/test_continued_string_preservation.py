"""Preserve escaped physical newlines inside ordinary string tokens."""

import ast
import sys

import pytest

from docformatter import Formatter


@pytest.mark.integration
@pytest.mark.parametrize("args", [[""], ["--black", ""]])
@pytest.mark.parametrize("newline", ["\n", "\r\n"])
@pytest.mark.parametrize(
    "source",
    [
        'value = "first\\\nsecond"\n',
        "value = 'first\\\nsecond'\n",
        'value = r"first\\\nsecond"\n',
        'value = b"first\\\nsecond"\n',
        'value = u"first\\\nsecond"\n',
        'print("first\\\nsecond")\n',
        'def value():\n    return "first\\\nsecond"\n',
        'value = "first\\\nsecond\\\nthird"\n',
        'value = "first\\\nsecond" "suffix"\n',
        'value = "first\\\nsecond" + "suffix"\n',
        'value = "first\\\nsecond"',
        'value = (\n    "first\\\nsecond"\n)\n',
    ],
)
def test_continued_string_is_preserved(source, newline, test_args, args):
    """A continuation within a string must not duplicate surrounding Python code."""
    source = source.replace("\n", newline)
    formatter = Formatter(test_args, sys.stderr, sys.stdin, sys.stdout)

    formatted = formatter._do_format_code(source)

    assert formatted == source
    assert ast.dump(ast.parse(formatted)) == ast.dump(ast.parse(source))
    assert formatter._do_format_code(formatted) == formatted


@pytest.mark.integration
@pytest.mark.parametrize("args", [[""], ["--black", ""]])
@pytest.mark.parametrize("newline", ["\n", "\r\n"])
def test_continued_string_after_docstring_rewrite(newline, test_args, args):
    """Preserve string-token positions when docstring formatting shifts later rows."""
    source = 'class Example:\n    """Summary."""\n    value = "first\\\nsecond"\n'
    expected = source.replace('"""Summary."""\n', '"""Summary."""\n\n')
    source = source.replace("\n", newline)
    expected = expected.replace("\n", newline)
    formatter = Formatter(test_args, sys.stderr, sys.stdin, sys.stdout)

    formatted = formatter._do_format_code(source)

    assert formatted == expected
    assert ast.dump(ast.parse(formatted)) == ast.dump(ast.parse(source))
    assert formatter._do_format_code(formatted) == formatted
