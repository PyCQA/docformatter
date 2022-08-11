How to Use docformatter
=======================

There are several ways you can use ``docformatter``.  You can use it from the
command line, as a file watcher in PyCharm, in your pre-commit checks, and as
a GitHub action.  However, before you can use ``docformatter``, you'll need
to install it.

Installation
------------
The latest released version of ``docformatter`` is available from PyPi.  To
install it using pip:

.. code-block:: console

    $ pip install --upgrade docformatter

Or, if you want to use pyproject.toml to configure ``docformatter``:

.. code-block:: console

    $ pip install --upgrade docformatter[tomli]

If you'd like to use an unreleased version, you can also use pip to install
``docformatter`` from GitHub.

.. code-block:: console

    $ python -m pip install git+https://github.com/PyCQA/docformatter.git@v1.5.0-rc1

Replace the tag ``v1.5.0-rc1`` with a commit SHA to install an untagged
version.

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
      -e, --exclude         exclude directories and files by names

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
- **3** - if any file needs to be formatted (in ``--check`` mode)

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

How to Configure docformatter
=============================

The command line options for ``docformatter`` can also be stored in a
configuration file.  Currently only ``pyproject.toml``, ``setup.cfg``, and
``tox.ini`` are supported.  The configuration file can be passed with a full
path.  For example:

.. code-block:: console

      $ docformatter --config ~/.secret/path/to/pyproject.toml

If no configuration file is explicitly passed, ``docformatter`` will search
the current directory for the supported files and use the first one found.
The order of precedence is ``pyproject.toml``, ``setup.cfg``, then ``tox.ini``.

In any of the configuration files, add a section ``[tool.docformatter]`` with
options listed using the same name as command line options.  For example:

.. code-block:: yaml

      [tool.docformatter]
      recursive = true
      wrap-summaries = 82
      blank = true

The ``setup.cfg`` and ``tox.ini`` files will also support the
``[tool:docformatter]`` syntax.

Known Issues and Idiosyncrasies
===============================

There are some know issues or idiosyncrasies when using ``docformatter``.
These are stylistic issues and are in the process of being addressed.

Wrapping Descriptions
---------------------

``docformatter`` will wrap descriptions, but only in simple cases. If there is
text that seems like a bulleted/numbered list, ``docformatter`` will leave the
description as is:

.. code-block:: rest

    - Item one.
    - Item two.
    - Item three.

This prevents the risk of the wrapping turning things into a mess. To force
even these instances to get wrapped use ``--force-wrap``.  This is being
addressed by the constellation of issues related to the various syntaxes used
in docstrings.

Interaction with Black
----------------------

Black places a space between the opening triple quotes and the first
character, but only if the first character is a quote.  Thus, black turns this:

.. code-block:: rest

    """"Good" politicians don't exist."""

into this:

.. code-block:: rest

    """ "Good" politicians don't exist."""

``docformatter`` will then turn this:

.. code-block:: rest

    """ "Good" politicians don't exist."""

into this:

.. code-block:: rest

    """"Good" politicians don't exist."""

If you pass the ``--pre-summary-space`` option to ``docformatter``, this:

.. code-block:: rest

    """Good, politicians don't exist."""

becomes this:

.. code-block:: rest

    """ Good, politicians don't exist."""

which black will turn into this:

.. code-block:: rest

    """Good, politicians don't exist."""

For now, you'll have to decide whether you like chickens or eggs and then
execute the tools in the order you prefer.  This is being addressed by issue
#94.
