import sys
from typing import TYPE_CHECKING, Sequence

from ...functions.data import to_sequence
from .commands.group import ModelsGroup
from .commands.model import CommandModel
from .helper import Helper
from .parser import CommandParser

if TYPE_CHECKING:
	from .parser.entitites import CommandEntity

__all__ = ["ModelsGroup", "Terminalyzer", "CommandModel"]

class Terminalyzer:
	"""Обработчик команд."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def helper(self) -> Helper:
		"""Моудль помощи."""

		return self.__helper

	#==========================================================================================#
	# >>>>> ПРИВАТНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __find_model(self, parameters: tuple[str, ...]) -> CommandModel | None:
		"""
		Производит поиск соответствующей параметрам модели команды.

		:param parameters: Последовательность строк, представляющих команду.
		:type parameters: tuple[str, ...]
		:return: Модель команды.
		:rtype: CommandModel | None
		"""

		for group in self.__groups:
			for model in group.models:
				if model.indentificator.match(parameters):
					return model

		return None

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self):
		"""Обработчик команд."""

		self.__helper = Helper()
		self.__groups: tuple["ModelsGroup", ...] = ()

	def set_commands_groups(self, groups: ModelsGroup | Sequence[ModelsGroup]):
		"""
		Задаёт последовательность групп команд. Последовательность будет преобразована в кортеж для защиты от внешнего изменения.

		:param groups: Последовательность групп команд.
		:type groups: ModelsGroup | Sequence[ModelsGroup]
		"""

		self.__groups = to_sequence(groups)

	def parse_parameters(self, parameters: Sequence[str] | None = None) -> "CommandEntity | None":
		"""
		Парсит параметры команды, представленные последовательностью строк. Если команда не передана, будут обработаны аргументы точки запуска скрипта Python.

		Для получения последовательности из строки рекомендуется использовать `shlex.split()`.

		:param parameters: Последовательность строк, представляющих команду.
		:type parameters: Sequence[str] | None
		:return: Сущность команды или `None`, если не удалось сопаставить параметры ни с одной моделью.
		:rtype: CommandEntity | None
		"""

		if parameters is None:
			parameters = tuple(sys.argv[1:])
		else:
			parameters = tuple(parameters)

		if not parameters:
			return None

		model: "CommandModel | None" = self.__find_model(parameters)

		if not model:
			return None

		return CommandParser(model, parameters).parse()
