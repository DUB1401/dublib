from typing import TYPE_CHECKING

from prettytable import PLAIN_COLUMNS, PrettyTable

from ...text_styler import FastStyler, get_styled_text_from_html
from ..commands.parameters import Argument, Flag, Key
from .options import HelperOptions

if TYPE_CHECKING:
	from ..commands import CommandModel, ModelsGroup
	from ..commands.positions import BasePosition, Position
	
__all__ = ["Helper", "HelperOptions"]

class Helper:
	"""Генератор справки по командам."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def options(self) -> HelperOptions:
		"""Опции генератора справки по командам."""

		return self.__options

	#==========================================================================================#
	# >>>>> ПРИВАТНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __build_base_position_info(self, base: "BasePosition") -> list[str]:
		"""
		Строит описание базовой позиции.

		:param base: Базовая позиция.
		:type base: BasePosition
		:return: Список строк, описывающих позицию.
		:rtype: list[str]
		"""

		info: list[str] = []

		if not base.parameters:
			return info

		for parameter in base.parameters:
			parameter_info = self.options.base_marker
			parameter_info += self.__build_parameter_label(parameter)

			if parameter.description:
				parameter_info += f": {parameter.description}"

			info.append(parameter_info)

		for Index in range(len(info)):
			info[Index] = f"\n{self.options.indent}" + info[Index]

		return info

	def __build_command_map(self, model: "CommandModel") -> str:
		"""
		Генерирует позиционную карту команды.

		:param model: Модель команды.
		:type model: CommandModel
		:return: Позиционная карта.
		:rtype: str
		"""

		command_map: str = ""

		for position in model.positions:
			name: str = self.__get_stylized_position_name(position)
			command_map += f" {{{name}}}"

		if model.base.parameters:
			command_map += " …"

		return command_map

	def __build_parameter_label(self, parameter: Argument | Flag | Key) -> str:
		"""
		Строит надпись-индикатор для параметра.

		:param parameter: Параметр позиции.
		:type parameter: Argument | Flag | Key
		:return: Надпиьс-индикатор.
		:rtype: str
		:raises TypeError: Передан неверный объект.
		"""

		if isinstance(parameter, Argument):
			typer: str = f"<{parameter.type.value.__name__}>" if self.options.typing else ""
			return f"[argument{typer}]"

		if isinstance(parameter, Flag):
			naming: str = self.__build_parameter_naming(parameter.name, parameter.aliases)
			return f"[flag {naming}]"

		if isinstance(parameter, Key):
			typer: str = f"<{parameter.type.value.__name__}>" if self.options.typing else ""
			naming: str = self.__build_parameter_naming(parameter.name, parameter.aliases)
			return f"[key{typer} {naming}]"

		raise TypeError(f"Unsupported parameter object: {type(parameter)}.")

	def __build_parameter_naming(self, name: str, aliases: list[str]) -> str:
		"""
		Возвращает форматированное имя параметра вместе с псевдонимами.

		:param name: Имя параметра.
		:type name: str
		:param aliases: Список псевдонимов.
		:type aliases: list[str]
		:return: Форматированное имя параметра вместе с псевдонимами.
		:rtype: str
		"""

		name = FastStyler(name).decorate.bold if self.options.stylize else name

		if self.options.stylize:
			for Index in range(len(aliases)): 
				aliases[Index] = FastStyler(aliases[Index]).decorate.bold

		if aliases:
			return ", ".join([name] + aliases)

		return name

	def __build_position_info(self, position: "Position") -> list[str]:
		"""
		Строит описание позиции.

		:param position: Данные позиции.
		:type position: _Position
		:return: Список строк, описывающих позицию.
		:rtype: list[str]
		"""

		info: list[str] = []
		
		title = self.options.position_marker
		title += self.__get_stylized_position_name(position)

		if len(position.parameters) == 1:
			title += " " + self.__build_parameter_label(position.parameters[0])

			if position.description:
				title += f": {position.description}"

			info.append(title)

		else:
			if position.description:
				description = get_styled_text_from_html(position.description) if self.options.parse_html else position.description
				title += f": {description}"

			info.append(title)

			for parameter in position.parameters:
				parameter_info: str = self.options.indent * 2
				parameter_info += self.__build_parameter_label(parameter)

				if parameter.description:
					description = get_styled_text_from_html(parameter.description) if self.options.parse_html else position.description
					parameter_info += f": {parameter.description}"

				info.append(parameter_info)
	
		for Index in range(len(info)):
			info[Index] = f"\n{self.options.indent}" + info[Index]

		return info

	def __get_stylized_position_name(self, position: "Position") -> str:
		"""
		Возвращает стилизованное имя позиции (синее для обязательной, серое для необязательной). Автоматически обрабатывает параметры стилизации.

		:param position: Позиция.
		:type position: Position
		:return: Стилизованное имя позиции.
		:rtype: str
		"""

		name: str = position.name

		if not self.options.stylize:
			return name

		if position.is_important:
			return FastStyler(name).colorize.blue

		return FastStyler(name).colorize.gray

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, options: HelperOptions | None = None):
		"""
		Генератор справки по командам.

		:param options: Опции генератора справки по командам.
		:type options: HelperOptions | None
		"""

		self.__options: HelperOptions = options or HelperOptions()

	def generate_command_info(self, model: "CommandModel") -> str:
		"""
		Генерирует справку по команде.

		:param model: Модель команды.
		:type model: CommandModel
		:return: Справка по команде.
		:rtype: str
		"""

		string_indentificator: str = model.indentificator.as_str()
		info: str = FastStyler(string_indentificator).decorate.bold if self.options.stylize else string_indentificator
		info += self.__build_command_map(model)

		if model.description:
			info += "\n"
			info += FastStyler(model.description).decorate.italic if self.options.stylize else model.description

		for position in model.positions:
			lines: list[str] = self.__build_position_info(position)
			if lines: info += "".join(lines)

		lines = self.__build_base_position_info(model.base)
		if lines: info += "".join(lines)

		return info

	def generate_group_list(self, group: "ModelsGroup") -> str:
		"""
		Генерирует список команд группы.

		:param group: Группа команд.
		:type group: ModelsGroup
		:return: Строка, представляющая таблицу со списком команд и описанием.
		:rtype: str
		"""

		models: tuple["CommandModel", ...] = group.models

		if self.options.sort:
			models = tuple(sorted(models, key = lambda model: model.name))
			
		super_command = f"{group.name} " if group.is_supergroup else ""
		table_data: dict[str, str] = {super_command + model.name: model.description or "" for model in models}

		table_generator = PrettyTable()
		table_generator.set_style(PLAIN_COLUMNS)
		table_generator.align = "l"
		table_generator.header = False

		for command_data in table_data.items():
			table_generator.add_row(list(command_data))

		return table_generator.get_string()