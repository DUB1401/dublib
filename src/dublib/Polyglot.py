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

		#---> Генерация динамических атрибутов.
		#==========================================================================================#
		# Регулярное выражение фильтрации тегов HTML.
		self.__AllTagsRegex = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
		# Обрабатываемый текст.
		self.__Text = text	

	def __str__(self) -> str:
		return self.__Text

	def remove_tags(self, tags: list[str] | None = None):
		"""
		Удаляет теги HTML из текста.
			tags – список тегов, которые необходимо удалить.
		"""

		# Если фильтр не установлен.
		if tags == None:
			# Удаление найденных по регулярному выражению тегов.
			self.__Text = str(re.sub(self.__AllTagsRegex, "", self.__Text))

		else:

			# Для каждого тега.
			for Tag in tags:
				# Удаление открывающих и закрывающих тегов.
				self.__Text = re.sub(f"<{Tag}[^>]*>", "", self.__Text)
				self.__Text = re.sub(f"</{Tag}>", "", self.__Text)

	def replace_tag(self, origin: str, new: str):
		"""
		Заменяет переданный тип тега HTML другим.
			origin – замещаемый тег;\n
			new – новый тег.
		"""

		# Поиск открывающих тегов.
		Matches = re.findall(f"<{origin}[^>]*>", self.__Text)
		# Для каждого совпадения произвести замену.
		for Match in Matches: self.__Text = self.__Text.replace(f"<{origin}", f"<{new}")
		# Замена закрывающих тегов.
		self.__Text = re.sub(f"</{origin}>", f"</{new}>", self.__Text)

	def unescape(self):
		"""Преобразует спецсимволы HTML в Unicode."""

		# Конвертирование спецсимволов HTML в Unicode.
		self.__Text = html.unescape(self.__Text)

class Markdown:
	"""Объектная реализация обработчика Markdown."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def escaped_text(self) -> str:
		"""Текст с экранированными спецсимволами."""

		# Буфер текста.
		Text = self.__Text
		# Для каждого спецсимвола провести экранирование.
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
		# Обрабатываемый текст.
		self.__Text = str(text)
		# Список спецсимволов.
		self.__SpecialCharacters = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']

	def __str__(self) -> str:
		return self.__Text

	def escape(self):
		"""Экранирует спецсимволы."""

		# Для каждого спецсимвола провести экранирование.
		for Character in self.__SpecialCharacters: self.__Text = re.sub(f"(?<!\\\\)\\{Character}", f"\\{Character}", self.__Text)