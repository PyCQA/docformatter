#!/usr/bin/env python
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

"""Formats docstrings to follow PEP 257."""


from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

# Standard Library Imports
import argparse
import collections
import contextlib
import io
import locale
import os
import re
import signal
import sys
import sysconfig
import textwrap
import tokenize
from configparser import ConfigParser
from typing import List, Tuple, Union

# Third Party Imports
import untokenize

try:
    # Third Party Imports
    import tomli

    TOMLI_INSTALLED = True
except ImportError:
    TOMLI_INSTALLED = False

__version__ = "1.5.0"


if sys.version_info.major == 3:
    unicode = str


HEURISTIC_MIN_LIST_ASPECT_RATIO = 0.4

CR = "\r"
LF = "\n"
CRLF = "\r\n"
STR_QUOTE_TYPES = (
    '"""',
    "'''",
)
RAW_QUOTE_TYPES = (
    'r"""',
    'R"""',
    "r'''",
    "R'''",
)
UCODE_QUOTE_TYPES = (
    'u"""',
    'U"""',
    "u'''",
    "U'''",
)
QUOTE_TYPES = STR_QUOTE_TYPES + RAW_QUOTE_TYPES + UCODE_QUOTE_TYPES

_PYTHON_LIBS = set(sysconfig.get_paths().values())


class FormatResult(object):
    """Possible exit codes."""

    ok = 0
    error = 1
    interrupted = 2
    check_failed = 3


class Configurator:
    """Read and store all the docformatter configuration information."""

    parser = None
    """Parser object."""

    flargs_dct = {}
    """Dictionary of configuration file arguments."""

    configuration_file_lst = [
        "pyproject.toml",
        "setup.cfg",
        "tox.ini",
    ]
    """List of supported configuration files."""

    args: argparse.Namespace = None

    def __init__(self, args: List[Union[bool, int, str]]) -> None:
        """Initialize a Configurator class instance.

        Parameters
        ----------
        args : list
            Any command line arguments passed during invocation.
        """
        self.args_lst = args
        self.config_file = ""
        self.parser = argparse.ArgumentParser(
            description=__doc__,
            prog="docformatter",
        )

        try:
            self.config_file = self.args_lst[
                self.args_lst.index("--config") + 1
            ]
        except ValueError:
            for _configuration_file in self.configuration_file_lst:
                if os.path.isfile(_configuration_file):
                    self.config_file = f"./{_configuration_file}"
                    break

        if os.path.isfile(self.config_file):
            self._do_read_configuration_file()

    def do_parse_arguments(self) -> None:
        """Parse configuration file and command line arguments."""
        changes = self.parser.add_mutually_exclusive_group()
        changes.add_argument(
            "-i",
            "--in-place",
            action="store_true",
            help="make changes to files instead of printing diffs",
        )
        changes.add_argument(
            "-c",
            "--check",
            action="store_true",
            help="only check and report incorrectly formatted files",
        )
        self.parser.add_argument(
            "-r",
            "--recursive",
            action="store_true",
            default=bool(self.flargs_dct.get("recursive", False)),
            help="drill down directories recursively",
        )
        self.parser.add_argument(
            "-e",
            "--exclude",
            nargs="*",
            help="exclude directories and files by names",
        )
        self.parser.add_argument(
            "--wrap-summaries",
            default=int(self.flargs_dct.get("wrap-summaries", 79)),
            type=int,
            metavar="length",
            help="wrap long summary lines at this length; "
            "set to 0 to disable wrapping "
            "(default: %(default)s)",
        )
        self.parser.add_argument(
            "--wrap-descriptions",
            default=int(self.flargs_dct.get("wrap-descriptions", 72)),
            type=int,
            metavar="length",
            help="wrap descriptions at this length; "
            "set to 0 to disable wrapping "
            "(default: %(default)s)",
        )
        self.parser.add_argument(
            "--force-wrap",
            action="store_true",
            default=bool(self.flargs_dct.get("force-wrap", False)),
            help="force descriptions to be wrapped even if it may "
            "result in a mess (default: %(default)s)",
        )
        self.parser.add_argument(
            "--tab_width",
            type=int,
            dest="tab_width",
            metavar="width",
            default=int(self.flargs_dct.get("tab-width", 1)),
            help="tabs in indentation are this many characters when "
                 "wrapping lines (default: %(default)s)",
        )
        self.parser.add_argument(
            "--blank",
            dest="post_description_blank",
            action="store_true",
            default=bool(self.flargs_dct.get("blank", False)),
            help="add blank line after description (default: %(default)s)",
        )
        self.parser.add_argument(
            "--pre-summary-newline",
            action="store_true",
            default=bool(self.flargs_dct.get("pre-summary-newline", False)),
            help="add a newline before the summary of a multi-line docstring "
            "(default: %(default)s)",
        )
        self.parser.add_argument(
            "--pre-summary-space",
            action="store_true",
            default=bool(self.flargs_dct.get("pre-summary-space", False)),
            help="add a space after the opening triple quotes "
            "(default: %(default)s)",
        )
        self.parser.add_argument(
            "--make-summary-multi-line",
            action="store_true",
            default=bool(
                self.flargs_dct.get("make-summary-multi-line", False)
            ),
            help="add a newline before and after the summary of a one-line "
            "docstring (default: %(default)s)",
        )
        self.parser.add_argument(
            "--close-quotes-on-newline",
            action="store_true",
            default=bool(
                self.flargs_dct.get("close-quotes-on-newline", False)
            ),
            help="place closing triple quotes on a new-line when a "
            "one-line docstring wraps to two or more lines "
            "(default: %(default)s)",
        )
        self.parser.add_argument(
            "--range",
            metavar="line",
            dest="line_range",
            default=self.flargs_dct.get("range", None),
            type=int,
            nargs=2,
            help="apply docformatter to docstrings between these "
            "lines; line numbers are indexed at 1 (default: %(default)s)",
        )
        self.parser.add_argument(
            "--docstring-length",
            metavar="length",
            dest="length_range",
            default=self.flargs_dct.get("docstring-length", None),
            type=int,
            nargs=2,
            help="apply docformatter to docstrings of given length range "
            "(default: %(default)s)",
        )
        self.parser.add_argument(
            "--non-strict",
            action="store_true",
            default=bool(self.flargs_dct.get("non-strict", False)),
            help="don't strictly follow reST syntax to identify lists (see "
            "issue #67) (default: False)",
        )
        self.parser.add_argument(
            "--config", help="path to file containing docformatter options"
        )
        self.parser.add_argument(
            "--version", action="version", version=f"%(prog)s {__version__}"
        )
        self.parser.add_argument(
            "files", nargs="+", help="files to format or '-' for standard in"
        )

        self.args = self.parser.parse_args(self.args_lst[1:])

        if self.args.line_range:
            if self.args.line_range[0] <= 0:
                self.parser.error("--range must be positive numbers")
            if self.args.line_range[0] > self.args.line_range[1]:
                self.parser.error(
                    "First value of --range should be less than or equal "
                    "to the second"
                )

        if self.args.length_range:
            if self.args.length_range[0] <= 0:
                self.parser.error(
                    "--docstring-length must be positive numbers"
                )
            if self.args.length_range[0] > self.args.length_range[1]:
                self.parser.error(
                    "First value of --docstring-length should be less "
                    "than or equal to the second"
                )

    def _do_read_configuration_file(self) -> None:
        """Read docformatter options from a configuration file."""
        argfile = os.path.basename(self.config_file)
        for f in self.configuration_file_lst:
            if argfile == f:
                break

        fullpath, ext = os.path.splitext(self.config_file)
        filename = os.path.basename(fullpath)

        if ext == ".toml" and TOMLI_INSTALLED and filename == "pyproject":
            self._do_read_toml_configuration()

        if (ext == ".cfg" and filename == "setup") or (
            ext == ".ini" and filename == "tox"
        ):
            self._do_read_parser_configuration()

    def _do_read_toml_configuration(self) -> None:
        """Load configuration information from a *.toml file."""
        with open(self.config_file, "rb") as f:
            config = tomli.load(f)

        result = config.get("tool", {}).get("docformatter", None)
        if result is not None:
            self.flargs_dct = {
                k: v if isinstance(v, list) else str(v)
                for k, v in result.items()
            }

    def _do_read_parser_configuration(self) -> None:
        """Load configuration information from a *.cfg or *.ini file."""
        config = ConfigParser()
        config.read(self.config_file)

        for _section in ["tool:docformatter", "docformatter"]:
            if _section in config.sections():
                self.flargs_dct = {
                    k: v if isinstance(v, list) else str(v)
                    for k, v in config[_section].items()
                }


def has_correct_length(length_range, start, end):
    """Return True if docstring's length is in range."""
    if length_range is None:
        return True
    min_length, max_length = length_range

    docstring_length = end + 1 - start
    return min_length <= docstring_length <= max_length


def is_in_range(line_range, start, end):
    """Return True if start/end is in line_range."""
    if line_range is None:
        return True
    return any(
        line_range[0] <= line_no <= line_range[1]
        for line_no in range(start, end + 1)
    )


def reindent(text, indentation):
    """Return reindented text that matches indentation."""
    if "\t" not in indentation:
        text = text.expandtabs()

    text = textwrap.dedent(text)

    return (
        "\n".join(
            [(indentation + line).rstrip() for line in text.splitlines()]
        ).rstrip()
        + "\n"
    )


def _find_shortest_indentation(lines):
    """Return shortest indentation."""
    assert not isinstance(lines, str)

    indentation = None

    for line in lines:
        if line.strip():
            non_whitespace_index = len(line) - len(line.lstrip())
            _indent = line[:non_whitespace_index]
            if indentation is None or len(_indent) < len(indentation):
                indentation = _indent

    return indentation or ""


def format_code(source, **kwargs):
    """Return source code with docstrings formatted.

    Wrap summary lines if summary_wrap_length is greater than 0.

    See "_format_code()" for parameters.
    """
    try:
        original_newline = find_newline(source.splitlines(True))
        code = _format_code(source, **kwargs)

        return normalize_line_endings(code.splitlines(True), original_newline)
    except (tokenize.TokenError, IndentationError):
        return source


def _format_code(
    source,
    summary_wrap_length=79,
    description_wrap_length=72,
    force_wrap=False,
    tab_width=1,
    pre_summary_newline=False,
    pre_summary_space=False,
    make_summary_multi_line=False,
    close_quotes_on_newline=False,
    post_description_blank=False,

    line_range=None,
    length_range=None,
    strict=True,
):
    """Return source code with docstrings formatted."""
    if not source:
        return source

    if line_range is not None:
        assert line_range[0] > 0 and line_range[1] > 0

    if length_range is not None:
        assert length_range[0] > 0 and length_range[1] > 0

    modified_tokens = []

    sio = io.StringIO(source)
    previous_token_string = ""
    previous_token_type = None
    only_comments_so_far = True

    for (
        token_type,
        token_string,
        start,
        end,
        line,
    ) in tokenize.generate_tokens(sio.readline):
        if (
            token_type == tokenize.STRING
            and token_string.startswith(QUOTE_TYPES)
            and (
                previous_token_type == tokenize.INDENT or only_comments_so_far
            )
            and is_in_range(line_range, start[0], end[0])
            and has_correct_length(length_range, start[0], end[0])
        ):
            indentation = "" if only_comments_so_far else previous_token_string

            token_string = format_docstring(
                indentation,
                token_string,
                summary_wrap_length=summary_wrap_length,
                description_wrap_length=description_wrap_length,
                force_wrap=force_wrap,
                tab_width=tab_width,
                pre_summary_newline=pre_summary_newline,
                pre_summary_space=pre_summary_space,
                make_summary_multi_line=make_summary_multi_line,
                close_quotes_on_newline=close_quotes_on_newline,
                post_description_blank=post_description_blank,
                strict=strict,
            )

        if token_type not in [tokenize.COMMENT, tokenize.NEWLINE, tokenize.NL]:
            only_comments_so_far = False

        previous_token_string = token_string
        previous_token_type = token_type

        # If the current token is a newline, the previous token was a
        # newline or a comment, and these two sequential newlines follow a
        # function definition, ignore the blank line.
        if (
            len(modified_tokens) <= 2
            or token_type not in {tokenize.NL, tokenize.NEWLINE}
            or modified_tokens[-1][0] not in {tokenize.NL, tokenize.NEWLINE}
            or modified_tokens[-2][1] != ":"
            and modified_tokens[-2][0] != tokenize.COMMENT
            or modified_tokens[-2][4][:3] != "def"
        ):
            modified_tokens.append(
                (token_type, token_string, start, end, line)
            )

    return untokenize.untokenize(modified_tokens)


def format_docstring(
    indentation,
    docstring,
    summary_wrap_length=0,
    description_wrap_length=0,
    force_wrap=False,
    tab_width=1,
    pre_summary_newline=False,
    pre_summary_space=False,
    make_summary_multi_line=False,
    close_quotes_on_newline=False,
    post_description_blank=False,
    strict=True,
):
    """Return formatted version of docstring.

    Wrap summary lines if summary_wrap_length is greater than 0.

    Relevant parts of PEP 257:
        - For consistency, always use triple double quotes around docstrings.
        - Triple quotes are used even though the string fits on one line.
        - Multi-line docstrings consist of a summary line just like a one-line
          docstring, followed by a blank line, followed by a more elaborate
          description.
        - Unless the entire docstring fits on a line, place the closing quotes
          on a line by themselves.
    """
    contents, open_quote = strip_docstring(docstring)
    open_quote = f"{open_quote} " if pre_summary_space else open_quote

    # Skip if there are nested triple double quotes
    if contents.count(QUOTE_TYPES[0]):
        return docstring

    # Do not modify things that start with doctests.
    if contents.lstrip().startswith(">>>"):
        return docstring

    summary, description = split_summary_and_description(contents)

    # Leave docstrings with underlined summaries alone.
    if remove_section_header(description).strip() != description.strip():
        return docstring

    if not force_wrap and is_some_sort_of_list(summary, strict):
        # Something is probably not right with the splitting.
        return docstring

    # Compensate for textwrap counting each tab in indentation as 1 character.
    tab_compensation = indentation.count('\t') * (tab_width - 1)
    summary_wrap_length -= tab_compensation
    description_wrap_length -= tab_compensation

    if description:
        # Compensate for triple quotes by temporarily prepending 3 spaces.
        # This temporary prepending is undone below.
        initial_indent = (
            indentation if pre_summary_newline else 3 * " " + indentation
        )
        pre_summary = "\n" + indentation if pre_summary_newline else ""
        summary = wrap_summary(
            normalize_summary(summary),
            wrap_length=summary_wrap_length,
            initial_indent=initial_indent,
            subsequent_indent=indentation,
        ).lstrip()
        description = wrap_description(
            description,
            indentation=indentation,
            wrap_length=description_wrap_length,
            force_wrap=force_wrap,
            strict=strict,
        )
        post_description = "\n" if post_description_blank else ""
        return f'''\
{open_quote}{pre_summary}{summary}

{description}{post_description}
{indentation}"""\
'''
    else:
        if not make_summary_multi_line:
            summary_wrapped = wrap_summary(
                open_quote + normalize_summary(contents) + '"""',
                wrap_length=summary_wrap_length,
                initial_indent=indentation,
                subsequent_indent=indentation,
            ).strip()
            if close_quotes_on_newline and "\n" in summary_wrapped:
                summary_wrapped = (
                    f"{summary_wrapped[:-3]}"
                    f"\n{indentation}"
                    f"{summary_wrapped[-3:]}"
                )
            return summary_wrapped
        else:
            beginning = f"{open_quote}\n{indentation}"
            ending = f'\n{indentation}"""'
            summary_wrapped = wrap_summary(
                normalize_summary(contents),
                wrap_length=summary_wrap_length,
                initial_indent=indentation,
                subsequent_indent=indentation,
            ).strip()
            return f"{beginning}{summary_wrapped}{ending}"


def is_probably_beginning_of_sentence(line):
    """Return True if this line begins a new sentence."""
    # Check heuristically for a parameter list.
    for token in ["@", "-", r"\*"]:
        if re.search(r"\s" + token + r"\s", line):
            return True

    stripped_line = line.strip()
    is_beginning_of_sentence = re.match(r'[^\w"\'`\(\)]', stripped_line)
    is_pydoc_ref = re.match(r"^:\w+:", stripped_line)

    return is_beginning_of_sentence and not is_pydoc_ref


def split_summary_and_description(contents):
    """Split docstring into summary and description.

    Return tuple (summary, description).
    """
    split_lines = contents.rstrip().splitlines()

    for index in range(1, len(split_lines)):
        found = False

        # Empty line separation would indicate the rest is the description or,
        # symbol on second line probably is a description with a list.
        if not split_lines[index].strip() or is_probably_beginning_of_sentence(
            split_lines[index]
        ):
            found = True

        if found:
            return (
                "\n".join(split_lines[:index]).strip(),
                "\n".join(split_lines[index:]).rstrip(),
            )

    # Break on first sentence.
    split = split_first_sentence(contents)
    if split[0].strip() and split[1].strip():
        return (
            split[0].strip(),
            _find_shortest_indentation(split[1].splitlines()[1:])
            + split[1].strip(),
        )

    return contents, ""


def split_first_sentence(text):
    """Split text into first sentence and the rest.

    Return a tuple (sentence, rest).
    """
    sentence = ""
    rest = text
    delimiter = ""
    previous_delimiter = ""

    while rest:
        split = re.split(r"(\s)", rest, maxsplit=1)
        word = split[0]
        if len(split) == 3:
            delimiter = split[1]
            rest = split[2]
        else:
            assert len(split) == 1
            delimiter = ""
            rest = ""

        sentence += previous_delimiter + word

        if sentence.endswith(("e.g.", "i.e.", "Dr.", "Mr.", "Mrs.", "Ms.")):
            # Ignore false end of sentence.
            pass
        elif sentence.endswith((".", "?", "!")):
            break
        elif sentence.endswith(":") and delimiter == "\n":
            # Break on colon if it ends the line. This is a heuristic to detect
            # the beginning of some parameter list afterwards.
            break

        previous_delimiter = delimiter
        delimiter = ""

    return sentence, delimiter + rest


def is_some_sort_of_list(text, strict):
    """Return True if text looks like a list."""
    split_lines = text.rstrip().splitlines()

    # TODO: Find a better way of doing this.
    # Very large number of lines but short columns probably means a list of
    # items.
    if (
        len(split_lines)
        / max([len(line.strip()) for line in split_lines] + [1])
        > HEURISTIC_MIN_LIST_ASPECT_RATIO
    ) and not strict:
        return True

    return any(
        (
            re.match(r"\s*$", line)
            or
            # "1. item"
            re.match(r"\s*\d\.", line)
            or
            # "@parameter"
            re.match(r"\s*[\-*:=@]", line)
            or
            # "parameter - description"
            re.match(r".*\s+[\-*:=@]\s+", line)
            or
            # "parameter: description"
            re.match(r"\s*\S+[\-*:=@]\s+", line)
            or
            # "parameter:\n    description"
            re.match(r"\s*\S+:\s*$", line)
            or
            # "parameter -- description"
            re.match(r"\s*\S+\s+--\s+", line)
        )
        for line in split_lines
    )


def is_some_sort_of_code(text):
    """Return True if text looks like code."""
    return any(len(word) > 50 for word in text.split())


def find_newline(source):
    """Return type of newline used in source.

    Input is a list of lines.
    """
    assert not isinstance(source, unicode)

    counter = collections.defaultdict(int)
    for line in source:
        if line.endswith(CRLF):
            counter[CRLF] += 1
        elif line.endswith(CR):
            counter[CR] += 1
        elif line.endswith(LF):
            counter[LF] += 1
    return (sorted(counter, key=counter.get, reverse=True) or [LF])[0]


def normalize_line(line, newline):
    """Return line with fixed ending, if ending was present in line.

    Otherwise, does nothing.
    """
    stripped = line.rstrip("\n\r")
    return stripped + newline if stripped != line else line


def normalize_line_endings(lines, newline):
    """Return fixed line endings.

    All lines will be modified to use the most common line ending.
    """
    return "".join([normalize_line(line, newline) for line in lines])


def strip_docstring(docstring: str) -> Tuple[str, str]:
    """Return contents of docstring and opening quote type.

    Strips the docstring of its triple quotes, trailing white space,
    and line returns.  Determines type of docstring quote (either string,
    raw, or unicode) and returns the opening quotes, including the type
    identifier, with single quotes replaced by double quotes.

    Parameters
    ----------
    docstring: str
        The docstring, including the opening and closing triple quotes.

    Returns
    -------
    (docstring, open_quote) : tuple
        The docstring with the triple quotes removed.
        The opening quote type with single quotes replaced by double quotes.
    """
    docstring = docstring.strip()

    for quote in QUOTE_TYPES:
        if quote in RAW_QUOTE_TYPES + UCODE_QUOTE_TYPES and (
            docstring.startswith(quote) and docstring.endswith(quote[1:])
        ):
            return docstring.split(quote, 1)[1].rsplit(quote[1:], 1)[
                0
            ].strip(), quote.replace("'", '"')
        elif docstring.startswith(quote) and docstring.endswith(quote):
            return docstring.split(quote, 1)[1].rsplit(quote, 1)[
                0
            ].strip(), quote.replace("'", '"')

    raise ValueError(
        "docformatter only handles triple-quoted (single or double) strings"
    )


def unwrap_summary(summary):
    """Return summary with newlines removed in preparation for wrapping."""
    return re.sub(r"\s*\n\s*", " ", summary)


def normalize_summary(summary):
    """Return normalized docstring summary."""
    # remove trailing whitespace
    summary = summary.rstrip()

    # Add period at end of sentence
    if (
        summary
        and (summary[-1].isalnum() or summary[-1] in ['"', "'"])
        and (not summary.startswith("#"))
    ):
        summary += "."

    return summary


def wrap_summary(summary, initial_indent, subsequent_indent, wrap_length):
    """Return line-wrapped summary text."""
    if wrap_length > 0:
        return textwrap.fill(
            unwrap_summary(summary),
            width=wrap_length,
            initial_indent=initial_indent,
            subsequent_indent=subsequent_indent,
        ).strip()
    else:
        return summary


def wrap_description(text, indentation, wrap_length, force_wrap, strict):
    """Return line-wrapped description text.

    We only wrap simple descriptions. We leave doctests, multi-paragraph
    text, and bulleted lists alone.
    """
    text = strip_leading_blank_lines(text)

    # Do not modify doctests at all.
    if ">>>" in text:
        return text

    text = reindent(text, indentation).rstrip()

    # Ignore possibly complicated cases.
    if wrap_length <= 0 or (
        not force_wrap
        and (is_some_sort_of_list(text, strict) or is_some_sort_of_code(text))
    ):
        return text

    return (
        indentation
        + "\n".join(
            textwrap.wrap(
                textwrap.dedent(text),
                width=wrap_length,
                initial_indent=indentation,
                subsequent_indent=indentation,
            )
        ).strip()
    )


def remove_section_header(text):
    r"""Return text with section header removed.

    >>> remove_section_header('----\nfoo\nbar\n')
    'foo\nbar\n'

    >>> remove_section_header('===\nfoo\nbar\n')
    'foo\nbar\n'
    """
    stripped = text.lstrip()
    if not stripped:
        return text

    first = stripped[0]
    return (
        text
        if (
            first.isalnum()
            or first.isspace()
            or stripped.splitlines()[0].strip(first).strip()
        )
        else stripped.lstrip(first).lstrip()
    )


def strip_leading_blank_lines(text):
    """Return text with leading blank lines removed."""
    split = text.splitlines()

    found = next(
        (index for index, line in enumerate(split) if line.strip()), 0
    )

    return "\n".join(split[found:])


def open_with_encoding(filename, encoding, mode="r"):
    """Return opened file with a specific encoding."""
    return io.open(
        filename, mode=mode, encoding=encoding, newline=""
    )  # Preserve line endings


def detect_encoding(filename):
    """Return file encoding."""
    try:
        with open(filename, "rb") as input_file:
            # Standard Library Imports
            from lib2to3.pgen2 import tokenize as lib2to3_tokenize

            encoding = lib2to3_tokenize.detect_encoding(input_file.readline)[0]

            # Check for correctness of encoding.
            with open_with_encoding(filename, encoding) as check_file:
                check_file.read()
        return encoding
    except (SyntaxError, LookupError, UnicodeDecodeError):
        return "latin-1"


def format_file(filename, args, standard_out):
    """Run format_code() on a file.

    Return: one of the FormatResult codes.
    """
    encoding = detect_encoding(filename)
    with open_with_encoding(filename, encoding=encoding) as input_file:
        source = input_file.read()
        formatted_source = _format_code_with_args(source, args)

    if source != formatted_source:
        if args.check:
            return FormatResult.check_failed
        elif args.in_place:
            with open_with_encoding(
                filename, mode="w", encoding=encoding
            ) as output_file:
                output_file.write(formatted_source)
        else:
            # Standard Library Imports
            import difflib

            diff = difflib.unified_diff(
                source.splitlines(),
                formatted_source.splitlines(),
                f"before/{filename}",
                f"after/{filename}",
                lineterm="",
            )
            standard_out.write("\n".join(list(diff) + [""]))

    return FormatResult.ok


def _format_code_with_args(source, args):
    """Run format_code with parsed command-line arguments."""
    return format_code(
        source,
        summary_wrap_length=args.wrap_summaries,
        description_wrap_length=args.wrap_descriptions,
        force_wrap=args.force_wrap,
        tab_width=args.tab_width,
        pre_summary_newline=args.pre_summary_newline,
        pre_summary_space=args.pre_summary_space,
        make_summary_multi_line=args.make_summary_multi_line,
        close_quotes_on_newline=args.close_quotes_on_newline,
        post_description_blank=args.post_description_blank,
        line_range=args.line_range,
        strict=not args.non_strict,
    )


def _main(argv, standard_out, standard_error, standard_in):
    """Run internal main entry point."""
    configurator = Configurator(argv)
    configurator.do_parse_arguments()

    if "-" in configurator.args.files:
        _format_standard_in(
            configurator.args,
            parser=configurator.parser,
            standard_out=standard_out,
            standard_in=standard_in,
        )
    else:
        return _format_files(
            configurator.args,
            standard_out=standard_out,
            standard_error=standard_error,
        )


def _format_standard_in(args, parser, standard_out, standard_in):
    """Print formatted text to standard out."""
    if len(args.files) > 1:
        parser.error("cannot mix standard in and regular files")

    if args.in_place:
        parser.error("--in-place cannot be used with standard input")

    if args.recursive:
        parser.error("--recursive cannot be used with standard input")

    encoding = None
    source = standard_in.read()
    if not isinstance(source, unicode):
        encoding = standard_in.encoding or _get_encoding()
        source = source.decode(encoding)

    formatted_source = _format_code_with_args(source, args=args)

    if encoding:
        formatted_source = formatted_source.encode(encoding)

    standard_out.write(formatted_source)


def _get_encoding():
    """Return preferred encoding."""
    return locale.getpreferredencoding() or sys.getdefaultencoding()


def find_py_files(sources, recursive, exclude=None):
    """Find Python source files.

    Parameters
        - sources: iterable with paths as strings.
        - recursive: drill down directories if True.
        - exclude: string based on which directories and files are excluded.

    Return: yields paths to found files.
    """

    def not_hidden(name):
        """Return True if file 'name' isn't .hidden."""
        return not name.startswith(".")

    def is_excluded(name, exclude):
        """Return True if file 'name' is excluded."""
        return (
            any(
                re.search(re.escape(str(e)), name, re.IGNORECASE)
                for e in exclude
            )
            if exclude
            else False
        )

    for name in sorted(sources):
        if recursive and os.path.isdir(name):
            for root, dirs, children in os.walk(unicode(name)):
                dirs[:] = [
                    d
                    for d in dirs
                    if not_hidden(d) and not is_excluded(d, _PYTHON_LIBS)
                ]
                dirs[:] = sorted(
                    [d for d in dirs if not is_excluded(d, exclude)]
                )
                files = sorted(
                    [
                        f
                        for f in children
                        if not_hidden(f) and not is_excluded(f, exclude)
                    ]
                )
                for filename in files:
                    if filename.endswith(".py") and not is_excluded(
                        root, exclude
                    ):
                        yield os.path.join(root, filename)
        else:
            yield name


def _format_files(args, standard_out, standard_error):
    """Format multiple files.

    Return: one of the FormatResult codes.
    """
    outcomes = collections.Counter()
    for filename in find_py_files(
        set(args.files), args.recursive, args.exclude
    ):
        try:
            result = format_file(
                filename, args=args, standard_out=standard_out
            )
            outcomes[result] += 1
            if result == FormatResult.check_failed:
                print(unicode(filename), file=standard_error)
        except IOError as exception:
            outcomes[FormatResult.error] += 1
            print(unicode(exception), file=standard_error)

    return_codes = [  # in order of preference
        FormatResult.error,
        FormatResult.check_failed,
        FormatResult.ok,
    ]

    for code in return_codes:
        if outcomes[code]:
            return code


def main():
    """Run main entry point."""
    # SIGPIPE is not available on Windows.
    with contextlib.suppress(AttributeError):
        # Exit on broken pipe.
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    try:
        return _main(
            sys.argv,
            standard_out=sys.stdout,
            standard_error=sys.stderr,
            standard_in=sys.stdin,
        )
    except KeyboardInterrupt:  # pragma: no cover
        return FormatResult.interrupted  # pragma: no cover


if __name__ == "__main__":
    sys.exit(main())
