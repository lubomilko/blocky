# Blocky template engine

[Blocky](https://github.com/lubomilko/blocky) is a minimalistic generic Python template engine
able to generate various types of text-based content, e.g., standard text, source code in various
languages, markdown or reStructuredText files, HTML pages, XML or JSON data files, etc.


# Quick start

The following Python script illustrates most of the high-level automated template filling features.
The template is loaded from the `template` string and filled using the `data` dictionary. Then the
generated content is printed at the end.

``` python
import sys

sys.path.insert(0, f"{sys.path[0]}/relative/path/to/dir/with/blocky")

from blocky import Block


template = """
                            SHOPPING LIST
  Items                                                        Quantity
-----------------------------------------------------------------------
<ITEMS>
* <FLAG>IMPORTANT! <^FLAG>MAYBE? </FLAG><ITEM><+>              <QTY>
<ALT_WRAP>
  - alternatives: <ALTS><ITEM><.>, <^.></.></ALTS>
</ALT_WRAP>
</ITEMS>


Short list: <ITEMS><ITEM><.>, <^.></.></ITEMS>
"""

data = {
    "items": [
        {"flag": None, "item": "apples", "qty": "1 kg", "alt_wrap":
          {"alts": [{"item": "pears"}]}},
        {"flag": {"vari_idx": 0}, "item": "potatoes", "qty": "2 kg", "alt_wrap": None},
        {"flag": None, "item": "rice", "qty": "1 kg", "alt_wrap":
          {"alts": [{"item": "pasta"}, {"item": "quinoa"}, {"item": "couscous"}]}},
        {"flag": {"vari_idx": 1}, "item": "cooking magazine", "qty": None, "alt_wrap": None},
    ]
}

blk = Block(template)
blk.fill(data)
print(blk.content)
```

Prints the following generated content:

``` text
                            SHOPPING LIST
  Items                                                        Quantity
-----------------------------------------------------------------------
* apples                                                       1 kg
  - alternatives: pears
* IMPORTANT! potatoes                                          2 kg
* rice                                                         1 kg
  - alternatives: pasta, quinoa, couscous
* MAYBE? cooking magazine


Short list: apples, potatoes, rice, cooking magazine
```

## Template basics

The template contains the following important elements:

* **Variables** consisting of a single XML-like tag, i.e.: `<VARIABLE>`. Useful for simple string
  replacement.

* **Blocks** consisting of XML-like tag pairs: `<BLOCK>content</BLOCK>`. The whole template is
  a block too, just an unnamed one. Blocks can contain variables and other subblocks. Blocks can
  be cloned, i.e., duplicated as many times as needed.

* **Variation blocks** providing a selectable content:
  `<BLOCK>content variation 1<^BLOCK>content variation 2</BLOCK>`.

  There can be two or more variations of the content separated by the `<^BLOCK>` tags.

  Variation blocks cannot be cloned, they must be placed within the standard cloned blocks if
  cloning is needed.

* **Autorepeat** tag `<+>`. Special tag automatically repeating the first character located
  right after this tag until another character is detected. Useful for text alignment.
  Can repeat also non-whitespace characters, e.g. dots: `<ITEM><+>...................<QTY>`.

* **Autovariation** blocks: `<.>std<^.>last</.>`. Special variation-like blocks to be
  placed in a parent block being cloned. All clones except for the last one will automatically
  have the first variation - `std` defined by the autovariation block and the last clone will
  have the second variation - `last`.

  It is possible to define an autovariation block with three variants of content:
  `<.>std<^.>last<^.>first</.>`, where the `first` variation of a content is applied
  only in the first clone of a parent block.

> *Note:* All tags must use uppercase letters, but can be referenced by lowercase letters
> in the data dictionary.


## Dictionary content data basics

A Python dictionary can be used to fill the template by the `fill()` method to generate an output
content using the principles below:

* Template **variables** and **blocks** are represented by the dictionary keys. The dictionary
  values are used to fill the corresponding template variables and blocks as described below:

  - Simple type values (string, number, boolean) correspond to template variable values.
    - `variable: value`: Simple setting of a `<VARIABLE>` tag to the `value`.
  - Dictionary holds the template block content values.
    - `block: {variable: value, ...}`: Setting variables within block tags
      `<BLOCK> ... </BLOCK>`.
  - List or tuple defines the content of multiple block clones.
    - `block: [{variable: value_1, ...}, {variable: value_2, ...}]`: Cloning the content defined
      by block tags `<BLOCK> ... </BLOCK>` and setting variables within each clone to different
      values.

* **Variable removal** can be done by setting its value to an empty string or `None`, e.g.:
  `variable: ""` or `variable: None`.

* **Block removal** can be done by setting its value to an empty dictionary, empty list, `None`,
  `0` or `False`, e.g.: `block: {}`, `block: []`, `block: None`, `block: 0`, `block: False`.

* **Block setting** without setting any of its child variables or subblocks (useful when a
  block content is constant, i.e., without child variables and subblocks) can be done by setting
  its value to a non-empty string, non-zero numeric value or `True`, e.g.: `block: "anything"`,
  `block: 1`, `block: True`.

* Selection of a **block content variation** is done by setting the artificial variable `vari_idx`
  within the block to a numeric or boolean value with the following meaning:

  - Positive or zero value sets the specified block variation, e.g. `block: {"vari_idx": 1}`
    sets the second content variation of a template block `<BLOCK>` (value 0 corresponds to the
    first variation).
  - Numeric value below zero removes the block, e.g. `block: {"vari_idx": -1}` removes the
    template block `<BLOCK>` completely.
  - `True` sets the first content variation, i.e., has the same effect as setting the `vari_idx`
    to `1`.
  - `False` removes the block, i.e., has the same effect as setting the `vari_idx` to negative
    value.


> *Note:* The [documentation](https://lubomilko.github.io/blocky) is still not finished...
> But the API chapter provides a description of low-level features that can be used instead
> of a high-level filling by the `fill()` method illustrated above.
