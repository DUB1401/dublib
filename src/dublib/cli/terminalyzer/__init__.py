import sys
from typing import TYPE_CHECKING, Sequence

from ...functions.data import to_sequence
from .commands.group import ModelsGroup
from .commands.model import CommandModel
from .parser import CommandParser

if TYPE_CHECKING:
	from .parser.entitites import CommandEntity

__all__ = ["ModelsGroup", "Terminalyzer"]

class Terminalyzer:
	"""Обработчик команд."""

	@property
	def groups(self) -> tuple[ModelsGroup, ...]:
		"""Последовательность групп моделей команд."""

		return self.__groups

	def __init__(self):
		"""Обработчик команд."""

		self.__groups: tuple["ModelsGroup", ...] = ()

	def find_model(self, parameters: Sequence[str]) -> CommandModel | None:
		"""
		Производит поиск соответствующей параметрам модели команды.

		:param parameters: Последовательность строк, представляющих команду.
		:type parameters: Sequence[str]
		:return: Модель команды.
		:rtype: CommandModel | None
		"""

		for group in self.__groups:
			for model in group.models:
				if model.indentificator.match(parameters):
					return model

		return None

	def set_models_groups(self, groups: ModelsGroup | Sequence[ModelsGroup]):
		"""
		Set commands models group sequence. Sequence will be transformated into a tuple to protect it from external modification. 

		:param groups: Group of commands models or it sequence.
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

		model: "CommandModel | None" = self.find_model(parameters)

		if not model:
			return None

		return CommandParser(model, parameters).parse()
