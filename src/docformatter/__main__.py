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


from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

# Standard Library Imports
import contextlib
import signal
import sys

# docformatter Package Imports
import docformatter.configuration as _configuration
import docformatter.format as _format


def _main(argv, standard_out, standard_error, standard_in):
    """Run internal main entry point."""
    configurator = _configuration.Configurater(argv)
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
