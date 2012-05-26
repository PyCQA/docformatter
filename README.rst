============
docformatter
============

Formats docstrings to follow `PEP 257`_.

.. _`PEP 257`: http://www.python.org/dev/peps/pep-0257/

.. image:: https://secure.travis-ci.org/myint/docformatter.png
   :target: https://secure.travis-ci.org/myint/docformatter
   :alt: Build status

-----
Usage
-----

Options::

   usage: docformatter [-h] [--in-place] [--no-backup] files [files ...]

   Formats docstrings to follow PEP 257.

   positional arguments:
     files        files to format

   optional arguments:
     -h, --help   show this help message and exit
     --in-place   make changes to file instead of printing diff
     --no-backup  do not write backup files
