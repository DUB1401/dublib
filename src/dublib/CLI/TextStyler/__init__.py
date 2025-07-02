from .Codes import BackgroundsColorsCodes, ColorsCodes, DecorationsCodes, DropsCodes
from .Escapes import Decorations, Drops

from types import MappingProxyType
from typing import Iterable

#==========================================================================================#
# >>>>> СТИЛИЗАЦИЯ ИЗ HTML <<<<< #
#==========================================================================================#

_SupportedTags = MappingProxyType({
	"b": (Decorations.Bold, Drops.DISABLE_BOLD),
	"i": (Decorations.Italic, Drops.DISABLE_ITALIC),
	"u": (Decorations.Underlined, Drops.DISABLE_UNDERLINED),
	"s": (Decorations.Throughline, Drops.DISABLE_THROUGHLINED)
})

def GetStyledTextFromHTML(text: str) -> str:
		"""
		Преобразовывает теги HTML в управляющие последовательности ANSI.

		Поддерживаемые теги: `b`, `i`, `u`, `s`.

		:param text: Стилизуемый текст.
		:type text: str
		:return: Стилизованный текст.
		:rtype: str
		"""

		for Tag in _SupportedTags.keys():
			text = text.replace(f"<{Tag}>", _SupportedTags[Tag][0])
			text = text.replace(f"</{Tag}>", _SupportedTags[Tag][1])

		return text

#==========================================================================================#
# >>>>> ОСНОВНОЙ КЛАСС <<<<< #
#==========================================================================================#

class TextStyler:
	"""Стилизатор текста."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def decorations(self) -> tuple[DecorationsCodes] | None:
		"""Набор кодов декораций."""

		return self.__Decorations
	
	@property
	def text_color(self) -> ColorsCodes | None:
		"""Код цвета текста."""

		return self.__TextColor
	
	@property
	def background_color(self) -> BackgroundsColorsCodes | None:
		"""Код цвета фона."""

		return self.__BackgroundColor
	
	@property
	def is_autoreset(self) -> bool:
		"""Состояние переключателя: нужно ли добавлять последовательность сброса стилей в конец строки."""

		return self.__Autoreset

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(
			self,
			decorations: DecorationsCodes | Iterable[DecorationsCodes] | None = None,
			text_color: ColorsCodes | None = None,
			background_color: BackgroundsColorsCodes | None = None,
			autoreset: bool = True
		):
		"""
		Стилизатор текста.

		:param decorations: Код декорации или набор кодов декораций.
		:type decorations: DecorationsCodes | Iterable[DecorationsCodes] | None
		:param text_color: Код цвета текста.
		:type text_color: ColorsCodes | None
		:param background_color: Код цвета фона.
		:type background_color: BackgroundsColorsCodes | None
		:param autoreset: Указывает, нужно ли добавить последовательность сброса стилей в конец строки.
		:type autoreset: bool
		"""

		self.__Decorations = tuple(decorations) if decorations else None
		self.__TextColor = text_color
		self.__BackgroundColor = background_color
		self.__Autoreset = autoreset

	def build_ansi_escape(self, codes: Iterable[BackgroundsColorsCodes | ColorsCodes | DecorationsCodes | DropsCodes]) -> str:
		"""
		Строит управляющую последовательность из кодов.

		:param codes: Код ANSI или набор кодов из предоставляемых перечислений.
		:type codes: Enum | Iterable[Enum]
		:return: Управляющая последовательность.
		:rtype: str
		"""

		codes = tuple(str(Element.value) for Element in codes)
		codes = ";".join(codes)

		return f"\033[{codes}m"

	def get_styled_text(self, text: str) -> str:
		"""
		Возвращает стилизованный с помощью управляющих последовательностей ANSI текст, используя заданные в объекте стили.

		:param text: Стилизуемый текст.
		:type text: str
		:return: Стилизованный текст.
		:rtype: str
		"""

		Codes = list()
		if self.__Decorations: Codes.extend(self.__Decorations)
		if self.__TextColor: Codes.append(self.__TextColor)
		if self.__BackgroundColor: Codes.append(self.__BackgroundColor)
		
		text = self.build_ansi_escape(Codes) + text
		if self.__Autoreset: text += Drops.RESET

		return text
	
	#==========================================================================================#
	# >>>>> МЕТОДЫ УСТАНОВКИ СТИЛЕЙ <<<<< #
	#==========================================================================================#

	def set_decorations(self, decorations: DecorationsCodes | Iterable[DecorationsCodes] | None):
		"""
		Задаёт декорации.

		:param decorations: Код декорации или набор кодов декораций.
		:type decorations: DecorationsCodes | Iterable[DecorationsCodes] | None
		"""

		self.__Decorations = tuple(decorations) if decorations else None

	def set_text_color(self, text_color: ColorsCodes | None):
		"""
		Задаёт цвет текста.

		:param text_color: Код цвета текста.
		:type text_color: ColorsCodes | None
		"""

		self.__TextColor = text_color

	def set_background_color(self, background_color: BackgroundsColorsCodes | None):
		"""
		Задаёт цвет фона.

		:param background_color: Код цвета фона.
		:type background_color: BackgroundsColorsCodes | None
		"""

		self.__BackgroundColor = background_color

	def enable_autoreset(self, status: bool):
		"""
		Переключает добавление последовательности сброса стилей в конец строки.

		:param status: Статус добавления последовательности.
		:type status: bool
		"""
		
		self.__Autoreset = status