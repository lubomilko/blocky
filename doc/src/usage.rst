###################################################################################################
Usage
###################################################################################################

The following chapters describe the essential concepts needed for the creation of templates
and for filling them with data to generate an output content.

However, it is also possible to quickly jump to the :ref:`basic <tgt_auto_fill_basic_example>` or
:ref:`advanced <tgt_auto_fill_advanced_example>` example to get a quick overview of all the
principles used in the :ref:`automatic template filling <tgt_auto_fill>`.


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


.. _tgt_basic_tags:

Basic tags
===================================================================================================

The templates used by Blocky contain two primary elements:

*   **Variables** consisting of a single tag, e.g., ``<VARIABLE>`` representing a variable named
    ``VARIABLE`` that can be set to the required value using a simple string replacement.

*   **Blocks** consisting of a tag start-end pair, e.g., ``<BLOCK>content</BLOCK>`` representing a
    block named ``BLOCK`` having an internal content consisting of a simple string ``content``.
    Apart from string constants, a block can also contain *variables* and other *subblocks*.

    A block can have multiple predefined **content variations** with each variation separated by
    a special tag, which by default has a ``<^BLOCK>`` format (this is also
    :ref:`configurable <tgt_config>`). For example, the
    ``<BLOCK>content 1<^BLOCK>content 2<^BLOCK>content 3</BLOCK>`` defines a block with three
    variations of a content selectable by the filling script.

    The standard (non-variation) block content can be **cloned**, i.e., duplicated as many times
    as needed, and variables in each clone can be filled with different values.

.. note::
    The whole template is a block too, just an unnamed one, i.e, it is not marked by any tag pair.


.. _tgt_auto_tags:

Special automatic tags
===================================================================================================

The template can contain special tags that are filled automatically (i.e., without any values
implicitly assigned in the filling script). These special autotags are described below:

*   **Alignment character repeat** tag ``<+>``: A special tag automatically repeating the first
    character located right after this tag until another character is detected in the template
    regardless of the length of a content located before the tag. This special autotag is useful
    for the text alignment.

    Example of a template using the character repeat autotag:

    .. code-block:: text

        <NAME><+>               <SURNAME>

    repeats the space character located after the ``<+>`` tag right until the beginning of a
    surname. This effectively keeps the surname start column always the same, regardless of the
    length of the ``NAME`` variable value, i.e., filling the template using name-surname pairs
    ``John``, ``Connor`` and ``Thomas``, ``Anderson`` results in both surnames aligned to the
    same column:

    .. code-block:: text

        John                    Connor
        Thomas                  Anderson

*   **Clone variation** blocks ``<.>standard<^.>last</.>``: Special
    :ref:`variation-like blocks <tgt_basic_tags>` that can be placed in a block being cloned.
    All content clones, except for the last one, will have the ``standard`` content of the
    *clone variation* autoblock, while the last clone will have the second variation - ``last``.

    It is also possible to define the *clone variation* autoblock with three variants of content:
    ``<.>standard<^.>last<^.>first</.>``, where the ``first`` variation of a content will be
    applied only in the first clone of a parent block. This autoblock can be useful for example
    for the comma-separation of variables within a cloned block.

    Example of a template with the clone variation blocks having the *standard* content set to a
    comma ``, `` and the *last* content set to an empty string ````:

    .. code-block:: text

        <VALUE_LIST><VALUE><.>, <^.></.></VALUE_LIST>

    Cloning the ``VALUE_LIST`` block with values ``1``, ``2``, ``3``, ``4`` set to the ``VALUE``
    variable of each cloned content will result in a following string (notice that the last
    value ``4`` is not followed by a comma):

    .. code-block:: text

        1, 2, 3, 4

.. note::
    The format of the automatic tags can also be customized by the
    :ref:`configuration object <tgt_config>`.


.. _tgt_auto_fill:

***************************************************************************************************
Automatic filling
***************************************************************************************************

The automatic template filling is the simplest way to generate a templated content. The data used
for setting the values in a template is defined by a Python dictionary with keys representing the
template :ref:`variable and block tag names <tgt_basic_tags>`.

To fill the template variables and blocks with data, it is first necessary to load the whole
template into the primary :py:class:`.Block` object. This can be done by setting a template string
text or a text file in the :py:meth:`.Block.__init__` constructor. Alternatively, the
:py:attr:`.Block.template` attribute, or the :py:meth:`.Block.load_template` method can be used.


.. _tgt_auto_fill_basic:

Basic automatic filling
===================================================================================================

The template can be filled by the :py:meth:`.Block.fill` method with the required data dictionary
provided as an argument.

The dictionary values can perform one of the operations in a list below depending on the data
type of the dictionary value:

*   **Setting a variable value** using a **basic data type** (i.e., ``int``, ``float``, ``str``,
    and ``bool``). For example, the key-value dictionary pair ``name: "John"`` sets the variable
    ``name`` to the value ``John``.

*   **Setting a block content** using a **dictionary** (i.e., ``{...}``. For example, the
    ``date: {day: 24, month: December}`` sets the ``date`` block containing two variables ``day``
    and ``month`` set to values ``24``, ``December`` respectively.

*   **Cloning blocks and setting their content** using a **list or tuple of dictionaries**. As an
    example, the ``date: [{day: 24, month: 12}, {day: 25, month: 12}]`` key-value pairt creates
    and sets two clones of a ``date`` block with the ``day`` and ``month`` variables in each block
    clone set to the values ``24``, ``12`` in the first clone and to the ``25``, ``12`` in the
    second clone.


.. _tgt_auto_fill_basic_example:

The following filling script example shows all simple concepts described above, i.e., the template
containing the :ref:`basic tags <tgt_basic_tags>` and also :ref:`automatic tags <tgt_auto_tags>`
filled using the :ref:`basic principles <tgt_auto_fill_basic>` of automatic filling. The template
is defined directly by the ``template`` string and the data to fill the template with are defined
by the ``data`` dictionary.

.. code-block:: python

    import sys

    sys.path.insert(0, f"{sys.path[0]}/relative/path/to/dir/with/blocky")

    from blocky import Block


    template = """
                                SHOPPING LIST
      Items                                                         Quantity
    ------------------------------------------------------------------------
    <ITEMS>
    * <ITEM><+>                                                     <QTY>
    </ITEMS>


    Short list: <ITEMS><ITEM><.>, <^.></.></ITEMS>
    """

    data = {
        "items": [
            {"item": "apples", "qty": "1 kg"},
            {"item": "potatoes", "qty": "2 kg"},
            {"item": "rice", "qty": "1 kg"},
            {"item": "orange juice", "qty": "1 l"},
            {"item": "cooking magazine", "qty": 1},
        ]
    }

    blk = Block(template)
    blk.fill(data)
    print(blk.content)


The script prints the following generated content:

.. code-block:: text

                                SHOPPING LIST
      Items                                                         Quantity
    ------------------------------------------------------------------------
    * apples                                                        1 kg
    * potatoes                                                      2 kg
    * rice                                                          1 kg
    * orange juice                                                  1 l
    * cooking magazine                                              1


    Short list: apples, potatoes, rice, orange juice, cooking magazine

.. note::
    Notice that the template contains two ``ITEMS`` blocks containing the variable ``ITEM`` and
    that both blocks are automatically filled by the same data, since they have the same name.


.. _tgt_auto_fill_advanced:

Advanced automatic filling
===================================================================================================

*   **Setting a block content without setting any of its child elements** by setting the block
    value to a **non-empty string, non-zero numeric value or a boolean true**, i.e.,
    ``date: "anything"``, ``date: 1``, ``date: True`` all set the content of a block amed ``date``
    into the final generated output without explicitly setting any of its internal values or other
    subblocks (it is expected that the block is either constant, i.e., without variables, or the
    variables have been already set).

*   **Setting a block content variation** by a **dictionary with an artificial variable**
    ``vari_idx`` set to a numeric or boolean value with the following meaning:

    -   A numeric value zero or higher sets the specified block variation, e.g.
        ``date: {"vari_idx": 1}`` sets the second content variation of a ``date`` block (value 0
        corresponds to the first variation).
    -   A numeric value below zero removes the block, e.g. ``date: {"vari_idx": -1}`` removes the
        ``date`` block from the generated content.
    -   A boolean ``True`` has the same effect as value zero (i.e., sets the first content
        variation) and boolean ``False`` has the same effect as negative value (i.e., removes
        the block).

*   **Removing a variable** by setting its value to an **empty string or to none**, i.e.,
    ``name: ""`` or ``name: None`` both remove the ``name`` variable from the generated content.

*   **Removing a block** by setting its value to an **empty dictionary, empty list, none, zero,
    or boolean false**, i.e., ``date: {}``, ``date: []``, ``date: None``, ``date: 0``,
    ``date: False`` all remove the ``date`` block from the generated content.


.. _tgt_auto_fill_advanced_example:

The filling script below expands the :ref:`basic automatic filling concepts<tgt_auto_fill_basic>`
with the :ref:`advanced concepts <tgt_auto_fill_advanced>` described above. The template is
defined directly by the ``template`` string and the data to fill the template with are defined by
the ``data`` dictionary.

.. code-block:: python

    import sys

    sys.path.insert(0, f"{sys.path[0]}/relative/path/to/dir/with/blocky")

    from blocky import Block

    template = """
                                SHOPPING LIST
      Items                                                         Quantity
    ------------------------------------------------------------------------
    <ITEMS>
    * <FLAG>IMPORTANT! <^FLAG>MAYBE? </FLAG><ITEM><+>               <QTY><UNIT> kg<^UNIT> l</UNIT>
    </ITEMS>


    Short list: <ITEMS><ITEM><.>, <^.></.></ITEMS>
    """

    data = {
        "items": [
            {"flag": None, "item": "apples", "qty": "1", "unit": True},
            {"flag": True, "item": "potatoes", "qty": "2", "unit": {"vari_idx": 0}},
            {"flag": None, "item": "rice", "qty": "1", "unit": {"vari_idx": 0}},
            {"flag": None, "item": "orange juice", "qty": "1", "unit": {"vari_idx": 1}},
            {"flag": {"vari_idx": 1}, "item": "cooking magazine", "qty": None, "unit": None},
        ]
    }

    blk = Block(template)
    blk.fill(data)
    print(blk.content)

The script prints the following generated content:

.. code-block:: text

                                SHOPPING LIST
    Items                                                           Quantity
    ------------------------------------------------------------------------
    * apples                                                        1 kg
    * IMPORTANT! potatoes                                           2 kg
    * rice                                                          1 kg
    * orange juice                                                  1 l
    * MAYBE? cooking magazine
