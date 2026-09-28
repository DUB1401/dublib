from enum import Enum

class MessagesTypes(Enum):
	"""Messages types enumeration."""

	Debug = "debug"
	Info = "info"
	Warning = "warning"
	Error = "error"
	Critical = "critical"
