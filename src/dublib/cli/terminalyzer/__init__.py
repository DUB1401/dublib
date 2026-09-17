import shlex
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

	def parse_parameters(self, parameters: str | Sequence[str] | None = None, call_handler: bool = True) -> "CommandEntity | None":
		"""
		Parse command parameters. 

		:param parameters: Input parameters. If no parameters, it will be received from Python script arguments. If parameters given as string, it will be splitted by `shlex.split()`.
		:type parameters: str | Sequence[str] | None
		:param call_handler: Automatically call provided by command model hadnler if available.
		:type call_handler: bool
		:return: Command parsed data as entity or `None` if model not found for processed parameters.
		:rtype: CommandEntity | None
		"""

		if parameters is None:
			parameters = tuple(sys.argv[1:])
		elif isinstance(parameters, str):
			parameters = shlex.split(parameters)
		else:
			parameters = tuple(parameters)

		if not parameters:
			return None

		model: "CommandModel | None" = self.find_model(parameters)

		if not model:
			return None

		entity = CommandParser(model, parameters).parse()

		if call_handler and model.handler:
			model.handler(entity)

		return entity
