###################################################################################################
Introduction
###################################################################################################

`Blocky <https://github.com/lubomilko/blocky>`_ is a minimalistic general-purpose Python template
engine able to generate various types of text-based content, e.g., standard text, source code in
various languages, markdown or reStructuredText files, HTML pages, XML or JSON data files, etc.

The form of a content to be generated is defined by the template and the logic of filling the
template with data is defined by the user-defined Python script as illustrated on the diagram
below:

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

The template and input data can be external (i.e., in suitable input files) or they can be a part
of the filling script itself.

The filling logic is controlled purely by Python using the blocky module. No custom template
engine language is used
