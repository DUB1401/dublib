# Patcher
This module provides text file patching operator with simple editing methods.

It is important to remember that when new line characters are added to a file, the line indexing changes!

## How to use
```Python
from dublib.engine.patcher import Patch

patch = Patch("file.py")
patch.replace("var: str", "variable: str") # Rename variable.
patch.prepend_line(0, "# ") # Comment first line.

if patch.save():
    print("Patch saved.")
else:
    print("No changes.")
```

## Members
```{eval-rst}
.. automodule:: dublib.engine.patcher
	:members:
```