import re
from os import PathLike
from pathlib import Path
from typing import TYPE_CHECKING

from ..functions.filesystem import text

if TYPE_CHECKING:
	from collections.abc import Sequence

class Patch:
	"""Text file patcher."""

	#==========================================================================================#
	# >>>>> PROPERTIES <<<<< #
	#==========================================================================================#

	@property
	def lines(self) -> tuple[str, ...]:
		"""File lines."""

		return tuple(self.__lines)
	
	@property
	def lines_count(self) -> int:
		"""File lines count."""

		return len(self.__lines)

	@property
	def original_lines(self) -> tuple[str, ...]:
		"""Original file lines."""

		return self.__original_lines

	@property
	def original_text(self) -> str:
		"""Original file content."""

		return self.__original_text

	@property
	def text(self) -> str:
		"""File content."""

		return self.__text

	#==========================================================================================#
	# >>>>> PRIVATE METHODS <<<<< #
	#==========================================================================================#

	def __update(self, value: "str | Sequence[str]"):
		"""
		Update internal content variables.

		:param value: Text or line after patch operation.
		:type value: str | Sequence[str]
		"""

		if isinstance(value, str):
			self.__text = value
			self.__lines = value.split("\n")

		else:
			self.__text = "\n".join(value)
			self.__lines = list(value)

	#==========================================================================================#
	# >>>>> PUBLIC METHODS <<<<< #
	#==========================================================================================#

	def __init__(self, path: PathLike[str] | str):
		"""
		Text file patcher.

		:param path: Path to file.
		:type path: PathLike[str] | str
		"""

		self.__file: Path = Path(path)

		self.__original_text: str = text.read(path)
		self.__original_lines: tuple[str, ...] = tuple(self.__original_text.split("\n"))

		self.__text: str = text.read(path)
		self.__lines: list[str] = self.__text.split("\n")

	def insert_line(self, index: int, line: str):
		"""
		Add new line to index.

		:param index: Line index.
		:type index: int
		:param line: Line value.
		:type line: str
		"""

		self.__lines.insert(index, line)
		self.__update(self.__lines)

	def pop_line(self, index: int) -> str:
		"""
		Remove line by index.

		:param index: Line index.
		:type index: int
		"""

		line: str = self.__lines.pop(index)
		self.__update(self.__lines)

		return line

	def prepend_line(self, index: int, substring: str):
		"""
		Add substring to start of line with index.

		:param index: Line index.
		:type index: int
		:param substring: Prepended value.
		:type substring: str
		"""

		self.__lines[index] = substring + self.__lines[index]
		self.__update(self.__lines)

	def replace(self, old: str, new: str, count: int | None = None):
		"""
		Replace occurrences of one substring with another.

		:param old: Replaceable substring.
		:type old: str
		:param new: New value.
		:type new: str
		:param count: Count of replacements. Not limited if `None`.
		:type count: int | None
		"""

		if count is None: count = -1
		self.__text = self.__text.replace(old, new, count)
		self.__update(self.__text)

	def replace_by_regex(self, regex: str, new: str, count: int | None = None):
		"""
		Replace occurrences of regular exprisson matches with substring.

		:param regex: Regular expression.
		:type regex: str
		:param new: New value.
		:type new: str
		:param count: Count of replacements. Not limited if `None`.
		:type count: int | None
		"""

		if count is None: count = 0
		self.__text = re.sub(regex, new, self.__text, count)
		self.__update(self.__text)

	def save(self):
		"""Save file with all changes."""

		text.write(self.__file, self.__text)
