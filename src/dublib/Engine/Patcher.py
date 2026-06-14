from ..Methods.Filesystem import ReadTextFile, WriteTextFile

from pathlib import Path
from os import PathLike
import re

class Patch:
	"""Патч."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def lines(self) -> tuple[str, ...]:
		"""Содержимое файла после применения патчей в виде списка строк."""

		return tuple(self.__TextLines)
	
	@property
	def lines_count(self) -> int:
		"""Количество строк в файле."""

		return len(self.__TextLines)

	@property
	def text(self) -> str:
		"""Содержимое файла после применения патчей."""

		return "\n".join(self.__TextLines)

	#==========================================================================================#
	# >>>>> МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, path: str | PathLike[str]):
		"""
		Патч.

		:param path: Путь к файлу.
		:type path: str | PathLike[str]
		"""

		self.__Path = Path(path)
		self.__TextLines: list[str] = list(ReadTextFile(path, split = True))

	def append_line(self, index: int, text: str):
		"""
		Добавляет новую строку на указанный индекс.

		:param index: Индекс позиции для добавление.
		:type index: int
		:param text: Строка.
		:type text: str
		"""

		self.__TextLines.insert(index, text)

	def comment(self, index: int, commentator: str = "# "):
		"""
		Комментирует строку путём добавления символа в её начало.

		:param index: Индекс комментируемой строки.
		:type index: int
		:param commentator: Набор символов, используемый в качестве последовательности комментирования.
		:type commentator: str
		:raises ValueError: Не задан набор символов комментирования.
		"""

		if not commentator: raise ValueError("Commentator is empty.")
		self.__TextLines[index] = commentator + self.__TextLines[index]

	def remove_line(self, index: int):
		"""
		Удаляет строку.

		:param index: Индекс строки.
		:type index: int
		"""

		del self.__TextLines[index]

	def replace(self, old: str, new: str, count: int | None = None):
		"""
		Заменяет вхождения одной подстроки на другую.

		:param old: Заменяемая подстрока.
		:type old: str
		:param new: Новое значение.
		:type new: str
		:param count: Количество замен. `None` для негораниченного.
		:type count: int | None
		"""

		if count is None: count = -1
		self.__TextLines = self.text.replace(old, new, count).split("\n")

	def replace_by_regex(self, regex: str, text: str, count: int = 0):
		"""
		Заменяет все вхождения подстрок, соответствующих реуглярному выражению.

		:param regex: Регулярное выражение.
		:type regex: str
		:param text: Значение для подстановки.
		:type text: str
		:param count: Количество подстановок. `0` для неограниченного.
		:type count: int
		"""

		self.__TextLines = re.sub(regex, text, self.text, count).split("\n")

	def replace_line(self, index: int, line: str, keep_indentation: bool = True):
		"""
		Заменяет строку.

		:param index: Индекс заменяемой строки.
		:type index: int
		:param line: Новое значение.
		:type line: str
		:param keep_indentation: Указывает, следует ли сохранить отступы.
		:type keep_indentation: bool
		"""

		Indentation = ""

		if keep_indentation:
			Result = re.match("^\\s+", self.__TextLines[index])
			if Result: Indentation = Result[0]

		self.__TextLines[index] = Indentation + line

	def uncomment(self, index: int, commentator: str = "#"):
		"""
		Удаляет комментирующий набор символов.

		:param index: Индекс строки.
		:type index: int
		:param commentator: Набор символов, используемый в качестве последовательности комментирования.
		:type commentator: str
		"""

		if self.__TextLines[index].startswith(commentator): self.__TextLines[index] = self.__TextLines[index][len(commentator):]

	def save(self):
		"""Сохраняет пропатченный файл."""

		WriteTextFile(self.__Path, self.__TextLines)