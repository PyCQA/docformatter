How to Use docformatter
=======================

There are several ways you can use ``docformatter``.  You can use it from the
command line, as a file watcher in PyCharm, in your pre-commit checks, and as
a GitHub action.  However, before you can use ``docformatter``, you'll need
to install it.

Use from the Command Line
-------------------------

To use ``docformatter`` from the command line, simply:

.. code-block:: console

    $ docformatter name_of_python_file.py

``docformatter`` recognizes a number of options for controlling how the tool
runs as well as how it will treat various patterns in the docstrings.  The
help output provides a summary of these options:

.. code-block:: console

    usage: docformatter [-h] [-i | -c] [-d] [-r] [-e [EXCLUDE ...]]
                        [-n [NON-CAP ...]] [-s [style]] [--rest-section-adorns REGEX]
                        [--black] [--wrap-summaries length]
                        [--wrap-descriptions length] [--force-wrap]
                        [--tab-width width] [--blank] [--pre-summary-newline]
                        [--pre-summary-space] [--make-summary-multi-line]
                        [--close-quotes-on-newline] [--range line line]
                        [--docstring-length length length] [--non-strict]
                        [--config CONFIG] [--version] files [files ...]

    Formats docstrings to follow PEP 257.

    positional arguments:
      files                 files to format or '-' for standard in

    optional arguments:
      -h, --help            show this help message and exit
      -i, --in-place        make changes to files instead of printing diffs
      -c, --check           only check and report incorrectly formatted files
      -r, --recursive       drill down directories recursively
      -e, --exclude         in recursive mode, exclude directories and files by names
      -n, --non-cap         list of words not to capitalize when they appear as the
                            first word in the summary

      -s style, --style style
                            the docstring style to use when formatting parameter
                            lists.  One of epytext, sphinx. (default: sphinx)
      --rest-section-adorns REGEX
                            regular expression for identifying reST section adornments
                            (default: [!\"#$%&'()*+,-./\\:;<=>?@[]^_`{|}~]{4,})
      --black               make formatting compatible with standard black options
                            (default: False)
      --wrap-summaries length
                            wrap long summary lines at this length; set to 0 to
                            disable wrapping (default: 79, 88 with --black option)
      --wrap-descriptions length
                            wrap descriptions at this length; set to 0 to disable
                            wrapping (default: 72, 88 with --black option)
      --force-wrap
                            force descriptions to be wrapped even if it may result
                            in a mess (default: False)
      --tab_width width
                            tabs in indentation are this many characters when
                            wrapping lines (default: 1)
      --blank
                            add blank line after elaborate description
                            (default: False)
      --pre-summary-newline
                            add a newline before one-line or the summary of a
                            multi-line docstring
                            (default: False)
      --pre-summary-space
                            add a space between the opening triple quotes and
                            the first word in a one-line or summary line of a
                            multi-line docstring
                            (default: False)
      --make-summary-multi-line
                            add a newline before and after a one-line docstring
                            (default: False)
      --close-quotes-on-newline
                            place closing triple quotes on a new-line when a
                            one-line docstring wraps to two or more lines
                            (default: False)
      --range start_line end_line
                            apply docformatter to docstrings between these lines;
                            line numbers are indexed at 1
      --docstring-length min_length max_length
                            apply docformatter to docstrings of given length range
      --non-strict
                            do not strictly follow reST syntax to identify lists
                            (see issue #67) (default: False)
      --config CONFIG
                            path to file containing docformatter options
                            (default: ./pyproject.toml)
      --version
                            show program's version number and exit

Possible exit codes from ``docformatter``:

- **1** - if any error encountered
- **2** - if it was interrupted
- **3** - if any file needs to be formatted (in ``--check`` or ``--in-place`` mode)

Use as a PyCharm File Watcher
-----------------------------

``docformatter`` can be configured as a PyCharm file watcher to automatically
format docstrings on saving python files.

Head over to ``Preferences > Tools > File Watchers``, click the ``+`` icon
and configure ``docformatter`` as shown below:

.. image:: https://github.com/PyCQA/docformatter/blob/master/docs/images/pycharm-file-watcher-configurations.png?raw=true
   :alt: PyCharm file watcher configurations

Use with pre-commit
-------------------

``docformatter`` is configured for `pre-commit`_ and can be set up as a hook
with the following ``.pre-commit-config.yaml`` configuration:

.. _`pre-commit`: https://pre-commit.com/

.. code-block:: yaml

  - repo: https://github.com/PyCQA/docformatter
    rev: v1.7.5
    hooks:
      - id: docformatter
        additional_dependencies: [tomli]
        args: [--in-place, --config, ./pyproject.toml]

You will need to install ``pre-commit`` and run ``pre-commit install``.

Whether you use ``args: [--check]`` or ``args: [--in-place]``, the commit
will fail if ``docformatter`` processes a change.  The ``--in-place`` option
fails because pre-commit does a diff check and fails if it detects a hook
changed a file.  The ``--check`` option fails because ``docformatter`` returns
a non-zero exit code.

The ``additional_dependencies: [tomli]`` is only required if you are using
``pyproject.toml`` for ``docformatter``'s configuration.

Use with GitHub Actions
-----------------------

``docformatter`` is one of the tools included in the `python-lint-plus`_
action.

.. _`python-lint-plus`: https://github.com/marketplace/actions/python-code-style-quality-and-lint

Dostring Text Patterns
======================

``docformatter`` began as a simple tool to format docstrings to follow PEP257.  It
was originally a single Python script of 118 lines containing seven functions.
That's no longer the case as an inspection of the codebase will show.  Over time,
``docformatter`` has grown to include a number of features that have been requested
by its most fantastic user base.

In the early days, ``docformatter`` only formatted simple docstrings.  "Complex" text
patterns like lists, parameter descriptions, and reStructuredText (reST) sections
caused ``docformatter`` to simply skip formatting the docstring.  As feature requests
have been and will be incorporated, ``docformatter`` has gained the ability to
recognize and format more complex text patterns.

As a result, it is necessary for the user to properly format their docstrings to
follow the patterns documented in the various specifications.  These specifications
would include:

- PEP 257 - Docstring Conventions
    https://www.python.org/dev/peps/pep-0257/
- reStructuredText (reST) Markup Specification
    https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html
- Sphinx Documentation Style
    https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html
- Epydoc Documentation Style
    http://epydoc.sourceforge.net/manual-fields.html

Any docstring that does not follow these specifications may not be formatted properly
as these patterns may be recognized by ``docformatter`` as simple text that needs to
formatted.  For example, if a user writes a docstring that contains a list but does not
format the list according to reST specifications, ``docformatter`` may not recognize
the list and may format the list items as simple text.  This could result in a
list that is not properly indented or wrapped.

The user is encouraged to read and follow these specifications when writing
docstrings to ensure that ``docformatter`` can properly format them.  Issues reported
to the ``docformatter`` project that are the result of docstrings not following these
specifications will be closed as ``S:wontfix`` with a request for the user to update
their docstrings to follow the specifications.

Additionally, as ``docformatter`` continues to add support for more text patterns (e.g.,
Numpy or Google style docstrings), new releases may result in significant docstring
formatting changes in your code base.  While we hate to see this happen to our users,
it is the result of our desire to make ``docformatter`` the best tool it can be for
formatting docstrings and the best way to achieve that is to strigently comply with
the various specifications.  We appreciate your understanding and patience as we
continue to improve ``docformatter``.
