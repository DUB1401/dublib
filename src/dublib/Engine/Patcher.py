from ..Methods.Filesystem import NormalizePath, ReadTextFile, WriteTextFile

import re

class Patch:
	"""Патч."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	def lines(self) -> list[str]:
		"""Содержимое файла после применения патчей в виде списка строк."""

		return self.__Text.split("\n")
	
	def lines_count(self) -> int:
		"""Количество строк в файле."""

		return len(self.lines)

	def text(self) -> str:
		"""Содержимое файла после применения патчей."""

		return self.__Text

	#==========================================================================================#
	# >>>>> МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, path: str):
		"""
		Патч.
			path – путь к файлу.
		"""

		#---> Генерация динамических атрибутов.
		#==========================================================================================#
		# Путь к файлу.
		self.__Path = NormalizePath(path)
		# Содержимое файла.
		self.__Text = ReadTextFile(path)

	def append_line(self, line: int, text: str):
		"""
		Добавляет новую строку после указанной.
			line – номер строки;\n
			text – текст новой строки.
		"""

		# Список строк.
		Lines = self.__Text.split("\n")
		# Добавление строки.
		Lines.insert(line, text)
		# Объединение строк.
		self.__Text = "\n".join(Lines)

	def comment(self, line: int, character: str = "#", space: bool = True):
		"""
		Делает строку кода комментарием.
			line – номер строки;\n
			character – символ, использующийся для определения комментария;\n
			space – указывает, отделять ли символ комментария от строки пробелом.
		"""

		# Список строк.
		Lines = self.__Text.split("\n")
		# Определение использование пробела.
		space = " " if space else ""
		# Комментирование строки.
		Lines[line - 1] = character + space + Lines[line - 1]
		# Объединение строк.
		self.__Text = "\n".join(Lines)

	def remove_line(self, line: int):
		"""
		Удаляет строку.
			line – номер строки.
		"""

		# Список строк.
		Lines = self.__Text.split("\n")
		# Удаление строки.
		del Lines[line]
		# Объединение строк.
		self.__Text = "\n".join(Lines)

	def replace_by_regex(self, regex: str, text: str, count: int = 0):
		"""
		Заменяет все вхождения подстрок, соответствующих реуглярному выражению.
			regex – регулярное выражение;\n
			text – текст для замещения.
		"""

		self.__Text = re.sub(regex, text, self.__Text, count)

	def replace_line(self, line: int, text: str, indentation: bool = False):
		"""
		Заменяет строку.
			line – номер строки;\n
			text – текст для замещения;\n
			indentation – указывает, заменять ли также отступы.
		"""

		# Список строк.
		Lines = self.__Text.split("\n")
		# Отступ.
		Indentation = ""

		# Если замена отступов отключена.
		if not indentation:
			# Поиск отступа.
			Result = re.match("^\\s+", Lines[line - 1])
			# Если поиск успешен, сохранить отступ.
			if Result: Indentation = Result[0]

		# Замена строки.
		Lines[line - 1] = Indentation + text
		# Объединение строк.
		self.__Text = "\n".join(Lines)

	def uncomment(self, line: int, character: str = "#", space: bool = True):
		"""
		Делает комментарий строкой кода.
			line – номер строки;\n
			character – символ, использующийся для определения комментария;\n
			space – указывает, отделён ли символ комментария от строки пробелом.
		"""

		# Список строк.
		Lines = self.__Text.split("\n")
		# Определение использование пробела.
		space = 1 if space else 0
		# Раскомментирование строки.
		Lines[line - 1] = Lines[line - 1][len(character) + space:]
		# Объединение строк.
		self.__Text = "\n".join(Lines)

	def save(self):
		"""Сохраняет пропатченный файл."""

		WriteTextFile(self.__Path, self.__Text)