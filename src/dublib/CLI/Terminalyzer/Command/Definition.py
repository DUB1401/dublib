from ..Enums import ParametersTypes

from typing import Iterable

#==========================================================================================#
# >>>>> ПАРАМЕТРЫ КОМАНДЫ <<<<< #
#==========================================================================================#

class _Argument:
	"""Аргумент команды."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def description(self) -> str | None:
		"""Описание аргумента."""

		return self.__Description
	
	@property
	def is_important(self) -> bool:
		"""Состояние: является ли аргумент обязательным."""

		return self.__IsImportant

	@property
	def type(self) -> ParametersTypes:
		"""Тип значения аргумента."""

		return self.__Type

	#==========================================================================================#
	# >>>>> МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, type: ParametersTypes, description: str | None, important: bool):
		"""
		Аргумент команды.

		:param type: nип значения аргумента.
		:type type: ParametersTypes
		:param description: Описание аргумента.
		:type description: str | None
		:param important: Указывает, является ли аргумент обязательным.
		:type important: bool
		"""

		self.__Type = type
		self.__Description = description
		self.__IsImportant = important

class _Flag:
	"""Флаг команды."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def aliases(self) -> list[str]:
		"""Список псевдонимов."""

		return self.__Aliases.copy()

	@property
	def description(self) -> str | None:
		"""Описание флага."""

		return self.__Description
	
	@property
	def is_important(self) -> bool:
		"""Состояние: является ли флаг обязательным."""

		return self.__IsImportant
	
	@property
	def name(self) -> str:
		"""Название флага."""

		return self.__Name

	#==========================================================================================#
	# >>>>> МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, name: str, aliases: Iterable[str] | None, description: str | None, important: bool):
		"""
		Флаг команды.

		:param name: Название флага.
		:type name: str
		:param aliases: Список псевдонимов.
		:type aliases: Iterable[str] | None
		:param description: Описание флага.
		:type description: str | None
		:param important: Указывает, является ли флаг обязательным.
		:type important: bool
		"""

		self.__Name = name
		self.__Aliases = list(aliases) if aliases else list()
		self.__Description = description
		self.__IsImportant = important

class _Key:
	"""Ключ команды."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def aliases(self) -> list[str]:
		"""Список псевдонимов."""

		return self.__Aliases.copy()

	@property
	def description(self) -> str | None:
		"""Описание ключа."""

		return self.__Description
	
	@property
	def is_important(self) -> bool:
		"""Состояние: является ли ключ обязательным."""

		return self.__IsImportant
	
	@property
	def name(self) -> str:
		"""Название ключа."""

		return self.__Name
	
	@property
	def type(self) -> ParametersTypes:
		"""Тип значения ключа."""

		return self.__Type

	#==========================================================================================#
	# >>>>> МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, name: str, aliases: Iterable[str] | None, type: ParametersTypes, description: str | None, important: bool):
		"""
		Ключ команды.

		:param name: Название ключа.
		:type name: str
		:param aliases: Список псевдонимов.
		:type aliases: Iterable[str] | None
		:param type: Тип значения ключа.
		:type type: ParametersTypes
		:param description: Описание ключа.
		:type description: str | None
		:param important: Указывает, является ли ключ обязательным.
		:type important: bool
		"""
		
		self.__Name = name
		self.__Aliases = list(aliases) if aliases else list()
		self.__Type = type
		self.__Description = description
		self.__IsImportant = important

#==========================================================================================#
# >>>>> ТИПЫ ПОЗИЦИЙ <<<<< #
#==========================================================================================#

class _BasePosition:
	"""Базовая позиция команды."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def arguments(self) -> list[_Argument]:
		"""Список аргументов."""

		return self.__Arguments.copy()
	
	@property
	def flags(self) -> list[_Flag]:
		"""Список флагов."""

		return self.__Flags.copy()

	@property
	def keys(self) -> list[_Key]:
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

		Count = 0
		for Flag in self.__Flags:
			if Flag.is_important: Count += 1

		for Key in self.__Keys:
			if Key.is_important: Count += 2

		for Argument in self.__Arguments:
			if Argument.is_important: Count += 1

		return Count

	@property
	def parameters(self) -> list[_Argument | _Flag | _Key]:
		"""Список всех описанных параметров позиции."""

		return self.__Arguments + self.__Flags + self.__Keys

	#==========================================================================================#
	# >>>>> МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self):
		"""Базовая позиция команды."""
		
		self.__Arguments: list[_Argument] = list()
		self.__Flags: list[_Flag] = list()
		self.__Keys: list[_Key] = list()
		
	def add_argument(self, type: ParametersTypes = ParametersTypes.All, description: str | None = None):
		"""
		Добавляет аргумент на позицию.

		:param type: Тип аргумента.
		:type type: ParametersTypes
		:param description: Описание аргумента.
		:type description: str | None
		"""

		self.__Arguments.append(_Argument(type, description, important = False))

	def add_flag(self, name: str, aliases: Iterable[str] | None = None, description: str | None = None):
		"""
		Добавляет флаг на позицию.

		:param name: Название флага.
		:type name: str
		:param aliases: Список псевдонимов.
		:type aliases: Iterable[str] | None
		:param description: Описание флага.
		:type description: str | None
		"""

		self.__Flags.append(_Flag(name, aliases, description, important = False))

	def add_key(self, name: str, aliases: Iterable[str] | None = None, type: ParametersTypes = ParametersTypes.All, description: str | None = None):
		"""
		Добавляет ключ на позицию.

		:param name: Название ключа.
		:type name: str
		:param aliases: Список псевдонимов.
		:type aliases: Iterable[str] | None
		:param type: Тип значения ключа.
		:type type: ParametersTypes
		:param description: Описание ключа.
		:type description: str | None
		"""

		self.__Keys.append(_Key(name, aliases, type, description, important = False))

class _Position:
	"""Позиция команды."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def argument(self) -> _Argument:
		"""Аргумент."""

		return self.__Argument

	@property
	def description(self) -> str | None:
		"""Описание позиции."""

		return self.__Description
	
	@property
	def flags(self) -> list[_Flag]:
		"""Список флагов."""

		return self.__Flags.copy()

	@property
	def is_important(self) -> bool:
		"""Состояние: является ли позиция обязательной."""

		return self.__IsImportant

	@property
	def keys(self) -> list[_Key]:
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
	def parameters(self) -> list[_Argument | _Flag | _Key]:
		"""Список всех описанных параметров позиции."""

		List = self.__Flags + self.__Keys
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
		
		self.__Argument: _Argument | None = None
		self.__Flags: list[_Flag] = list()
		self.__Keys: list[_Key] = list()

	def add_flag(self, name: str, aliases: Iterable[str] | None = None, description: str | None = None):
		"""
		Добавляет флаг на позицию.

		:param name: Название флага.
		:type name: str
		:param aliases: Список псевдонимов.
		:type aliases: Iterable[str] | None
		:param description: Описание флага.
		:type description: str | None
		"""

		self.__Flags.append(_Flag(name, aliases, description, self.__IsImportant))

	def add_key(self, name: str, aliases: Iterable[str] | None = None, type: ParametersTypes = ParametersTypes.All, description: str | None = None):
		"""
		Добавляет ключ на позицию.

		:param name: Название ключа.
		:type name: str
		:param aliases: Список псевдонимов.
		:type aliases: Iterable[str] | None
		:param type: Тип значения ключа.
		:type type: ParametersTypes
		:param description: Описание ключа.
		:type description: str | None
		"""

		self.__Keys.append(_Key(name, aliases, type, description, self.__IsImportant))

	def set_argument(self, type: ParametersTypes = ParametersTypes.All, description: str | None = None):
		"""
		Устанавливает аргумент на позицию.

		:param type: Тип аргумента. По умолчанию `ParametersTypes.All`.
		:type type: ParametersTypes
		:param description: Описание аргумента. По умолчанию `None`.
		:type description: str | None
		"""

		self.__Argument = _Argument(type, description, self.__IsImportant)

#==========================================================================================#
# >>>>> ОСНОВНОЙ КЛАСС <<<<< #
#==========================================================================================#

class Command:
	"""Описание команды."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def base(self) -> _BasePosition:
		"""Базовая позиция команды."""

		return self.__BasePosition

	@property
	def category(self) -> str | None:
		"""Название категории, к которой относится команда."""

		return self.__Category

	@property
	def description(self) -> str:
		"""Описание команды."""

		return self.__Description

	@property
	def max_parameters_count(self) -> int:
		"""Максимальное количество параметров."""

		return sum(position.max_parameters_count for position in self.positions) + self.__BasePosition.max_parameters_count

	@property
	def min_parameters_count(self) -> int:
		"""Минимальное количество параметров."""

		return sum(position.min_parameters_count for position in self.positions) + self.__BasePosition.min_parameters_count

	@property
	def name(self) -> str:
		"""Название команды."""

		return self.__Name

	@property
	def positions(self) -> list[_Position]:
		"""Список позиций."""

		return self.__Positions.copy()

	#==========================================================================================#
	# >>>>> МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, name: str, description: str | None = None, category: str | None = None):
		"""
		Структура описания команды.

		:param name: Название команды.
		:type name: str
		:param description: Описание команды.
		:type description: str | None
		:param category: Название категории, к которой относится команда.
		:type category: str | None
		"""

		self.__Name = name
		self.__Description = description
		self.__Category = category

		self.__BasePosition = _BasePosition()
		self.__Positions: list[_Position] = list()

	def create_position(self, name: str, description: str | None = None, important: bool = False) -> _Position:
		"""
		Создаёт дополнительную позицию.

		:param name: Название позиции.
		:type name: str
		:param description: Описание позиции.
		:type description: str | None
		:param important: Указывает, является ли позиция обязательной. Для всех параметров позиции автоматически выставляется такое же значение.
		:type important: bool
		:return: Представление новой позиции.
		:rtype: Position
		"""

		NewPosition = _Position(name, description, important)
		self.__Positions.append(NewPosition)

		return self.__Positions[-1]
	
	def set_category(self, category: str | None):
		"""
		Задаёт категорию, в которой будет отображаться команда при выводе помощи.

		:param category: Название категории.
		:type category: str | None
		"""

		self.__Category = category