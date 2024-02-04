from .Methods import ReplaceRegexSubstring

import html
import re

class HTML:
	"""Объектная реализация обработчика HTML."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА ТОЛЬКО ДЛЯ ЧТЕНИЯ <<<<< #
	#==========================================================================================#

	@property
	def plain_text(self) -> str:
		"""Текст без тегов и спецсимволов HTML."""
		
		# Конвертирование спецсимволов HTML в Unicode.
		PlainText = html.unescape(self.__Text)
		# Удаление найденных по регулярному выражению тегов.
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

		#---> Генерация динамических свойств.
		#==========================================================================================#
		# Регулярное выражение фильтрации тегов HTML.
		self.__AllTagsRegex = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
		# Обрабатываемый текст.
		self.__Text = text	

	def __str__(self) -> str:
		return self.__Text

	def remove_tags(self):
		"""Удаляет все теги HTML из текста."""

		# Удаление найденных по регулярному выражению тегов.
		self.__Text = str(re.sub(self.__AllTagsRegex, "", self.__Text))

	def unescape(self):
		"""Преобразует спецсимволы HTML в Unicode."""

		# Конвертирование спецсимволов HTML в Unicode.
		self.__Text = html.unescape(self.__Text)

class Markdown:
	"""Объектная реализация обработчика Markdown."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА ТОЛЬКО ДЛЯ ЧТЕНИЯ <<<<< #
	#==========================================================================================#

	@property
	def escaped_text(self) -> str:
		"""Текст с экранированными спецсимволами."""

		# Буфер текста.
		Text = self.__Text
		# Для каждого спецсимвола провести экранирование.
		for Character in self.__SpecialCharacters: Text = ReplaceRegexSubstring(Text, f"(?<!\\\\)\\{Character}", f"\\{Character}")

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

		#---> Генерация динамических свойств.
		#==========================================================================================#
		# Обрабатываемый текст.
		self.__Text = str(text)
		# Список спецсимволов.
		self.__SpecialCharacters = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']

	def __str__(self) -> str:
		return self.__Text

	def escape(self):
		"""Экранирует спецсимволы."""

		# Для каждого спецсимвола провести экранирование.
		for Character in self.__SpecialCharacters: self.__Text = ReplaceRegexSubstring(self.__Text, f"(?<!\\\\)\\{Character}", f"\\{Character}")