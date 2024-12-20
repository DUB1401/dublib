from ..Methods.Filesystem import NormalizePath, ReadTextFile, WriteTextFile

import re

class Patch:
	"""Патч."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def lines(self) -> list[str]:
		"""Содержимое файла после применения патчей в виде списка строк."""

		return self.__Text.split("\n")
	
	@property
	def lines_count(self) -> int:
		"""Количество строк в файле."""

		return len(self.lines)

	@property
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
		self.__Path = NormalizePath(path)
		self.__Text = ReadTextFile(path)

	def append_line(self, line: int, text: str):
		"""
		Добавляет новую строку после указанной.
			line – номер строки;\n
			text – текст новой строки.
		"""

		Lines = self.__Text.split("\n")
		Lines.insert(line, text)
		self.__Text = "\n".join(Lines)

	def comment(self, line: int, character: str = "#", space: bool = True):
		"""
		Делает строку кода комментарием.
			line – номер строки;\n
			character – символ, использующийся для определения комментария;\n
			space – указывает, отделять ли символ комментария от строки пробелом.
		"""

		Lines = self.__Text.split("\n")
		space = " " if space else ""
		Lines[line - 1] = character + space + Lines[line - 1]
		self.__Text = "\n".join(Lines)

	def remove_line(self, line: int):
		"""
		Удаляет строку.
			line – номер строки.
		"""

		Lines = self.__Text.split("\n")
		del Lines[line - 1]
		self.__Text = "\n".join(Lines)

	def replace(self, old: str, new: str, count: int | None = None):
		"""
		Заменяет текст.
			old – старый текст;\n
			new – новый текст;\n
			count – количество замен.
		"""

		if count == None: count = -1
		self.__Text = self.__Text.replace(old, new, count)

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

		Lines = self.__Text.split("\n")
		Indentation = ""

		if not indentation:
			Result = re.match("^\\s+", Lines[line - 1])
			if Result: Indentation = Result[0]

		Lines[line - 1] = Indentation + text
		self.__Text = "\n".join(Lines)

	def uncomment(self, line: int, character: str = "#", space: bool = True):
		"""
		Делает комментарий строкой кода.
			line – номер строки;\n
			character – символ, использующийся для определения комментария;\n
			space – указывает, отделён ли символ комментария от строки пробелом.
		"""

		Lines = self.__Text.split("\n")
		space = 1 if space else 0
		Lines[line - 1] = Lines[line - 1][len(character) + space:]
		self.__Text = "\n".join(Lines)

	def save(self):
		"""Сохраняет пропатченный файл."""

		WriteTextFile(self.__Path, self.__Text)