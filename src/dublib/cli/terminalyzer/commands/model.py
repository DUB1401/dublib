from typing import TYPE_CHECKING

from .identificator import CommandIdentificator
from .positions import BasePosition, Position

if TYPE_CHECKING:
	from .group import ModelsGroup

__all__ = ["CommandModel"]

class CommandModel:
	"""Модель команды."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def base(self) -> BasePosition:
		"""Базовая позиция команды."""

		return self.__base_position

	@property
	def description(self) -> str | None:
		"""Описание команды."""

		return self.__description

	@property
	def group(self) -> "ModelsGroup":
		"""Группа, к которой отностися модель."""

		return self.__group

	@property
	def indentificator(self) -> CommandIdentificator:
		"""Идентификатор команды."""

		return self.__identificator

	@property
	def max_parameters_count(self) -> int:
		"""Максимальное количество параметров."""

		return sum(position.max_parameters_count for position in self.positions) + self.__base_position.max_parameters_count

	@property
	def min_parameters_count(self) -> int:
		"""Минимальное количество параметров."""

		return sum(position.min_parameters_count for position in self.positions) + self.__base_position.min_parameters_count

	@property
	def name(self) -> str:
		"""Название команды."""

		return self.__name

	@property
	def positions(self) -> tuple[Position, ...]:
		"""Список позиций."""

		return tuple(self.__positions.values())

	#==========================================================================================#
	# >>>>> МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, group: "ModelsGroup", name: str, description: str | None = None):
		"""
		Модель команды.

		:param group: Группа, к которой относится модель.
		:type group: ModelsGroup
		:param name: Название команды.
		:type name: str
		:param description: Описание команды.
		:type description: str | None
		"""

		self.__group: "ModelsGroup" = group
		self.__name: str = name
		self.__description: str | None = description

		self.__identificator: "CommandIdentificator" = CommandIdentificator(self)

		self.__base_position = BasePosition()
		self.__positions: dict[str, Position] = {}

	def create_position(self, name: str, description: str | None = None, important: bool = False) -> Position:
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

		position = Position(name, description, important)
		self.__positions[name] = position

		return position
	
	def get_position(self, name: str) -> Position:
		"""
		Возвращает позицию.

		:param name: Имя позиции.
		:type name: str
		:return: Позиция.
		:rtype: Position
		:raises KeyError: Позиция не найдена.
		"""

		return self.__positions[name]