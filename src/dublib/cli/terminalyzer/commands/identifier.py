from typing import TYPE_CHECKING, Sequence

from .... import exceptions

if TYPE_CHECKING:
	from .model import CommandModel

class CommandIdentifier:
	"""Идентификатор команды."""

	@property
	def values(self) -> tuple[str] | tuple[str, str]:
		"""Кортеж из имени супергруппы (если включена) и команды."""

		if self.__model.group.supergroup:
			return (self.__model.group.supergroup, self.__model.name)

		return (self.__model.name,)

	def __init__(self, model: "CommandModel"):
		"""
		Идентификатор команды.

		:param model: Модель команды.
		:type model: CommandModel
		"""

		self.__model: "CommandModel" = model

	def as_str(self) -> str:
		"""
		Строка с идентификатором команды.

		:return: Имена супергруппы (если включена) и команды, разделённые пробелом.
		:rtype: str
		"""

		return " ".join(self.values)

	def clear_parameters(self, parameters: Sequence[str]) -> tuple[str, ...]:
		"""
		Удаляет идентификатор команды из параметров.

		:param parameters: Последовательность строк, начинающаяся с имени супергруппы и команды.
		:type parameters: Sequence[str]
		:return: Последовательность параметров без идентификатора.
		:rtype: tuple[str, ...]
		"""

		self.match(parameters, exception = True)
		identifiers_count: int = len(self.values)

		return tuple(parameters[identifiers_count:])

	def match(self, parameters: Sequence[str], exception: bool = False) -> bool:
		"""
		Проверяет соответствие идентификатора команды набору параметров.

		:param parameters: Последовательность строк, начинающаяся с имени супергруппы и команды.
		:type parameters: Sequence[str]
		:param exception: Переключает выброс исключения.
		:type exception: bool
		:return: Возвращает `True`, если идентификатор совпадает с переданными параметрами.
		:rtype: bool
		:raises UnfamiliarParametersError: Обрабатываемые параметры не соответствуют идентификатору модели.
		"""

		identifiers = self.values
		identifiers_count: int = len(identifiers)
		parameters_tuple: tuple[str, ...] = tuple(parameters)

		is_match: bool = False

		if identifiers_count > len(parameters_tuple):
			is_match = False
		else:
			is_match = parameters_tuple[: identifiers_count] == identifiers

		if not is_match and exception:
			raise exceptions.cli.terminalyzer.parameters.UnfamiliarParametersError(self)

		return is_match
