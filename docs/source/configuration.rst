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

In ``pyproject.toml``, add a section ``[tool.docformatter]`` with
options listed using the same name as command line argument.  For example:

.. code-block:: yaml

      [tool.docformatter]
      recursive = true
      wrap-summaries = 82
      blank = true

In ``setup.cfg`` or ``tox.ini``, add a ``[docformatter]`` section.

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

A Note on Options to Control Styles
-----------------------------------
There are various ``docformatter`` options that can be used to control the
style of the docstring.  These options can be passed on the command line or
set in a configuration file.  Currently, the style options are:

    * ``--black``
    * ``-s`` or ``--style``

When passing the ``--black`` option, the following arguments are set
automatically:

    * ``--pre-summary-space`` is set to True
    * ``--wrap-descriptions`` is set to 88
    * ``--wrap-summaries`` is set to 88

All of these options can be overridden from the command line or in the configuration
file.  Further, the ``--pre-summary-space`` option only inserts a space before the
summary when the summary begins with a double quote (").  For example:

    ``"""This summary gets no space."""`` becomes ``"""This summary gets no space."""``

and

    ``""""This" summary does get a space."""`` becomes ``""" "This" summary does get a space."""``

The ``--style`` argument takes a string which is the name of the field list style you
are using.  Currently, only ``sphinx`` and ``epytext`` are recognized, but ``numpy``
and ``google`` are future styles.  For the selected style, each line in the field lists
will be wrapped at the ``--wrap-descriptions`` length as well as any portion of the
elaborate description preceding the parameter list.  Field lists that don't follow the
passed style will cause the entire elaborate description to be ignored and remain
unwrapped.

A Note on reST Header Adornments Regex
--------------------------------------
``docformatter-1.7.2`` added a new option ``--rest-section-adorns``.  This allows for
setting the characters used as overline and underline adornments for reST section
headers.  Per the `ReStructuredText Markup Specification <https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html#sections>`_,
the following are all valid adornment characters,

.. code-block::

    ! " # $ % & ' ( ) * + , - . / : ; < = > ? @ [ \ ] ^ _ ` { | } ~

Thus, the default regular expression ``[!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~]{4,}``
looks for any of these characters appearing at least four times in a row.  Note that the
list of valid adornment characters includes the double quote (") and the greater-than
sign (>).  Four repetitions was selected because:

    * Docstrings open and close with triple double quotes.
    * Doctests begin with >>>.
    * It would be rare for a section header to consist of fewer than four characters.

The user can override this default list of characters by passing a regex from the
command line or setting the ``rest-section-adorns`` option in the configuration file.
It may be usefule to set this regex to only include the subset of characters you
actually use in your docstrings.  For example, to only recognize the recommended list
in the ReStructuredText Markup Specification, the following regular expression would
be used:

.. code-block::

    [=-`:.'"~^_*+#]{4,}
