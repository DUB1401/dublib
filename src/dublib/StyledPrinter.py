from dublib.Exceptions.StyledPrinter import DuplicatedStyles

import enum

class Styles:
	"""
	Содержит перечисления декораций и стилей.
	"""

	class Colors(enum.Enum):
		"""
		Перечисление цветов.
		"""

		Black = "0"
		Red = "1"
		Green = "2"
		Yellow = "3"
		Blue = "4"
		Purple = "5"
		Cyan = "6"
		White = "7"

	class Decorations(enum.Enum):
		"""
		Перечисление декораций.
		"""

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
	"""
	Контейнер стилей. Предоставляет возможность комбинировать стили для их однократной инициализации с последующим многократным использования.
	"""

	def __init__(self, decorations: list[Styles.Decorations] = list(), text_color: Styles.Colors | None = None, background_color: Styles.Colors | None = None):
		"""
		Контейнер стилей. Предоставляет возможность комбинировать стили для их однократной инициализации с последующим многократным использования.
			decorations – список декораций;
			text_color – цвет текста;
			background_color – цвет фона.
		"""

		#---> Генерация динамических свойств.
		#==========================================================================================#
		# Строка маркеров стилей.
		self.__StylesMarkers = "\033["

		# Добавить каждый маркер стиля к общей строке.
		for Decoration in decorations: self.__StylesMarkers += Decoration + ";"
		# Если передан цвет текста, создать соответствующий маркер.
		if TextColor != None: self.__StylesMarkers += "3" + TextColor.value + ";"
		# Если передан цвет фона, создать соответствующий маркер.
		if BackgroundColor != None: self.__StylesMarkers += "4" + BackgroundColor.value + ";"
		# Постановка завершающего символа маркировки.
		self.__StylesMarkers = self.__StylesMarkers.rstrip(';') + "m"

	def __str__(self):
		return self.__StylesMarkers

def StyledPrinter(text: str, styles: StylesGroup | None = None, decorations: list[Styles.Decorations] = list(), text_color: Styles.Colors | None = None, background_color: Styles.Colors | None = None, autoreset: bool = True, end: bool = True):
	"""
	Выводит в терминал стилизованный текст.
		text – стилизуемый текст;
		styles – контейнер стилей;
		decorations – список декораций;
		text_color – цвет текста;
		background_color – цвет фона;
		autoreset – указывает, необходимо ли сбросить стили после вывода;
		end – переходить ли на новую строку после завершения вывода.
	Примечание:
		Не используйте одновременно группу стилей и отдельные стили, так как это приводит к ошибке переопределения.
	"""
		
	# Указатель новой строки.
	End = "\n" if end == True else ""
	# Генерация форматированного текста.
	text = TextStyler(text, styles, decorations, text_color, background_color, autoreset)
	# Если указано, добавить маркер сброса стилей.
	if autoreset == True: text += "\033[0m"
	# Вывод в консоль: стилизованный текст.
	print(text, end = End)

def TextStyler(text: str, styles: StylesGroup | None = None, decorations: list[Styles.Decorations] = list(), text_color: Styles.Colors | None = None, background_color: Styles.Colors | None = None, autoreset: bool = True) -> str:
	"""
	Стилизует текст.
		text – стилизуемый текст;
		styles – контейнер стилей;
		decorations – список декораций;
		text_color – цвет текста;
		background_color – цвет фона;
		autoreset – указывает, необходимо ли сбросить стили в конце текста.
	Примечание:
		Не используйте одновременно группу стилей и отдельные стили, так как это приводит к ошибке переопределения.
	"""
		
	# Маркер стилей строки.
	StyleMarkers = None

	# Если не указана группа стилей.
	if styles == None:
		# Инициализация маркера стилей строки.
		StyleMarkers = "\033["

		# Добавить каждую декорацию.
		for Decoration in decorations: StyleMarkers += Decoration + ";"
		# Если передан цвет текста, создать соответствующий маркер.
		if text_color != None: StyleMarkers += "3" + text_color.value + ";"
		# Если передан цвет фона, создать соответствующий маркер.
		if background_color != None: StyleMarkers += "4" + background_color.value + ";"
		# Постановка завершающего символа маркировки.
		StyleMarkers = StyleMarkers.rstrip(';') + "m"

	# Если указана и группа стилей, и стили по отдельности, выбросить исключение.
	elif styles != None and decorations != list() or text_color != None or background_color != None: raise DuplicatedStyles()

	else:
		# Запись маркера стилей строки.
		StyleMarkers = str(styles)

	# Добавление стилей к строке.
	text = StyleMarkers + text
	# Если указано, добавить маркер сброса стилей.
	if autoreset == True: text += "\033[0m"

	return text