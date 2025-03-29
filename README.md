# Blocky template engine

[Blocky](https://github.com/lubomilko/blocky) is a lightweight Python templating engine able to generate various types
of text-based files or strings, e.g., source code in various languages, markdown or reStructuredText files, HTML pages,
XML or JSON data files, etc.


# Quick start

The following example shows a script loading a template from the *template.txt* file, genereting
a content from it using data provided by the `blk_data` dictionary and then saving it into a
*generated.txt* file:

Input *template.txt* file content:

``` text
typedef struct
{
<MEMBERS>
    <TYPE><T> <^TYPE><T> *<^TYPE>const <T> <^TYPE>const <T> *<^TYPE></TYPE><NAME><ARR>[<SIZE>]</ARR>;
</MEMBERS>
}<STRUCT_NAME>;

/* Generated structure members:
<MEMBERS>
* <NAME>
</MEMBERS>
*/

<TO_SET>set content</TO_SET>
<TO_CLEAR>cleared content</TO_CLEAR>

<TO_SET>another set content</TO_SET>
<TO_CLEAR>another cleared content</TO_CLEAR>
```

Script to fill the template:

``` python
blk_data = {
    "to_set": 1,
    "to_clear": 0,
    "struct_name": "SOME_STRUCT_T",
    "members": (
        {"type": {"vari_idx": 0, "t": "UNSIGNED8"}, "name": "u8Var", "arr": None},
        {"type": {"vari_idx": 1, "t": "UNSIGNED16"}, "name": "au16Var", "arr": {"size": 10}},
        {"type": {"vari_idx": 2, "t": "SIGNED8"}, "name": "ps8Var", "arr": None},
        {"type": {"vari_idx": 3, "t": "SIGNED16"}, "name": "aps16Var", "arr": {"size": 20}},
        {"type": {"vari_idx": -1}, "name": "InvalidVar1", "arr": None},
        {"type": {"vari_idx": False}, "name": "InvalidVar2", "arr": None},
        {"type": None, "name": "InvalidVar3", "arr": None},
        {"type": {}, "name": "InvalidVar4", "arr": None})}

blk_file = Block(template="template.txt")
blk_file.fill(blk_data)
blk_file.save_content("generated.txt")
```

Output *generated.txt* file content:

``` text
typedef struct
{
    UNSIGNED8 u8Var;
    UNSIGNED16 *au16Var[10];
    const SIGNED8 ps8Var;
    const SIGNED16 *aps16Var[20];
    InvalidVar1;
    InvalidVar2;
    InvalidVar3;
    InvalidVar4;
}SOME_STRUCT_T;

/*
* u8Var
* au16Var
* ps8Var
* aps16Var
* InvalidVar1
* InvalidVar2
* InvalidVar3
* InvalidVar4
*/

set content


another set content
```

The [documentation](https://lubomilko.github.io/blocky) is still not finished... But the API
chapter provides a description of low-level functions that can be used for template filling
instead of a high-level filling using the `fill()` method as described above.
