from typing import Sequence

from ....validators import ValidableTypes
from .parameters import Argument, Flag, Key

__all__ = ["BasePosition", "Position"]

class BasePosition:
	"""Базовая позиция команды."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def arguments(self) -> list[Argument]:
		"""Список аргументов."""

		return self.__Arguments.copy()
	
	@property
	def flags(self) -> list[Flag]:
		"""Список флагов."""

		return self.__Flags.copy()

	@property
	def keys(self) -> list[Key]:
		"""Список ключей."""

		return self.__Keys.copy()

	@property
	def max_parameters_count(self) -> int:
		"""Максимальное количество параметров на позиции."""

		Count = len(self.__Flags)
		Count += len(self.__Arguments)
		Count += len(self.__Keys) * 2
	
		return Count

	@property
	def min_parameters_count(self) -> int:
		"""Минимальное количество параметров на позиции."""

		count = 0
		for flag in self.__Flags:
			if flag.is_important: count += 1

		for key in self.__Keys:
			if key.is_important: count += 2

		for argument in self.__Arguments:
			if argument.is_important: count += 1

		return count

	@property
	def parameters(self) -> list[Argument | Flag | Key]:
		"""Список всех описанных параметров позиции."""

		return self.__Arguments + self.__Flags + self.__Keys

	#==========================================================================================#
	# >>>>> МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self):
		"""Базовая позиция команды."""
		
		self.__Arguments: list[Argument] = []
		self.__Flags: list[Flag] = []
		self.__Keys: list[Key] = []
		
	def add_argument(self, value_type: ValidableTypes = ValidableTypes.All, description: str | None = None):
		"""
		Добавляет аргумент на позицию.

		:param value_type: Тип аргумента.
		:type value_type: ValidableTypes
		:param description: Описание аргумента.
		:type description: str | None
		"""

		self.__Arguments.append(Argument(value_type, description, important = False))

	def add_flag(self, name: str, aliases: Sequence[str] | None = None, description: str | None = None):
		"""
		Добавляет флаг на позицию.

		:param name: Название флага.
		:type name: str
		:param aliases: Список псевдонимов.
		:type aliases: Sequence[str] | None
		:param description: Описание флага.
		:type description: str | None
		"""

		self.__Flags.append(Flag(name, aliases, description, important = False))

	def add_key(self, name: str, aliases: Sequence[str] | None = None, value_type: ValidableTypes = ValidableTypes.All, description: str | None = None):
		"""
		Добавляет ключ на позицию.

		:param name: Название ключа.
		:type name: str
		:param aliases: Список псевдонимов.
		:type aliases: Sequence[str] | None
		:param value_type: Тип значения ключа.
		:type value_type: ValidableTypes
		:param description: Описание ключа.
		:type description: str | None
		"""

		self.__Keys.append(Key(name, aliases, value_type, description, important = False))

class Position:
	"""Позиция команды."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def argument(self) -> Argument | None:
		"""Аргумент."""

		return self.__Argument

	@property
	def description(self) -> str | None:
		"""Описание позиции."""

		return self.__Description
	
	@property
	def flags(self) -> list[Flag]:
		"""Список флагов."""

		return self.__Flags.copy()

	@property
	def is_important(self) -> bool:
		"""Состояние: является ли позиция обязательной."""

		return self.__IsImportant

	@property
	def keys(self) -> list[Key]:
		"""Список ключей."""

		return self.__Keys.copy()

	@property
	def max_parameters_count(self) -> int:
		"""Максимальное количество параметров на позиции."""

		if self.keys: return 2
		elif self.__Argument or self.__Flags: return 1
		else: return 0

	@property
	def min_parameters_count(self) -> int:
		"""Минимальное количество параметров на позиции."""

		if self.__IsImportant:
			if self.keys and not self.__Argument and not self.__Flags: return 2
			elif self.__Argument or self.__Flags: return 1
			else: return 0

		else: return 0

	@property
	def name(self) -> str:
		"""Название позиции."""

		return self.__Name

	@property
	def parameters(self) -> list[Argument | Flag | Key]:
		"""Список всех описанных параметров позиции."""

		List: list[Argument | Flag | Key] = []
		List += self.__Flags
		List += self.__Keys
		if self.__Argument: List.append(self.__Argument)

		return List

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, name: str, description: str | None = None, important: bool = False):
		"""
		Позиции команды.

		:param name: Название позиции.
		:type name: str
		:param description: Описание позиции.
		:type description: str | None
		:param important: Указывает, является ли позиция обязательной.
		:type important: bool
		"""

		self.__Name = name
		self.__Description = description
		self.__IsImportant = important
		
		self.__Argument: Argument | None = None
		self.__Flags: list[Flag] = []
		self.__Keys: list[Key] = []

	def add_flag(self, name: str, aliases: Sequence[str] | None = None, description: str | None = None):
		"""
		Добавляет флаг на позицию.

		:param name: Название флага.
		:type name: str
		:param aliases: Список псевдонимов.
		:type aliases: Sequence[str] | None
		:param description: Описание флага.
		:type description: str | None
		"""

		self.__Flags.append(Flag(name, aliases, description, self.__IsImportant))

	def add_key(self, name: str, aliases: Sequence[str] | None = None, value_type: ValidableTypes = ValidableTypes.All, description: str | None = None):
		"""
		Добавляет ключ на позицию.

		:param name: Название ключа.
		:type name: str
		:param aliases: Список псевдонимов.
		:type aliases: Sequence[str] | None
		:param value_type: Тип значения ключа.
		:type value_type: ValidableTypes
		:param description: Описание ключа.
		:type description: str | None
		"""

		self.__Keys.append(Key(name, aliases, value_type, description, self.__IsImportant))

	def set_argument(self, value_type: ValidableTypes = ValidableTypes.All, description: str | None = None):
		"""
		Устанавливает аргумент на позицию.

		:param value_type: Тип аргумента. По умолчанию `ValidableTypes.All`.
		:type value_type: ValidableTypes
		:param description: Описание аргумента. По умолчанию `None`.
		:type description: str | None
		"""

		self.__Argument = Argument(value_type, description, self.__IsImportant)
