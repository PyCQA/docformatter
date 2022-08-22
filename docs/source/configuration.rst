
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

In ``pyproject.toml`` or ``tox.ini``, add a section ``[tool.docformatter]`` with
options listed using the same name as command line argument.  For example:

.. code-block:: yaml

      [tool.docformatter]
      recursive = true
      wrap-summaries = 82
      blank = true

In ``setup.cfg``, add a ``[docformatter]``, ``[tool.docformatter]``, or
``[tool:docformatter]`` section.

.. code-block:: yaml

      [docformatter]
      recursive = true
      wrap-summaries = 82
      blank = true

Command line arguments will take precedence over configuration file settings.
For example, if the following is in your ``pyproject.toml``

.. code-block:: yaml

      [tool.docformatter]
      recursive = true
      wrap-summaries = 82
      wrap-descriptions = 81
      blank = true

And you invoke docformatter as follows:

.. code-block:: console

      $ docformatter --config ~/.secret/path/to/pyproject.toml --wrap-summaries 68

Summaries will be wrapped at 68, not 82.
