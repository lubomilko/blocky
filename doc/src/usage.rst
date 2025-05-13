########################################################################################################################
Usage principles
########################################################################################################################

Using *blocky* to generate a text-based content can be described by the following main steps:

#.  Define the template of the content to be generated. The template consists of static parts and dynamic parts
    defined using :ref:`tags <ref-tags>`.
#.  Define custom python script using the *blocky* module to load the template into the :py:class:`.Block` objects
    and filling the dynamic parts with the required values.
#.  Save the generated content of filled :py:class:`.Block` objects.

.. _ref-tags:


************************************************************************************************************************
Template tags
************************************************************************************************************************

All tags defining the dynamic parts of a template belong to one of the three main categories:

*   **Variables** - Tags to be directly substituted by the required values. Default tag format:

    .. code-block:: text

        <VARIABLE_NAME>

*   **Blocks** - Tags defining the parts of the template that can be extraced into the :py:class:`.Block` objects and
    then processed further, e.g., the blocks can be cloned (duplicated), cleared, etc. The blocks in a template can be
    nested, i.e., it is possible to have multiple layers of subblocks. Block area is defined using two tags indicating
    the beginning and end of the block, except the whole template string that is considered to be a block of its own
    even without the block tags. Default tag format:

    .. code-block:: text

        <BLOCK_NAME>
        ...
        </BLOCK_NAME>
    
    where the three dots ``...`` represent a block content with static parts and dynamic variables and potentially
    other subblocks.
    
    alternative for single-line blocks:

    .. code-block:: text

        <BLOCK_NAME>...</BLOCK_NAME>

*   **Special** - Tags with predefined special formatting or other purposes. These tags are handled automatically
    by blocky, i.e., they are typically not meant to be processed manually by the user-defined template filling script.

.. note::
    The template tag names in this documentation and examples use uppercase letters with underscores for word
    separation, e.g., ``<TAG_NAME>``. However, this convention is not mandatory.

    The angle brackets ``<>`` and other characters used for the tag definition can be customized, i.e., changed
    with other characters (or strings) by the :py:class:`.TagsFormat` subobject of the :py:class:`.BlockConfig`
    object which can then be assigned to the :py:attr:`.Block.config` attribute of the :py:class:`.Block` object.
    The details of tag customization will be described later.


########################################################################################################################
Manual template filling
########################################################################################################################

Blocky provides the :py:class:`.Block` class to define objects corresponding to the blocks defined within the template.
The :py:class:`.Block` objects can then be used in the user-defined script to "fill" the template with required values.
Manually using the :py:class:`.Block` object methods and attributes provides a precise control over the generated
content creation and allows to use any data to fill the dynamic parts of the template.

************************************************************************************************************************
Loading the block template
************************************************************************************************************************

The template string needs to be loaded into the primary :py:class:`.Block` object first. This object can then be used to
fill the template, i.e., to create the required generated content. It often makes sense to define the template in a
text-based file, which can then be loaded using the :py:meth:`.load_template` method as illustrated below:

*C:/template.txt* file content:

.. code-block:: text

    List of items:
    <ITEMS>
    * <ITEM>
    </ITEMS>

User defined Python script:

.. code-block:: python

    from blocky import Block

    # Create the main Block object.
    blk_main = Block()
    # Load the Block object template from file.
    blk_main.load_template("C:/template.txt")

Alternatively, the template can be set in the :py:class:`.Block` object definition, through the :py:attr:`.template`
attribute or using the :py:meth:`.load_template` method which also supports string arguments:

.. code-block:: python

    from blocky import Block

    # Option 1: Set the template file in the Block object definition.
    blk_main = Block("C:/template.txt")
    # Option 2: Set the template string in the Block object definition.
    blk_main = Block("Name: <NAME> <SURNAME>, Age: <AGE>")
    # Option 3: Set the template string through an attribute.
    blk_main.template = "Name: <NAME> <SURNAME>, Age: <AGE>"
    # Option 4: Load the template from a string instead of the file.
    blk_main.load_template("Name: <NAME> <SURNAME>, Age: <AGE>")


************************************************************************************************************************
Getting subblocks
************************************************************************************************************************


************************************************************************************************************************
Setting and clearing block variables
************************************************************************************************************************


************************************************************************************************************************
Cloning blocks
************************************************************************************************************************


************************************************************************************************************************
Setting, clearing and resetting blocks
************************************************************************************************************************


************************************************************************************************************************
Saving the generated block content
************************************************************************************************************************


########################################################################################################################
Automated template filling
########################################################################################################################

.. warning::
    The documentation is in progress. In the meantime please see some basic examples of use in the *samples* and also
    *test* directories in the `Blocky repository <https://github.com/lubomilko/blocky>`_.
