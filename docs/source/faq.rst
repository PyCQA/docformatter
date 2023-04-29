
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
