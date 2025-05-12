# Blocky template engine

[Blocky](https://github.com/lubomilko/blocky) is a minimalistic general-purpose Python template
engine able to generate various types of text-based content, e.g., standard text, source code in
various languages, markdown or reStructuredText files, HTML pages, XML or JSON data files, etc.

Please read the [documentation here](https://lubomilko.github.io/blocky).


# Quick start

The following Python script serves as a small illustration of the provided features. The template
is loaded from the `template` string and filled using the `data` dictionary. Then the generated
content is printed at the end.

``` python
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
```

Prints the following generated content:

``` text
                            SHOPPING LIST
  Items                                                         Quantity
------------------------------------------------------------------------
* apples                                                        1 kg
* IMPORTANT! potatoes                                           2 kg
* rice                                                          1 kg
* orange juice                                                  1 l
* MAYBE? cooking magazine


Short list: apples, potatoes, rice, orange juice, cooking magazine
```
