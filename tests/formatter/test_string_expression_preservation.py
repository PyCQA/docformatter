"""Protect value expressions from docstring rewriting."""

import ast
import io

import pytest

from docformatter import Configurater, Formatter


def format_source(source):
    configuration = Configurater(["docformatter", "-"])
    configuration.do_parse_arguments()
    formatter = Formatter(
        configuration.args, io.StringIO(), io.StringIO(), io.StringIO()
    )
    return formatter._do_format_code(source)


@pytest.mark.integration
@pytest.mark.parametrize(
    "source",
    [
        'def value():\n    return """lowercase value"""\n',
        'def value():\n    return (\n        """lowercase value"""\n    )\n',
        'def value():\n    return """first line.\nsecond line"""\n',
        'def value():\n    print("""lowercase value""")\n',
        'def value():\n    yield """lowercase value"""\n',
        'def value():\n    yield (\n        """lowercase value"""\n    )\n',
        'def value():\n    assert """lowercase value"""\n',
        'def value():\n    value="""lowercase value"""\n',
        'def value():\n    value: str = """lowercase value"""\n',
        'def value(arg="""lowercase value"""):\n    pass\n',
        'def value() -> """lowercase annotation""":\n    pass\n',
        'def value():\n    """lowercase value""" + "suffix"\n',
        'def value():\n    """lowercase value""".format()\n',
        'def value():\n    """lowercase value""",\n',
        'def value():\n    """lowercase value""" "suffix"\n',
        'def value():\n    """lowercase value"""[0]\n',
        'def value(): """lowercase docstring"""\n',
        'def value():\n    ("""lowercase docstring""")\n',
        'def value():\n    """lowercase docstring"""; pass\n',
        'def value():\n    return \\\n        """lowercase value"""\n',
        (
            "def value():\n    return (\n"
            "        # Keep this runtime value.\n"
            '        """lowercase value"""\n    )\n'
        ),
        'class Value:\n    print("""lowercase value""")\n',
        '@decorate("""lowercase value""")\ndef value():\n    pass\n',
    ],
)
def test_string_expressions_are_preserved(source):
    """Literal values and unsupported inline forms must not be rewritten."""
    formatted = format_source(source)
    assert formatted == source
    assert ast.dump(ast.parse(formatted)) == ast.dump(ast.parse(source))
    assert format_source(formatted) == formatted
