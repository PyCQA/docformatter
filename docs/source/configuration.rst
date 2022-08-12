
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
