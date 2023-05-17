How to Install docformatter
===========================

Install from PyPI
-----------------
The latest released version of ``docformatter`` is available from PyPI.  To
install it using pip:

.. code-block:: console

    $ pip install --upgrade docformatter

Extras
``````
If you want to use pyproject.toml to configure ``docformatter``, you'll need
to install with TOML support:

.. code-block:: console

    $ pip install --upgrade docformatter[tomli]

This is only necessary if you are using Python < 3.11.  Beginning with Python 3.11,
docformatter will utilize ``tomllib`` from the standard library.

Install from GitHub
-------------------

If you'd like to use an unreleased version, you can also use pip to install
``docformatter`` from GitHub.

.. code-block:: console

    $ python -m pip install git+https://github.com/PyCQA/docformatter.git@v1.5.0-rc1

Replace the tag ``v1.5.0-rc1`` with a commit SHA to install an untagged
version.
