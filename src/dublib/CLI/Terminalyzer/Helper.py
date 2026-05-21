from .Command.Definition import _Argument, _BasePosition, Command, _Flag, _Key, _Position
from ..TextStyler import FastStyler

from dataclasses import dataclass
from typing import Callable

from prettytable import PLAIN_COLUMNS, PrettyTable

#==========================================================================================#
# >>>>> ДОПОЛНИТЕЛЬНЫЕ СТРУКТУРЫ ДАННЫХ <<<<< #
#==========================================================================================#

@dataclass
class _HelpLabels:
	"""
	Контейнер используемых в модуле помощи строк.

	Для `COMMAND_NOT_FOUND` можно определить место подстановки команды через `%c`.
	"""

	COMMAND_DESCRIPTION: str = "Print list of supported commands. For details, add name of command as argument."
	ARGUMENT_DESCRIPTION: str = "The name of command for which you want to see detailed help."
	COMMAND_NOT_FOUND: str = "Command \"%c\" not found."
	CATEGORY_OTHER: str = "Other"

#==========================================================================================#
# >>>>> ОСНОВНОЙ КЛАСС <<<<< #
#==========================================================================================#

class Helper:
	"""Модуль помощи."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def callback(self) -> Callable:
		"""Функция, в которую направляется вывод помощи."""

		return self.__Callback
	
	@property
	def category(self) -> str | None:
		"""Категория команд."""

		return self.__Category

	@property
	def command(self) -> Command:
		"""Описание команды помощи."""

		return self.__HelpCommand

	@property
	def is_enabled(self) -> bool:
		"""Состояние: активирован ли модуль помощи."""

		return self.__IsEnabled
	
	@property
	def is_sorting_enabled(self) -> bool:
		"""Состояние: выполняется ли сортировка команд по алфавиту."""

		return self.__IsSortingEnabled

	@property
	def labels(self) -> _HelpLabels:
		"""Оператор работы с используемыми в модуле помощи строками."""

		return self.__Labels

	#==========================================================================================#
	# >>>>> ПРИВАТНЫЕ МЕТОДЫ ГЕНЕРАЦИИ ПОМОЩИ <<<<< #
	#==========================================================================================#
	
	def __BuildBasePositionDescription(self, base_position: "_BasePosition", typing: bool = True) -> list[str]:
		"""
		Строит описание базовой позиции.

		:param base_position: Данные базовой позиции.
		:type base_position: _BasePosition
		:param typing: Переключает отображение типов.
		:type typing: bool
		:return: Список строк, описывающих позицию.
		:rtype: list[str]
		"""

		Indicator = "• "
		Indent = "  "
		Help = list()

		if not base_position.parameters: return Help
		Help.append(f"{Indicator}Other parameters:")

		for CurrentParameter in base_position.parameters:
			Description = Indent * 2
			Description += self.__BuildParameterLabel(CurrentParameter, typing)
			if CurrentParameter.description: Description += f": {CurrentParameter.description}"
			Help.append(Description)

		for Index in range(len(Help)): Help[Index] = f"\n{Indent}" + Help[Index]

		return Help

	def __BuildParameterLabel(self, parameter: _Argument | _Flag | _Key, typing: bool = True) -> str:
		"""
		Строит надпись-индикатор для параметра.

		:param parameter: Параметр позиции.
		:type parameter: Argument | Flag | Key
		:param typing: Переключает отображение типов.
		:type typing: bool
		:raises ValueError: Передан неверный объект.
		:return: Надпиьс-индикатор.
		:rtype: str
		"""

		match parameter.__class__.__name__:

			case "_Argument": 
				Typer = f"<{parameter.type.value}>" if typing else ""
				return f"[argument{Typer}]"
			
			case "_Flag":
				Name = self.__GetParameterName(parameter.name, parameter.aliases)
				return f"[flag {Name}]"
			
			case "_Key":
				Typer = f"<{parameter.type.value}>" if typing else ""
				Name = self.__GetParameterName(parameter.name, parameter.aliases)
				return f"[key{Typer} {Name}]"
			
			case _: raise ValueError(f"Incorrect parameter object: {parameter}.")

	def __BuildPositionDescription(self, position: _Position, typing: bool = True) -> list[str]:
		"""
		Строит описание позиции.

		:param position: Данные позиции.
		:type position: _Position
		:param typing: Переключает отображение типов.
		:type typing: bool
		:return: Список строк, описывающих позицию.
		:rtype: list[str]
		"""

		Indicator = "• "
		Indent = "  "
		Help = list()
		
		Title = Indicator
		Name = position.name
		if position.is_important: Name = FastStyler(Name).colorize.blue
		Title += Name

		if len(position.parameters) == 1:
			Title += " " + self.__BuildParameterLabel(position.parameters[0], typing)
			if position.description: Title += f": {position.description}"
			Help.append(Title)

		else:
			if position.description: Title += f": {position.description}"
			Help.append(Title)

			for CurrentParameter in position.parameters:
				Description = Indent * 2
				Description += self.__BuildParameterLabel(CurrentParameter, typing)
				if CurrentParameter.description: Description += f": {CurrentParameter.description}"
				Help.append(Description)
	
		for Index in range(len(Help)): Help[Index] = f"\n{Indent}" + Help[Index]

		return Help

	def __GenerateCommandMap(self, command: Command) -> str:
		"""
		Генерирует позиционную карту команды.

		:param command: Данные команды.
		:type command: Command
		:return: Позиционная карта. Обязательные позиции выделены синим.
		:rtype: str
		"""

		CommandMap = str()

		for Position in command.positions:
			Name = Position.name or "POSITION"
			if Position.is_important: Name = FastStyler(Name).colorize.blue
			CommandMap += " {" + Name + "}"

		return CommandMap

	def __GetParameterName(self, name: str, aliases: list[str]) -> str:
		"""
		Возвращает форматированное имя параметра вместе с псевдонимами.

		:param name: Имя параметра.
		:type name: str
		:param aliases: Список псевдонимов.
		:type aliases: list[str]
		:return: Форматированное имя параметра вместе с псевдонимами.
		:rtype: str
		"""

		name = FastStyler(name).decorate.bold
		for Index in range(len(aliases)): aliases[Index] = FastStyler(aliases[Index]).decorate.bold
		if aliases: return ", ".join([name] + aliases)

		return name

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self):
		"""Модуль помощи."""

		self.__Labels = _HelpLabels()
		self.__Callback = print
		self.__Category = None

		self.__IsEnabled = False
		self.__IsSortingEnabled = False

		self.__HelpCommand = Command("help", self.labels.COMMAND_DESCRIPTION, self.__Category)
		ComPos = self.__HelpCommand.create_position("COMMAND", "Command name for help details.")
		ComPos.set_argument()
		self.__HelpCommand.base.add_flag("-t", aliases = ("--typed",), description = "Show arguments and keys expected types.")

	def generate_help_command(self, commands: list[Command], command_name: str, typing: bool = True):
		"""
		Отправляет подробное описание команды в callback-функцию.

		:param commands: Описательные структуры комманд.
		:type commands: list[Command]
		:param command_name: Название команды, для которой требуется получить помощь.
		:type command_name: str
		:param typing: Переключает отображение типов.
		:type typing: bool
		"""

		CommandForHelp = None

		for CurrentCommand in commands:
			if CurrentCommand.name == command_name:
				CommandForHelp = CurrentCommand
				break

		if CommandForHelp:
			Help = FastStyler(CommandForHelp.name).decorate.bold
			Help += self.__GenerateCommandMap(CommandForHelp)
			if CommandForHelp.description: Help += "\n" + FastStyler(CommandForHelp.description).decorate.italic
			
			for Position in CommandForHelp.positions:
				Lines = self.__BuildPositionDescription(Position, typing)
				if Lines: Help += "".join(Lines)

			Lines = self.__BuildBasePositionDescription(CommandForHelp.base, typing)
			if Lines: Help += "".join(Lines)

			self.__Callback(Help)

		else: self.__Callback(self.__Labels.COMMAND_NOT_FOUND.replace(r"%c", command_name))

	def generate_help_list(self, commands: list[Command]):
		"""
		Отправляет список команд с их описанием в callback-функцию.

		:param commands: Описательные структуры комманд.
		:type commands: list[Command]
		"""

		#---> Получение данных.
		#==========================================================================================#
		CommandsCategories: dict[None | str, list[Command]] = {
			None: []
		}

		if self.__IsSortingEnabled: commands = sorted(commands, key = lambda CurrentCommand: CurrentCommand.name)

		for CurrentCommand in commands:
			if CurrentCommand.category in CommandsCategories.keys(): CommandsCategories[CurrentCommand.category].append(CurrentCommand)
			else: CommandsCategories[CurrentCommand.category] = [CurrentCommand]

		# Помещение команд без категории в конец.
		if len(CommandsCategories.keys()) > 1:
			NoneCategory = CommandsCategories[None]
			del CommandsCategories[None]
			CommandsCategories[None] = NoneCategory

		#---> Генерация таблицы.
		#==========================================================================================#
		TableString = ""

		for Category in CommandsCategories.keys():
			HelpTable = {
				"Commands": [],
				"Descriptions": []
			}

			Commands = sorted(CommandsCategories[Category], key = lambda Element: Element.name)

			for CurrentCommand in Commands:
				HelpTable["Commands"].append("  " + CurrentCommand.name)
				HelpTable["Descriptions"].append(CurrentCommand.description or "")

			TableObject = PrettyTable()
			if len(CommandsCategories.keys()) > 1: TableObject.title = FastStyler(Category or self.__Labels.CATEGORY_OTHER).decorate.bold
			TableObject.set_style(PLAIN_COLUMNS)

			for ColumnName in HelpTable.keys():
				Buffer = FastStyler(ColumnName).decorate.bold
				TableObject.add_column(Buffer, HelpTable[ColumnName])

			TableObject.align = "l"
			TableString += TableObject.get_string(header = False)
			TableString += "\n\n"

		self.__Callback(TableString.rstrip())

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ НАСТРОЙКИ <<<<< #
	#==========================================================================================#

	def enable(self, status: bool = True):
		"""
		Переключает использование модуля помощи.

		:param status: Статус использования модуля.
		:type status: bool
		"""

		self.__IsEnabled = status

	def enable_sorting(self, status: bool = True):
		"""
		Переключает сортировку команд в алфавитном порядке.

		:param status: Состояние сортировки.
		:type status: bool
		"""

		self.__IsSortingEnabled = status

	def set_callback(self, callback: Callable):
		"""
		Задаёт функцию, в которую будет передан вывод помощи.

		:param callback: Функция, в которую направляется вывод помощи. Принимает строку в качестве аргумента.
		:type callback: Callable
		"""

		self.__Callback = callback

	def set_category(self, category: str | None):
		"""
		Задаёт категорию для команды помощи.

		:param category: Название категории.
		:type category: str | None
		"""

		self.__Category = category
