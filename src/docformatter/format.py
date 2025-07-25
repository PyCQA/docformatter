#!/usr/bin/env python
#
#       docformatter.format.py is part of the docformatter project
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
"""This module provides docformatter's Formattor class."""


# Standard Library Imports
import argparse
import collections
import contextlib
import difflib
import io
import tokenize
from typing import TextIO, Union

# docformatter Package Imports
import docformatter.classify as _classify
import docformatter.encode as _encode
import docformatter.patterns as _patterns
import docformatter.strings as _strings
import docformatter.util as _util
import docformatter.wrappers as _wrappers
from docformatter.constants import QUOTE_TYPES

unicode = str


def _do_remove_preceding_blank_lines(
    tokens: list[tokenize.TokenInfo],
    blocks: list[tuple[int, int, str]],
) -> list[tokenize.TokenInfo]:
    """Remove all blank lines preceding a docstring.

    docformatter_6.8: No blank lines before a class docstring.
    docformatter_8.3: No blank lines before a module docstring.
    docformatter_8.3: One blank line before a module docstring if the docstring
    follows immediately after a shebang line.
    docformatter_9.9: No blank lines before a function or method docstring.
    docformatter_12.2: No blank lines before an attribute docstring.

    Parameters
    ----------
    tokens : list
        A list of tokens from the source code.
    blocks : list
        A list of tuples containing the index of any docstrings and the docstring type.

    Returns
    -------
    tokens : list
        A list of tokens with blank lines preceding docstrings removed.
    """
    _num_tokens = len(tokens)
    _indices_to_remove = []

    for i in range(_num_tokens):
        match = next(((s, d, t) for (s, d, t) in blocks if d == i), None)
        if match:
            s, d, typ = match
            for j in range(d - 1, 0, -1):
                # Break out of loop once we reach a class, function, method, or
                # attribute.  No more blank lines should be removed once we get to the
                # structure the docstring is associated with.
                if (
                    tokens[j].type == tokenize.NAME
                    and tokens[j].string in ("class", "def", "async")
                ) or (tokens[j].type == tokenize.OP and tokens[j].string in ("=", ":")):
                    break
                elif (
                    tokens[j].type in (tokenize.NEWLINE, tokenize.NL)
                    and tokens[j].line == "\n"
                    and not tokens[j - 1].line.startswith("#!/")
                ):
                    _indices_to_remove.append(j)

    # We need to go in reverse order to prevent the token list indices from
    # getting out of whack.  For example, if _indices_to_remove = [5, 21] and we
    # removed index 5 first, then old index 22 would become the new index 21 and
    # the next iteration of the loop would remove the wrong token.
    _indices_to_remove.sort(reverse=True)

    # Loop through the token indices in reverse order and remove them from the token
    # line.
    for i in _indices_to_remove:
        tokens.pop(i)

    return tokens


def _do_update_token_indices(
    tokens: list[tokenize.TokenInfo],
) -> list[tokenize.TokenInfo]:
    """Update the indices of tokens after a newline that is to be removed.

    When a newline before a docstring is removed, the indices of all following tokens
    must be updated to reflect the missing newline.

    Parameters
    ----------
    tokens : list
        A list of tokens from the source code.

    Returns
    -------
    list
        The updated list of tokens.
    """
    _end_row = tokens[0].end[0]
    _end_col = tokens[0].end[1]
    _num_tokens = len(tokens)

    for i in range(1, _num_tokens):
        _num_rows, _num_cols = _get_num_rows_columns(tokens[i])

        # If the current token line is the same as the preceding token line,
        # the starting row for the current token should be the same as the ending
        # line for the previous token unless both lines are NEWLINES.
        if tokens[i].line == tokens[i - 1].line and tokens[i - 1].type not in (
            tokenize.NEWLINE,
            tokenize.NL,
        ):
            _start_idx, _end_idx = _get_start_end_indices(
                tokens[i],
                tokens[i - 1],
                _num_rows,
                _num_cols,
            )

            tokens[i] = tokens[i]._replace(start=_start_idx)
            tokens[i] = tokens[i]._replace(end=_end_idx)
            if tokens[i].type in (tokenize.NEWLINE, tokenize.NL) and tokens[
                i - 1
            ].type in (tokenize.NEWLINE, tokenize.NL):
                tokens[i] = tokens[i]._replace(start=(_end_idx[0], tokens[i].start[1]))
        # If the current token line is different from the preceding token line,
        # the current token starting row should be one greater than the previous
        # token's end row.
        else:
            _start_idx, _end_idx = _get_unmatched_start_end_indices(
                tokens[i],
                tokens[i - 1],
                _num_rows,
            )

            tokens[i] = tokens[i]._replace(start=_start_idx)
            tokens[i] = tokens[i]._replace(end=_end_idx)

    return tokens


def _get_attribute_docstring_newlines(
    tokens: list[tokenize.TokenInfo],
    index: int,
) -> int:
    """Return number of newlines after an attribute docstring.

    docformatter_12.1: One blank line after an attribute docstring.
    docformatter_12.1.1: Two blank lines if followed by top-level class or function
                         definition.

    Parameters
    ----------
    tokens : list
        A list of tokens from the source code.
    index : int
        The index of the docstring token in the list of tokens.

    Returns
    -------
    newlines : int
        The number of newlines to insert after the docstring.
    """
    _num_tokens = len(tokens)
    _offset = 2

    for i in range(index + 2, _num_tokens - index - 1):
        if tokens[i].line == "\n":
            _offset += 1
        else:
            break

    if tokens[index + _offset].line.startswith("class") or tokens[
        index + _offset
    ].line.startswith("def"):
        return 2

    return 1


def _get_class_docstring_newlines(
    tokens: list[tokenize.TokenInfo],
    index: int,
) -> int:
    """Return number of newlines after a class docstring.

    PEP_257_6.1: One blank line after a class docstring.
    docformatter_6.9: Keep in-line comment after triple quotes in-line.

    Parameters
    ----------
    tokens : list
        A list of tokens from the source code.
    index : int
        The index of the docstring token in the list of tokens.

    Returns
    -------
    newlines : int
        The number of newlines to insert after the docstring.
    """
    j = index + 1

    # The docstring is followed by a comment.
    if tokens[j].string.startswith("#"):
        return 0

    return 1


def _get_function_docstring_newlines(  # noqa: PLR0911
    tokens: list[tokenize.TokenInfo],
    index: int,
    black: bool = False,
) -> int:
    """Return number of newlines after a function or method docstring.

    PEP_257_9.5: No blank lines after a function or method docstring.
    docformatter_9.6: One blank line after a function or method docstring if there is
    an inner function definition when in black mode.
    docformatter_9.7: Two blank lines after a function docstring if the stub function
    has no code.
    docformatter_9.8: One blank line after a method docstring if the stub method has
    no code.

    Parameters
    ----------
    tokens : list
        A list of tokens from the source code.
    index : int
        The index of the docstring token in the list of tokens.

    Returns
    -------
    newlines : int
        The number of newlines to insert after the docstring.
    """
    j = index + 1

    # The docstring is followed by a comment.
    if tokens[j].string.startswith("#"):
        return 0

    # Scan ahead to skip decorators and check for def/async def
    while j < len(tokens):
        if tokens[j].type == tokenize.OP and tokens[j].string == "@":
            # Skip to the end of the decorator line
            while j < len(tokens) and tokens[j][0] != tokenize.NEWLINE:
                j += 1
            j += 1
            continue

        # The docstring is followed by an attribute assignment.
        if tokens[j].type == tokenize.OP and tokens[j].string == "=":
            return 0

        # There is a line of code following the docstring.
        if _classify.is_code_line(tokens[j]):
            if tokens[j].start[1] == 0:
                return 1

            return 0

        # There is a method definition or nested function or class definition following
        # the docstring and docformatter is running in black mode.
        if _classify.is_nested_definition_line(tokens[j]):
            return 1

        # There is a function or class definition following the docstring.
        if _classify.is_definition_line(tokens[j]):
            return 2

        j += 1

    return 0


def _get_module_docstring_newlines(black: bool = False) -> int:
    """Return number of newlines after a module docstring.

    docformatter_8.2: One blank line after a module docstring.
    docformatter_8.2.1: Two blank lines after a module docstring when in black mode.

    Parameters
    ----------
    black : bool
        Indicates whether we're using black formatting rules.

    Returns
    -------
    newlines : int
        The number of newlines to insert after the docstring.
    """
    if black:
        return 2

    return 1


def _get_newlines_by_type(
    tokens: list[tokenize.TokenInfo],
    index: int,
    black: bool = False,
) -> int:
    """Dispatch to the correct docstring formatter based on context.

    Returns the number of newlines to insert after the docstring.

    Parameters
    ----------
    tokens : list
        A list of tokens from the source code.
    index : int
        The index of the docstring token in the list of tokens.
    black : bool
        Whether docformatter is running in black mode.

    Returns
    -------
    int
        The number of newlines to insert after the docstring.
    """
    if _classify.is_module_docstring(tokens, index):
        # print("Module")
        return _get_module_docstring_newlines(black)
    elif _classify.is_class_docstring(tokens, index):
        # print("Class")
        return _get_class_docstring_newlines(tokens, index)
    elif _classify.is_function_or_method_docstring(tokens, index):
        # print("Function or method")
        return _get_function_docstring_newlines(tokens, index, black)
    elif _classify.is_attribute_docstring(tokens, index):
        # print("Attribute")
        return _get_attribute_docstring_newlines(tokens, index)

    return 0  # Default: probably a string literal


def _get_num_rows_columns(token: tokenize.TokenInfo) -> tuple[int, int]:
    """Determine the number of rows and columns needed for the docstring.

    Parameters
    ----------
    token : tokenize.TokenInfo
        The token whose rows and columns needs to be determined.

    Returns
    -------
    rows_cols : tuple(int, int)
        The number of rows and columns for the token.
    """
    # Find the number of rows and columns the line requires.  When the docstring is
    # multiple lines, we'll need to update the row in the end index appropriately.
    # The number of columns is needed to properly set the end index column number.
    _split_line = token.line.split("\n")
    _num_rows = len(_split_line) - 1
    _num_cols = len(_split_line[_num_rows - 1])

    return _num_rows, _num_cols


def _get_start_end_indices(
    token: tokenize.TokenInfo,
    prev_token: tokenize.TokenInfo,
    num_rows: int,
    num_cols: int,
) -> tuple[tuple[int, int], tuple[int, int]]:
    """Determine the start and end indices for the token.

    Parameters
    ----------
    token : tokenize.TokenInfo
        The token whose start and end indices are being determined.
    prev_token : tokenize.TokenInfo
        The token prior to the token whose start and end indices are being determined.
    num_rows : int
        The number of rows the token requires.
    num_cols : int
        The number of columns the token requires.

    Returns
    -------
    indices : tuple(tuple(int, int), tuple(int, int))
        The start and end index for the token.
    """
    _start_row = prev_token.end[0]
    _start_col = token.start[1]
    _end_row = _start_row
    _end_col = token.end[1]

    if num_rows > 1 and _end_row != prev_token.end[0]:
        _end_row = _start_row + num_rows - 1
        _end_col = num_cols

    return (_start_row, _start_col), (_end_row, _end_col)


def _get_unmatched_start_end_indices(
    token: tokenize.TokenInfo,
    prev_token: tokenize.TokenInfo,
    num_rows: int,
) -> tuple[tuple[int, int], tuple[int, int]]:
    """Determine the start and end indices for the token if it doesn't match the prior.

    Parameters
    ----------
    token : tokenize.TokenInfo
        The token whose start and end indices are being determined.
    prev_token : tokenize.TokenInfo
        The token prior to the token whose start and end indices are being determined.
    num_rows : int
        The number of rows the token requires.

    Returns
    -------
    indices : tuple(tuple(int, int), tuple(int, int))
        The start and end index for the token.
    """
    _start_row = prev_token.end[0] + 1
    _start_col = token.start[1]
    _end_row = _start_row
    _end_col = token.end[1]

    if any(
        [
            _classify.is_inline_comment(token),
            _classify.is_string_variable(token, prev_token),
            _classify.is_newline_continuation(token, prev_token),
            _classify.is_line_following_indent(token, prev_token),
            _classify.is_closing_quotes(token, prev_token),
            _classify.is_f_string(token, prev_token),
        ]
    ):
        _start_row = prev_token.end[0]

    if num_rows > 1 and token.type != tokenize.INDENT:
        _end_row = _end_row + num_rows - 1

    return (_start_row, _start_col), (_end_row, _end_col)


class FormatResult:
    """Possible exit codes."""

    ok = 0
    error = 1
    interrupted = 2
    format_required = 3


# noinspection PyArgumentList
class Formatter:
    """Format docstrings."""

    parser = None
    """Parser object."""

    args: argparse.Namespace = argparse.Namespace()

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

        self.new_tokens: list[tokenize.TokenInfo] = []

    def do_format_standard_in(self, parser: argparse.ArgumentParser) -> None:
        """Print formatted text from standard in to standard out.

        Parameters
        ----------
        parser : argparse.ArgumentParser
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

    def do_format_files(self) -> Union[int, None]:
        """Format multiple files.

        Return
        ------
        code : int | None
            One of the FormatResult return codes.
        """
        outcomes: dict[int, int] = collections.Counter()

        return_codes = [  # in order of preference
            FormatResult.error,
            FormatResult.format_required,
            FormatResult.ok,
        ]

        _files_to_format = _util.find_py_files(
            list(self.args.files), self.args.recursive, self.args.exclude
        )

        is_empty = True
        for filename in _files_to_format:
            is_empty = False
            try:
                result = self._do_format_file(filename)
                outcomes[result] += 1
            except OSError as exception:
                outcomes[FormatResult.error] += 1
                # noinspection PyTypeChecker
                print(unicode(exception), file=self.stderror)

        # There were no files to process.
        if is_empty:
            outcomes[FormatResult.error] += 1

        for code in return_codes:
            if outcomes[code]:
                return code

        return 0

    def _do_add_blank_lines(
        self,
        num_blank_lines: int,
        start_row: int,
        end_row: int,
    ) -> None:
        """Add the number of blank lines specified by num_blanks after the docstring.

        Parameters
        ----------
        num_blank_lines : int
            The number of blank lines to add.
        start_row : int
            The start index row for the first blank line.
        end_row : int
            The end index row for the first blank line.
        """
        _start = (start_row, 0)
        _end = (end_row, 1)
        for k in range(num_blank_lines):
            new_tok = tokenize.TokenInfo(
                type=tokenize.NEWLINE,
                string="\n",
                start=_start,
                end=_end,
                line="\n",
            )
            self.new_tokens.append(new_tok)
            _start = (_end[0] + 1, 0)
            _end = (_start[0], 1)

    def _do_add_formatted_docstring(
        self,
        token: tokenize.TokenInfo,
        next_token: tokenize.TokenInfo,
        docstring_type: str,
        blank_line_count: int,
    ) -> None:
        """Add a formatted docstring to the new tokens list.

        Parameters
        ----------
        token : tokenize.TokenInfo
            The token representing the docstring.
        next_token : tokenize.TokenInfo
            The next token after the docstring.
        docstring_type : str
            The type of the docstring (e.g., module, class, function, attribute).
        blank_line_count : int
            The number of blank lines to add after the docstring.
        """
        _indent = " " * token.start[1] if docstring_type != "module" else ""
        _formatted = self._do_format_docstring(_indent, token.string)
        _line = _indent + _formatted

        # Add a newline to the end of the docstring line unless it already
        # has one or there is an in-line comment following it.
        if not _line.endswith("\n") and not next_token.string.startswith("#"):
            _line += "\n"

        # Add a token with the formatted docstring line.
        _new_tok = tokenize.TokenInfo(
            type=tokenize.STRING,
            string=_formatted,
            start=token.start,
            end=token.end,
            line=_line,
        )
        self.new_tokens.append(_new_tok)

        with contextlib.suppress(IndexError):
            if (
                self.new_tokens[-2].type == tokenize.INDENT
                and self.new_tokens[-2].end[0] == _new_tok.start[0]
            ):
                self.new_tokens[-2] = self.new_tokens[-2]._replace(line=_line)

        # If a comment follows the docstring, skip adding a newline token for
        # the line.
        if not next_token.string.startswith("#"):
            _new_tok = tokenize.TokenInfo(
                type=tokenize.NEWLINE,
                string="\n",
                start=token.end,
                end=(token.end[0], token.end[1] + 1),
                line=_line,
            )
            self.new_tokens.append(_new_tok)

        # Add the appropriate number of NEWLINE tokens based on the type of
        # docstring.
        self._do_add_blank_lines(
            blank_line_count,
            _new_tok.end[0] + 1,
            _new_tok.end[0] + 1,
        )

    def _do_add_unformatted_docstring(
        self,
        token: tokenize.TokenInfo,
        docstring_type: str,
    ) -> None:
        """Add an unformatted docstring to the new tokens list.

        Parameters
        ----------
        token : tokenize.TokenInfo
            The token representing the docstring.
        docstring_type : str
            The type of the docstring (e.g., module, class, function, attribute).
        """
        _indent = " " * token.start[1] if docstring_type != "module" else ""
        _line = _indent + token.string
        _new_token = tokenize.TokenInfo(
            type=tokenize.STRING,
            string=token.string,
            start=token.start,
            end=token.end,
            line=_line,
        )
        self.new_tokens.append(_new_token)

        # Add a token for the newline after the docstring.
        _new_token = tokenize.TokenInfo(
            type=tokenize.NEWLINE,
            string="\n",
            start=token.end,
            end=(token.end[0], token.end[1] + 1),
            line=_line,
        )
        self.new_tokens.append(_new_token)

    def _do_format_file(self, filename: str) -> int:
        """Format docstrings in a file.

        Parameters
        ----------
        filename : str
            The path to the file to be formatted.

        Return
        ------
        result_code : int
            One of the FormatResult codes.
        """
        self.encodor.do_detect_encoding(filename)

        with self.encodor.do_open_with_encoding(filename) as input_file:
            source = input_file.read()
            formatted_source = self._do_format_code(source)

        ret = FormatResult.ok
        show_diff = self.args.diff

        if source != formatted_source:
            ret = FormatResult.format_required
            if self.args.check:
                # noinspection PyTypeChecker
                print(unicode(filename), file=self.stderror)
            elif self.args.in_place:
                with self.encodor.do_open_with_encoding(
                    filename,
                    mode="w",
                ) as output_file:
                    output_file.write(formatted_source)
            else:
                show_diff = True

            if show_diff:
                diff = difflib.unified_diff(
                    source.splitlines(),
                    formatted_source.splitlines(),
                    f"before/{filename}",
                    f"after/{filename}",
                    lineterm="",
                )
                self.stdout.write("\n".join(list(diff) + [""]))

        return ret

    def _do_format_code(self, source: str) -> str:
        """Return source code with docstrings formatted.

        Parameters
        ----------
        source : str
            The text from the source file.

        Returns
        -------
        formatted : str
            The source file text with docstrings formatted.
        """
        if not source:
            return source

        if self.args.line_range is not None:
            assert self.args.line_range[0] > 0 and self.args.line_range[1] > 0

        if self.args.length_range is not None:
            assert self.args.length_range[0] > 0 and self.args.length_range[1] > 0

        try:
            _original_newline = self.encodor.do_find_newline(source.splitlines(True))
            tokens = list(
                tokenize.generate_tokens(io.StringIO(source, newline="").readline)
            )

            # Perform docstring rewriting
            self._do_rewrite_docstring_blocks(tokens)
            _code = tokenize.untokenize(self.new_tokens)

            return _strings.do_normalize_line_endings(
                _code.splitlines(True), _original_newline
            ).rstrip(" ")
        except (tokenize.TokenError, IndentationError):
            return source

    def _do_format_docstring(  # noqa PLR0911
        self,
        indentation: str,
        docstring: str,
    ) -> str:
        """Return formatted version of docstring.

        Parameters
        ----------
        indentation : str
            The indentation characters for the docstring.
        docstring : str
            The docstring itself.

        Returns
        -------
        docstring_formatted : str
            The docstring formatted according the various options.
        """
        contents, open_quote = _strings.do_strip_docstring(docstring)

        if (
            self.args.black
            and contents.startswith('"')
            or not self.args.black
            and self.args.pre_summary_space
        ):
            open_quote = f"{open_quote} "

        # Skip if there are nested triple double quotes
        if contents.count(QUOTE_TYPES[0]):
            return docstring

        # Do not modify things that start with doctests.
        if contents.lstrip().startswith(">>>"):
            return docstring

        # Do not modify docstring if the only thing it contains is a link.
        _links = _patterns.do_find_links(contents)
        with contextlib.suppress(IndexError):
            if _links[0][0] == 0 and _links[0][1] == len(contents):
                return docstring

        summary, description = _strings.do_split_summary_and_description(contents)

        # Leave docstrings with only field lists alone.
        if _patterns.is_field_list(
            summary,
            self.args.style,
        ):
            return docstring

        if not self.args.force_wrap and (
            _patterns.is_type_of_list(
                summary,
                self.args.non_strict,
                self.args.style,
            )
            or _patterns.do_find_links(summary)
        ):
            # Something probably isn't right with the splitting.
            return docstring

        # Compensate for textwrap counting each tab in indentation as 1
        # character.
        tab_compensation = indentation.count("\t") * (self.args.tab_width - 1)
        self.args.wrap_summaries -= tab_compensation
        self.args.wrap_descriptions -= tab_compensation

        if description:
            return self._do_format_multiline_docstring(
                indentation,
                summary,
                description,
                open_quote,
            )

        return self._do_format_oneline_docstring(
            indentation,
            contents,
            open_quote,
        )

    def _do_format_oneline_docstring(
        self,
        indentation: str,
        contents: str,
        open_quote: str,
    ) -> str:
        """Format one line docstrings.

        Parameters
        ----------
        indentation : str
            The indentation to use for each line.
        contents : str
            The contents of the original docstring.
        open_quote : str
            The type of quote used by the original docstring.  Selected from
            QUOTE_TYPES.

        Returns
        -------
        formatted_docstring : str
            The formatted docstring.
        """
        if self.args.make_summary_multi_line:
            beginning = f"{open_quote}\n{indentation}"
            ending = f'\n{indentation}"""'
            summary_wrapped = _wrappers.do_wrap_summary(
                _strings.do_normalize_summary(contents, self.args.non_cap),
                wrap_length=self.args.wrap_summaries,
                initial_indent=indentation,
                subsequent_indent=indentation,
            ).strip()
            return f"{beginning}{summary_wrapped}{ending}"
        else:
            summary_wrapped = _wrappers.do_wrap_summary(
                open_quote
                + _strings.do_normalize_summary(contents, self.args.non_cap)
                + '"""',
                wrap_length=self.args.wrap_summaries,
                initial_indent=indentation,
                subsequent_indent=indentation,
            ).strip()
            if self.args.close_quotes_on_newline and "\n" in summary_wrapped:
                summary_wrapped = (
                    f"{summary_wrapped[:-3]}"
                    f"\n{indentation}"
                    f"{summary_wrapped[-3:]}"
                )
            return summary_wrapped

    def _do_format_multiline_docstring(
        self,
        indentation: str,
        summary: str,
        description: str,
        open_quote: str,
    ) -> str:
        """Format multiline docstrings.

        Parameters
        ----------
        indentation : str
            The indentation to use for each line.
        summary : str
            The summary from the original docstring.
        description : str
            The long description from the original docstring.
        open_quote : str
            The type of quote used by the original docstring.  Selected from
            QUOTE_TYPES.

        Returns
        -------
        formatted_docstring : str
            The formatted docstring.
        """
        # Compensate for triple quotes by temporarily prepending 3 spaces.
        # This temporary prepending is undone below.
        initial_indent = (
            indentation if self.args.pre_summary_newline else 3 * " " + indentation
        )
        pre_summary = "\n" + indentation if self.args.pre_summary_newline else ""
        summary = _wrappers.do_wrap_summary(
            _strings.do_normalize_summary(summary, self.args.non_cap),
            wrap_length=self.args.wrap_summaries,
            initial_indent=initial_indent,
            subsequent_indent=indentation,
        ).lstrip()
        description = _wrappers.do_wrap_description(
            description,
            indentation=indentation,
            wrap_length=self.args.wrap_descriptions,
            force_wrap=self.args.force_wrap,
            strict=self.args.non_strict,
            rest_sections=self.args.rest_section_adorns,
            style=self.args.style,
        )
        post_description = "\n" if self.args.post_description_blank else ""
        return f'''\
{open_quote}{pre_summary}{summary}

{description}{post_description}
{indentation}"""\
'''

    def _do_rewrite_docstring_blocks(
        self,
        tokens: list[tokenize.TokenInfo],
    ) -> None:
        """Replace all docstring blocks with properly formatted docstrings.

        Parameters
        ----------
        tokens : list[TokenInfo]
            The tokenized Python source code.
        """
        blocks = _classify.do_find_docstring_blocks(tokens)
        self.new_tokens = []
        skip_indices: set[int] = set()

        for i, tok in enumerate(tokens):
            if i in skip_indices:
                continue

            match = next(((s, d, t) for (s, d, t) in blocks if d == i), None)
            if match:
                s, d, typ = match

                # Skip tokens from anchor (s) up to and including the docstring (d),
                # plus trailing blank lines
                j = d + 1
                while j < len(tokens) and tokens[j].type in (
                    tokenize.NL,
                    tokenize.NEWLINE,
                ):
                    j += 1
                skip_indices.update(range(s + 1, j))

                _docstring_token = tokens[d]
                _indent = " " * _docstring_token.start[1] if typ != "module" else ""
                _blank_line_count = _get_newlines_by_type(
                    tokens, d, black=self.args.black
                )

                if _util.is_in_range(
                    self.args.line_range,
                    _docstring_token.start[0],
                    _docstring_token.end[0],
                ) and _util.has_correct_length(
                    self.args.length_range,
                    _docstring_token.start[0],
                    _docstring_token.end[0],
                ):
                    self._do_add_formatted_docstring(
                        _docstring_token,
                        tokens[i + 1],
                        typ,
                        _blank_line_count,
                    )
                else:
                    self._do_add_unformatted_docstring(_docstring_token, typ)

                if (
                    (
                        self.new_tokens[-2].string == tokens[i + 1].string
                        and _docstring_token.line == tokens[i + 1].line
                    )
                    or tokens[i + 1].string == "\n"
                    or tokens[i + 1].type in (tokenize.NEWLINE, tokenize.NL)
                ):
                    skip_indices.add(i + 1)
                    continue
            else:
                _new_tok = tok
                # If it's a standalone STRING (not identified as a docstring block),
                # ensure .line ends with newline
                if tok.type == tokenize.STRING:
                    _line = tok.line
                    if not _line.endswith("\n"):
                        _line += "\n"
                    _new_tok = tokenize.TokenInfo(
                        type=tok.type,
                        string=tok.string,
                        start=tok.start,
                        end=tok.end,
                        line=_line,
                    )

                self.new_tokens.append(_new_tok)

        self.new_tokens = _do_remove_preceding_blank_lines(self.new_tokens, blocks)
        self.new_tokens = _do_update_token_indices(self.new_tokens)
