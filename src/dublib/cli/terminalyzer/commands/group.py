from typing import Sequence

from .... import exceptions
from ....functions.data import to_sequence
from .model import CommandModel

__all__ = ["ModelsGroup"]

class ModelsGroup:
	"""Группа команд."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def supergroup(self) -> str | None:
		"""Имя супергруппы."""

		return self.__supergroup

	@property
	def models(self) -> tuple["CommandModel", ...]:
		"""Последовательность моделей команд."""

		return tuple(self.__commands.values())

	@property
	def name(self) -> str | None:
		"""Имя группы."""

		return self.__name

	#==========================================================================================#
	# >>>>> ПРИВАТНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __add(self, models: "CommandModel | Sequence[CommandModel]"):
		"""
		Добавляет модель команды в группу.

		:param model: Модель команды.
		:type model: CommandModel | Sequence[CommandModel]
		:raises CommandModelOverridingError: Переопределение модели команды.
		:raises EmptyPositionError: Для позиции не описан ни один параметр.
		"""

		for model in to_sequence(models):
			self.__check_for_empty_positions(model)
			self.__check_descriptions_overriding(model)

			command_name: str = model.name

			if command_name in self.__commands:
				raise exceptions.cli.terminalyzer.groups.CommandModelOverridingError(command_name)

			self.__commands[command_name] = model

	def __check_descriptions_overriding(self, model: "CommandModel"):
		"""
		Проверяет позиции модели команды на переопределение описаний единственным параметром.

		:param model: Модель команды.
		:type model: CommandModel
		:raises PositionDescriptionOverridingError: Переопределение описания позиции.
		"""

		for position in model.positions:
			if position.description and len(position.parameters) == 1 and position.parameters[0].description:
				raise exceptions.cli.terminalyzer.positions.PositionDescriptionOverridingError(model.name, position.name)

	def __check_for_empty_positions(self, model: "CommandModel"):
		"""
		Проверяет позиции модели команды на пустоту.

		:param model: Модель команды.
		:type model: CommandModel
		:raises EmptyPositionError: Для позиции не описан ни один параметр.
		"""

		for position in model.positions:
			if not position.parameters:
				raise exceptions.cli.terminalyzer.positions.EmptyPositionError(model.name, position.name)

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, name: str | None = None, supergroup: str | None = None):
		"""
		Группа комманд.

		:param name: Имя группы.
		:type name: str | None
		:param supergroup: Указывает идентификатор супергруппы, используемый для обращения к командам группы по шаблону: `{supergroup} {command} {parameters}`.
		:type supergroup: str
		:raises ValueError: Супергруппа должна иметь имя.
		"""

		if supergroup and not name:
			raise ValueError("Supergroup must have name.")

		self.__name: str | None = name
		self.__supergroup: str | None = supergroup

		self.__commands: dict[str, "CommandModel"] = {}

	def clear(self):
		"""Удаляет хранимые модели команд."""

		self.__commands.clear()

	def create_model(self, name: str, description: str | None = None) -> CommandModel:
		"""
		Инициализирует модель команды и привязывает её к группе.

		:param name: Имя команды.
		:type name: str
		:param description: Описание команды.
		:type description: str | None
		:return: Модель команды.
		:rtype: CommandModel
		"""

		model = CommandModel(self, name, description)
		self.__add(model)

		return model

	def remove(self, command_name: str) -> bool:
		"""
		Удаляет команду из группы.

		:param command_name: Имя команды.
		:type command_name: str
		:return: Возвращает `True`, если команда найдена и удалена.
		:rtype: bool
		"""

		if command_name in self.__commands:
			del self.__commands[command_name]
			return True

		return False