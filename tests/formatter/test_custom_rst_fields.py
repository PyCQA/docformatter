# pylint: skip-file
# type: ignore
#
#       tests.formatter.test_custom_rst_fields.py is part of the docformatter project
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
"""Regression coverage for custom reStructuredText fields (issue #279)."""

# Standard Library Imports
import sys

# Third Party Imports
import pytest

# docformatter Package Imports
from docformatter.format import Formatter
from docformatter.patterns.fields import do_find_field_lists, is_sphinx_field_list


@pytest.mark.parametrize(
    "field",
    [
        "calls",
        "custom-name",
        "param dict[str, int] value",
        "custom:name",
        r"escaped\: name",
        "字段",
    ],
)
def test_custom_field_markers(field):
    text = "Prose mentions :func:`a_role`.\n    :" + field + ": body\n"
    indices, wrap = do_find_field_lists(text, "sphinx")
    assert wrap
    assert [text[start:end] for start, end in indices] == [":" + field + ":"]
    assert is_sphinx_field_list(":" + field + ": body")


@pytest.mark.parametrize(
    "text",
    [
        "Prose :calls: text",
        ":class:`Thing`",
        ":: text",
        ": calls: text",
        ":name : text",
        ":calls:body",
    ],
)
def test_prose_and_roles_are_not_field_markers(text):
    assert do_find_field_lists(text, "sphinx")[0] == []
    assert not is_sphinx_field_list(text)


@pytest.mark.parametrize("args", [[""], ["--black", ""]])
@pytest.mark.parametrize(
    "field", ["calls", "custom-name", "param dict[str, int] value"]
)
def test_custom_field_wrapping_is_indented_and_idempotent(test_args, args, field):
    source = (
        "def f():\n"
        '    """Create a file.\n\n'
        "    :" + field + ": `PUT /repos/{owner}/{repo}/contents/{path} "
        "<https://docs.github.com/en/rest/reference/repos#create-or-update-file-contents>`_\n"
        "    :param path: string, (required), path of the file in the repository\n"
        "    :param message: string, (required), commit message\n"
        '    """\n'
    )
    formatter = Formatter(test_args, sys.stderr, sys.stdin, sys.stdout)
    result = formatter._do_format_code(source)
    lines = result.splitlines()
    start = next(
        i for i, line in enumerate(lines) if line.startswith("    :" + field + ":")
    )
    end = next(i for i, line in enumerate(lines) if line.startswith("    :param path:"))
    assert lines[start].startswith("    :" + field + ": ")
    assert end > start + 1
    assert all(line.startswith("        ") for line in lines[start + 1 : end])
    assert formatter._do_format_code(result) == result
