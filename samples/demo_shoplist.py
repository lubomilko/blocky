# pylint: disable = missing-module-docstring, missing-class-docstring, missing-function-docstring
import sys

sys.path.insert(0, f"{sys.path[0]}/../src")

from blocky import Block    # pylint: disable = wrong-import-position   # noqa E402


def demo_shoplist() -> None:
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


def demo_shoplist_1() -> None:
    template = """
                            SHOPPING LIST
  Items
-----------------------------------------------------------------------
<ITEMS>
* <ITEM>
</ITEMS>
"""

    data = {
        "items": [
            {"item": "apples", "qty": "1 kg"},
            {"item": "potatoes", "qty": "2 kg"},
            {"item": "rice", "qty": "1 kg"},
            {"item": "cooking magazine", "qty": None},
        ]
    }

    blk = Block(template)
    blk.fill(data)
    print(blk.content)


if __name__ == "__main__":
    demo_shoplist_1()
    demo_shoplist()
