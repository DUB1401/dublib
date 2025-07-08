import re

class Markdown:
	"""Обработчик Markdown."""

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
		Обработчик Markdown.

		:param text: Обрабатываемый текст.
		:type text: str
		"""

		self.__Text = text

		self.__SpecialCharacters = ("_", "*", "[", "]", "(", ")", "~", "`", ">", "#", "+", "-", "=", "|", "{", "}", ".", "!")

	def __str__(self) -> str:
		"""
		Преобразует объект в строку.

		:return: Строковое представление.
		:rtype: str
		"""

		return self.__Text

	def escape(self) -> str:
		"""
		Экранирует спецсимволы.

		:return: Строковое представление.
		:rtype: str
		"""

		self.__Text = self.escaped_text

		return self.__Text