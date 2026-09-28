import shlex
import sys
from collections.abc import Sequence
from typing import TYPE_CHECKING

from ...functions.data import to_sequence
from .commands.group import ModelsGroup
from .commands.model import CommandModel
from .parser import CommandParser

if TYPE_CHECKING:
	from .parser.entities import CommandEntity

__all__ = ["ModelsGroup", "Terminalyzer"]

class Terminalyzer:
	"""Commands processor."""

	@property
	def groups(self) -> tuple[ModelsGroup, ...]:
		"""Models groups."""

		return self.__groups

	def __init__(self):
		"""Commands processor."""

		self.__groups: tuple[ModelsGroup, ...] = ()

	def find_model(self, data: Sequence[str]) -> CommandModel | None:
		"""
		Search model by command data.

		:param data: Command data.
		:type data: Sequence[str]
		:return: Command model.
		:rtype: CommandModel | None
		"""

		for group in self.__groups:
			for model in group.models:
				if model.indentificator.match(data):
					return model

		return None

	def set_models_groups(self, groups: ModelsGroup | Sequence[ModelsGroup]):
		"""
		Set commands models group sequence. Sequence will be transformed into a tuple to protect it from external modification. 

		:param groups: Group of commands models or it sequence.
		:type groups: ModelsGroup | Sequence[ModelsGroup]
		"""

		self.__groups = to_sequence(groups)

	def parse_command(self, data: str | Sequence[str] | None = None, call_handler: bool = True) -> "CommandEntity | None":
		"""
		Parse command data. 

		:param data: Input data. If no data, it will be received from Python script arguments. If data given as string, it will be split by `shlex.split()`.
		:type data: str | Sequence[str] | None
		:param call_handler: Automatically call provided by command model handler if available.
		:type call_handler: bool
		:return: Command parsed data as entity or `None` if model not found for processed parameters.
		:rtype: CommandEntity | None
		"""

		if data is None:
			data = tuple(sys.argv[1:])
		elif isinstance(data, str):
			data = shlex.split(data)
		else:
			data = tuple(data)

		if not data:
			return None

		model: CommandModel | None = self.find_model(data)

		if not model:
			return None

		entity = CommandParser(model, data).parse()

		if call_handler:
			entity.run_handler()

		return entity
