#!/usr/bin/env python
"""Setup for docformatter."""

from distutils import core


def version():
    """Return version string."""
    with open('docformatter.py') as input_file:
        for line in input_file:
            if line.startswith('__version__'):
                import ast
                return ast.literal_eval(line.split('=')[1].strip())


with open('README.rst') as readme:
    core.setup(name='docformatter',
               version=version(),
               description='Formats docstrings to follow PEP 257.',
               long_description=readme.read(),
               license='Expat License',
               author='myint',
               url='https://github.com/myint/docformatter',
               classifiers=['Intended Audience :: Developers',
                            'Environment :: Console',
                            'Programming Language :: Python :: 2.6',
                            'Programming Language :: Python :: 2.7',
                            'Programming Language :: Python :: 3',
                            'License :: OSI Approved :: MIT License'],
               keywords='PEP 257, pep257, style, formatter, docstrings',
               py_modules=['docformatter'],
               scripts=['docformatter'])
