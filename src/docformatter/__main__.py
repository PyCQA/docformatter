#!/usr/bin/env python
#
# Copyright (C) 2012-2023 Steven Myint
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


# Standard Library Imports
import contextlib
import signal
import sys

# docformatter Package Imports
import docformatter.configuration as _configuration
import docformatter.format as _format


def _help():
    """Print docformatter's help."""
    print(
        """\
usage: docformatter [-h] [-i | -c] [-d] [-r] [-e [EXCLUDE ...]]
                    [-n [NON-CAP ...]] [-s [style]] [--rest-section-adorns REGEX]
                    [--black] [--wrap-summaries length]
                    [--wrap-descriptions length] [--force-wrap]
                    [--tab-width width] [--blank] [--pre-summary-newline]
                    [--pre-summary-space] [--make-summary-multi-line]
                    [--close-quotes-on-newline] [--range line line]
                    [--docstring-length length length] [--non-strict]
                    [--config CONFIG] [--version] files [files ...]

positional arguments:
  files                 files to format or '-' for standard in

options:
  -h, --help            show this help message and exit
  -i, --in-place        make changes to files instead of printing diffs
  -c, --check           only check and report incorrectly formatted files
  -d, --diff            when used with `--check` or `--in-place`, also what
                        changes would be made
  -r, --recursive       drill down directories recursively
  -e [EXCLUDE ...], --exclude [EXCLUDE ...]
                        in recursive mode, exclude directories and files by
                        names
  -n [NON-CAP ...], --non-cap [NON-CAP ...]
                        list of words not to capitalize when they appear as the
                        first word in the summary

  -s style, --style style
                        the docstring style to use when formatting parameter
                        lists.  One of epytext, sphinx. (default: sphinx)
  --rest-section-adorns REGEX
                        regular expression for identifying reST section adornments
                        (default: [!\"#$%&'()*+,-./\\:;<=>?@[]^_`{|}~]{4,})
  --black               make formatting compatible with standard black options
                        (default: False)
  --wrap-summaries length
                        wrap long summary lines at this length; set to 0 to
                        disable wrapping (default: 79, 88 with --black option)
  --wrap-descriptions length
                        wrap descriptions at this length; set to 0 to disable
                        wrapping (default: 72, 88 with --black option)
  --force-wrap          force descriptions to be wrapped even if it may result
                        in a mess (default: False)
  --tab-width width     tabs in indentation are this many characters when
                        wrapping lines (default: 1)
  --blank               add blank line after description (default: False)
  --pre-summary-newline
                        add a newline before the summary of a multi-line
                        docstring (default: False)
  --pre-summary-space   add a space after the opening triple quotes
                        (default: False)
  --make-summary-multi-line
                        add a newline before and after the summary of a
                        one-line docstring (default: False)
  --close-quotes-on-newline
                        place closing triple quotes on a new-line when a
                        one-line docstring wraps to two or more lines
                        (default: False)
  --range line line     apply docformatter to docstrings between these lines;
                        line numbers are indexed at 1 (default: None)
  --docstring-length length length
                        apply docformatter to docstrings of given length range
                        (default: None)
  --non-strict          don't strictly follow reST syntax to identify lists
                        (see issue #67) (default: False)
  --config CONFIG       path to file containing docformatter options
  --version             show program's version number and exit
"""
    )


def _main(argv, standard_out, standard_error, standard_in):
    """Run internal main entry point."""
    configurator = _configuration.Configurater(argv)

    if "--help" in configurator.args_lst:
        _help()
        return 0
    else:
        configurator.do_parse_arguments()

    formator = _format.Formatter(
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
        return _format.FormatResult.interrupted  # pragma: no cover


if __name__ == "__main__":
    sys.exit(main())
