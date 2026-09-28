# Messages
Messages generator with fast pre-styled printers.

## How to use
Generate message with function `generate_message()` and certain type from `MessagesTypes`.

```Python
from dublib.cli.messages.generator import MessagesTypes, generate_message

message: str = generate_message(
	text = "Simple message.",
	message_type = MessagesTypes.Warning,
	origin = __name__,
	colorize = True,
)
print(message) # [warning:main] Simple message.
```
### Generator
```{eval-rst}
.. autofunction:: dublib.cli.messages.generator.generate_message
```

Or use fast pre-styled printers.

```Python
from dublib.cli.messages.printers import print_warning

print_warning(
	text = "Simple text.",
	origin = __name__,
) # [warning:main] Simple message.
```

### Printers
```{eval-rst}
.. automodule:: dublib.cli.messages.printers
    :members:
```