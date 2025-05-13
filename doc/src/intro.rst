########################################################################################################################
Introduction
########################################################################################################################

`Blocky <https://github.com/lubomilko/blocky>`_ is a lightweight Python templating engine able to generate various types
of text-based files or strings, e.g., source code in various languages, markdown or reStructuredText files, HTML pages,
XML or JSON data files, etc.

Blocky has its name derived from its operational principle - variable parts of a template are enclosed using special
tags into so called *blocks* of strings which can be nested together creating a multi-layered structure of blocks and
their subblocks. Each block in a template can contain multiple variables represented also by appropriate tags. Blocky is
able to extract the string blocks from a template into the Python :py:class:`.Block` objects that provide multipe methods
(:py:meth:`.set_variables`, :py:meth:`.clone`, :py:meth:`.clear`, etc.) to generate the output scontent
using a simple user-defined Python script.

Blocky is developed around the following ideas:

*   **Logic-less templates** - Templates define primarily the formatting part of the content to be generated. Logic to
    fill the data into the variable parts of a template is defined separately in a user-defined Python script.
*   **No custom templating language** - Rendering logic is defined by the Python script importing the :py:mod:`blocky`
    module, i.e., no proprietary language model is used.
*   **No custom data model** - Python script is directly used to read any input data needed to fill the variable parts
    of templates or to control the rendering logic.
*   **Minimalism** - Blocky is a single Python module with no external dependencies. Even usage of built-in Python
    modules is limited to minimum.
*   **Versatility** - There are no restrictions regarding the generated content as long as it is text-based. Data used
    for filling the variable parts of templates do not need to have any predefined format. Template filling logic is
    defined purely by the user-defined Python script, which allows great flexibility.


The logic of the templated content generation heavily relies on the user-defined Python script provided for the
specified template. The following diagram illustrates the processing flow of the content generation:

.. code-block:: text

     template           input data
         |                  |
         V                  V
    python template filling script <- blocky
                   |
                   V
           generated content

The *python template filling script* uses :py:class:`.Block` objects provided by the imported :py:mod:`blocky` module
to fill the variable parts of the *template* with the variable content extracted from the *input data* to generate
the output *generated content*.
