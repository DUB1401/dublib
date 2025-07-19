from .FastStyler import FastStyler
from . import Codes, Escapes

from types import MappingProxyType
from typing import Iterable

#==========================================================================================#
# >>>>> СТИЛИЗАЦИЯ ИЗ HTML <<<<< #
#==========================================================================================#

_SupportedTags = MappingProxyType({
	"b": (Escapes.Decorations.Bold, Escapes.Drops.DISABLE_BOLD),
	"i": (Escapes.Decorations.Italic, Escapes.Drops.DISABLE_ITALIC),
	"u": (Escapes.Decorations.Underlined, Escapes.Drops.DISABLE_UNDERLINED),
	"s": (Escapes.Decorations.Throughline, Escapes.Drops.DISABLE_THROUGHLINED)
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
	def decorations(self) -> tuple[Codes.Decorations] | None:
		"""Набор кодов декораций."""

		return self.__Decorations
	
	@property
	def text_color(self) -> Codes.Colors | None:
		"""Код цвета текста."""

		return self.__TextColor
	
	@property
	def background_color(self) -> Codes.BackgroundsColors | None:
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
			decorations: Codes.Decorations | Iterable[Codes.Decorations] | None = None,
			text_color: Codes.Colors | None = None,
			background_color: Codes.BackgroundsColors | None = None,
			autoreset: bool = True
		):
		"""
		Стилизатор текста.

		:param decorations: Код декорации или набор кодов декораций.
		:type decorations: Codes.Decorations | Iterable[Codes.Decorations] | None
		:param text_color: Код цвета текста.
		:type text_color: Codes.Colors | None
		:param background_color: Код цвета фона.
		:type background_color: Codes.BackgroundsColors | None
		:param autoreset: Указывает, нужно ли добавить последовательность сброса стилей в конец строки.
		:type autoreset: bool
		"""

		self.__Decorations = tuple(decorations) if decorations else None
		self.__TextColor = text_color
		self.__BackgroundColor = background_color
		self.__Autoreset = autoreset

	def build_ansi_escape(self, codes: Iterable[Codes.BackgroundsColors | Codes.Colors | Codes.Decorations | Codes.Drops]) -> str:
		"""
		Строит управляющую последовательность из кодов.

		:param codes: Код ANSI или набор кодов из предоставляемых перечислений.
		:type codes: Iterable[Codes.BackgroundsColors | Codes.Colors | Codes.Decorations | Codes.Drops]
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
		if self.__Autoreset: text += Escapes.Drops.RESET

		return text
	
	#==========================================================================================#
	# >>>>> МЕТОДЫ УСТАНОВКИ СТИЛЕЙ <<<<< #
	#==========================================================================================#

	def set_decorations(self, decorations: Codes.Decorations | Iterable[Codes.Decorations] | None):
		"""
		Задаёт декорации.

		:param decorations: Код декорации или набор кодов декораций.
		:type decorations: Codes.Decorations | Iterable[Codes.Decorations] | None
		"""

		self.__Decorations = tuple(decorations) if decorations else None

	def set_text_color(self, text_color: Codes.Colors | None):
		"""
		Задаёт цвет текста.

		:param text_color: Код цвета текста.
		:type text_color: Codes.Colors | None
		"""

		self.__TextColor = text_color

	def set_background_color(self, background_color: Codes.BackgroundsColors | None):
		"""
		Задаёт цвет фона.

		:param background_color: Код цвета фона.
		:type background_color: Codes.BackgroundsColors | None
		"""

		self.__BackgroundColor = background_color

	def enable_autoreset(self, status: bool):
		"""
		Переключает добавление последовательности сброса стилей в конец строки.

		:param status: Статус добавления последовательности.
		:type status: bool
		"""
		
		self.__Autoreset = status