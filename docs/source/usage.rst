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

    usage: docformatter [-h] [-i | -c] [-r] [--wrap-summaries length]
                        [--wrap-descriptions length] [--blank]
                        [--pre-summary-newline] [--make-summary-multi-line]
                        [--force-wrap] [--range start_line end_line]
                        [--docstring-length min_length max_length]
                        [--config CONFIG] [--version]
                        files [files ...]

    Formats docstrings to follow PEP 257.

    positional arguments:
      files                 files to format or '-' for standard in

    optional arguments:
      -h, --help            show this help message and exit
      -i, --in-place        make changes to files instead of printing diffs
      -c, --check           only check and report incorrectly formatted files
      -r, --recursive       drill down directories recursively
      -e, --exclude         in recursive mode, exclude directories and files by names

      --wrap-summaries length
                            wrap long summary lines at this length; set
                            to 0 to disable wrapping
                            (default: 79)
      --wrap-descriptions length
                            wrap descriptions at this length; set to 0 to
                            disable wrapping
                            (default: 72)
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
      --force-wrap
                            force descriptions to be wrapped even if it may result
                            in a mess (default: False)
      --tab_width width
                            tabs in indentation are this many characters when
                            wrapping lines (default: 1)
      --range start_line end_line
                            apply docformatter to docstrings between these lines;
                            line numbers are indexed at 1
      --docstring-length min_length max_length
                            apply docformatter to docstrings of given length range
      --non-strict
                            do not strictly follow reST syntax to identify lists
                            (see issue #67)
                            (default: False)
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
    rev: v1.5.0
    hooks:
      - id: docformatter
        args: [--in-place --config ./pyproject.toml]

You will need to install ``pre-commit`` and run ``pre-commit install``.

Whether you use ``args: [--check]`` or ``args: [--in-place]``, the commit
will fail if ``docformatter`` processes a change.  The ``--in-place`` option
fails because pre-commit does a diff check and fails if it detects a hook
changed a file.  The ``--check`` option fails because ``docformatter`` returns
a non-zero exit code.

Use with GitHub Actions
-----------------------

``docformatter`` is one of the tools included in the `python-lint-plus`_
action.

.. _`python-lint-plus`: https://github.com/marketplace/actions/python-code-style-quality-and-lint
