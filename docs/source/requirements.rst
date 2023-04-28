=========================
docformatter Requirements
=========================

The goal of ``docformatter`` is to be an autoformatting tool for producing
PEP 257 compliant docstrings.  This document provides a discussion of the
requirements from various sources for ``docformatter``.  Every effor will be
made to keep this document up to date, but this is not a formal requirements
document and shouldn't be construed as such.

PEP 257 Requirements
--------------------

PEP 257 provides conventions for docstrings.  Conventions are general agreements
or customs of usage rather than strict engineering requirements.  This is
appropriate for providing guidance to a broad community.  In order to provide a
tool for automatically formatting or style checking docstrings, however, some
objective criteria is needed.  Fortunately, the language of PEP 257 lends
itself to defining objective criteria, or requirements, for such tools.

The conventions in PEP 257 define the high-level structure of docstrings:

    * How the docstring needs to be formatted.
    * What information needs to be in a docstring.

PEP 257 explicitly ignores markup syntax in the docstring; these are style
choices left to the individual or organization to enforce.  This gives us two
categories of requirements in PEP 257.  Let's call them  *convention*
requirements and *methodology* requirements to be consistent with PEP 257
terminology.

An autoformatter should produce docstrings with the proper *convention* so tools
such as ``Docutils`` or ``pydocstyle`` can process them properly.  The
contents of a docstring are irrelevant to tools like ``Docutils`` or
``pydocstyle``.  An autoformatter may be able to produce some content, but
much of the content requirements would be difficult at best to satisfy
automatically.

Requirements take one of three types, **shall**, **should**, and **may**.
Various sources provide definitions of, and synonyms for, these words.  But
generally:

    * **Shall** represents an absolute.
    * **Should** represents a goal.
    * **May** represents an option.

Thus, an autoformatting tool:

    * Must produce output that satisfies all the *convention* **shall** requirements.
    * Ought to provide arguments to allow the user to dictate how each *convention* **should** or **may** requirement is interpreted.
    * Would be nice to produce as much output that satisfies the *methodology* requirements.
    * Would be nice to provide arguments to allow the user to turn on/off each *methodology* requirement the tool supports.

Docstring Syntax
----------------

There are at least three "flavors" of docstrings in common use today; Sphinx,
NumPy, and Google.  Each of these docstring flavors follow the PEP 257
*convention* requirements.  What differs between the three docstring flavors
is the reST syntax used in the elaborate description of the multi-line
docstring.

For example, here is how each syntax documents function arguments.

Google syntax:

.. code-block::

    Args:
        param1 (int): The first parameter.

NumPy syntax:

.. code-block::

    Parameters
    ----------
    param1 : int
        The first parameter.

Sphinx syntax:

.. code-block::

    :param param1: The first parameter, defaults to 1.
    :type: int

Syntax is also important to ``Docutils``.  An autoformatter should be aware of
syntactical directives so they can be placed properly in the structure of the
docstring.  To accommodate the various syntax flavors used in docstrings, a
third requirement category is introduced, *style*.

Another consideration in for the *style* category is line wrapping.
According to PEP 257, splitting a one-line docstring is to allow "Emacs’
``fill-paragraph`` command" to be used.  The ``fill-paragraph`` command is a
line-wrapping command.  Additionally, it would be desirable to wrap
docstrings for visual continuity with the code.

NumPy makes a stylistic decision to place a blank line after the long
description.

Some code formatting tools also format docstrings.  For example, black places
a space before a one-line or the summary line when that line begins with a
double quote (").  It would be desirable to provide the user an option to
have docformatter also insert this space for compatibility.

Thus, an autoformatting tool:

    * Ought to provide arguments to allow the user to select the *style* or "flavor" of their choice.
    * Ought to provide arguments to allow the user to, as seamlessly as possible, produce output of a compatible *style* with other formatting tools in the eco-system.
    * Would be nice to to provide short cut arguments that represent aliases for a commonly used group of *style* arguments.

Program Control
---------------

Finally, how the ``docformatter`` tool is used should have some user-defined
options to accommodate various use-cases.  These could best be described as
*stakeholder* requirements.  An autoformatting tool:

    * Ought to provide arguments to allow the user to integrate it into their existing workflow.

Exceptions and Interpretations
``````````````````````````````
As anyone who's ever been involved with turning a set of engineering
requirements into a real world product knows, they're never crystal clear and
they're always revised along the way.  Interpreting and taking exception to
the requirements for an aerospace vehicle would be frowned upon without
involving the people who wrote the requirements.  However, the consequences
for a PEP 257 autoformatting tool doing this are slightly less dire.  We have
confidence the GitHub issue system is the appropriate mechanism if there's a
misinterpretation or inappropriate exception taken.

The following items are exceptions or interpretations of the PEP 257
requirements:

    * One-line and summary lines can end with any punctuation.  ``docformatter`` will recognize any of [. ! ?].  Exception to requirement PEP_257_4.5; consistent with Google style.  See also #56 for situations when this is not desired.
    * One-line and summary lines will have the first word capitalized.  ``docformatter`` will capitalize the first word for grammatical correctness.  Interpretation of requirement PEP_257_4.5.
    * PEP 257 discusses placing closing quotes on a new line in the multi-line section.  However, it really makes no sense here as there is no way this condition could be met for a multi-line docstring.  Given the basis provided in PEP 257, this requirement really applies to wrapped one-liners.  Thus, this is assumed to apply to wrapped one-liners and the closing quotes will be placed on a line by themselves in this case.  However, an argument will be provided to allow the user to select their desired behavior.  Interpretation of requirement PEP_257_5.5.

These give rise to the *derived* requirement category which would also cover
any requirements that must be met for a higher level requirement to be met.

The table below summarizes the requirements for ``docformatter``.  It
includes an ID for reference, the description from PEP 257, which category
the requirement falls in, the type of requirement, and whether
``docformatter`` has implemented the requirement.

.. csv-table:: **PEP 257 Requirements Summary**
    :align: left
    :header: " ID", " Requirement", " Category", " Type", " Implemented"
    :quote: '
    :widths: auto

    ' PEP_257_1','Always use """triple double quotes"""',' Convention',' Shall',' Yes'
    ' PEP_257_2','Use r"""raw triple double quotes""" if you use backslashes.',' Convention',' Shall',' Yes'
    ' PEP_257_3','Use u"""unicode triple double quotes""" for unicode docstrings.',' Convention',' Shall',' Yes'
    ' PEP_257_4','**One-line docstrings:**'
    ' PEP_257_4.1',' Should fit on a single line.',' Convention',' Should',' Yes'
    ' PEP_257_4.2',' Use triple quotes.',' Convention',' Shall',' Yes'
    ' PEP_257_4.3',' Closing quotes are on the same line as opening quotes.',' Convention',' Shall',' Yes'
    ' PEP_257_4.4',' No blank line before or after the docstring.',' Convention',' Shall',' Yes'
    ' PEP_257_4.5',' Is a phrase ending in a period.',' Convention',' Shall',' Yes'
    ' docformatter_4.5.1', ' One-line docstrings may end in any of the following punctuation marks [. ! ?]', ' Derived', ' May', ' Yes'
    ' docformatter_4.5.2', ' One-line docstrings will have the first word capitalized.', ' Derived', ' Shall', ' Yes'
    ' docformatter_4.5.2.1', ' First words in one-line docstrings that are variables or filenames shall remain unchanged.', ' Derived', ' Shall', ' Yes [PR #185, #188]'
    ' docformatter_4.5.2.2', ' First words in one-line docstrings that are user-specified to not be capitalized shall remain unchanged.', ' Derived', ' Shall', ' Yes [PR #194]'
    ' docformatter_4.5.3', ' Shall not place a newline after the first line of a wrapped one-line docstring.' ' Derived', ' Shall', ' Yes [PR #179]'
    ' PEP_257_5','**Multi-line docstrings:**'
    ' PEP_257_5.1',' A summary is just like a one-line docstring.',' Convention',' Shall',' Yes'
    ' docformatter_5.1.1', ' The summary line shall satisfy all the requirements of a one-line docstring.', ' Derived', ' Shall', ' Yes'
    ' PEP_257_5.2',' The summary line may be on the same line as the opening quotes or the next line.',' Convention',' May',' Yes, with option'
    ' PEP_257_5.3',' A blank line.', ' Convention', ' Shall',' Yes'
    ' PEP_257_5.4',' A more elaborate description.',' Convention',' Shall',' Yes'
    ' PEP_257_5.5',' Place the closing quotes on a line by themselves unless the entire docstring fits on a line.',' Convention',' Shall',' Yes, with option'
    ' docformatter_5.5.1', ' An argument should be provided to allow the user to choose where the closing quotes are placed for one-line docstrings.', ' Derived', ' Should', ' Yes [*PR #104*]'
    ' PEP_257_5.6',' Indented the same as the quotes at its first line.',' Convention',' Shall',' Yes'
    ' PEP_257_6','**Class  docstrings:**'
    ' PEP_257_6.1',' Insert blank line after.',' Convention',' Shall',' Yes'
    ' PEP_257_6.2',' Summarize its behavior.',' Methodology',' Should',' No'
    ' PEP_257_6.3',' List the public methods and instance variables.',' Methodology',' Should',' No'
    ' PEP_257_6.4',' List subclass interfaces separately.',' Methodology',' Should',' No'
    ' PEP_257_6.5',' Class constructor should be documented in the __init__ method docstring.',' Methodology',' Should',' No'
    ' PEP_257_6.6',' Use the verb "override" to indicate that a subclass method replaces a superclass method.',' Methodology',' Should',' No'
    ' PEP_257_6.7',' Use the verb "extend" to indicate that a subclass method calls the superclass method and then has additional behavior.', ' Methodology',' Should',' No'
    ' PEP_257_7','**Script docstring:**'
    ' PEP_257_7.1',' Should be usable as its "usage" message.',' Methodology',' Should',' No'
    ' PEP_257_7.2',' Should document the scripts function and command line syntax, environment variables, and files.',' Methodology',' Should',' No'
    ' PEP_257_8','**Module and Package docstrings:**'
    ' PEP_257_8.1',' List classes, exceptions, and functions that are exported by the module with a one-line summary of each.',' Methodology',' Should',' No'
    ' PEP_257_9','**Function and Method docstrings:**'
    ' PEP_257_9.1',' Summarize its behavior.',' Methodology',' Should',' No'
    ' PEP_257_9.2',' Document its arguments, return values(s), side effects, exceptions raised, and restrictions on when it can be called.',' Methodology',' Should',' No'
    ' PEP_257_9.3',' Optional arguments should be indicated.',' Methodology',' Should',' No'
    ' PEP_257_9.4',' Should be documented whether keyword arguments are part of the interface.',' Methodology',' Should',' No'
    ' docformatter_10', '**docstring Syntax**'
    ' docformatter_10.1', ' Should wrap docstrings at n characters.', ' Style', ' Should', ' Yes'
    ' docformatter_10.1.1', ' Shall not wrap lists or syntax directive statements', ' Derived', ' Shall', ' Yes'
    ' docformatter_10.1.1.1', ' Should allow wrapping of lists and syntax directive statements.', ' Stakeholder', ' Should', ' Yes [*PR #5*, *PR #93*]'
    ' docformatter_10.1.2', ' Should allow/disallow wrapping of one-line docstrings.', ' Derived', ' Should', ' No'
    ' docformatter_10.1.3', ' Shall not wrap links that exceed the wrap length.', ' Derived', ' Shall', ' Yes [*PR #114*]'
    ' docformatter_10.1.3.1', ' Shall maintain in-line links on one line even if the resulting line exceeds wrap length.', ' Derived', ' Shall', ' Yes [*PR #152*]'
    ' docformatter_10.1.3.2', ' Shall not place a newline between description text and a wrapped link.', ' Derived', ' Shall', ' Yes [PR #182]'
    ' docformatter_10.2', ' Should format docstrings using NumPy style.', ' Style', ' Should', ' No'
    ' docformatter_10.3', ' Should format docstrings using Google style.', ' Style', ' Should', ' No'
    ' docformatter_10.4', ' Should format docstrings using Sphinx style.', ' Style', ' Should', ' No'
    ' docformatter_10.5', ' Should format docstrings compatible with black.', ' Style', ' Should', ' Yes [PR #192]'
    ' docformatter_10.5.1', ' Should wrap summaries at 88 characters by default in black mode.', ' Style', ' Should', ' Yes'
    ' docformatter_10.5.2', ' Should wrap descriptions at 88 characters by default in black mode.', ' Style', ' Should', ' Yes'
    ' docformatter_10.5.3', ' Should insert a space before the first word in the summary if that word is quoted when in black mode.', ' Style', ' Should', ' Yes'
    ' docformatter_10.5.4', ' Default black mode options should be over-rideable by passing arguments or using configuration files.', ' Style', ' Should', ' Yes'
    ' docformatter_11', '**Program Control**'
    ' docformatter_11.1', ' Should check formatting and report incorrectly documented docstrings.', ' Stakeholder', ' Should', ' Yes [*PR #32*]'
    ' docformatter_11.2', ' Should fix formatting and save changes to file.', ' Stakeholder', ' Should', ' Yes'
    ' docformatter_11.3', ' Should only format docstrings that are [minimum, maximum] lines long.', ' Stakeholder', ' Should', ' Yes [*PR #63*]'
    ' docformatter_11.4', ' Should only format docstrings found between [start, end] lines in the file.', ' Stakeholder', ' Should', ' Yes [*PR #7*}'
    ' docformatter_11.5', ' Should exclude processing directories and files by name.', ' Stakeholder', ' Should', ' Yes'
    ' docformatter_11.6', ' Should recursively search directories for files to check and format.', ' Stakeholder', ' Should', ' Yes [*PR #44*]'
    ' docformatter_11.7', ' Should be able to store configuration options in a configuration file.', ' Stakeholder', ' Should', ' Yes [*PR #77*]'
    ' docformatter_11.7.1', ' Command line options shall take precedence over configuration file options.', ' Derived', ' Shall', ' Yes'
    ' docformatter_11.8',' Should read docstrings from stdin and report results to stdout.', ' Stakeholder', ' Should', ' Yes [*PR #8*]'

Requirement ID's that begin with PEP_257 are taken from PEP 257.  Those
prefaced with docformatter are un-related to PEP 257.

Test Suite
----------

Each requirement in the table above should have one or more test in the test
suite to verify compliance.  Ideally the test docstring will reference the
requirement(s) it is verifying to provide traceability.

Current Implementation
----------------------

``docformatter`` currently provides the following arguments for interacting
with *convention* requirements.
::

    --pre-summary-newline [boolean, default False]
        Boolean to indicate whether to place the summary line on the line after
        the opening quotes in a multi-line docstring.  See requirement
        PEP_257_5.2.

``docformatter`` currently provides these arguments for *style* requirements.
::

    --black [boolean, default False]
        Boolean to indicate whether to format docstrings to be compatible
        with black.
    --blank [boolean, default False]
        Boolean to indicate whether to add a blank line after the
        elaborate description.
    --close-quotes-on-newline [boolean, default False]
        Boolean to indicate whether to place closing triple quotes on new line
        for wrapped one-line docstrings.
    --make-summary-multi-line [boolean, default False]
        Boolean to indicate whether to add a newline before and after a
        one-line docstring.  This option results in non-conventional
        docstrings; violates requirements PEP_257_4.1 and PEP_257_4.3.
    --non-strict [boolean, default False]
        Boolean to indicate whether to ignore strict compliance with reST list
        syntax (see issue #67).
    --pre-summary-space [boolean, default False]
        Boolean to indicate whether to add a space between the opening triple
        quotes and the first word in a one-line or summary line of a
        multi-line docstring.
    --tab-width [integer, defaults to 1]
        Sets the number of characters represented by a tab when line
        wrapping, for Richard Hendricks and others who use tabs instead of
        spaces.
    --wrap-descriptions length [integer, default 79]
        Wrap long descriptions at this length.
    --wrap-summaries length [integer, default 72]
        Wrap long one-line docstrings and summary lines in multi-line
        docstrings at this length.

``docformatter`` currently provides these arguments for *stakeholder* requirements.
::

    --check
        Only check and report incorrectly formatted files.
    --config CONFIG
        Path to the file containing docformatter options.
    --docstring-length min_length max_length
        Only format docstrings that are [min_length, max_length] rows long.
    --exclude
        Exclude directories and files by names.
    --force-wrap
        Force descriptions to be wrapped even if it may result in a mess.
        This should likely be removed after implementing the syntax option.
    --in-place
        Make changes to files instead of printing diffs.
    --range start end
        Only format docstrings that are between [start, end] rows in the file.
    --recursive
        Drill down directories recursively.

Arguments Needed for Future Releases
------------------------------------

The following are new arguments that are needed to implement **should** or
**may** *convention* requirements:
::

    --wrap-one-line [boolean, default False]
        Boolean to indicate whether to wrap one-line docstrings.  Provides
        option for requirement PEP_257_4.1.

The following are new *style* arguments needed to accommodate the various style options:
::

    --syntax [string, default "sphinx"]
        One of sphinx, numpy, or google

Issue and Version Management
----------------------------

As bug reports and feature requests arise in the GitHub issue system, these
will need to be prioritized.  The requirement categories, coupled with the
urgency of the issue reported can be used to provide the general
prioritization scheme:

    * Priority 1: *convention* **bug**
    * Priority 2: *style* **bug**
    * Priority 3: *stakeholder* **bug**
    * Priority 4: *convention* **enhancement**
    * Priority 5: *style* **enhancement**
    * Priority 6: *stakeholder* **enhancement**
    * Priority 7: **chore**

Integration of a bug fix will result in a patch version bump (i.e., 1.5.0 ->
1.5.1).  Integration of one or more enhancements will result in a minor
version bump (i.e., 1.5.0 -> 1.6.0).  One or more release candidates will be
provided for each minor or major version bump.  These will be indicated by
appending `-rcX` to the version number, where the X is the release candidate
number beginning with 1.  Release candidates will not be uploaded to PyPi,
but will be made available via GitHub Releases.