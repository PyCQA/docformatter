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
from typing import Dict, List, TextIO, Tuple, Union

# Third Party Imports
import untokenize  # type: ignore
from charset_normalizer import from_path  # pylint: disable=import-error

try:
    # Third Party Imports
    import tomli

    TOMLI_INSTALLED = True
except ImportError:
    TOMLI_INSTALLED = False

__version__ = "1.5.0"

unicode = str


HEURISTIC_MIN_LIST_ASPECT_RATIO = 0.4

CR = "\r"
LF = "\n"
CRLF = "\r\n"

_PYTHON_LIBS = set(sysconfig.get_paths().values())


class FormatResult:
    """Possible exit codes."""

    ok = 0
    error = 1
    interrupted = 2
    check_failed = 3


class Configurator:
    """Read and store all the docformatter configuration information."""

    parser = None
    """Parser object."""

    flargs_dct: Dict[str, Union[bool, float, int, str]] = {}
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
            "set to 0 to disable wrapping (default: 79)",
        )
        self.parser.add_argument(
            "--wrap-descriptions",
            default=int(self.flargs_dct.get("wrap-descriptions", 72)),
            type=int,
            metavar="length",
            help="wrap descriptions at this length; "
            "set to 0 to disable wrapping (default: 72)",
        )
        self.parser.add_argument(
            "--force-wrap",
            action="store_true",
            default=bool(self.flargs_dct.get("force-wrap", False)),
            help="force descriptions to be wrapped even if it may "
            "result in a mess (default: False)",
        )
        self.parser.add_argument(
            "--tab-width",
            type=int,
            dest="tab_width",
            metavar="width",
            default=int(self.flargs_dct.get("tab-width", 1)),
            help="tabs in indentation are this many characters when "
            "wrapping lines (default: 1)",
        )
        self.parser.add_argument(
            "--blank",
            dest="post_description_blank",
            action="store_true",
            default=bool(self.flargs_dct.get("blank", False)),
            help="add blank line after description (default: False)",
        )
        self.parser.add_argument(
            "--pre-summary-newline",
            action="store_true",
            default=bool(self.flargs_dct.get("pre-summary-newline", False)),
            help="add a newline before the summary of a multi-line docstring "
            "(default: False)",
        )
        self.parser.add_argument(
            "--pre-summary-space",
            action="store_true",
            default=bool(self.flargs_dct.get("pre-summary-space", False)),
            help="add a space after the opening triple quotes "
            "(default: False)",
        )
        self.parser.add_argument(
            "--make-summary-multi-line",
            action="store_true",
            default=bool(
                self.flargs_dct.get("make-summary-multi-line", False)
            ),
            help="add a newline before and after the summary of a one-line "
            "docstring (default: False)",
        )
        self.parser.add_argument(
            "--close-quotes-on-newline",
            action="store_true",
            default=bool(
                self.flargs_dct.get("close-quotes-on-newline", False)
            ),
            help="place closing triple quotes on a new-line when a "
            "one-line docstring wraps to two or more lines "
            "(default: False)",
        )
        self.parser.add_argument(
            "--range",
            metavar="line",
            dest="line_range",
            default=self.flargs_dct.get("range", None),
            type=int,
            nargs=2,
            help="apply docformatter to docstrings between these "
            "lines; line numbers are indexed at 1 (default: None)",
        )
        self.parser.add_argument(
            "--docstring-length",
            metavar="length",
            dest="length_range",
            default=self.flargs_dct.get("docstring-length", None),
            type=int,
            nargs=2,
            help="apply docformatter to docstrings of given length range "
            "(default: None)",
        )
        self.parser.add_argument(
            "--non-strict",
            action="store_true",
            default=bool(self.flargs_dct.get("non-strict", False)),
            help="don't strictly follow reST syntax to identify lists (see "
            "issue #67) (default: False)",
        )
        self.parser.add_argument(
            "--config",
            default=self.config_file,
            help="path to file containing docformatter options",
        )
        self.parser.add_argument(
            "--version",
            action="version",
            version=f"%(prog)s {__version__}",
        )
        self.parser.add_argument(
            "files",
            nargs="+",
            help="files to format or '-' for standard in",
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

        for _section in [
            "tool.docformatter",
            "tool:docformatter",
            "docformatter",
        ]:
            if _section in config.sections():
                self.flargs_dct = {
                    k: v if isinstance(v, list) else str(v)
                    for k, v in config[_section].items()
                }


class Formator:
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

        self.encodor = Encodor()

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
        for filename in find_py_files(
            set(self.args.files), self.args.recursive, self.args.exclude
        ):
            try:
                result = self._do_format_file(filename)
                outcomes[result] += 1
                if result == FormatResult.check_failed:
                    print(unicode(filename), file=self.stderror)
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

        if source != formatted_source:
            if self.args.check:
                return FormatResult.check_failed
            elif self.args.in_place:
                with self.encodor.do_open_with_encoding(
                    filename,
                    mode="w",
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
                self.stdout.write("\n".join(list(diff) + [""]))

        return FormatResult.ok

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

            return normalize_line_endings(
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
        previous_token_string = ""
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
                        or only_comments_so_far
                    )
                    and is_in_range(self.args.line_range, start[0], end[0])
                    and has_correct_length(
                        self.args.length_range, start[0], end[0]
                    )
                ):
                    indentation = (
                        "" if only_comments_so_far else previous_token_string
                    )
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

                previous_token_string = token_string
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
                    or modified_tokens[-2][4][:3] != "def"
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

        summary, description = split_summary_and_description(contents)

        # Leave docstrings with underlined summaries alone.
        if remove_section_header(description).strip() != description.strip():
            return docstring

        if not self.args.force_wrap and is_some_sort_of_list(
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
            summary = wrap_summary(
                normalize_summary(summary),
                wrap_length=self.args.wrap_summaries,
                initial_indent=initial_indent,
                subsequent_indent=indentation,
            ).lstrip()
            description = wrap_description(
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
                summary_wrapped = wrap_summary(
                    open_quote + normalize_summary(contents) + '"""',
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
                summary_wrapped = wrap_summary(
                    normalize_summary(contents),
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


class Encodor:
    """Encoding and decoding of files."""

    CR = "\r"
    LF = "\n"
    CRLF = "\r\n"

    def __init__(self):
        """Initialize an Encodor instance."""
        self.encoding = "latin-1"
        self.system_encoding = (
            locale.getpreferredencoding() or sys.getdefaultencoding()
        )

    def do_detect_encoding(self, filename: str) -> None:
        """Return the detected file encoding.

        Parameters
        ----------
        filename : str
            The full path name of the file whose encoding is to be detected.
        """
        try:
            self.encoding = from_path(filename).best().encoding

            # Check for correctness of encoding.
            with self.do_open_with_encoding(filename) as check_file:
                check_file.read()
        except (SyntaxError, LookupError, UnicodeDecodeError):
            self.encoding = "latin-1"

    def do_find_newline(self, source: str) -> Dict[int, int]:
        """Return type of newline used in source.

        Paramaters
        ----------
        source : list
            A list of lines.

        Returns
        -------
        counter : dict
            A dict with the count of new line types found.
        """
        assert not isinstance(source, unicode)

        counter = collections.defaultdict(int)
        for line in source:
            if line.endswith(self.CRLF):
                counter[self.CRLF] += 1
            elif line.endswith(self.CR):
                counter[self.CR] += 1
            elif line.endswith(self.LF):
                counter[self.LF] += 1

        return (sorted(counter, key=counter.get, reverse=True) or [self.LF])[0]

    def do_open_with_encoding(self, filename: str, mode: str = "r"):
        """Return opened file with a specific encoding.

        Parameters
        ----------
        filename : str
            The full path name of the file to open.
        mode : str
            The mode to open the file in.  Defaults to read-only.

        Returns
        -------
        contents : TextIO
            The contents of the file.
        """
        return io.open(
            filename, mode=mode, encoding=self.encoding, newline=""
        )  # Preserve line endings


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


def is_some_sort_of_code(text: str) -> bool:
    """Return True if text looks like code."""
    return any(
        len(word) > 50
        and not re.match(r"<{0,1}(http:|https:|ftp:|sftp:)", word)
        for word in text.split()
    )


def do_preserve_links(
    text: str,
    indentation: str,
    wrap_length: int,
) -> List[str]:
    """Rebuild links in docstring.

    Parameters
    ----------
    text : str
        The docstring description.
    indentation : str
        The indentation (number of spaces or tabs) to place in front of each
        line.
    wrap_length : int
        The column to wrap each line at.

    Returns
    -------
    lines : list
        A list containing each line of the description with any links put
        back together.
    """
    lines = textwrap.wrap(
        textwrap.dedent(text),
        width=wrap_length,
        initial_indent=indentation,
        subsequent_indent=indentation,
    )

    url = next(
        (
            line
            for line in lines
            if re.search(r"<?(http://|https://|ftp://|sftp://)", line)
        ),
        "",
    )

    if url != "":
        url_idx = lines.index(url)

        # Is this an in-line link (i.e., enclosed in <>)?  We want to keep
        # the '<' and '>' part of the link.
        if re.search(r"<", url):
            lines[url_idx] = f"{indentation}" + url.split(sep="<")[0].strip()
            url = f"{indentation}<" + url.split(sep="<")[1]
            url = url + lines[url_idx + 1].strip()
            lines[url_idx + 1] = url
        # Is this a link target definition (i.e., .. a link: https://)?  We
        # want to keep the .. a link: on the same line as the url.
        elif re.search(r"(\.\. )", url):
            url = url + lines[url_idx + 1].strip()
            lines[url_idx] = url
            lines.pop(url_idx + 1)
        # Is this a simple link (i.e., just a link in the text) that should
        # be unwrapped?  We want to break the url out from the rest of the
        # text.
        elif len(lines[url_idx]) >= wrap_length:
            lines[url_idx] = (
                f"{indentation}" + url.strip().split(sep=" ")[0].strip()
            )
            url = f"{indentation}" + url.strip().split(sep=" ")[1].strip()
            url = url + lines[url_idx + 1].strip().split(sep=" ")[0].strip()
            lines.append(
                indentation
                + " ".join(lines[url_idx + 1].strip().split(sep=" ")[1:])
            )
            lines[url_idx + 1] = url

        with contextlib.suppress(IndexError):
            if lines[url_idx + 2].strip() in [".", "?", "!", ";"] or re.search(
                r">", lines[url_idx + 2]
            ):
                url = url + lines[url_idx + 2].strip()
                lines[url_idx + 1] = url
                lines.pop(url_idx + 2)

    return lines


def is_some_sort_of_list(text, strict) -> bool:
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
        and (is_some_sort_of_code(text) or is_some_sort_of_list(text, strict))
    ):
        return text

    text = do_preserve_links(text, indentation, wrap_length)

    return indentation + "\n".join(text).strip()


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


def _main(argv, standard_out, standard_error, standard_in):
    """Run internal main entry point."""
    configurator = Configurator(argv)
    configurator.do_parse_arguments()

    formator = Formator(
        configurator.args,
        stderror=standard_error,
        stdin=standard_in,
        stdout=standard_out,
    )

    if "-" in configurator.args.files:
        formator.do_format_standard_in(
            configurator.parser,
        )
    else:
        return formator.do_format_files()


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
