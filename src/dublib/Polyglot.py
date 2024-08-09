import html
import re

class HTML:
	"""Объектная реализация обработчика HTML."""

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
		Объектная реализация обработчика HTML.
			text – текст, подлежащий обработке.
		"""

		#---> Генерация динамических атрибутов.
		#==========================================================================================#
		self.__AllTagsRegex = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
		self.__Text = text	

	def __str__(self) -> str:
		return self.__Text

	def remove_tags(self, tags: list[str] | None = None):
		"""
		Удаляет теги HTML из текста.
			tags – список тегов, которые необходимо удалить.
		"""

		if tags == None:
			self.__Text = str(re.sub(self.__AllTagsRegex, "", self.__Text))

		else:

			for Tag in tags:
				self.__Text = re.sub(f"<{Tag}[^>]*>", "", self.__Text)
				self.__Text = re.sub(f"</{Tag}>", "", self.__Text)

	def replace_tag(self, origin: str, new: str):
		"""
		Заменяет переданный тип тега HTML другим.
			origin – замещаемый тег;\n
			new – новый тег.
		"""

		Matches = re.findall(f"<{origin}[^>]*>", self.__Text)
		for Match in Matches: self.__Text = self.__Text.replace(f"<{origin}", f"<{new}")
		self.__Text = re.sub(f"</{origin}>", f"</{new}>", self.__Text)

	def unescape(self):
		"""Преобразует спецсимволы HTML в Unicode."""

		self.__Text = html.unescape(self.__Text)

class Markdown:
	"""Объектная реализация обработчика Markdown."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def escaped_text(self) -> str:
		"""Текст с экранированными спецсимволами."""

		Text = self.__Text
		for Character in self.__SpecialCharacters: Text = re.sub(f"(?<!\\\\)\\{Character}", f"\\{Character}", Text)

		return Text

	@property
	def text(self) -> str:
		"""Текст."""

		return self.__Text

	#==========================================================================================#
	# >>>>> МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, text: str):
		"""
		Объектная реализация обработчика Markdown.
			text – текст, подлежащий обработке.
		"""

		#---> Генерация динамических атрибутов.
		#==========================================================================================#
		self.__Text = str(text)
		self.__SpecialCharacters = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']

	def __str__(self) -> str:
		return self.__Text

	def escape(self):
		"""Экранирует спецсимволы."""

		for Character in self.__SpecialCharacters: self.__Text = re.sub(f"(?<!\\\\)\\{Character}", f"\\{Character}", self.__Text)