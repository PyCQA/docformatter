============
docformatter
============

Formats docstrings to follow `PEP 257`_.

.. _`PEP 257`: http://www.python.org/dev/peps/pep-0257/

.. image:: https://secure.travis-ci.org/myint/docformatter.png
   :target: https://secure.travis-ci.org/myint/docformatter
   :alt: Build status

--------
Features
--------

docformatter currently automatically formats docstrings to follow a subset of
the PEP 257 conventions. Below are the relevant items quoted from PEP 257.

- For consistency, always use triple double quotes around docstrings.
- Triple quotes are used even though the string fits on one line.
- Multi-line docstrings consist of a summary line just like a one-line
  docstring, followed by a blank line, followed by a more elaborate
  description.
- The BDFL recommends inserting a blank line between the last paragraph
  in a multi-line docstring and its closing quotes, placing the closing
  quotes on a line by themselves.

-------
Example
-------

After running::

    $ docformatter example.py

this code::

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


gets formatted into this::

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

-------
Options
-------

Below is the help output::

    usage: docformatter [-h] [--in-place] [--no-backup]
                        [--wrap-long-summaries LENGTH] [--version]
                        files [files ...]

    Formats docstrings to follow PEP 257.

    positional arguments:
      files                 files to format

    optional arguments:
      -h, --help            show this help message and exit
      --in-place            make changes to files instead of printing diffs
      --no-backup           do not write backup files
      --wrap-long-summaries LENGTH
                            wrap long summary lines at this length (default: 0)
      --version             show program's version number and exit

------
Issues
------

Issues can be reported on the `GitHub page`_.

.. _`GitHub page`: https://github.com/myint/docformatter/issues
