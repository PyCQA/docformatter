"""Formats docstrings to follow PEP 257."""

import re
import tokenize
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


__version__ = '0.1'


def format_code(source):
    """Return source code with docstrings formatted."""
    sio = StringIO(source)
    formatted = ''
    previous_token_string = ''
    previous_token_type = None
    last_row = 0
    last_column = -1
    for token in tokenize.generate_tokens(sio.readline):
        token_type = token[0]
        token_string = token[1]
        start_row, start_column = token[2]
        end_row, end_column = token[3]

        if start_row > last_row:
            last_column = 0
        if start_column > last_column:
            formatted += (' ' * (start_column - last_column))

        if (token_type == tokenize.STRING and
                starts_with_triple(token_string) and
                previous_token_type == tokenize.INDENT):
            formatted += format_docstring(previous_token_string, token_string)
        else:
            formatted += token_string

        previous_token_string = token_string
        previous_token_type = token_type

        last_row = end_row
        last_column = end_column

    return formatted


def starts_with_triple(string):
    """Return True if the string starts with triple single/double quotes."""
    return (string.strip().startswith('"""') or
            string.strip().startswith("''''"))


def format_docstring(indentation, docstring):
    """Return formatted version of docstring."""
    contents = strip_docstring(docstring)

    if not contents:
        return ''

    summary, description = split_summary_and_description(contents)

    if description:
        return '''\
"""{summary}

{description}

{indentation}"""\
'''.format(summary=normalize_summary(summary),
           description='\n'.join([indent_non_indented(l, indentation).rstrip()
                                  for l in description.split('\n')]),
           indentation=indentation)
    else:
        return '"""' + contents + '"""'


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
    split = contents.split('\n')
    if len(split) > 1 and not split[1].strip():
        return (split[0], '\n'.join(split[2:]))
    else:
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
    summary = re.sub('\s*\n\s*', ' ', summary.strip())

    # Add period at end of sentence
    if not summary.endswith('.'):
        summary += '.'
    return summary
