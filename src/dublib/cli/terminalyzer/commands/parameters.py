from typing import Sequence

from ....validators import ValidableTypes

__all__ = ["Argument", "Flag", "Key"]

class Argument:
	"""Аргумент команды."""

	@property
	def description(self) -> str | None:
		"""Описание аргумента."""

		return self.__Description
	
	@property
	def is_important(self) -> bool:
		"""Состояние: является ли аргумент обязательным."""

		return self.__IsImportant

	@property
	def type(self) -> ValidableTypes:
		"""Тип значения аргумента."""

		return self.__Type

	def __init__(self, value_type: ValidableTypes, description: str | None, important: bool):
		"""
		Аргумент команды.

		:param value_type: nип значения аргумента.
		:type value_type: ValidableTypes
		:param description: Описание аргумента.
		:type description: str | None
		:param important: Указывает, является ли аргумент обязательным.
		:type important: bool
		"""

		self.__Type = value_type
		self.__Description = description
		self.__IsImportant = important

class Flag:
	"""Флаг команды."""

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

	def __init__(self, name: str, aliases: Sequence[str] | None, description: str | None, important: bool):
		"""
		Флаг команды.

		:param name: Название флага.
		:type name: str
		:param aliases: Список псевдонимов.
		:type aliases: Sequence[str] | None
		:param description: Описание флага.
		:type description: str | None
		:param important: Указывает, является ли флаг обязательным.
		:type important: bool
		"""

		self.__Name = name
		self.__Aliases = list(aliases) if aliases else []
		self.__Description = description
		self.__IsImportant = important

class Key:
	"""Ключ команды."""

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
	def type(self) -> ValidableTypes:
		"""Тип значения ключа."""

		return self.__Type

	def __init__(self, name: str, aliases: Sequence[str] | None, value_type: ValidableTypes, description: str | None, important: bool):
		"""
		Ключ команды.

		:param name: Название ключа.
		:type name: str
		:param aliases: Список псевдонимов.
		:type aliases: Sequence[str] | None
		:param value_type: Тип значения ключа.
		:type value_type: ValidableTypes
		:param description: Описание ключа.
		:type description: str | None
		:param important: Указывает, является ли ключ обязательным.
		:type important: bool
		"""
		
		self.__Name = name
		self.__Aliases = list(aliases) if aliases else []
		self.__Type = value_type
		self.__Description = description
		self.__IsImportant = important
