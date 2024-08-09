from ..Exceptions.CLI import DuplicatedStyles

import enum

#==========================================================================================#
# >>>>> СТИЛИЗАЦИЯ ТЕКСТА <<<<< #
#==========================================================================================#

class Styles:
	"""Перечисления декораций и стилей."""

	class Colors(enum.Enum):
		"""Перечисление цветов."""

		Black = "0"
		Red = "1"
		Green = "2"
		Yellow = "3"
		Blue = "4"
		Purple = "5"
		Cyan = "6"
		White = "7"

	class Decorations(enum.Enum):
		"""Перечисление декораций."""

		Bold = "1"
		Faded = "2"
		Italic = "3"
		Underlined = "4"
		Flashing = "5"
		Throughline = "9"
		DoubleUnderlined = "21"
		Framed = "51"
		Surrounded = "52"
		Upperlined = "53"

class StylesGroup:
	"""Контейнер стилей. Предоставляет возможность комбинировать стили для их однократной инициализации с последующим многократным использованием."""

	def __init__(self, decorations: list[Styles.Decorations] = list(), text_color: Styles.Colors | None = None, background_color: Styles.Colors | None = None):
		"""
		Контейнер стилей. Предоставляет возможность комбинировать стили для их однократной инициализации с последующим многократным использованием.
			decorations – список декораций;\n
			text_color – цвет текста;\n
			background_color – цвет фона.
		"""

		#---> Генерация динамических атрибутов.
		#==========================================================================================#
		self.__StylesMarkers = "\033["

		for Decoration in decorations: self.__StylesMarkers += Decoration.value + ";"
		if text_color != None: self.__StylesMarkers += "3" + text_color.value + ";"
		if background_color != None: self.__StylesMarkers += "4" + background_color.value + ";"
		self.__StylesMarkers = self.__StylesMarkers.rstrip(';') + "m"

	def __str__(self):
		return self.__StylesMarkers

def StyledPrinter(text: str, styles: StylesGroup | None = None, decorations: list[Styles.Decorations] = list(), text_color: Styles.Colors | None = None, background_color: Styles.Colors | None = None, autoreset: bool = True, end: bool = True):
	"""
	Выводит в терминал стилизованный с помощью ANSI-кодов текст.
		text – стилизуемый текст;\n
		styles – контейнер стилей;\n
		decorations – список декораций;\n
		text_color – цвет текста;\n
		background_color – цвет фона;\n
		autoreset – указывает, необходимо ли сбросить стили после вывода;\n
		end – переходить ли на новую строку после завершения вывода.
	Примечание:
		Не используйте одновременно группу стилей и отдельные стили, так как это приводит к ошибке переопределения.
	"""
		
	End = "\n" if end == True else ""
	text = TextStyler(text, styles, decorations, text_color, background_color, autoreset)
	if autoreset == True: text += "\033[0m"
	print(text, end = End)

def TextStyler(text: str, styles: StylesGroup | None = None, decorations: list[Styles.Decorations] = list(), text_color: Styles.Colors | None = None, background_color: Styles.Colors | None = None, autoreset: bool = True) -> str:
	"""
	Стилизует текст с помощью ANSI-кодов.
		text – стилизуемый текст;\n
		styles – контейнер стилей;\n
		decorations – список декораций;\n
		text_color – цвет текста;\n
		background_color – цвет фона;\n
		autoreset – указывает, необходимо ли сбросить стили в конце текста.
	Примечание:
		Не используйте одновременно группу стилей и отдельные стили, так как это приводит к ошибке переопределения.
	"""
		
	StyleMarkers = None

	if styles == None:
		StyleMarkers = "\033["

		for Decoration in decorations: StyleMarkers += Decoration.value + ";"
		if text_color != None: StyleMarkers += "3" + text_color.value + ";"
		if background_color != None: StyleMarkers += "4" + background_color.value + ";"
		StyleMarkers = StyleMarkers.rstrip(';') + "m"

	elif styles != None and decorations != list() or text_color != None or background_color != None: raise DuplicatedStyles()

	else:
		StyleMarkers = str(styles)

	text = StyleMarkers + text
	if autoreset == True: text += "\033[0m"

	return text