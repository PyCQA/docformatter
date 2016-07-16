============
docformatter
============

Formats docstrings to follow `PEP 257`_.

.. _`PEP 257`: http://www.python.org/dev/peps/pep-0257/

.. image:: https://travis-ci.org/myint/docformatter.svg?branch=master
   :target: https://travis-ci.org/myint/docformatter
   :alt: Build status


Features
========

*docformatter* currently automatically formats docstrings to follow a
subset of the PEP 257 conventions. Below are the relevant items quoted
from PEP 257.

- For consistency, always use triple double quotes around docstrings.
- Triple quotes are used even though the string fits on one line.
- Multi-line docstrings consist of a summary line just like a one-line
  docstring, followed by a blank line, followed by a more elaborate
  description.
- The BDFL recommends inserting a blank line between the last paragraph
  in a multi-line docstring and its closing quotes, placing the closing
  quotes on a line by themselves.

docformatter also handles some of the PEP 8 conventions.

- Don't write string literals that rely on significant trailing
  whitespace. Such trailing whitespace is visually indistinguishable
  and some editors (or more recently, reindent.py) will trim them.


Installation
============

From pip::

    $ pip install --upgrade docformatter


Example
=======

After running::

    $ docformatter --in-place example.py

this code

.. code-block:: python

    """   Here are some examples.

        This module docstring should be dedented."""


    def launch_rocket():
        """Launch
    the
    rocket. Go colonize space."""


    def factorial(x):
        '''

        Return x factorial.

        This uses math.factorial.

        '''
        import math
        return math.factorial(x)


    def print_factorial(x):
        """Print x factorial"""
        print(factorial(x))


    def main():
        """Main
        function"""
        print_factorial(5)
        if factorial(10):
            launch_rocket()


gets formatted into this

.. code-block:: python

    """Here are some examples.

    This module docstring should be dedented.

    """


    def launch_rocket():
        """Launch the rocket.

        Go colonize space.

        """


    def factorial(x):
        """Return x factorial.

        This uses math.factorial.

        """
        import math
        return math.factorial(x)


    def print_factorial(x):
        """Print x factorial."""
        print(factorial(x))


    def main():
        """Main function."""
        print_factorial(5)
        if factorial(10):
            launch_rocket()


Options
=======

Below is the help output::

    usage: docformatter [-h] [-i] [-r] [--wrap-summaries length]
                        [--wrap-descriptions length] [--no-blank]
                        [--pre-summary-newline] [--force-wrap] [--range line line]
                        [--version]
                        files [files ...]

    Formats docstrings to follow PEP 257.

    positional arguments:
      files                 files to format or '-' for standard in

    optional arguments:
      -h, --help            show this help message and exit
      -i, --in-place        make changes to files instead of printing diffs
      -r, --recursive       drill down directories recursively
      --wrap-summaries length
                            wrap long summary lines at this length (default: 79)
      --wrap-descriptions length
                            wrap descriptions at this length (default: 72)
      --no-blank            do not add blank line after description
      --pre-summary-newline
                            add a newline before the summary of a multi-line
                            docstring
      --force-wrap          force descriptions to be wrapped even if it may result
                            in a mess
      --range line line     apply docformatter to docstrings between these lines;
                            line numbers are indexed at 1
      --version             show program's version number and exit


Wrapping descriptions
=====================

docformatter will wrap descriptions, but only in simple cases. If there is text
that seems like a bulleted/numbered list, docformatter will leave the
description as is::

    - Item one.
    - Item two.
    - Item three.

This prevents the risk of the wrapping turning things into a mess. To force
even these instances to get wrapped use ``--force-wrap``.


Issues
======

Bugs and patches can be reported on the `GitHub page`_.

.. _`GitHub page`: https://github.com/myint/docformatter/issues


Links
=====

* Coveralls_

.. _`Coveralls`: https://coveralls.io/r/myint/docformatter
