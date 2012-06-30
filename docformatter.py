"""Formats docstrings to follow PEP 257."""

import re
import tokenize
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


__version__ = '0.2.2'


def format_code(source,
                summary_wrap_length=0,
                pre_summary_newline=False,
                post_description_blank=True):
    """Return source code with docstrings formatted.

    Wrap summary lines if summary_wrap_length is greater than 0.

    """
    sio = StringIO(source)
    formatted = ''
    previous_token_string = ''
    previous_token_type = None
    previous_line = ''
    last_row = 0
    last_column = -1
    for token in tokenize.generate_tokens(sio.readline):
        token_type = token[0]
        token_string = token[1]
        start_row, start_column = token[2]
        end_row, end_column = token[3]

        # Preserve escaped newlines
        if (not previous_line.lstrip().startswith('#') and
            start_row > last_row and
                (previous_line.endswith('\\\n') or
                 previous_line.endswith('\\\r\n') or
                 previous_line.endswith('\\\r'))):
            formatted += previous_line[len(previous_line.rstrip(' \t\n\r\\')):]

        # Preserve spacing
        if start_row > last_row:
            last_column = 0
        if start_column > last_column:
            formatted += ' ' * (start_column - last_column)

        if (token_type == tokenize.STRING and
                starts_with_triple(token_string) and
                previous_token_type == tokenize.INDENT):
            formatted += format_docstring(
                previous_token_string,
                token_string,
                summary_wrap_length=summary_wrap_length,
                pre_summary_newline=pre_summary_newline,
                post_description_blank=post_description_blank)
        else:
            formatted += token_string

        previous_token_string = token_string
        previous_token_type = token_type
        previous_line = token[4]

        last_row = end_row
        last_column = end_column

    return formatted


def starts_with_triple(string):
    """Return True if the string starts with triple single/double quotes."""
    return (string.strip().startswith('"""') or
            string.strip().startswith("'''"))


def format_docstring(indentation, docstring,
                     summary_wrap_length=0,
                     pre_summary_newline=False,
                     post_description_blank=True):
    """Return formatted version of docstring.

    Wrap summary lines if summary_wrap_length is greater than 0.

    Relevant parts of PEP 257:
        - For consistency, always use triple double quotes around docstrings.
        - Triple quotes are used even though the string fits on one line.
        - Multi-line docstrings consist of a summary line just like a one-line
          docstring, followed by a blank line, followed by a more elaborate
          description.
        - The BDFL recommends inserting a blank line between the last paragraph
          in a multi-line docstring and its closing quotes, placing the closing
          quotes on a line by themselves.

    """
    contents = strip_docstring(docstring)

    # Skip if there are nested triple double quotes
    if contents.count('"""'):
        return docstring

    summary, description = split_summary_and_description(contents)

    if description:
        # Compensate for triple quotes by temporarily prepending 3 spaces.
        # This temporary prepending is undone below.
        if pre_summary_newline:
            summary = indentation + summary
        else:
            summary = indentation + 3 * ' ' + summary

        return '''\
"""{pre_summary}{summary}

{description}{post_description}
{indentation}"""\
'''.format(pre_summary=('\n' + indentation if pre_summary_newline else ''),
           summary=wrap_summary(normalize_summary(summary),
                                wrap_length=summary_wrap_length,
                                indentation=indentation).lstrip(),
           description='\n'.join([indent_non_indented(l, indentation).rstrip()
                                  for l in description.splitlines()]),
           post_description=('\n' if post_description_blank else ''),
           indentation=indentation)
    else:
        return wrap_summary(indentation +
                            '"""' + normalize_summary(contents) + '"""',
                            wrap_length=summary_wrap_length,
                            indentation=indentation).strip()


def indent_non_indented(line, indentation):
    """Return indented line if it has no indentation."""
    if line.lstrip() == line:
        return indentation + line
    else:
        return line


def split_summary_and_description(contents):
    """Split docstring into summary and description.

    Return tuple (summary, description).

    """
    split = contents.splitlines()
    if len(split) > 1 and not split[1].strip():
        # Empty line separation would indicate the rest is the description.
        return (split[0], '\n'.join(split[2:]))
    elif len(split) > 1 and not split[1].strip()[0].isalnum():
        # Symbol on second line probably is a description with a list.
        return (split[0], '\n'.join(split[1:]))
    else:
        # Break on first sentence.
        split = re.split('\.\s', string=contents, maxsplit=1)
        if len(split) == 2:
            return (split[0].strip() + '.', split[1].strip())
        else:
            return (split[0].strip(), '')


def strip_docstring(docstring):
    """Return contents of docstring."""
    triple = '"""'
    if docstring.lstrip().startswith("'''"):
        triple = "'''"
        assert docstring.rstrip().endswith("'''")

    return docstring.split(triple, 1)[1].rsplit(triple, 1)[0].strip()


def normalize_summary(summary):
    """Return normalized docstring summary."""
    # Remove newlines
    summary = re.sub('\s*\n\s*', ' ', summary.rstrip())

    # Add period at end of sentence
    if summary and summary[-1].isalnum():
        summary += '.'

    return summary


def wrap_summary(summary, indentation, wrap_length):
    """Return line-wrapped summary text."""
    if wrap_length > 0:
        import textwrap
        return '\n'.join(
            textwrap.wrap(summary,
                          width=wrap_length,
                          subsequent_indent=indentation)).strip()
    else:
        return summary


def open_with_encoding(filename, encoding, mode='r'):
    """Open and return a file with a specific encoding."""
    try:
        # Python 3
        return open(filename, mode=mode, encoding=encoding)
    except TypeError:
        return open(filename, mode=mode)


def detect_encoding(filename):
    """Return file encoding."""
    try:
        # Python 3
        try:
            with open(filename, 'rb') as input_file:
                encoding = tokenize.detect_encoding(input_file.readline)[0]

                # Check for correctness of encoding
                import io
                with io.TextIOWrapper(input_file, encoding) as wrapper:
                    wrapper.read()

            return encoding
        except (SyntaxError, LookupError, UnicodeDecodeError):
            return 'latin-1'
    except AttributeError:
        return 'utf-8'


def main(argv, standard_out):
    """Main entry point."""
    import argparse
    parser = argparse.ArgumentParser(description=__doc__, prog='docformatter')
    parser.add_argument('--in-place', action='store_true',
                        help='make changes to files instead of printing diffs')
    parser.add_argument('--no-backup', dest='backup', action='store_false',
                        help='do not write backup files')
    parser.add_argument(
        '--wrap-long-summaries', default=0, type=int, metavar='LENGTH',
        help='wrap long summary lines at this length (default: %(default)s)')
    parser.add_argument('--no-blank', dest='post_description_blank',
                        action='store_false',
                        help='do not add blank line after description')
    parser.add_argument('--pre-summary-newline',
                        action='store_true',
                        help='add a newline before the summary of a '
                             'multi-line docstring')
    parser.add_argument('--version', action='version', version=__version__)
    parser.add_argument('files', nargs='+',
                        help='files to format')

    args = parser.parse_args(argv[1:])

    for filename in args.files:
        encoding = detect_encoding(filename)
        with open_with_encoding(filename, encoding=encoding) as input_file:
            source = input_file.read()
            formatted_source = format_code(
                source,
                summary_wrap_length=args.wrap_long_summaries,
                pre_summary_newline=args.pre_summary_newline,
                post_description_blank=args.post_description_blank)

        if source != formatted_source:
            if args.in_place:
                # Write output files with same encoding as input
                if args.backup:
                    with open_with_encoding(filename + '.backup', mode='w',
                                            encoding=encoding) as backup_file:
                        backup_file.write(source)

                with open_with_encoding(filename, mode='w',
                                        encoding=encoding) as output_file:
                    output_file.write(formatted_source)
            else:
                import difflib
                diff = difflib.unified_diff(
                    source.splitlines(True),
                    formatted_source.splitlines(True),
                    'before/' + filename,
                    'after/' + filename)
                standard_out.write(''.join(diff))
