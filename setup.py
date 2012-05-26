#!/usr/bin/env python

from distutils import core
import docformatter


core.setup(name='docformatter',
           version=docformatter.__version__,
           description='Formats docstrings to follow PEP 257.',
           long_description=open("README.rst").read(),
           license='Expat License',
           author='myint',
           url='https://github.com/myint/docformatter',
           classifiers=['Intended Audience :: Developers',
                        'Environment :: Console',
                        'Programming Language :: Python :: 2.6',
                        'Programming Language :: Python :: 2.7',
                        'Programming Language :: Python :: 3',
                        'License :: OSI Approved :: MIT License'],
           keywords="PEP 257, pep257, style, formatter, docstrings",
           py_modules=['docformatter'],
           scripts=['docformatter'])
