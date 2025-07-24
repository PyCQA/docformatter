# pylint: skip-file
# type: ignore
#
#       tests.formatter.test_do_format_docstring.py is part of the docformatter project
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
"""Module for testing the Formatter _do_format_docstring method."""


# Standard Library Imports
import contextlib
import itertools
import random
import sys

with contextlib.suppress(ImportError):
    if sys.version_info >= (3, 11):
        # Standard Library Imports
        import tomllib
    else:
        # Third Party Imports
        import tomli as tomllib

# Third Party Imports
import pytest

# docformatter Package Imports
from docformatter.format import Formatter

# docformatter Local Imports
from .. import generate_random_docstring

NO_ARGS = [""]
WRAP_DESC_72 = ["--wrap-descriptions", "72", ""]
WRAP_DESC_88 = ["--wrap-descriptions", "88", ""]
WRAP_BOTH_88 = ["--wrap-descriptions", "88", "--wrap-summaries", "88", ""]

with open("tests/_data/string_files/do_format_docstrings.toml", "rb") as f:
    TEST_STRINGS = tomllib.load(f)


@pytest.mark.integration
@pytest.mark.order(4)
@pytest.mark.parametrize(
    "test_key, args",
    [
        ("one_line", NO_ARGS),
        ("summary_end_quote", NO_ARGS),
        ("bad_indentation", ["--wrap-descriptions", "44", ""]),
        ("too_much_indentation", NO_ARGS),
        ("trailing_whitespace", ["--wrap-descriptions", "52", ""]),
        ("empty_docstring", NO_ARGS),
        ("no_summary_period", NO_ARGS),
        ("single_quotes", NO_ARGS),
        ("single_quotes_multiline", NO_ARGS),
        pytest.param(
            "skip_underlined_summary",
            NO_ARGS,
            marks=pytest.mark.skip(
                reason="LEGACY: Underlined summaries should now be processed as "
                "section headers."
            ),
        ),
        ("no_blank", NO_ARGS),
        ("presummary_newline", ["--pre-summary-newline", ""]),
        ("summary_multiline", ["--make-summary-multi-line", ""]),
        ("presummary_space", ["--pre-summary-space", ""]),
        ("quote_no_space_black", ["--black", ""]),
        ("quote_space_black", ["--black", ""]),
        ("quote_space_multiline_black", ["--black", ""]),
        ("epytext", ["--style", "epytext"] + WRAP_BOTH_88),
        ("epytext_numpy", ["--style", "numpy"] + WRAP_BOTH_88),
        ("sphinx", ["--style", "sphinx"] + WRAP_BOTH_88),
        ("sphinx_numpy", ["--style", "numpy"] + WRAP_BOTH_88),
        ("numbered_list", WRAP_DESC_72),
        ("parameter_dash", WRAP_DESC_72),
        ("parameter_colon", ["--style", "numpy"] + WRAP_DESC_72),
        ("many_short_columns", NO_ARGS),
        ("inline", WRAP_DESC_72),
        ("inline_short", WRAP_DESC_72),
        ("inline_long", WRAP_DESC_72),
        ("only_link", WRAP_DESC_72),
        ("weird_punctuation", ["--wrap-summaries", "79", ""]),
        ("description_wrap", WRAP_DESC_72),
        ("ignore_doctest", WRAP_DESC_72),
        ("ignore_summary_doctest", WRAP_DESC_72),
        ("same_indentation_doctest", WRAP_DESC_72),
        (
            "force_wrap",
            ["--wrap-descriptions", "72", "--wrap-summaries", "50", "--force-wrap", ""],
        ),
        ("summary_wrap_tab", ["--wrap-summaries", "30", "--tab-width", "4", ""]),
        (
            "one_line_wrap_newline",
            ["--wrap-summaries", "69", "--close-quotes-on-newline", ""],
        ),
        (
            "one_line_no_wrap",
            ["--wrap-summaries", "88", "--close-quotes-on-newline", ""],
        ),
        ("issue_75", WRAP_DESC_72),
        ("issue_75_2", WRAP_DESC_72),
        ("issue_75_3", WRAP_DESC_72),
        ("issue_127", ["--wrap-descriptions", "120", "--wrap-summaries", "120", ""]),
        ("issue_140", WRAP_DESC_72),
        ("issue_140_2", WRAP_DESC_72),
        ("issue_140_3", WRAP_DESC_72),
        ("issue_145", WRAP_DESC_72),
        ("issue_150", WRAP_DESC_72),
        ("issue_157", NO_ARGS),
        ("issue_157_url", WRAP_DESC_88),
        ("issue_157_2", WRAP_DESC_88),
        ("issue_157_3", WRAP_DESC_88),
        ("issue_157_4", WRAP_DESC_88),
        ("issue_157_5", WRAP_DESC_88),
        ("issue_157_6", WRAP_DESC_88),
        ("issue_157_11", WRAP_DESC_88),
        ("issue_159", WRAP_BOTH_88),
        ("issue_159", WRAP_BOTH_88),
        ("issue_180", WRAP_BOTH_88),
        ("issue_189", WRAP_DESC_72),
        ("issue_193", ["--non-cap", "eBay", "iPad", "-c", ""]),
        ("issue_199", NO_ARGS),
        ("issue_210", NO_ARGS),
        ("issue_218", NO_ARGS),
        ("issue_230", ["--style", "sphinx"] + WRAP_BOTH_88),
        ("issue_215", WRAP_BOTH_88),
        ("issue_217_222", WRAP_BOTH_88),
        ("issue_224", WRAP_BOTH_88),
        ("issue_228", WRAP_BOTH_88),
        ("issue_229", WRAP_BOTH_88),
        ("issue_229_2", WRAP_BOTH_88),
        ("issue_234", WRAP_BOTH_88),
        ("issue_235", WRAP_BOTH_88),
        ("issue_239", [""]),
        ("issue_239_sphinx", WRAP_BOTH_88),
        ("issue_245", WRAP_BOTH_88),
        ("issue_250", WRAP_BOTH_88),
        (
            "issue_253",
            [
                "--wrap-descriptions",
                "120",
                "--wrap-summaries",
                "120",
                "--pre-summary-newline",
                "--black",
                "",
            ],
        ),
        ("issue_263_sphinx", NO_ARGS),
        ("issue_263_epytext", ["-s", "epytext"] + NO_ARGS),
        ("issue_271", ["--pre-summary-newline"] + WRAP_BOTH_88),
        ("issue_259", NO_ARGS),
        ("issue_259_black", ["--black"] + NO_ARGS),
        ("issue_259_pre_summary_space", ["--pre-summary-space"] + NO_ARGS),
        ("issue_259_pre_summary_newline", ["--pre-summary-newline"] + NO_ARGS),
    ],
)
def test_do_format_docstring(test_key, test_args, args):
    uut = Formatter(
        test_args,
        sys.stderr,
        sys.stdin,
        sys.stdout,
    )

    source = TEST_STRINGS[test_key]["source"]
    expected = TEST_STRINGS[test_key]["expected"]

    if test_key == "summary_wrap_tab":
        _indentation = "\t\t"
    else:
        _indentation = "    "
    result = uut._do_format_docstring(
        _indentation,
        source,
    )
    assert result == expected, f"\nFailed {test_key}\nExpected {expected}\nGot {result}"


@pytest.mark.integration
@pytest.mark.parametrize("args", [[""]])
def test_do_format_docstring_random_with_wrap(
    test_args,
    args,
):
    uut = Formatter(
        test_args,
        sys.stderr,
        sys.stdin,
        sys.stdout,
    )

    # This function uses `random` so make sure each run of this test is
    # repeatable.
    random.seed(0)

    min_line_length = 50
    for max_length, num_indents in itertools.product(
        range(min_line_length, 100), range(20)
    ):
        indentation = " " * num_indents
        uut.args.wrap_summaries = max_length
        formatted_text = indentation + uut._do_format_docstring(
            indentation=indentation,
            docstring=generate_random_docstring(max_word_length=min_line_length // 2),
        )
        for line in formatted_text.split("\n"):
            # It is not the formatter's fault if a word is too long to
            # wrap.
            if len(line.split()) > 1:
                assert len(line) <= max_length
