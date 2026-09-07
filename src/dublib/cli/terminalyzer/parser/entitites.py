from typing import TYPE_CHECKING, Literal, Sequence, overload

from .... import exceptions
from .typing import SUPPORTED_TYPES

if TYPE_CHECKING:
	from ..commands.model import CommandModel
	from ..commands.parameters import Argument, Flag, Key
	from ..commands.positions import Position

__all__ = ["ArgumentEntity", "FlagEntity", "KeyEntity", "PositionEntity", "CommandEntity"]

class ArgumentEntity:
	"""Сущность аргумента."""

	@property
	def parameter(self) -> "Argument":
		"""Параметр."""

		return self.__parameter

	@property
	def value(self) -> SUPPORTED_TYPES:
		"""Значение аргумента."""

		return self.__value

	def __init__(self, parameter: "Argument", value: SUPPORTED_TYPES):
		"""
		Сущность аргумента.

		:param parameter: Параметр.
		:type parameter: Argument
		:param value: Значение аргумента.
		:type value: SUPPORTED_TYPES
		"""

		self.__parameter = parameter
		self.__value = value

class FlagEntity:
	"""Сущность флага."""

	@property
	def parameter(self) -> "Flag":
		"""Параметр."""

		return self.__parameter

	@property
	def value(self) -> bool:
		"""Состояние активации флага."""

		return self.__value

	def __init__(self, parameter: "Flag", value: bool):
		"""
		Сущность аргумента.

		:param parameter: Параметр.
		:type parameter: Flag
		:param value: Значение ключа.
		:type value: bool
		"""

		self.__parameter = parameter
		self.__value = value

class KeyEntity:
	"""Сущность ключа."""

	@property
	def parameter(self) -> "Key":
		"""Параметр."""

		return self.__parameter

	@property
	def value(self) -> SUPPORTED_TYPES:
		"""Значение ключа."""

		return self.__value

	def __init__(self, parameter: "Key", value: SUPPORTED_TYPES):
		"""
		Сущность аргумента.

		:param parameter: Параметр.
		:type parameter: Key
		:param value: Значение ключа.
		:type value: SUPPORTED_TYPES
		"""

		self.__parameter = parameter
		self.__value = value

class PositionEntity:
	"""Сущность позиции."""

	@property
	def content(self) -> ArgumentEntity | FlagEntity | KeyEntity | None:
		"""Содержимое позиции."""

		return self.__content

	@property
	def position(self) -> "Position":
		"""Позиция."""

		return self.__position

	def __init__(self, position: "Position", content: ArgumentEntity | FlagEntity | KeyEntity | None):
		"""
		Сущность позиции.

		:param position: Позиция.
		:type position: Position
		:param content: Содержимое позиции.
		:type content: ArgumentEntity | FlagEntity | KeyEntity | None
		:raises ImportantPositionEmptyError: Для обязательной позиции не задан параметр.
		"""

		self.__position: "Position" = position
		self.__content: ArgumentEntity | FlagEntity | KeyEntity | None = content

		if self.__position.is_important and self.__content is None:
			raise exceptions.cli.terminalyzer.positions.ImportantPositionEmptyError(self.__position.name)

class CommandEntity:
	"""Сущность команды."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def model(self) -> "CommandModel":
		"""Модель команды."""

		return self.__model

	#==========================================================================================#
	# >>>>> ПРИВАТНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __check_value_type[T: SUPPORTED_TYPES](self, value: SUPPORTED_TYPES | None, expected_type: type[T] | None = None) -> SUPPORTED_TYPES | None:
		"""
		Проверяет тип возвращаемого значения.

		:return: Возвращаемое значение.
		:rtype: SUPPORTED_TYPES | None
		:raises TypeError: Ожидается другой тип данных.
		"""

		if expected_type and value is not None:
			if not isinstance(value, expected_type):
				raise TypeError(f"Expected \"{expected_type}\", but key value is \"{type(value)}\" type.")

		return value

	def __get_activated_named_parameters_names(self, entity_type: type[FlagEntity | KeyEntity]) -> list[str]:
		"""
		Возвращает последовательность имён и алиасов именованных параметров определённого типа.

		:param entity_type: Тип сущности параметра.
		:type entity_type: type[FlagEntity | KeyEntity]
		:return: Последовательность имён активированных флагов и их алиасов.
		:rtype: list[str]
		"""

		names: list[str] = []

		for position in self.__positions.values():
			content = position.content

			if isinstance(content, entity_type):
				names.append(content.parameter.name)
				names += content.parameter.aliases

		for base_parameter_entity in self.__base:
			if isinstance(base_parameter_entity, entity_type):
				names.append(base_parameter_entity.parameter.name)
				names += base_parameter_entity.parameter.aliases

		return names

	def __get_parameters_entities_type[T: ArgumentEntity | FlagEntity | KeyEntity](self, entity_type: type[T]) -> list[T]:
		"""
		Возвращает последовательность сущностей параметров определённого типа.

		:param entity_type: Тип сущности параметра.
		:type entity_type: type[ArgumentEntity | FlagEntity | KeyEntity]
		:return: Последовательность имён активированных флагов и их алиасов.
		:rtype: list[ArgumentEntity | FlagEntity | KeyEntity]
		"""

		parameters_entities: list[T] = []

		for position in self.__positions.values():
			content = position.content

			if isinstance(content, entity_type):
				parameters_entities.append(content)

		for base_parameter_entity in self.__base:
			if isinstance(base_parameter_entity, entity_type):
				parameters_entities.append(base_parameter_entity)

		return parameters_entities

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, model: "CommandModel", base: Sequence["ArgumentEntity | FlagEntity | KeyEntity"], positions: Sequence["PositionEntity"]):
		"""
		Сущность команды.

		:param model: Модель команды.
		:type model: CommandModel
		:param group: Группа, к которой относится команда.
		:type group: ModelsGroup
		:param base: Сущности параметров базовой позиции.
		:type base: Sequence["ArgumentEntity | FlagEntity | KeyEntity"]
		:param positions: Сущности позиций.
		:type positions: Sequence["PositionEntity"]
		"""

		self.__model: "CommandModel" = model
		self.__base: Sequence["ArgumentEntity | FlagEntity | KeyEntity"] = base
		self.__positions: dict[str, "PositionEntity"] = {position.position.name: position for position in positions}

	def check_flag(self, flag: str) -> bool:
		"""
		Проверяет, активирован ли флаг.
		
		:param flag: Имя флага.
		:type flag: str
		:return: Результат проверки.
		:rtype: bool
		"""

		return flag in self.__get_activated_named_parameters_names(FlagEntity)

	def check_key(self, key: str) -> bool:
		"""
		Проверяет, активирован ли ключ.
		
		:param key: Имя ключа.
		:type key: str
		:return: Результат проверки.
		:rtype: bool
		"""

		return key in self.__get_activated_named_parameters_names(KeyEntity)

	@overload
	def get_key_value[T: SUPPORTED_TYPES](self, key: str, expected_type: type[T], not_found_error: Literal[True]) -> T: ...
	@overload
	def get_key_value[T: SUPPORTED_TYPES](self, key: str, expected_type: type[T], not_found_error: Literal[False] = False) -> T | None: ...
	@overload
	def get_key_value(self, key: str, expected_type: None = None, not_found_error: Literal[True] = True) -> SUPPORTED_TYPES: ...
	@overload
	def get_key_value(self, key: str, expected_type: None = None, not_found_error: Literal[False] = False) -> SUPPORTED_TYPES | None: ...

	def get_key_value[T: SUPPORTED_TYPES](self, key: str, expected_type: type[T] | None = None, not_found_error: bool = False) -> SUPPORTED_TYPES | None:
		"""
		Возвращает значение активированного ключа.

		:param key: Имя ключа.
		:type key: str
		:param expected_type: Ожидаемый тип значения. Если тип не соответствует, будет выброшено исключение `TypeError`. Проверяются только значения, отличные от `None`.
		:type expected_type: type[SUPPORTED_TYPES] | None
		:param not_found_error: Указывает, выбрасывать ли исключение, если ключ не активирован.
		:type not_found_error: bool
		:return: Значение ключа или `None` при отсутствующем ключе.
		:rtype: SUPPORTED_TYPES | None
		:raises KeyMissingError: Ключ не активирован. Выбрасывается только при активации параметра `not_found_error`.
		:raises TypeError: Ожидается другой тип данных.
		"""

		value: SUPPORTED_TYPES | None = None
		is_key_found: bool = False

		for key_entity in self.__get_parameters_entities_type(KeyEntity):
			key_parameter = key_entity.parameter

			if key_parameter.name == key or key in key_parameter.aliases:
				value = key_entity.value
				is_key_found = True
				break

		if not is_key_found and not_found_error:
			raise exceptions.cli.terminalyzer.parameters.KeyMissingError(key)

		return self.__check_value_type(value, expected_type)

	@overload
	def get_position_parameter(self, position_name: str, not_found_error: Literal[True] = True) -> ArgumentEntity | FlagEntity | KeyEntity: ...
	@overload
	def get_position_parameter(self, position_name: str, not_found_error: Literal[False] = False) -> ArgumentEntity | FlagEntity | KeyEntity | None: ...

	def get_position_parameter(self, position_name: str, not_found_error: bool = False) -> ArgumentEntity | FlagEntity | KeyEntity | None:
		"""
		Возвращает сущность параметра позиции.

		:param position_name: Имя позиции.
		:type position_name: str
		:param not_found_error: Указывает, выбрасывать ли исключение, если ключ не активирован.
		:type not_found_error: bool
		:return: Сущность параметра позиции или `None` при пустой позиции.
		:rtype: ArgumentEntity | FlagEntity | KeyEntity | None
		:raises PositionNotFoundError: Позиция не найдена.
		"""

		if position_name not in self.__positions:

			if not_found_error:
				raise exceptions.cli.terminalyzer.positions.PositionNotFoundError(position_name)

			return None

		return self.__positions[position_name].content

	@overload
	def get_position_value[T: SUPPORTED_TYPES](self, position_name: str, expected_type: type[T], important: Literal[True]) -> T: ...
	@overload
	def get_position_value[T: SUPPORTED_TYPES](self, position_name: str, expected_type: type[T], important: Literal[False] = False) -> T | None: ...
	@overload
	def get_position_value(self, position_name: str, expected_type: None = None, important: Literal[True] = True) -> SUPPORTED_TYPES: ...
	@overload
	def get_position_value(self, position_name: str, expected_type: None = None, important: Literal[False] = False) -> SUPPORTED_TYPES | None: ...

	def get_position_value[T: SUPPORTED_TYPES](self, position_name: str, expected_type: type[T] | None = None, important: bool = False) -> SUPPORTED_TYPES | None:
		"""
		Возвращает значение позиции.

		:param position_name: Имя позиции.
		:type position_name: str
		:param expected_type: Ожидаемый тип значения.
		:type expected_type: type[SUPPORTED_TYPES] | None
		:param important: Указывает, должна ли позиция обязательно иметь значение.
		:type important: bool
		:return: Параметр позиции или `None` при пустой позиции. Для флага возвращает статус активации.
		:rtype: SUPPORTED_TYPES | None
		:raises ImportantPositionEmptyError: Для обязательной позиции не задан параметр.
		:raises PositionNotFoundError: Позиция не найдена.
		:raises TypeError: Ожидается другой тип данных.
		"""

		parameter_entity: ArgumentEntity | FlagEntity | KeyEntity | None = self.get_position_parameter(position_name)
		value: SUPPORTED_TYPES | None = None

		if parameter_entity:
			value = parameter_entity.value

		if value is None and important:
			raise exceptions.cli.terminalyzer.positions.ImportantPositionEmptyError(position_name)

		return self.__check_value_type(value, expected_type)