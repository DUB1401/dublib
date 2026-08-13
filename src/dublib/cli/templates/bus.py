from ...engine.bus.enums import MessagesTypes
from .. import readline as readline
from ..text_styler import TextStyler, codes

#==========================================================================================#
# >>>>> ФУНКЦИИ ГЕНЕРАЦИИ И ВЫВОДА СООБЩЕНИЙ <<<<< #
#==========================================================================================#

def GenerateMessage(text: str, type: MessagesTypes | None = None, origin: str | None = None, colorize: bool = True) -> str:
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
	if origin:
		OriginPart = f"{origin}:"
	if type:
		TypePart = f"[{OriginPart}{type.name.upper()}] "

	Message = f"{TypePart}{text}"

	if colorize:
		ColorsDict: dict[MessagesTypes | None, codes.Colors | None] = {
			MessagesTypes.Debug: codes.Colors.Gray,
			MessagesTypes.Info: codes.Colors.White,
			MessagesTypes.Error: codes.Colors.Red,
			MessagesTypes.Warning: codes.Colors.Yellow,
			MessagesTypes.Critical: codes.Colors.Red,
			None: None
		}
		Message = TextStyler(text_color = ColorsDict[type]).get_styled_text(Message)

	return Message

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

	print(GenerateMessage(text, type, origin))

#==========================================================================================#
# >>>>> ШАБЛОНЫ ТИПОВ СООБЩЕНИЙ <<<<< #
#==========================================================================================#

def PrintDebug(text: str, origin: str | None = None):
	"""
	Выводит в консоль стилизованное сообщение отладки.

	:param text: Текст сообщения.
	:type text: str
	:param origin: Источник сообщения.
	:type origin: str | None
	"""

	PrintMessage(text, type = MessagesTypes.Debug, origin = origin)

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