
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
