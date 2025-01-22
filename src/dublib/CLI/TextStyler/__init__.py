from .Styles import Colors, Decorations

#==========================================================================================#
# >>>>> НАБОРЫ БЫСТРЫХ СТИЛЕЙ <<<<< #
#==========================================================================================#

class Background:
	"""Набор быстрых фоновых цветов."""

	@property
	def black(self) -> str:
		"""Чёрный."""

		return self.__Styler.stylize(background_color = Colors.Black)
	
	@property
	def red(self) -> str:
		"""Красный."""

		return self.__Styler.stylize(background_color = Colors.Red)
	
	@property
	def green(self) -> str:
		"""Зелёный."""

		return self.__Styler.stylize(background_color = Colors.Green)
	
	@property
	def yellow(self) -> str:
		"""Жёлтый."""

		return self.__Styler.stylize(background_color = Colors.Yellow)
	
	@property
	def blue(self) -> str:
		"""Синий."""

		return self.__Styler.stylize(background_color = Colors.Blue)
	
	@property
	def purple(self) -> str:
		"""Фиолетовый."""

		return self.__Styler.stylize(background_color = Colors.Purple)
	
	@property
	def cyan(self) -> str:
		"""Бирюзовый."""

		return self.__Styler.stylize(background_color = Colors.Cyan)
	
	@property
	def white(self) -> str:
		"""Белый."""

		return self.__Styler.stylize(background_color = Colors.White)
	
	def __init__(self, styler: "TextStyler"):
		"""
		Набор быстрых фоновых цветов.
			styler – стилизатор текста.
		"""

		#---> Генерация динамических атрибутов.
		#==========================================================================================#
		self.__Styler = styler

class Colorize:
	"""Набор быстрых цветов."""

	#==========================================================================================#
	# >>>>> БАЗОВЫЕ ЦВЕТА <<<<< #
	#==========================================================================================#

	@property
	def black(self) -> str:
		"""Чёрный."""

		return self.__Styler.stylize(text_color = Colors.Black)
	
	@property
	def red(self) -> str:
		"""Красный."""

		return self.__Styler.stylize(text_color = Colors.Red)
	
	@property
	def green(self) -> str:
		"""Зелёный."""

		return self.__Styler.stylize(text_color = Colors.Green)
	
	@property
	def yellow(self) -> str:
		"""Жёлтый."""

		return self.__Styler.stylize(text_color = Colors.Yellow)
	
	@property
	def blue(self) -> str:
		"""Синий."""

		return self.__Styler.stylize(text_color = Colors.Blue)
	
	@property
	def magenta(self) -> str:
		"""Фиолетовый."""

		return self.__Styler.stylize(text_color = Colors.Magenta)
	
	@property
	def cyan(self) -> str:
		"""Бирюзовый."""

		return self.__Styler.stylize(text_color = Colors.Cyan)
	
	@property
	def white(self) -> str:
		"""Белый."""

		return self.__Styler.stylize(text_color = Colors.White)
	
	#==========================================================================================#
	# >>>>> СВЕТЛЫЕ ОТТЕНКИ <<<<< #
	#==========================================================================================#

	@property
	def gray(self) -> str:
		"""Серый."""

		return self.__Styler.stylize(text_color = Colors.Gray)
	
	@property
	def bright_red(self) -> str:
		"""Светло-красный."""

		return self.__Styler.stylize(text_color = Colors.BrightRed)
	
	@property
	def bright_green(self) -> str:
		"""Светло-зелёный."""

		return self.__Styler.stylize(text_color = Colors.BrightGreen)
	
	@property
	def bright_yellow(self) -> str:
		"""Светло-жёлтый."""

		return self.__Styler.stylize(text_color = Colors.BrightYellow)
	
	@property
	def bright_blue(self) -> str:
		"""Светло-синий."""

		return self.__Styler.stylize(text_color = Colors.BrightBlue)
	
	@property
	def bright_magenta(self) -> str:
		"""Светло-фиолетовый."""

		return self.__Styler.stylize(text_color = Colors.BrightMagenta)
	
	@property
	def bright_cyan(self) -> str:
		"""Светло-бирюзовый."""

		return self.__Styler.stylize(text_color = Colors.BrightCyan)
	
	@property
	def bright_white(self) -> str:
		"""Светло-белый."""

		return self.__Styler.stylize(text_color = Colors.BrightWhite)

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, styler: "TextStyler"):
		"""
		Набор быстрых цветов.
			styler – стилизатор текста.
		"""

		#---> Генерация динамических атрибутов.
		#==========================================================================================#
		self.__Styler = styler

class Decorate:
	"""Набор быстрых декораций."""

	@property
	def bold(self) -> str:
		"""Полужирный."""

		return self.__Styler.stylize(decorations = Decorations.Bold)
	
	@property
	def faded(self) -> str:
		"""Затенённый."""

		return self.__Styler.stylize(decorations = Decorations.Faded)
	
	@property
	def italic(self) -> str:
		"""Курсив."""

		return self.__Styler.stylize(decorations = Decorations.Italic)
	
	@property
	def underlined(self) -> str:
		"""Подчёркнутый."""

		return self.__Styler.stylize(decorations = Decorations.Underlined)
	
	@property
	def flashing(self) -> str:
		"""Пульсирующий."""

		return self.__Styler.stylize(decorations = Decorations.Flashing)
	
	@property
	def throughline(self) -> str:
		"""Перечёркнутый."""

		return self.__Styler.stylize(decorations = Decorations.Throughline)
	
	@property
	def double_underlined(self) -> str:
		"""Дважды подчёркнутый."""

		return self.__Styler.stylize(decorations = Decorations.DoubleUnderlined)
	
	@property
	def framed(self) -> str:
		"""Обрамлённый."""

		return self.__Styler.stylize(decorations = Decorations.Framed)
	
	@property
	def surrounded(self) -> str:
		"""Окружённый."""

		return self.__Styler.stylize(decorations = Decorations.Surrounded)
	
	@property
	def upperlined(self) -> str:
		"""Надчёркнутый."""

		return self.__Styler.stylize(decorations = Decorations.Upperlined)
	
	def __init__(self, styler: "TextStyler"):
		"""
		Набор быстрых декораций.
			styler – стилизатор текста.
		"""

		#---> Генерация динамических атрибутов.
		#==========================================================================================#
		self.__Styler = styler

#==========================================================================================#
# >>>>> ОСНОВНОЙ КЛАСС <<<<< #
#==========================================================================================#

class TextStyler:
	"""Стилизатор текста. Использует только ANSI-коды."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def background(self) -> Background:
		"""Набор быстрых фоновых цветов."""

		return self.__Background

	@property
	def colorize(self) -> Colorize:
		"""Набор быстрых цветов."""

		return self.__Colorize
	
	@property
	def decorate(self) -> Decorate:
		"""Набор быстрых декораций."""

		return self.__Decorate

	@property
	def plain_text(self):
		"""Базовый текст."""

		return self.__Text

	@property
	def text(self):
		"""Стилизованный текст."""

		return self.stylize(self.__Text, self.__Decorations, self.__TextColor, self.__BackgroundColor, self.__Autoreset)

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(
			self,
			text: str | None = None,
			decorations: Decorations | list[Decorations] = list(),
			text_color: Colors | None = None,
			background_color: Colors | None = None,
			autoreset: bool = True
		):
		"""
		Стилизатор текста. Использует только ANSI-коды.
			text – стилизуемый текст;\n
			decorations – список декораций;\n
			text_color – цвет текста;\n
			background_color – цвет фона;\n
			autoreset – указывает, необходимо ли сбросить стили в конце текста.
		"""

		#---> Генерация динамических атрибутов.
		#==========================================================================================#
		self.__Text = str(text)
		self.__Decorations = decorations
		self.__TextColor = text_color
		self.__BackgroundColor = background_color
		self.__Autoreset = autoreset

		self.__Background = Background(self)
		self.__Colorize = Colorize(self)
		self.__Decorate = Decorate(self)

	def __str__(self) -> str:
		"""Возвращает стилизованный текст."""

		return self.text

	def print(self):
		"""Выводит в консоль стилизованный текст."""

		print(self.text)

	def stylize(
			self,
			text: str | None = None,
			decorations: Decorations | list[Decorations] = list(),
			text_color: Colors | None = None,
			background_color: Colors | None = None,
			autoreset: bool = True
		) -> str:
		"""
		Стилизует текст. Использует только ANSI-коды.
			text – стилизуемый текст;\n
			decorations – список декораций;\n
			text_color – цвет текста;\n
			background_color – цвет фона;\n
			autoreset – указывает, необходимо ли сбросить стили в конце текста.
		"""

		if not text: text = self.__Text
		if decorations and type(decorations) != list: decorations = [decorations]
		elif not decorations: decorations = []
		StyleMarkers = "\033["

		for Decoration in decorations: StyleMarkers += Decoration.value + ";"
		if text_color: StyleMarkers += text_color.value + ";"

		if background_color:
			BackgroundCode = background_color.value
			if BackgroundCode.startswith("3"): BackgroundCode = "4" + BackgroundCode[1:]
			elif BackgroundCode.startswith("9"): BackgroundCode = "10" + BackgroundCode[1:]
			StyleMarkers += BackgroundCode + ";"

		StyleMarkers = StyleMarkers.rstrip(';') + "m"

		text = StyleMarkers + text
		if autoreset == True: text += "\033[0m"

		return text