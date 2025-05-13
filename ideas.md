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
