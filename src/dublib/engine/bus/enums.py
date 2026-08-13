from enum import Enum

class MessagesTypes(Enum):
	"""Перечисление типов сообщений."""

	Debug = "debug"
	Info = "info"
	Warning = "warning"
	Error = "error"
	Critical = "critical"