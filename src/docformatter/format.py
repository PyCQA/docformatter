#!/usr/bin/env python
#
# Copyright (C) 2012-2022 Steven Myint
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
"""This module provides docformatter's Formattor class."""

# Standard Library Imports
import argparse
import collections
import io
import tokenize
from typing import TextIO, Tuple

# Third Party Imports
import untokenize

# docformatter Package Imports
import docformatter.strings as _strings
import docformatter.syntax as _syntax
import docformatter.util as _util
import docformatter.encode as _encode


unicode = str


class FormatResult:
    """Possible exit codes."""

    ok = 0
    error = 1
    interrupted = 2
    check_failed = 3


class Formatter:
    """Format docstrings."""

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

    parser = None
    """Parser object."""

    args: argparse.Namespace = None

    def __init__(
        self,
        args: argparse.Namespace,
        stderror: TextIO,
        stdin: TextIO,
        stdout: TextIO,
    ) -> None:
        """Initialize a Formattor instance.

        Parameters
        ----------
        args : argparse.Namespace
            Any command line arguments passed during invocation or
            configuration file options.
        stderror : TextIO
            The standard error device.  Typically, the screen.
        stdin :  TextIO
            The standard input device.  Typically, the keyboard.
        stdout : TextIO
            The standard output device.  Typically, the screen.

        Returns
        -------
        object
        """
        self.args = args
        self.stderror: TextIO = stderror
        self.stdin: TextIO = stdin
        self.stdout: TextIO = stdout

        self.encodor = _encode.Encoder()

    def do_format_standard_in(self, parser: argparse.ArgumentParser):
        """Print formatted text to standard out.

        Parameters
        ----------
        parser: argparse.ArgumentParser
            The argument parser containing the formatting options.
        """
        if len(self.args.files) > 1:
            parser.error("cannot mix standard in and regular files")

        if self.args.in_place:
            parser.error("--in-place cannot be used with standard input")

        if self.args.recursive:
            parser.error("--recursive cannot be used with standard input")

        encoding = None
        source = self.stdin.read()
        if not isinstance(source, unicode):
            encoding = self.stdin.encoding or self.encodor.system_encoding
            source = source.decode(encoding)

        formatted_source = self._do_format_code(source)

        if encoding:
            formatted_source = formatted_source.encode(encoding)

        self.stdout.write(formatted_source)

    def do_format_files(self):
        """Format multiple files.

        Return
        ------
        code: int
            One of the FormatResult codes.
        """
        outcomes = collections.Counter()
        for filename in _util.find_py_files(
            set(self.args.files), self.args.recursive, self.args.exclude
        ):
            try:
                result = self._do_format_file(filename)
                outcomes[result] += 1
            except IOError as exception:
                outcomes[FormatResult.error] += 1
                print(unicode(exception), file=self.stderror)

        return_codes = [  # in order of preference
            FormatResult.error,
            FormatResult.check_failed,
            FormatResult.ok,
        ]

        for code in return_codes:
            if outcomes[code]:
                return code

    def _do_format_file(self, filename):
        """Run format_code() on a file.

        Parameters
        ----------
        filename: str
            The path to the file to be formatted.

        Return
        ------
        result_code: int
            One of the FormatResult codes.
        """
        self.encodor.do_detect_encoding(filename)

        with self.encodor.do_open_with_encoding(filename) as input_file:
            source = input_file.read()
            formatted_source = self._do_format_code(source)

        ret = FormatResult.ok
        show_diff = self.args.diff

        if source != formatted_source:
            if self.args.check:
                print(unicode(filename), file=self.stderror)
                ret = FormatResult.check_failed
            elif self.args.in_place:
                with self.encodor.do_open_with_encoding(
                    filename,
                    mode="w",
                ) as output_file:
                    output_file.write(formatted_source)
            else:
                show_diff = True

            if show_diff:
                # Standard Library Imports
                import difflib

                diff = difflib.unified_diff(
                    source.splitlines(),
                    formatted_source.splitlines(),
                    f"before/{filename}",
                    f"after/{filename}",
                    lineterm="",
                )
                self.stdout.write("\n".join(list(diff) + [""]))

        return ret

    def _do_format_code(self, source):
        """Return source code with docstrings formatted.

        Parameters
        ----------
        source: str
            The text from the source file.
        """
        try:
            original_newline = self.encodor.do_find_newline(
                source.splitlines(True)
            )
            code = self._format_code(source)

            return _strings.normalize_line_endings(
                code.splitlines(True), original_newline
            )
        except (tokenize.TokenError, IndentationError):
            return source

    def _format_code(
        self,
        source,
    ):
        """Return source code with docstrings formatted.

        Parameters
        ----------
        source: str
            The source code string.

        Returns
        -------
        formatted_source: str
            The source code with formatted docstrings.
        """
        if not source:
            return source

        if self.args.line_range is not None:
            assert self.args.line_range[0] > 0 and self.args.line_range[1] > 0

        if self.args.length_range is not None:
            assert (
                self.args.length_range[0] > 0 and self.args.length_range[1] > 0
            )

        modified_tokens = []

        sio = io.StringIO(source)
        previous_token_type = None
        only_comments_so_far = True

        try:
            for (
                token_type,
                token_string,
                start,
                end,
                line,
            ) in tokenize.generate_tokens(sio.readline):
                if (
                    token_type == tokenize.STRING
                    and token_string.startswith(self.QUOTE_TYPES)
                    and (
                        previous_token_type == tokenize.INDENT
                        or previous_token_type == tokenize.NEWLINE
                        or only_comments_so_far
                    )
                    and _util.is_in_range(
                        self.args.line_range, start[0], end[0]
                    )
                    and _util.has_correct_length(
                        self.args.length_range, start[0], end[0]
                    )
                ):
                    indentation = " " * (len(line) - len(line.lstrip()))
                    token_string = self._do_format_docstring(
                        indentation,
                        token_string,
                    )

                if token_type not in [
                    tokenize.COMMENT,
                    tokenize.NEWLINE,
                    tokenize.NL,
                ]:
                    only_comments_so_far = False

                previous_token_type = token_type

                # If the current token is a newline, the previous token was a
                # newline or a comment, and these two sequential newlines
                # follow a function definition, ignore the blank line.
                if (
                    len(modified_tokens) <= 2
                    or token_type not in {tokenize.NL, tokenize.NEWLINE}
                    or modified_tokens[-1][0]
                    not in {tokenize.NL, tokenize.NEWLINE}
                    or modified_tokens[-2][1] != ":"
                    and modified_tokens[-2][0] != tokenize.COMMENT
                    or not modified_tokens[-2][4]
                    .lstrip()
                    .startswith(("def", "class"))
                ):
                    modified_tokens.append(
                        (token_type, token_string, start, end, line)
                    )

            return untokenize.untokenize(modified_tokens)
        except tokenize.TokenError:
            return source

    def _do_format_docstring(
        self,
        indentation: str,
        docstring: str,
    ) -> str:
        """Return formatted version of docstring.

        Parameters
        ----------
        indentation: str
            The indentation characters for the docstring.
        docstring: str
            The docstring itself.

        Returns
        -------
        docstring_formatted: str
            The docstring formatted according the various options.
        """
        contents, open_quote = self._do_strip_docstring(docstring)
        open_quote = (
            f"{open_quote} " if self.args.pre_summary_space else open_quote
        )

        # Skip if there are nested triple double quotes
        if contents.count(self.QUOTE_TYPES[0]):
            return docstring

        # Do not modify things that start with doctests.
        if contents.lstrip().startswith(">>>"):
            return docstring

        summary, description = _strings.split_summary_and_description(contents)

        # Leave docstrings with underlined summaries alone.
        if (
            _syntax.remove_section_header(description).strip()
            != description.strip()
        ):
            return docstring

        if not self.args.force_wrap and _syntax.is_some_sort_of_list(
            summary,
            self.args.non_strict,
        ):
            # Something is probably not right with the splitting.
            return docstring

        # Compensate for textwrap counting each tab in indentation as 1
        # character.
        tab_compensation = indentation.count("\t") * (self.args.tab_width - 1)
        self.args.wrap_summaries -= tab_compensation
        self.args.wrap_descriptions -= tab_compensation

        if description:
            # Compensate for triple quotes by temporarily prepending 3 spaces.
            # This temporary prepending is undone below.
            initial_indent = (
                indentation
                if self.args.pre_summary_newline
                else 3 * " " + indentation
            )
            pre_summary = (
                "\n" + indentation if self.args.pre_summary_newline else ""
            )
            summary = _syntax.wrap_summary(
                _strings.normalize_summary(summary),
                wrap_length=self.args.wrap_summaries,
                initial_indent=initial_indent,
                subsequent_indent=indentation,
            ).lstrip()
            description = _syntax.wrap_description(
                description,
                indentation=indentation,
                wrap_length=self.args.wrap_descriptions,
                force_wrap=self.args.force_wrap,
                strict=self.args.non_strict,
            )
            post_description = "\n" if self.args.post_description_blank else ""
            return f'''\
{open_quote}{pre_summary}{summary}

{description}{post_description}
{indentation}"""\
'''
        else:
            if not self.args.make_summary_multi_line:
                summary_wrapped = _syntax.wrap_summary(
                    open_quote + _strings.normalize_summary(contents) + '"""',
                    wrap_length=self.args.wrap_summaries,
                    initial_indent=indentation,
                    subsequent_indent=indentation,
                ).strip()
                if (
                    self.args.close_quotes_on_newline
                    and "\n" in summary_wrapped
                ):
                    summary_wrapped = (
                        f"{summary_wrapped[:-3]}"
                        f"\n{indentation}"
                        f"{summary_wrapped[-3:]}"
                    )
                return summary_wrapped
            else:
                beginning = f"{open_quote}\n{indentation}"
                ending = f'\n{indentation}"""'
                summary_wrapped = _syntax.wrap_summary(
                    _strings.normalize_summary(contents),
                    wrap_length=self.args.wrap_summaries,
                    initial_indent=indentation,
                    subsequent_indent=indentation,
                ).strip()
                return f"{beginning}{summary_wrapped}{ending}"

    def _do_strip_docstring(self, docstring: str) -> Tuple[str, str]:
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
            The opening quote type with single quotes replaced by double
            quotes.
        """
        docstring = docstring.strip()

        for quote in self.QUOTE_TYPES:
            if quote in self.RAW_QUOTE_TYPES + self.UCODE_QUOTE_TYPES and (
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
            "docformatter only handles triple-quoted (single or double) "
            "strings"
        )
