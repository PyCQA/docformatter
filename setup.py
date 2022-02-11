#!/usr/bin/env python

"""Setup for docformatter."""

from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

import ast
from pathlib import Path

from setuptools import setup


def version():
    """Return version string."""
    with open('docformatter.py') as input_file:
        for line in input_file:
            if line.startswith('__version__'):
                return ast.parse(line).body[0].value.s


setup(name='docformatter',
        version=version(),
        description='Formats docstrings to follow PEP 257.',
        long_description=Path('README.rst').read_text(),
        license='Expat License',
        author='Steven Myint',
        url='https://github.com/myint/docformatter',
        classifiers=['Intended Audience :: Developers',
                    'Environment :: Console',
                    'Programming Language :: Python :: 3',
                    'Programming Language :: Python :: 3.6',
                    'Programming Language :: Python :: 3.7',
                    'Programming Language :: Python :: 3.8',
                    'Programming Language :: Python :: 3.9',
                    'Programming Language :: Python :: 3.10',
                    'Programming Language :: Python :: Implementation',
                    'Programming Language :: Python :: Implementation :: PyPy',
                    'Programming Language :: Python :: Implementation :: CPython',
                    'License :: OSI Approved :: MIT License'],
        keywords='PEP 257, pep257, style, formatter, docstrings',
        py_modules=['docformatter'],
        entry_points={
            'console_scripts': ['docformatter = docformatter:main']},
        install_requires=['untokenize'],
        test_suite='test_docformatter')
