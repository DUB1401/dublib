from html.parser import HTMLParser
from typing import Iterable
import html
import re

#==========================================================================================#
# >>>>> ВАЛИДАТОРЫ HTML <<<<< #
#==========================================================================================#

class _Validator(HTMLParser):
	"""Валидатор базового HTML синтаксиса."""

	def __init__(self):
		"""Валидатор базового HTML синтаксиса."""

		super().__init__()

		self.stack = list()
		self.errors = list()

	def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]):
		self.stack.append(tag)

	def handle_endtag(self, tag: str):

		if not self.stack:
			self.errors.append(f"Closing tag </{tag}> not opened.")
			return
		
		if self.stack[-1] == tag:
			self.stack.pop()

		else:
			self.errors.append(f"Bad tags order: expected </{self.stack[-1]}>, found </{tag}>.")
			self.stack.pop()

	def error(self, message):
		self.errors.append(f"Parsing error: {message}.")

def _ValidateHTML(text: str) -> tuple[str]:
	"""
	Проводит валидацию структуры HTML.

	:param text: Обрабатываемый текст с тегами HTML.
	:type text: str
	:return: Набор ошибок валидации. Пустая последовательность при отсутствии ошибок.
	:rtype: tuple[str]
	"""

	Parser = _Validator()
	Parser.feed(text)

	if Parser.stack:
		for tag in reversed(Parser.stack): Parser.errors.append(f"Opening tag <{tag}> not closed.")

	return tuple(Parser.errors)

#==========================================================================================#
# >>>>> ОСНОВНОЙ КЛАСС <<<<< #
#==========================================================================================#

class HTML:
	"""Обработчик HTML."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def plain_text(self) -> str:
		"""Текст без тегов и спецсимволов HTML."""
		
		PlainText = html.unescape(self.__Text)
		PlainText = str(re.sub(self.__AllTagsRegex, "", PlainText))

		return PlainText

	@property
	def text(self) -> str:
		"""Текст."""

		return self.__Text

	#==========================================================================================#
	# >>>>> МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, text: str):
		"""
		Обработчик HTML.

		:param text: Обрабатываемый текст.
		:type text: str
		"""

		self.__Text = text

		self.__AllTagsRegex = re.compile("<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});")

	def __str__(self) -> str:
		"""
		Преобразует объект в строку.

		:return: Строковое представление.
		:rtype: str
		"""

		return self.__Text

	def has_tag(self, tag: str) -> int:
		"""
		Проверяет наличие тега в строке.

		:param tag: Проверяемый тег.
		:type tag: str
		:return: Количество вхождений тега.
		:rtype: int
		"""

		return len(re.findall(f"<{tag}[^>]*>", self.__Text))

	def remove_tags(self, tags: Iterable[str] | None = None) -> str:
		"""
		Удаляет теги из текста.

		:param tags: Набор удаляемых тегов или `None` для удаления всех тегов.
		:type tags: Iterable[str] | None
		:return: Строковое представление.
		:rtype: str
		"""

		if not tags:
			self.__Text = str(re.sub(self.__AllTagsRegex, "", self.__Text))

		else:

			for Tag in tags:
				self.__Text = re.sub(f"<{Tag}[^>]*>", "", self.__Text)
				self.__Text = re.sub(f"</{Tag}>", "", self.__Text)

		return self.__Text

	def replace_tag(self, original: str, new: str) -> str:
		"""
		Заменяет все вхождения одного тега на другой.

		:param original: Оригинальный тег.
		:type original: str
		:param new: Замещающий тег.
		:type new: str
		:return: Строковое представление
		:rtype: str
		"""

		Matches = re.findall(f"<{original}[^>]*>", self.__Text)
		for _ in Matches: self.__Text = self.__Text.replace(f"<{original}", f"<{new}")
		self.__Text = re.sub(f"</{original}>", f"</{new}>", self.__Text)

		return self.__Text

	def unescape(self) -> str:
		"""
		Преобразует спецсимволы HTML в Unicode.

		:return: Строковое представление.
		:rtype: str
		"""

		self.__Text = html.unescape(self.__Text)

		return self.__Text
	
	def validate(self, raise_exception: bool = False) -> tuple[str]:
		"""
		Проверяет валидность структуры HTML.

		:param raise_exception: Указывает, следует ли выбрасывать исключение при неудачной валидации.
		:type raise_exception: bool
		:raises ValueError: Выбрасывается в случае включения соответствующей опции при неудачной валидации.
		:return: Последовательность ошибок валидации.
		:rtype: tuple[str]
		"""

		Errors = _ValidateHTML(self.__Text)
		if Errors and raise_exception: raise ValueError(Errors[0])

		return Errors