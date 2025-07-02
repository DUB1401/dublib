from .Escapes import BackgroundColors, Colors, Decorations, Drops 

#==========================================================================================#
# >>>>> НАБОРЫ БЫСТРЫХ СТИЛИЗАТОРОВ <<<<< #
#==========================================================================================#

class Background:
	"""Набор быстрых фоновых цветов."""

	@property
	def black(self) -> str:
		"""Чёрный."""

		return f"{BackgroundColors.Black}{self.__Styler.plain_text}{Drops.DEFAULT_BACKGROUND}"
	
	@property
	def red(self) -> str:
		"""Красный."""

		return f"{BackgroundColors.Red}{self.__Styler.plain_text}{Drops.DEFAULT_BACKGROUND}"
	
	@property
	def green(self) -> str:
		"""Зелёный."""

		return f"{BackgroundColors.Green}{self.__Styler.plain_text}{Drops.DEFAULT_BACKGROUND}"
	
	@property
	def yellow(self) -> str:
		"""Жёлтый."""

		return f"{BackgroundColors.Yellow}{self.__Styler.plain_text}{Drops.DEFAULT_BACKGROUND}"
	
	@property
	def blue(self) -> str:
		"""Синий."""

		return f"{BackgroundColors.Blue}{self.__Styler.plain_text}{Drops.DEFAULT_BACKGROUND}"
	
	@property
	def magenta(self) -> str:
		"""Фиолетовый."""

		return f"{BackgroundColors.Magenta}{self.__Styler.plain_text}{Drops.DEFAULT_BACKGROUND}"
	
	@property
	def cyan(self) -> str:
		"""Бирюзовый."""

		return f"{BackgroundColors.Cyan}{self.__Styler.plain_text}{Drops.DEFAULT_BACKGROUND}"
	
	@property
	def white(self) -> str:
		"""Белый."""

		return f"{BackgroundColors.White}{self.__Styler.plain_text}{Drops.DEFAULT_BACKGROUND}"
	
	def __init__(self, fast_styler: "FastStyler"):
		"""
		Набор быстрых фоновых цветов.

		:param fast_styler: Быстрый стилизатор.
		:type fast_styler: FastStyler
		"""

		self.__Styler = fast_styler

class Colorize:
	"""Набор быстрых цветов."""

	#==========================================================================================#
	# >>>>> БАЗОВЫЕ ЦВЕТА <<<<< #
	#==========================================================================================#

	@property
	def black(self) -> str:
		"""Чёрный."""

		return f"{Colors.Black}{self.__Styler.plain_text}{Drops.DEFAULT_COLOR}"
	
	@property
	def red(self) -> str:
		"""Красный."""

		return f"{Colors.Red}{self.__Styler.plain_text}{Drops.DEFAULT_COLOR}"
	
	@property
	def green(self) -> str:
		"""Зелёный."""

		return f"{Colors.Green}{self.__Styler.plain_text}{Drops.DEFAULT_COLOR}"
	
	@property
	def yellow(self) -> str:
		"""Жёлтый."""

		return f"{Colors.Yellow}{self.__Styler.plain_text}{Drops.DEFAULT_COLOR}"
	
	@property
	def blue(self) -> str:
		"""Синий."""

		return f"{Colors.Blue}{self.__Styler.plain_text}{Drops.DEFAULT_COLOR}"
	
	@property
	def magenta(self) -> str:
		"""Фиолетовый."""

		return f"{Colors.Magenta}{self.__Styler.plain_text}{Drops.DEFAULT_COLOR}"
	
	@property
	def cyan(self) -> str:
		"""Бирюзовый."""

		return f"{Colors.Cyan}{self.__Styler.plain_text}{Drops.DEFAULT_COLOR}"
	
	@property
	def white(self) -> str:
		"""Белый."""

		return f"{Colors.White}{self.__Styler.plain_text}{Drops.DEFAULT_COLOR}"
	
	#==========================================================================================#
	# >>>>> СВЕТЛЫЕ ОТТЕНКИ <<<<< #
	#==========================================================================================#

	@property
	def gray(self) -> str:
		"""Серый."""

		return f"{Colors.Gray}{self.__Styler.plain_text}{Drops.DEFAULT_COLOR}"
	
	@property
	def bright_red(self) -> str:
		"""Светло-красный."""

		return f"{Colors.BrightRed}{self.__Styler.plain_text}{Drops.DEFAULT_COLOR}"
	
	@property
	def bright_green(self) -> str:
		"""Светло-зелёный."""

		return f"{Colors.BrightGreen}{self.__Styler.plain_text}{Drops.DEFAULT_COLOR}"
	
	@property
	def bright_yellow(self) -> str:
		"""Светло-жёлтый."""

		return f"{Colors.BrightYellow}{self.__Styler.plain_text}{Drops.DEFAULT_COLOR}"
	
	@property
	def bright_blue(self) -> str:
		"""Светло-синий."""

		return f"{Colors.BrightBlue}{self.__Styler.plain_text}{Drops.DEFAULT_COLOR}"
	
	@property
	def bright_magenta(self) -> str:
		"""Светло-фиолетовый."""

		return f"{Colors.BrightMagenta}{self.__Styler.plain_text}{Drops.DEFAULT_COLOR}"
	
	@property
	def bright_cyan(self) -> str:
		"""Светло-бирюзовый."""

		return f"{Colors.BrightCyan}{self.__Styler.plain_text}{Drops.DEFAULT_COLOR}"
	
	@property
	def bright_white(self) -> str:
		"""Светло-белый."""

		return f"{Colors.BrightWhite}{self.__Styler.plain_text}{Drops.DEFAULT_COLOR}"

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, fast_styler: "FastStyler"):
		"""
		Набор быстрых цветов.

		:param fast_styler: Быстрый стилизатор.
		:type fast_styler: FastStyler
		"""

		self.__Styler = fast_styler

class Decorate:
	"""Набор быстрых декораций."""

	@property
	def bold(self) -> str:
		"""Полужирный."""

		return f"{Decorations.Bold}{self.__Styler.plain_text}{Drops.DISABLE_BOLD}"
	
	@property
	def italic(self) -> str:
		"""Курсив."""

		return f"{Decorations.Italic}{self.__Styler.plain_text}{Drops.DISABLE_ITALIC}"
	
	@property
	def underlined(self) -> str:
		"""Подчёркнутый."""

		return f"{Decorations.Underlined}{self.__Styler.plain_text}{Drops.DISABLE_UNDERLINED}"
	
	@property
	def blincked(self) -> str:
		"""Мигающий."""

		return f"{Decorations.Blincked}{self.__Styler.plain_text}{Drops.DISABLE_BLINCKED}"
	
	@property
	def throughline(self) -> str:
		"""Перечёркнутый."""

		return f"{Decorations.Throughline}{self.__Styler.plain_text}{Drops.DISABLE_THROUGHLINED}"
	
	@property
	def double_underlined(self) -> str:
		"""Дважды подчёркнутый."""

		return f"{Decorations.DoubleUnderlined}{self.__Styler.plain_text}{Drops.DISABLE_UNDERLINED}"
	
	@property
	def upperlined(self) -> str:
		"""Надчёркнутый."""

		return f"{Decorations.Upperlined}{self.__Styler.plain_text}{Drops.DISABLE_UPPERLINED}"
	
	def __init__(self, fast_styler: "FastStyler"):
		"""
		Набор быстрых декораций.

		:param fast_styler: Быстрый стилизатор.
		:type fast_styler: FastStyler
		"""

		self.__Styler = fast_styler

#==========================================================================================#
# >>>>> ОСНОВНЫЕ КЛАССЫ <<<<< #
#==========================================================================================#

class FastStyler:
	"""Быстрый стилизатор текста."""

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
		"""Нестилизованный текст."""

		return self.__Text

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, text: str):
		"""
		Быстрый стилизатор текста.

		:param text: Стилизуемый текст.
		:type text: str
		"""

		self.__Text = text

		self.__Background = Background(self)
		self.__Colorize = Colorize(self)
		self.__Decorate = Decorate(self)