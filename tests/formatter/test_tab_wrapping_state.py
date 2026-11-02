"""Keep tab-width compensation local to each formatted docstring."""

import ast
import copy
import sys

import pytest

from docformatter import Formatter


@pytest.mark.integration
@pytest.mark.parametrize(
    "args",
    [
        ["--tab-width", "4", "--wrap-summaries", "40", "--wrap-descriptions", "40", ""],
        [
            "--tab-width",
            "8",
            "--wrap-summaries",
            "40",
            "--wrap-descriptions",
            "40",
            "--make-summary-multi-line",
            "",
        ],
        [
            "--tab-width",
            "4",
            "--wrap-summaries",
            "40",
            "--wrap-descriptions",
            "40",
            "--black",
            "",
        ],
        ["--tab-width", "4", "--wrap-summaries", "0", "--wrap-descriptions", "40", ""],
        ["--tab-width", "4", "--wrap-summaries", "40", "--wrap-descriptions", "0", ""],
        ["--tab-width", "4", "--wrap-summaries", "0", "--wrap-descriptions", "0", ""],
    ],
)
@pytest.mark.parametrize("indentation", ["\t", "\t\t"])
@pytest.mark.parametrize("with_description", [False, True])
def test_tab_wrapping_is_independent_of_previous_docstrings(
    args, test_args, indentation, with_description
):
    """Repeated docstrings and files must not consume the configured wrap widths."""
    widths = (test_args.wrap_summaries, test_args.wrap_descriptions)
    summary = "Return the requested value with several words in the summary."
    docstring = '"""' + summary
    if with_description:
        docstring += (
            "\n\n"
            + indentation
            + "Describe the returned value with enough words to require wrapping."
            + "\n"
            + indentation
        )
    docstring += '"""'
    source = f"def function_0():\n{indentation}{docstring}\n{indentation}pass\n\n"
    original_args = copy.copy(test_args)
    formatter = Formatter(test_args, sys.stderr, sys.stdin, sys.stdout)

    expected = formatter._do_format_code(source)
    assert (test_args.wrap_summaries, test_args.wrap_descriptions) == widths
    ast.parse(expected)
    assert all(
        line.startswith(indentation) for line in expected.splitlines()[1:] if line
    )
    if all(width > 0 for width in widths):
        assert all(
            len(line.expandtabs(test_args.tab_width)) <= min(widths)
            for line in expected.splitlines()
        )
    if widths[0] == 0:
        assert summary in expected
    if with_description and widths[1] == 0:
        assert (
            "Describe the returned value with enough words to require wrapping."
            in expected
        )
    assert formatter._do_format_code(expected) == expected
    # The same Formatter is reused when processing multiple files.
    assert formatter._do_format_code(source) == expected

    repeated_source = "".join(
        source.replace("function_0", f"function_{i}") for i in range(13)
    )
    repeated_expected = "".join(
        expected.replace("function_0", f"function_{i}") for i in range(13)
    )
    formatted = formatter._do_format_code(repeated_source)
    assert formatted == repeated_expected
    ast.parse(formatted)
    assert formatter._do_format_code(formatted) == formatted
    assert (test_args.wrap_summaries, test_args.wrap_descriptions) == widths

    # A preceding tab-indented file must not affect a space-indented file.
    space_source = source.replace("\t", "    ")
    fresh_formatter = Formatter(original_args, sys.stderr, sys.stdin, sys.stdout)
    assert formatter._do_format_code(space_source) == fresh_formatter._do_format_code(
        space_source
    )
