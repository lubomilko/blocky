###################################################################################################
Usage
###################################################################################################

***************************************************************************************************
Template tags
***************************************************************************************************

.. important:::
    Blocky uses templates containing *tags* to indicate variable parts of the template. By
    default, the tags have an XML-like form using uppercase letters for names, e.g.,
    ``<TAG_NAME>`` is a tag named ``TAG_NAME``.

    The tag names in a Python filling script are automatically converted to an uppercase format
    by default, i.e., it is possible to refer to the ``<TAG_NAME>`` tag using a lowercase name
    ``tag_name`` in the script.

    This tag format and automatic uppercase conversion is used in almost all examples within this
    document. However, the tag format is :ref:`configurable <tgt_config>`, as will be described
    later.

The templates used by Blocky contain two primary elements:

*   **Variables** consisting of a single tag, e.g., ``<VARIABLE>`` representing a variable named
    ``VARIABLE`` that can be set to the required value using a simple string replacement.

*   **Blocks** consisting of a tag start-end pair, e.g., ``<BLOCK>content</BLOCK>`` representing a
    block named ``BLOCK`` having an internal content consisting of a simple string ``content``.
    Apart from string constants, a block can also contain *variables* and other *subblocks*.

    The block content can be *cloned*, i.e., duplicated as many times as needed, and variables in
    each clone can be filled with different values.

    The whole template is a block too, just an unnamed one, i.e, it is not marked by any tag pair.

*Example:*

The following template string contains a single block ``ITEMS`` which contains a single variable
``ITEM`` in its content:

.. code-block::

    template = """
                                SHOPPING LIST
    Items
    -----------------------------------------------------------------------
    <ITEMS>
    * <ITEM>
    </ITEMS>
    """


***************************************************************************************************
Automatic template filling
***************************************************************************************************

TBD