import sys
from pathlib import Path


sys.path.insert(0, str(Path(Path(__file__).parent.parent, "src").resolve()))

from blocky import Block


def demo_item_list_essential() -> None:
    # Define template string.
    tmpl_str = "\n".join((
        "List of items:",
        "<ITEMS>",
        "* <ITEM>",
        "</ITEMS>"))

    # Define the main Block object and set its template string.
    blk_main = Block()
    blk_main.template = tmpl_str
    # Define anothe Block object corresponding to the template block marked by the ITEMS tags.
    # From now on the Block objects are referred to only as "blocks".
    blk_items = blk_main.get_subblock("ITEMS")

    for item_name in ("apples", "oranges", "bananas"):
        # Set value for a template variable marked by the ITEM tag.
        blk_items.set_variables(ITEM=item_name)
        # Clone the content of the ITEMS Block object to allow setting of another ITEM variable.
        blk_items.clone()
    # Set the filled ITEMS block into its parent main block.
    blk_items.set()

    # Print the main block content with filled ITEMS block. Outputs the following string:
    # List of items:
    # * apples
    # * oranges
    # * bananas
    print(f"{blk_main.content}")


def demo_item_lists() -> None:
    item_names = (
        ("red apples", "green apples"),
        ("oranges",),
        ("carrots", "peppers", "tomatoes"),
        ("eggs",),
        ("pen", "pencil"))

    item_numbers = ("2 kg each", 5, "", 10, "")

    blk_file = Block(template="template_item_lists.txt")

    blk_items = blk_file.get_subblock("ITEMS_1")
    blk_items_row = blk_items.get_subblock("ITEMS_ROW")
    for row_names in item_names:
        for name in row_names:
            blk_items_row.set_variables(autoclone=True, ITEM=name)
        blk_items_row.set()
        blk_items.clone()
    blk_items.set()

    blk_items = blk_file.get_subblock("ITEMS_2")
    blk_items_row = blk_items.get_subblock("ITEMS_ROW")
    for row_names in item_names:
        for name in row_names:
            blk_items_row.set_variables(autoclone=True, ITEM=name)
        blk_items_row.set()
        blk_items.clone()
    blk_items.set()

    blk_items = blk_file.get_subblock("ITEMS_3")
    blk_items_row = blk_items.get_subblock("ITEMS_ROW")
    for (i, row_names) in enumerate(item_names):
        for name in row_names:
            blk_items_row.set_variables(autoclone=True, ITEM=name)
        blk_items_row.set()
        blk_items.set_variables(NUM=item_numbers[i])
        blk_items.clone()
    blk_items.set()

    blk_items = blk_file.get_subblock("ITEMS_4")
    blk_items_row = blk_items.get_subblock("ITEMS_ROW")
    blk_items_row.set_variables(ITEM="ITEM NAME")
    blk_items_row.set()
    blk_items.set_variables(NUM="NUMBER")
    blk_items.clone()
    for (i, row_names) in enumerate(item_names):
        for name in row_names:
            blk_items_row.set_variables(autoclone=True, ITEM=name)
        blk_items_row.set()
        blk_items.set_variables(SEP=f"{32*' .'}", NUM=item_numbers[i])
        blk_items.clone()
    blk_items.set()

    blk_file.save_content("generated_item_lists.txt")


def main() -> None:
    demo_item_list_essential()
    demo_item_lists()


if __name__ == "__main__":
    main()
