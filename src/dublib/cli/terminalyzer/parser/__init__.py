from typing import TYPE_CHECKING, Sequence

from .... import exceptions
from .entitites import (
	ArgumentEntity,
	CommandEntity,
	FlagEntity,
	KeyEntity,
	PositionEntity,
)

if TYPE_CHECKING:
	from ..commands.model import CommandModel

__all__ = ["CommandParser"]

class CommandParser:
	"""Парсер команды."""

	#==========================================================================================#
	# >>>>> ПРИВАТНЫЕ МЕТОДЫ ВАЛИДАЦИИ <<<<< #
	#==========================================================================================#

	def __check_important_positions_parameters(self):
		"""
		Проверяет, все ли обязательные позиции заполнены.

		:raises ImportantPositionEmpty: Для обязательной позиции не задан параметр.
		"""

		for position in self.__model.positions:
			if position.is_important and self.__positions_parameters[position.name] is None:
				raise exceptions.cli.terminalyzer.positions.ImportantPositionEmptyError(position.name)

	def __check_prarameters_bounds(self):
		"""
		Проверяет, все ли параметры в команде использованы.

		:raises UnboundParameterError: Параметр не используется.
		"""

		if False in self.__parameters_locks:
			index: int = self.__parameters_locks.index(False)
			parameter: str = self.__parameters[index]
			raise exceptions.cli.terminalyzer.parameters.UnboundParameterError(parameter)

	def __chack_parameters_count(self):
		"""
		Проверяет соответвтсие количества параметров.
		
		:raises TooManyParametersError: Слишком много параметров.
		:raises NotEnoughParametersError: Недостаточно параметров.
		"""

		if self.__parameters_count > self.__model.max_parameters_count:
			raise exceptions.cli.terminalyzer.parameters.TooManyParametersError(self.__model.max_parameters_count, self.__parameters_count)

		if self.__parameters_count < self.__model.min_parameters_count:
			raise exceptions.cli.terminalyzer.parameters.NotEnoughParametersError(self.__model.min_parameters_count, self.__parameters_count)

	def __check_unbound_key(self, key: str, index: int):
		"""
		Проверяет ключ на наличие связи со значением по правилам:

		1. Ключ не должен быть последним параметром.
		2. Параметр после ключа не должен быть заблокирован.

		:param key: Имя ключа.
		:type key: str
		:param index: Индекс параметра.
		:type index: int
		:raises exceptions.cli.terminalyzer.parameters.UnboundKeyError: Ключ не связан со значением.
		"""

		if index + 1 == self.__parameters_count or self.__parameters_locks[index + 1]:
			raise exceptions.cli.terminalyzer.parameters.UnboundKeyError(key)

	#==========================================================================================#
	# >>>>> ПРИВАТНЫЕ МЕТОДЫ ПАРСИНГА <<<<< #
	#==========================================================================================#

	def __add_base_position_parameter(self, index: int, entity: ArgumentEntity | FlagEntity | KeyEntity):
		"""
		Добавляет сущность параметра на базовую позицию.

		:param index: Индекс параметра.
		:type index: int
		:param entity: Сущность параметра.
		:type entity: ArgumentEntity | FlagEntity | KeyEntity
		:raises IndexError: Параметр уже заблокирован.
		"""

		if self.__parameters_locks[index]:
			raise IndexError(f"Parameter with index {index} already locked.")

		self.__parameters_locks[index] = True
		if isinstance(entity, KeyEntity):
			self.__parameters_locks[index + 1] = True

		self.__base_parameters.append(entity)

	def __catch_parameters_for_base_position(self, parameter: str, index: int):
		"""
		Пытается интерпретировать каждый параметр для базовой позиции.

		:param parameter: Значение параметра.
		:type parameter: str
		:param index: Индекс параметра.
		:type index: int
		"""

		base = self.__model.base

		for flag in base.flags:
			if parameter == flag.name or parameter in flag.aliases:
				self.__add_base_position_parameter(index, FlagEntity(flag))
				return
		
		for key in base.keys:
			if parameter == key.name or parameter in key.aliases:
				self.__check_unbound_key(parameter, index)
				value = key.type.value.parse(self.__parameters[index + 1])
				self.__add_base_position_parameter(index, KeyEntity(key, value))
				return
			
		for argument in base.arguments:
			value = argument.type.value.parse(self.__parameters[index])
			self.__add_base_position_parameter(index, ArgumentEntity(argument, value))
			return

	def __catch_parameters_for_positions(self, parameter: str, index: int):
		"""
		Пытается интерпретировать каждый параметр для позиции.

		:param parameter: Значение параметра.
		:type parameter: str
		:param index: Индекс параметра.
		:type index: int
		"""

		for position in self.__model.positions:
			
			for flag in position.flags:
				if parameter == flag.name or parameter in flag.aliases:
					self.__lock_position(position.name, index, FlagEntity(flag))
					return
			
			for key in position.keys:
				if parameter == key.name or parameter in key.aliases:
					self.__check_unbound_key(parameter, index)
					value = key.type.value.parse(self.__parameters[index + 1])
					self.__lock_position(position.name, index, KeyEntity(key, value))
					return
				
			if position.argument and self.__positions_parameters[position.name] is None:
				value = position.argument.type.value.parse(self.__parameters[index])
				self.__lock_position(position.name, index, ArgumentEntity(position.argument, value))
				return

	def __lock_position(self, position_name: str, index: int, entity: ArgumentEntity | FlagEntity | KeyEntity):
		"""
		Заполняет позицию сущностью параметра.

		:param position_name: Имя позиции.
		:type position_name: str
		:param index: Индекс параметра.
		:type index: int
		:param entity: Сущность параметра.
		:type entity: ArgumentEntity | FlagEntity | KeyEntity
		:raises IndexError: Параметр уже заблокирован.
		:raises MultipleParametersOnPositionError: Попытка установить несколько параметров для одной позиции.
		"""

		if self.__parameters_locks[index]:
			raise IndexError(f"Parameter with index {index} already locked.")

		if self.__positions_parameters[position_name]:
			raise exceptions.cli.terminalyzer.positions.MultipleParametersOnPositionError(position_name)

		self.__parameters_locks[index] = True

		if isinstance(entity, KeyEntity):
			if self.__parameters_locks[index + 1]:
				raise IndexError(f"Key value parameter with index {index} already locked.")
			else:
				self.__parameters_locks[index + 1] = True

		self.__positions_parameters[position_name] = entity

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, model: "CommandModel", parameters: Sequence[str]):
		"""
		Парсер команды.

		:param model: Модель команды.
		:type model: CommandModel
		:param parameters: Последовательность строковых параметров команды без имени.
		:type parameters: Sequence[str]
		"""

		self.__model: "CommandModel" = model
		self.__parameters: tuple[str, ...] = tuple(self.__model.indentificator.clear_parameters(parameters))

		self.__parameters_count: int = len(self.__parameters)
		self.__parameters_locks: list[bool] = [False] * self.__parameters_count
		self.__positions_parameters: dict[str, ArgumentEntity | FlagEntity | KeyEntity | None] = {position.name: None for position in self.__model.positions}
		self.__base_parameters: list[ArgumentEntity | FlagEntity | KeyEntity] = []

	def parse(self) -> CommandEntity:
		"""
		Парсит параметры команды согласно модели в сущность.

		:return: Сущность команды.
		:rtype: CommandEntity
		"""

		parameters_range = range(self.__parameters_count)

		for index in parameters_range:
			if self.__parameters_locks[index]: continue
			self.__catch_parameters_for_positions(self.__parameters[index], index)

		for index in parameters_range:
			if self.__parameters_locks[index]: continue
			self.__catch_parameters_for_base_position(self.__parameters[index], index)

		self.__check_important_positions_parameters()
		self.__check_prarameters_bounds()
		self.__chack_parameters_count()

		return CommandEntity(
			model = self.__model,
			base = self.__base_parameters,
			positions = tuple(PositionEntity(position, self.__positions_parameters[position.name]) for position in self.__model.positions)
		)
