###################################################################################################
Introduction
###################################################################################################

`Blocky <https://github.com/lubomilko/blocky>`_ is a minimalistic generic Python template engine
able to generate various types of text-based content, e.g., standard text, source code in various
languages, markdown or reStructuredText files, HTML pages, XML or JSON data files, etc.

The form of a content to be generated is defined by the templates and the logic of filling the
template with data is defined by a user-defined Python script as illustrated on a diagram below:

.. code-block:: text

    +----------+   +------------+
    | template |   | input data |
    +----------+   +------------+
          |               |
          V               V
      +-----------------------+
      | Python filling script |
      |     using blocky      |
      +-----------------------+
                  |
                  V
        +-------------------+
        | generated content |
        +-------------------+

The template and input data can be external (i.e., suitable input files) or they can be a part of
the filling script itself.

**No custom template engine language is used**. The filling logic is controlled purely by Python
using a few methods from the blocky module.
