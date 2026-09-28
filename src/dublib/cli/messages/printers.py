from .generator import generate_message
from .types import MessagesTypes

def print_message(text: str, message_type: MessagesTypes | None = None, origin: str | None = None):
	"""
	Print styled message in terminal.

	:param text: Message text.
	:type text: str
	:param message_type: Message type.
	:type message_type: MessagesTypes | None
	:param origin: Message origin.
	:type origin: str | None
	"""

	print(generate_message(text, message_type, origin))

def print_debug(text: str, origin: str | None = None):
	"""
	Print styled **debug** message in terminal.

	:param text: Message text.
	:type text: str
	:param origin: Message origin.
	:type origin: str | None
	"""

	print_message(text, message_type = MessagesTypes.Debug, origin = origin)

def print_info(text: str, origin: str | None = None):
	"""
	Print styled **info** message in terminal.

	:param text: Message text.
	:type text: str
	:param origin: Message origin.
	:type origin: str | None
	"""

	print_message(text, message_type = MessagesTypes.Info, origin = origin)

def print_warning(text: str, origin: str | None = None):
	"""
	Print styled **warning** message in terminal.

	:param text: Message text.
	:type text: str
	:param origin: Message origin.
	:type origin: str | None
	"""

	print_message(text, message_type = MessagesTypes.Warning, origin = origin)

def print_error(text: str, origin: str | None = None):
	"""
	Print styled **error** message in terminal.

	:param text: Message text.
	:type text: str
	:param origin: Message origin.
	:type origin: str | None
	"""

	print_message(text, message_type = MessagesTypes.Error, origin = origin)

def print_critical(text: str, origin: str | None = None):
	"""
	Print styled **critical** message in terminal.

	:param text: Message text.
	:type text: str
	:param origin: Message origin.
	:type origin: str | None
	"""

	print_message(text, message_type = MessagesTypes.Critical, origin = origin)
