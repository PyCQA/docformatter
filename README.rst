============
docformatter
============

.. |CI| image:: https://img.shields.io/github/actions/workflow/status/PyCQA/docformatter/ci.yml?branch=master
    :target: https://github.com/PyCQA/docformatter/actions/workflows/ci.yml
.. |COVERALLS| image:: https://img.shields.io/coveralls/github/PyCQA/docformatter
    :target: https://coveralls.io/github/PyCQA/docformatter
.. |CONTRIBUTORS| image:: https://img.shields.io/github/contributors/PyCQA/docformatter
    :target: https://github.com/PyCQA/docformatter/graphs/contributors
.. |COMMIT| image:: https://img.shields.io/github/last-commit/PyCQA/docformatter
.. |BLACK| image:: https://img.shields.io/badge/%20style-black-000000.svg
    :target: https://github.com/psf/black
.. |ISORT| image:: https://img.shields.io/badge/%20imports-isort-%231674b1
    :target: https://pycqa.github.io/isort/
.. |SELF| image:: https://img.shields.io/badge/%20formatter-docformatter-fedcba.svg
    :target: https://github.com/PyCQA/docformatter
.. |SPHINXSTYLE| image:: https://img.shields.io/badge/%20style-sphinx-0a507a.svg
    :target: https://www.sphinx-doc.org/en/master/usage/index.html
.. |NUMPSTYLE| image:: https://img.shields.io/badge/%20style-numpy-459db9.svg
    :target: https://numpydoc.readthedocs.io/en/latest/format.html
.. |GOOGSTYLE| image:: https://img.shields.io/badge/%20style-google-3666d6.svg
    :target: https://google.github.io/styleguide/pyguide.html#s3.8-comments-and-docstrings

.. |VERSION| image:: https://img.shields.io/pypi/v/docformatter
.. |LICENSE| image:: https://img.shields.io/pypi/l/docformatter
.. |PYVERS| image:: https://img.shields.io/pypi/pyversions/docformatter
.. |PYMAT| image:: https://img.shields.io/pypi/format/docformatter
.. |DD| image:: https://img.shields.io/pypi/dd/docformatter

+----------------+----------------------------------------------------------+
| **Code**       + |BLACK| |ISORT|                                          +
+----------------+----------------------------------------------------------+
| **Docstrings** + |SELF| |NUMPSTYLE|                                       +
+----------------+----------------------------------------------------------+
| **GitHub**     + |CI| |CONTRIBUTORS| |COMMIT|                             +
+----------------+----------------------------------------------------------+
| **PyPi**       + |VERSION| |LICENSE| |PYVERS| |PYMAT| |DD|                +
+----------------+----------------------------------------------------------+

Formats docstrings to follow `PEP 257`_.

.. _`PEP 257`: http://www.python.org/dev/peps/pep-0257/

Features
========

``docformatter`` automatically formats docstrings to follow a subset of the PEP
257 conventions. Below are the relevant items quoted from PEP 257.

- For consistency, always use triple double quotes around docstrings.
- Triple quotes are used even though the string fits on one line.
- Multi-line docstrings consist of a summary line just like a one-line
  docstring, followed by a blank line, followed by a more elaborate
  description.
- Unless the entire docstring fits on a line, place the closing quotes
  on a line by themselves.

``docformatter`` also handles some of the PEP 8 conventions.

- Don't write string literals that rely on significant trailing
  whitespace. Such trailing whitespace is visually indistinguishable
  and some editors (or more recently, reindent.py) will trim them.

See the the full documentation at `read-the-docs`_, especially the
`requirements`_ section for a more detailed discussion of PEP 257 and other
requirements.

.. _read-the-docs: https://docformatter.readthedocs.io
.. _requirements: https://docformatter.readthedocs.io/en/latest/requirements.html

Installation
============

From pip::

    $ pip install --upgrade docformatter

Or, if you want to use pyproject.toml to configure docformatter::

    $ pip install --upgrade docformatter[tomli]

Or, if you want to use a release candidate (or any other tag)::

    $ pip install git+https://github.com/PyCQA/docformatter.git@<RC_TAG>

Where <RC_TAG> is the release candidate tag you'd like to install.  Release
candidate tags will have the format v1.6.0-rc1  Release candidates will also be
made available as a Github Release.

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

Marketing
=========
Do you use *docformatter*?  What style docstrings do you use?  Add some badges to your project's **README** and let everyone know.

|SELF|

.. code-block::

    .. image:: https://img.shields.io/badge/%20formatter-docformatter-fedcba.svg
        :target: https://github.com/PyCQA/docformatter

|SPHINXSTYLE|

.. code-block::

    .. image:: https://img.shields.io/badge/%20style-sphinx-0a507a.svg
        :target: https://www.sphinx-doc.org/en/master/usage/index.html

|NUMPSTYLE|

.. code-block::

    .. image:: https://img.shields.io/badge/%20style-numpy-459db9.svg
        :target: https://numpydoc.readthedocs.io/en/latest/format.html

|GOOGSTYLE|

.. code-block::

    .. image:: https://img.shields.io/badge/%20style-google-3666d6.svg
        :target: https://google.github.io/styleguide/pyguide.html#s3.8-comments-and-docstrings

Issues
======

Bugs and patches can be reported on the `GitHub page`_.

.. _`GitHub page`: https://github.com/PyCQA/docformatter/issues
