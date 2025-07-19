from ..TextStyler import Codes, TextStyler
from .. import readline

import enum

#==========================================================================================#
# >>>>> ПЕРЕЧИСЛЕНИЯ <<<<< #
#==========================================================================================#

class MessagesTypes(enum.Enum):
	"""Перечисление типов сообщений."""

	Info = "info"
	Warning = "warning"
	Error = "error"
	Critical = "critical"

#==========================================================================================#
# >>>>> ФУНКЦИИ ГЕНЕРАЦИИ И ВЫВОДА СООБЩЕНИЙ <<<<< #
#==========================================================================================#

def GenerateMessage(text: str, type: MessagesTypes | None = None, origin: str | None = None) -> str:
	"""
	Генерирует сообщение на основе переданных параметров.

	:param text: Текст сообщения.
	:type text: str
	:param type: Тип сообщения.
	:type type: MessagesTypes | None
	:param origin: Источник сообщения.
	:type origin: str | None
	:return: Текст сообщения в формате `[{ORIGIN}:{TYPE}] {MESSAGE}`.
	:rtype: str
	"""

	OriginPart = ""
	TypePart = ""
	if origin: OriginPart = f"{origin}:"
	if type: TypePart = f"[{OriginPart}{type.name.upper()}] "

	return f"{TypePart}{text}"

def PrintMessage(text: str, type: MessagesTypes | None = None, origin: str | None = None):
	"""
	Выводит в консоль стилизованное сообщение.

	:param text: Текст сообщения.
	:type text: str
	:param type: Тип сообщения.
	:type type: MessagesTypes | None
	:param origin: Источник сообщения.
	:type origin: str | None
	"""

	ColorsDict = {
		MessagesTypes.Info: Codes.Colors.White,
		MessagesTypes.Error: Codes.Colors.Red,
		MessagesTypes.Warning: Codes.Colors.Yellow,
		MessagesTypes.Critical: Codes.Colors.Red,
		None: Codes.Drops.DEFAULT_COLOR
	}

	print(TextStyler(text_color = ColorsDict[type]).get_styled_text(GenerateMessage(text, type, origin)))

#==========================================================================================#
# >>>>> ШАБЛОНЫ ТИПОВ СООБЩЕНИЙ <<<<< #
#==========================================================================================#

def PrintInfo(text: str, origin: str | None = None):
	"""
	Выводит в консоль стилизованное информационное сообщение.

	:param text: Текст сообщения.
	:type text: str
	:param origin: Источник сообщения.
	:type origin: str | None
	"""

	PrintMessage(text, type = MessagesTypes.Info, origin = origin)

def PrintWarning(text: str, origin: str | None = None):
	"""
	Выводит в консоль стилизованное предупреждение.

	:param text: Текст сообщения.
	:type text: str
	:param origin: Источник сообщения.
	:type origin: str | None
	"""

	PrintMessage(text, type = MessagesTypes.Warning, origin = origin)

def PrintError(text: str, origin: str | None = None):
	"""
	Выводит в консоль стилизованное сообщение об ошибке.

	:param text: Текст сообщения.
	:type text: str
	:param origin: Источник сообщения.
	:type origin: str | None
	"""

	PrintMessage(text, type = MessagesTypes.Error, origin = origin)

def PrintCritical(text: str, origin: str | None = None):
	"""
	Выводит в консоль стилизованное сообщение о критической ошибке.

	:param text: Текст сообщения.
	:type text: str
	:param origin: Источник сообщения.
	:type origin: str | None
	"""

	PrintMessage(text, type = MessagesTypes.Critical, origin = origin)