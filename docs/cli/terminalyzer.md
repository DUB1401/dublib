# Terminalyzer
This module provides system for parsing and typing CLI parameters with react-like model and automatic help generation.

## How it works
You build commands models in groups and pass it into **Terminalyzer**. Than get your command data as _Shell-like_ string and parse it with command processor.

### Terms
- **Command data** – command identifier plus it parameters.
- **Command identifier** – command identifier is supergroup name and command name. For example, in `create file file.txt` identifier is `["create", "file"]`.
- **Command parameters** – command parameters given from data without identifier. For example, in `create file file.txt` parameters is `["file.txt"]`.
    - **Argument** – value that supports casting to a specific type.
    - **Flag** – logical switcher.
    - **Key** – identifier that indicates the next parameter is a value of a specific type (a named argument that supports logical presence checks).
- **Supergroup** – commands group with activated supergroup argument for semantic naming commands like `crete file …` and `create directory …` instead `touch …` and `mkdir …`.

### Parameters types
|  | Argument | Flag | Key |
|---|---|---|---|
| Named | ❌ | ✅ | ✅ |
| Aliases | ❌ | ✅ | ✅ |
| Checkable | ❌ | ✅ | ✅ |
| Value | ✅ | ❌ | ✅ |
| Typing | ✅ | ❌ | ✅ |
| Example | `value` | `-f` | `--key value` |

## How to use
```Python
from pathlib import Path
from typing import TYPE_CHECKING

from dublib.cli.terminalyzer import ModelsGroup, Terminalyzer
from dublib.functions.filesystem import text
from dublib.validators import ValidableTypes

if TYPE_CHECKING:
    from dublib.cli.terminalyzer.parser.entities import CommandEntity

# Create command handler.
def handler_touch(entity: "CommandEntity"):
    file_path = entity.get_position_value("PATH", expected_type = Path, important = True)
    text.write(file_path, "")

# Initialize models group.
group = ModelsGroup()

# Build model.
model = group.create_model("touch", "Create empty file.")
position = model.create_position("PATH", "File path.")
position.set_argument(ValidableTypes.Path)
model.register_handler(handler_touch)

# Initialize terminalyzer.
terminalyzer = Terminalyzer()
terminalyzer.set_models_groups(group)

# Parse Python script arguments.
entity: "CommandEntity | None" = terminalyzer.parse_command(call_handler = True)

if entity is None:
    print("Command not found.")

# If you don't want to use handlers process entity in another way.
if not entity.is_handled:
    match entity.model.indentificator.as_str():
        case "touch": handler_touch(entity)
```

### Members
```{eval-rst}
.. automodule:: dublib.cli.terminalyzer
    :members:
```

## Helper
**Terminalyzer** also can generate commands lists by groups and info (help functional).
```Python
from dublib.cli.terminalyzer import ModelsGroup
from dublib.cli.terminalyzer.helper import Helper, HelperOptions

group = ModelsGroup()
model = group.create_model("clear", "Clear terminal.")

# Disable commands sorting by names.
options = HelperOptions(
    sort = False,
)

helper = Helper(options)
styled_commands_list: str = helper.generate_group_list(group)
model_info: str = helper.generate_model_info(model)
```

### Members
```{eval-rst}
.. automodule:: dublib.cli.terminalyzer.helper
    :members:
```
