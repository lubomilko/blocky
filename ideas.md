# No whitespace after <+> if new line is the last char

Do not generate whitespaces if the last char is new line (\n). Other repeated characters still
need to be generated.


# Restrict while True loops

Change the "while True" loops to have a finite maximum number of loops to avoid a potential freeze.


# Shortcuts

Shortcut definition using <@...>...</@...> block tags and a shortcut reference by the <@...> tag:
``` text
<@1><VALS><VAL><.>, <^.></.></VALS></@1>

Values: <@1><+>         (<DESCRIPTION>)
```

With `data = {"vals": [{"val": 1}, {"val": 2}, {"val": 3}], "desc": "Just some values."}` it
should generate:
``` text
Values: 1, 2, 3         (Just some values.)
```

# Bugs

Assumming that block blk_b is within the blk_a. The blk_b.set(1) in the following code does not
work. Works only if it's called after blk_a.set_variables(...) as shown by the commented code line.

``` python
for i in i_list:
    blk_b.set(1)
    blk_a.set_variables(...)
    # blk_b.set(1)

    blk_a.clone()
blk_a.set()
```

The blk_a.set_variables(autoclone=True, ...) does not work properly, generates unfilled string at
the end. Works only if blk_a is cloned manually as shown by the commented code line.

``` python
for i in i_list:
    blk_a.set_variables(autoclone=True, ...)
    for j in j_list:
        blk_b.set_variables(autoclone=True, ...)
    blk_b.set()
    # blk_a.clone()
blk_a.set()
```