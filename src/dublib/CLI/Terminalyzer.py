from .TextStyler.FastStyler import FastStyler
from ..Exceptions.CLI import *

from typing import Any, Callable, Iterable
from dataclasses import dataclass
from datetime import datetime
from functools import reduce
import enum
import sys
import os

from prettytable import PLAIN_COLUMNS, PrettyTable
import dateparser
import validators

#==========================================================================================#
# >>>>> ПЕРЕЧИСЛЕНИЯ ТИПОВ <<<<< #
#==========================================================================================#

class ParametersTypes(enum.Enum):
	"""Перечисление типов значений параметров."""

	All = "All"
	Base64 = "Base64"
	Bool = "Bool"
	Date = "Date"
	Email = "Email"
	Float = "Float"
	Integer = "Integer"
	IPv4 = "IPv4"
	IPv6 = "IPv6"
	Number = "Number"
	ValidPath = "ValidPath"
	Alpha = "Alpha"
	URL = "URL"

#==========================================================================================#
# >>>>> ПАРАМЕТРЫ КОМАНДЫ <<<<< #
#==========================================================================================#

class Argument:
	"""Аргумент команды."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def description(self) -> str | None:
		"""Описание аргумента."""

		return self.__Description
	
	@property
	def is_important(self) -> bool:
		"""Состояние: является ли аргумент обязательным."""

		return self.__IsImportant

	@property
	def type(self) -> ParametersTypes:
		"""Тип значения аргумента."""

		return self.__Type

	#==========================================================================================#
	# >>>>> МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, type: ParametersTypes, description: str | None, important: bool):
		"""
		Аргумент команды.

		:param type: nип значения аргумента.
		:type type: ParametersTypes
		:param description: Описание аргумента.
		:type description: str | None
		:param important: Указывает, является ли аргумент обязательным.
		:type important: bool
		"""

		#---> Генерация динамических атрибутов.
		#==========================================================================================#
		self.__Type = type
		self.__Description = description
		self.__IsImportant = important

class Flag:
	"""Флаг команды."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def description(self) -> str | None:
		"""Описание флага."""

		return self.__Description
	
	@property
	def is_important(self) -> bool:
		"""Состояние: является ли флаг обязательным."""

		return self.__IsImportant
	
	@property
	def name(self) -> str:
		"""Название флага."""

		return self.__Name

	#==========================================================================================#
	# >>>>> МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, name: str, description: str | None, important: bool):
		"""
		Флаг команды.

		:param name: Название флага.
		:type name: str
		:param description: Описание флага.
		:type description: str | None
		:param important: Указывает, является ли флаг обязательным.
		:type important: bool
		"""

		#---> Генерация динамических атрибутов.
		#==========================================================================================#
		self.__Name = name
		self.__Description = description
		self.__IsImportant = important

class Key:
	"""Ключ команды."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def description(self) -> str | None:
		"""Описание ключа."""

		return self.__Description
	
	@property
	def is_important(self) -> bool:
		"""Состояние: является ли ключ обязательным."""

		return self.__IsImportant
	
	@property
	def name(self) -> str:
		"""Название ключа."""

		return self.__Name
	
	@property
	def type(self) -> ParametersTypes:
		"""Тип значения ключа."""

		return self.__Type

	#==========================================================================================#
	# >>>>> МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, name: str, type: ParametersTypes, description: str | None, important: bool):
		"""
		Ключ команды.

		:param name: Название ключа.
		:type name: str
		:param type: Тип значения ключа.
		:type type: ParametersTypes
		:param description: Описание ключа.
		:type description: str | None
		:param important: Указывает, является ли ключ обязательным.
		:type important: bool
		"""

		#---> Генерация динамических атрибутов.
		#==========================================================================================#
		self.__Name = name
		self.__Type = type
		self.__Description = description
		self.__IsImportant = important

#==========================================================================================#
# >>>>> ВСПОМОГАТЕЛЬНЫЕ ТИПЫ ДАННЫХ <<<<< #
#==========================================================================================#
	
class Position:

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def arguments(self) -> list[Argument]:
		"""Список аргументов."""

		return self.__Arguments

	@property
	def description(self) -> str | None:
		"""Описание позиции."""

		return self.__Description
	
	@property
	def flags(self) -> list[Flag]:
		"""Список флагов."""

		return self.__Flags
	
	@property
	def is_base(self) -> bool:
		"""Состояние: является ли позиция базовой для команды."""

		return self.__IsBase

	@property
	def is_important(self) -> bool:
		"""Состояние: является ли позиция обязательной."""

		return self.__IsImportant

	@property
	def keys(self) -> list[Key]:
		"""Список ключей."""

		return self.__Keys

	@property
	def max_parameters_count(self) -> int:
		"""Максимальное количество параметров на позиции."""

		if self.__IsBase:
			Count = len(self.__Flags)
			Count += len(self.__Arguments)
			Count += len(self.__Keys) * 2
			return Count

		if self.keys: return 2
		elif self.__Arguments or self.__Flags: return 1
		else: return 0

	@property
	def min_parameters_count(self) -> int:
		"""Минимальное количество параметров на позиции."""

		if self.__IsBase:
			Count = 0
			for Flag in self.__Flags:
				if Flag.is_important: Count += 1

			for Key in self.__Keys:
				if Key.is_important: Count += 2

			for Argument in self.__Arguments:
				if Argument.is_important: Count += 1
				break

			return Count

		if self.__IsImportant:
			
			if self.keys and not self.__Arguments and not self.__Flags: return 2
			elif self.__Arguments or self.__Flags: return 1
			else: return 0

		else: return 0

	@property
	def name(self) -> str | None:
		"""Название позиции."""

		return self.__Name

	#==========================================================================================#
	# >>>>> МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, name: str | None = None, description: str | None = None, important: bool = False, is_base: bool = False):
		"""
		Позиции команды.

		:param name: Название позиции. По умолчанию `None`.
		:type name: str | None
		:param description: Описание позиции. По умолчанию `None`.
		:type description: str | None
		:param important: Указывает, является ли позиция обязательной. По умолчанию `False`.
		:type important: bool
		:param is_base: Указывает, является ли позиция базовой для команды. По умолчанию `False`.
		:type is_base: bool
		"""

		#---> Генерация динамических атрибутов.
		#==========================================================================================#
		self.__IsImportant = important
		self.__Name = name
		self.__Description = description
		self.__IsBase = is_base
		
		self.__Arguments: list[Argument] = list()
		self.__Flags: list[Flag] = list()
		self.__Keys: list[Key] = list()
		
	def add_argument(self, type: ParametersTypes = ParametersTypes.All, description: str | None = None, important: bool = False):
		"""
		Добавляет аргумент на позицию.

		:param type: Тип аргумента. По умолчанию `ParametersTypes.All`.
		:type type: ParametersTypes
		:param description: Описание аргумента. По умолчанию `None`.
		:type description: str | None
		:param important: Описание аргумента. По умолчанию `None`.
		:type important: bool
		"""

		if important: self.__IsImportant = True
		self.__Arguments.append(Argument(type, description, important))

	def add_flag(self, name: str, description: str | None = None, important: bool = False):
		"""
		Добавляет флаг на позицию.

		:param name: Название флага.
		:type name: str
		:param description: Описание флага. По умолчанию `None`.
		:type description: str | None
		:param important: Указывает, является ли флаг обязательным. По умолчанию `False`.
		:type important: bool
		"""

		if important: self.__IsImportant = True
		self.__Flags.append(Flag(name, description, important))

	def add_key(self, name: str, type: ParametersTypes = ParametersTypes.All, description: str | None = None, important: bool = False):
		"""
		Добавляет ключ на позицию.

		:param name: Название ключа.
		:type name: str
		:param type: Тип значения ключа. По умолчанию `ParametersTypes.All`.
		:type type: ParametersTypes
		:param description: Описание ключа. По умолчанию `None`.
		:type description: str | None
		:param important: Указывает, является ли ключ обязательным. По умолчанию `False`.
		:type important: bool
		"""

		if important: self.__IsImportant = True
		self.__Keys.append(Key(name, type, description, important))

class Command:
	"""Описание команды."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def arguments(self) -> list[Argument]:
		"""Список аргументов на базовой позиции."""

		return self.__BasePosition.arguments

	@property
	def base(self) -> Position:
		"""Базовая позиция команды."""

		return self.__BasePosition

	@property
	def category(self) -> str | None:
		"""Название категории, к которой относится команда."""

		return self.__Category

	@property
	def check_parameters_count(self) -> bool:
		"""Состояние: нужно ли проверять количество переданных параметров."""

		return self.__ChackParametersCount

	@property
	def description(self) -> str:
		"""Описание команды."""

		return self.__BasePosition.description

	@property
	def flags(self) -> list[Flag]:
		"""Список флагов на базовой позиции."""

		return self.__BasePosition.flags

	@property
	def keys(self) -> list[Key]:
		"""Список ключей на базовой позиции."""

		return self.__BasePosition.keys

	@property
	def max_parameters_count(self) -> int:
		"""Максимальное количество параметров."""

		if self.__MaxParametersCount != None: return self.__MaxParametersCount

		return reduce(lambda x, y: x + y, [Position.max_parameters_count for Position in self.positions])

	@property
	def min_parameters_count(self) -> int:
		"""Минимальное количество параметров."""

		if self.__MinParametersCount != None: return self.__MinParametersCount

		return reduce(lambda x, y: x + y, [Position.min_parameters_count for Position in self.positions])

	@property
	def name(self) -> str:
		"""Название команды."""

		return self.__BasePosition.name

	@property
	def positions(self) -> list[Position]:
		"""Список позиций."""

		return self.__Positions + [self.__BasePosition]

	#==========================================================================================#
	# >>>>> МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, name: str, description: str | None = None, category: str | None = None, check_parameters_count: bool = True):
		"""
		Структура описания команды.

		:param name: Название команды.
		:type name: str
		:param description: Описание команды. По умолчанию `None`.
		:type description: str | None
		:param category: Название категории, к которой относится команда. По умолчанию `None`.
		:type category: str | None
		:param check_parameters_count: Указывает, необходимо ли проверять количество параметров. По умолчанию `False`.
		:type check_parameters_count: bool
		"""

		#---> Генерация динамических атрибутов.
		#==========================================================================================#
		self.__ChackParametersCount = check_parameters_count
		self.__Category = category

		self.__BasePosition = Position(name = name, description = description, is_base = True)
		self.__Positions: list[Position] = list()

		self.__MinParametersCount = None
		self.__MaxParametersCount = None

	def create_position(self, name: str | None = None, description: str | None = None, important: bool = False) -> Position:
		"""
		Создаёт дополнительную позицию.

		:param name: Название позиции. По умолчанию `None`.
		:type name: str | None
		:param description: Описание позиции. По умолчанию `None`.
		:type description: str | None
		:param important: Указывает, является ли позиция обязательной. По умолчанию `False`.
		:type important: bool
		:return: Представление новой позиции.
		:rtype: Position
		"""

		NewPosition = Position(name, description, important)
		self.__Positions.append(NewPosition)

		return self.__Positions[-1]
	
	def set_category(self, category: str | None):
		"""
		Задаёт название категории, к которой относится команда.

		:param category: Название категории.
		:type category: str | None
		"""

		self.__Category = category

	def set_max_parameters_count(self, count: int | None):
		"""
		Задаёт максимальное количество параметров команды.

		:param count: Количество параметров или `None` для автоматического подсчёта.
		:type count: int | None
		"""

		self.__MaxParametersCount = count

	def set_min_parameters_count(self, count: int | None):
		"""
		Задаёт минимальное количество параметров команды.

		:param count: Количество параметров или `None` для автоматического подсчёта.
		:type count: int | None
		"""

		self.__MinParametersCount = count

class ParsedCommandData:
	"""Данные обработанной команды."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def arguments(self) -> tuple[str]:
		"""Список аргументов."""

		return self.__Arguments
	
	@property
	def flags(self) -> tuple[str]:
		"""Список активированных флагов."""

		return self.__Flags
	
	@property
	def keys(self) -> dict[str, Any]:
		"""Cловарь активированных ключей и их значений."""

		return self.__Keys.copy()
	
	@property
	def name(self) -> str:
		"""Название команды."""

		return self.__Name

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, name: str, flags: tuple[str], keys: dict[str, Any], arguments: tuple[str]):
		"""
		Данные команды.

		:param name: Название команды.
		:type name: str
		:param flags: Набор активированных флагов.
		:type flags: tuple[str]
		:param keys: Словарь активированных ключей и их значений.
		:type keys: dict[str, Any]
		:param arguments: Набор значений аргументов.
		:type arguments: tuple[str]
		"""

		#---> Генерация динамических атрибутов.
		#==========================================================================================#
		self.__Arguments = arguments
		self.__Flags = flags
		self.__Keys = keys
		self.__Name = name

	def __str__(self):
		return str({
			"name": self.__Name, 
			"flags": self.__Flags, 
			"keys": self.__Keys, 
			"arguments": self.__Arguments
		})

	def check_flag(self, flag: str) -> bool:
		"""
		Проверяет, активирован ли флаг.
		
		:param flag: Название флага.
		:type flag: str
		:return: Состояние проверки.
		:rtype: bool
		"""

		IsActivated = False
		if flag in self.__Flags: IsActivated = True

		return IsActivated
	
	def check_key(self, key: str) -> bool:
		"""
		Проверяет, активирован ли ключ.
		
		:param flag: Название ключа.
		:type flag: str
		:return: Состояние проверки.
		:rtype: bool
		"""

		IsActivated = False
		if key in self.__Keys.keys(): IsActivated = True

		return IsActivated
	
	def get_key_value(self, key: str, exception: bool = False) -> Any:
		"""
		Возвращает значение активированного ключа.

		:param key: Название ключа.
		:type key: str
		:param exception: Указывает, нужно ли выбросить исключение при отсутствии ключа.
		:type exception: bool
		:raises KeyError: Выбрасывается в случае активации соответствующего параметра и запросе значения отсутствующего ключа.
		:return: Значение ключа.
		:rtype: Any
		"""

		Value = None
		if key in self.__Keys.keys(): Value = self.__Keys[key]
		elif exception: raise KeyError(key)

		return Value

#==========================================================================================#
# >>>>> МОДУЛЬ ПОМОЩИ <<<<< #
#==========================================================================================#

@dataclass
class HelpLabels:
	"""
	Контейнер используемых в модуле помощи строк.

	Для `COMMAND_NOT_FOUND` можно определить место подстановки команды через `%c`.
	"""

	COMMAND_DESCRIPTION: str = "Print list of supported commands. For details, add name of command as argument."
	ARGUMENT_DESCRIPTION: str = "The name of command for which you want to see detailed help."
	IMPORTANT_NOTE: str = "Important parameters marked with * symbol."
	COMMAND_NOT_FOUND: str = "Command \"%c\" not found."
	CATEGORY_OTHER: str = "Other"

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
	def is_enabled(self) -> bool:
		"""Состояние: активирован ли модуль помощи."""

		return self.__IsEnabled
	
	@property
	def is_sorting_enabled(self) -> bool:
		"""Состояние: выполняется ли сортировка команд по алфавиту."""

		return self.__IsSortingEnabled

	@property
	def labels(self) -> HelpLabels:
		"""Оператор работы с используемыми в модуле помощи строками."""

		return self.__Labels

	#==========================================================================================#
	# >>>>> ПРИВАТНЫЕ МЕТОДЫ ГЕНЕРАЦИИ ПОМОЩИ <<<<< #
	#==========================================================================================#

	def __BuildArgumentDescription(self, argument: Argument, indent: str | None = None) -> str:
		"""
		Строит описание для аргумента.
			argument – аргумент;\n
			indent – отступ, добавляемый к каждой строке.
		"""

		MSG_Indent = indent or "  "
		MSG_Type = f" <{argument.type.value}>"
		MSG_Description = f": {argument.description}" if argument.description else ""
		Description = f"\n{MSG_Indent}    • [argument{MSG_Type}]{MSG_Description}"

		return Description
	
	def __BuildFlagDescription(self, flag: Flag, indent: str | None = None) -> str:
		"""
		Строит описание для флага.
			flag – флаг;\n
			indent – отступ, добавляемый к каждой строке.
		"""

		MSG_Indent = indent or "  "
		MSG_Name = FastStyler(self.__Terminalyzer.flags_indicator + flag.name).decorate.bold
		MSG_Description = f": {flag.description}" if flag.description else ""
		Description = f"\n{MSG_Indent}    • [flag] {MSG_Name}{MSG_Description}"

		return Description
	
	def __BuildKeyDescription(self, key: Key, indent: str | None = None) -> str:
		"""
		Строит описание для ключа.
			key – ключ;\n
			indent – отступ, добавляемый к каждой строке.
		"""

		MSG_Indent = indent or "  "
		MSG_Name = FastStyler(self.__Terminalyzer.keys_indicator + key.name).decorate.bold
		MSG_Type = f" <{key.type.value}>"
		MSG_Description = f": {key.description}" if key.description else ""
		Description = f"\n{MSG_Indent}    • [key{MSG_Type}] {MSG_Name}{MSG_Description}"

		return Description

	def __BuildPositionDescription(self, position: Command | Position) -> str:
		"""
		Строит описание позиции или свободных параметров команды.
			position – позиция или описание команды.
		"""

		if not any((position.flags, position.keys, position.arguments)): return str()

		Help = ""
		Indent = "  "
		PositionName = f"{Indent}{position.name}" if position.name else f"{Indent}POS"
		Description = f": {position.description}" if position.description else ""

		if position.is_base:
			PositionName = f"{Indent}Other parameters:"
			Description = ""

		Help += FastStyler(f"\n{PositionName}").decorate.bold + Description
		
		for CurrentArgument in position.arguments: Help += self.__BuildArgumentDescription(CurrentArgument, Indent)
		for CurrentFlag in position.flags: Help += self.__BuildFlagDescription(CurrentFlag, Indent)
		for CurrentKey in position.keys: Help += self.__BuildKeyDescription(CurrentKey, Indent)

		return Help

	def __GenerateCommandMap(self, command: Command) -> str:
		"""
		Генерирует позиционную карту команды.
			command – описание команды.
		"""

		CommandMap = str()

		for Position in command.positions:
			if Position.is_base: continue
			Name = Position.name or "POSITION"
			IsImportant = "*" if Position.is_important else ""
			CommandMap += f" [{Name}{IsImportant}]"

		return CommandMap

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, terminalyzer: "Terminalyzer"):
		"""
		Модуль помощи.

		:param terminalyzer: Обработчик консольных параметров.
		:type terminalyzer: Terminalyzer
		"""

		self.__Terminalyzer = terminalyzer

		self.__Labels = HelpLabels()
		self.__Callback = print
		self.__Category = None

		self.__IsEnabled = False
		self.__IsSortingEnabled = False

	def generate_help_command(self, commands: list[Command], command_name: str):
		"""
		Отправляет подробное описание команды в callback-функцию.

		:param commands: Описательные структуры комманд.
		:type commands: list[Command]
		:param command_name: Название команды, для которой требуется получить помощь.
		:type command_name: str
		"""

		CommandForHelp = None

		for CurrentCommand in commands:
			if CurrentCommand.name == command_name: CommandForHelp = CurrentCommand

		if CommandForHelp:
			Help = FastStyler(CommandForHelp.name).decorate.bold
			Help += self.__GenerateCommandMap(CommandForHelp)
			if CommandForHelp.description: Help += "\n" + FastStyler(CommandForHelp.description).decorate.italic
			for Position in CommandForHelp.positions: Help += self.__BuildPositionDescription(Position)
			# Проверка на наличие обязательной позиции и соответствующего пояснения.
			if "*" in Help.split("\n")[0] and self.__Labels.IMPORTANT_NOTE: Help += "\n" + self.__Labels.IMPORTANT_NOTE or ""
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
			TableString += TableObject.get_string(header = False).strip()
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

#==========================================================================================#
# >>>>> ОСНОВНОЙ КЛАСС <<<<< #
#==========================================================================================#

class Terminalyzer:
	"""Обработчик консольных параметров."""

	@property
	def flags_indicator(self) -> str:
		"""Индикатор флагов."""

		return self.__FlagsIndicator

	@property
	def helper(self) -> Helper:
		"""Настройки модуля помощи."""

		return self.__Helper

	@property
	def keys_indicator(self) -> str:
		"""Индикатор ключей."""

		return self.__KeysIndicator

	#==========================================================================================#
	# >>>>> ПРИВАТНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __CheckCommand(self, command: Command) -> ParsedCommandData | None:
		"""
		Выполняет проверку соответствия параметров конкретной команде.
			command – описание команды.
		"""
		
		if self.__ConfirmCommandName(command):
			Flags = list()
			Keys = dict()
			Arguments = list()

			self.__Command = command
			self.__ParametersLocks = [False] * len(self.__Parameters)
			self.__ParametersLocks[0] = True
			for Position in command.positions: self.__PositionsLocks[Position.name] = False

			Flags, Keys, Arguments = self.__ParseParameters()

			if not self.__FreeMode: self.__CheckUnlockedParameters()
			self.__CheckParametersCount()

			self.__CommandData = ParsedCommandData(command.name, Flags, Keys, Arguments)

	def __CheckParametersCount(self):
		"""Проверяет соответвтсие количества параметров."""
		
		if not self.__Command.check_parameters_count: return
		if len(self.__Parameters) - 1 > self.__Command.max_parameters_count: raise TooManyParameters(" ".join(self.__Parameters))
		if len(self.__Parameters) - 1 < self.__Command.min_parameters_count: raise NotEnoughParameters(" ".join(self.__Parameters))

	def __CheckUnlockedParameters(self):
		"""Проверяет незаблокированные параметры."""

		IndicatorsOrder = [self.flags_indicator, self.keys_indicator]
		ExceptionsOrder = [UnknownFlag, UnknownKey]

		if len(self.keys_indicator) > len(self.flags_indicator):
			IndicatorsOrder.reverse()
			ExceptionsOrder.reverse()

		for Index in range(1, len(self.__Parameters)):

			if not self.__ParametersLocks[Index]:

				for Indicator, ExceptionType in zip(IndicatorsOrder, ExceptionsOrder):
					if self.__Parameters[Index].startswith(Indicator): raise ExceptionType(self.__Parameters[Index])

	def __ConfirmCommandName(self, command: Command) -> bool:
		"""
		Проверяет, соответствует ли название команды из описания текущему.
			command – описание команды.
		"""
		
		IsDetermined = False
		if command.name == self.__CommandName: IsDetermined = True
		
		return IsDetermined

	def __ConfirmParameterType(self, value: str, verifiable_type: ParametersTypes = ParametersTypes.All, exception: bool = True) -> bool | float | int | str | datetime:
		"""
		Проверяет, соответствует ли строка ожидаемому типу данных и преобразует её в этот самый тип.

		:param value: Проверяемая строка.
		:type value: str
		:param verifiable_type: Проверяемый тип.
		:type verifiable_type: ParametersTypes
		:param exception: Указывает, следует ли выбрасывать исключение при ошибке верификации типа параметра.
		:type exception: bool
		:raises InvalidParameterType: Выбрасывается при ошибке верификации типа параметра.
		:return: Преобразованные в целевой тип данные.
		:rtype: bool | float | int | str | datetime
		"""
		
		Value = None

		match verifiable_type:

			case ParametersTypes.All:
				Value = value

			case ParametersTypes.Alpha:
				if value.isalpha(): Value = value

			case ParametersTypes.Bool:
				Buffer = value.lower()
				if Buffer == "true": Value = True
				elif Buffer == "false": Value = False

			case ParametersTypes.Date:
				try: Value = dateparser.parse(value).date()
				except: pass

			case ParametersTypes.Float:
				if value.count("-") <= 1 and value.strip(".").count(".") == 1 and value.replace(".", "").isdigit(): Value = float(value)

			case ParametersTypes.Integer:
				if value.count("-") <= 1 and value.lstrip("-").isdigit(): Value = int(value)

			case ParametersTypes.Number:

				if "." in value:
					try: Value = float(value)
					except ValueError: pass

				else:
					try: Value = int(value)
					except ValueError: pass

			case ParametersTypes.ValidPath:
				if os.path.exists(value): Value = value

			case _:
				if self.__ValidableTypes[verifiable_type](value): Value = value

		if Value == None and exception: raise InvalidParameterType(value, verifiable_type.value)

		return Value

	#==========================================================================================#
	# >>>>> МЕТОДЫ ПАРСИНГА ПАРАМЕТРОВ <<<<< #
	#==========================================================================================#

	def __CheckFlag(self, parameter: str, index: int) -> str | None:
		"""
		Проверяет, является ли параметр флагом. При успехе возвращает имя флага.
			parameter – проверяемый параметр;\n
			index – индекс параметра.
		"""

		HasFlagIndicator = parameter.startswith(self.__FlagsIndicator)
		ParameterName = parameter

		if HasFlagIndicator and not self.__FreeMode: ParameterName = ParameterName[len(self.__FlagsIndicator):]
		elif not HasFlagIndicator and not self.__FreeMode: return

		for Position in self.__Command.positions:
			if self.__PositionsLocks[Position.name]: continue

			if ParameterName in [Flag.name for Flag in Position.flags]:
				if not Position.is_base: self.__PositionsLocks[Position.name] = parameter
				self.__ParametersLocks[index] = True
				return ParameterName
			
		return None

	def __CheckKey(self, parameter: str, index: int) -> tuple[str | None, Any]:
		"""
		Проверяет, является ли параметр ключом. При успехе возвращает имя ключа.
			parameter – проверяемый параметр;\n
			index – индекс параметра.
		"""

		HasKeyIndicator = parameter.startswith(self.__KeysIndicator)
		ParameterName = parameter

		if HasKeyIndicator and not self.__FreeMode: ParameterName = ParameterName[len(self.__KeysIndicator):]
		elif not HasKeyIndicator and not self.__FreeMode: return None, None

		for Position in self.__Command.positions:
			if self.__PositionsLocks[Position.name]: continue

			for Key in Position.keys:

				if ParameterName == Key.name:
					if not Position.is_base: self.__PositionsLocks[Position.name] = ParameterName
					self.__ParametersLocks[index] = True

					try:
						if not self.__ParametersLocks[index + 1]: self.__ParametersLocks[index + 1] = True

					except IndexError:
						if not self.__FreeMode: raise UnboundKey(parameter)

					Value = self.__ConfirmParameterType(self.__Parameters[index + 1], Key.type) 

					return ParameterName, Value
				
		return None, None

	def __CheckArgument(self, parameter: str, index: int) -> Any:
		"""
		Проверяет, является ли параметр аргументом. При успехе возвращает значение аргумента.
			parameter – проверяемый параметр;\n
			index – индекс параметра.
		"""

		#---> Проверка переполнения заблокированных позиций.
		#==========================================================================================#
		for Position in self.__Command.positions:
			if not self.__PositionsLocks[Position.name]: continue
			ParameterName = parameter

			HasFlagIndicator = parameter.startswith(self.__FlagsIndicator)
			HasKeyIndicator = parameter.startswith(self.__KeysIndicator)

			if HasFlagIndicator and not self.__FreeMode: ParameterName = ParameterName[len(self.__FlagsIndicator):]
			if HasKeyIndicator and not self.__FreeMode: ParameterName = ParameterName[len(self.__KeysIndicator):]

			if ParameterName in [Flag.name for Flag in Position.flags]: raise MutuallyExclusiveParameters(Position.name, self.__PositionsLocks[Position.name], parameter)
			if ParameterName in [Key.name for Key in Position.keys]: raise MutuallyExclusiveParameters(Position.name, self.__PositionsLocks[Position.name], parameter)

		#---> Определение принадлежности аргумента.
		#==========================================================================================#
		for Position in self.__Command.positions:
			if self.__PositionsLocks[Position.name]: continue

			for CurrentArgument in Position.arguments:

				try: parameter = self.__ConfirmParameterType(parameter, CurrentArgument.type)
				except InvalidParameterType: pass
				else:
					if not Position.is_base: self.__PositionsLocks[Position.name] = True
					self.__ParametersLocks[index] = True
					return parameter

		return parameter

	def __ParseParameters(self):
		"""Выполняет проверку соответствия параметров конкретной команде."""

		Flags = list()
		Keys = dict()
		Arguments = list()

		for Index in range(1, len(self.__Parameters)):
			if self.__ParametersLocks[Index]: continue
			Parameter = self.__Parameters[Index]

			#---> Проверка флагов.
			#==========================================================================================#
			ParameterCache = self.__CheckFlag(Parameter, Index)

			if ParameterCache:
				
				Flags.append(ParameterCache)
				continue

			#---> Проверка ключей.
			#==========================================================================================#
			ParameterCache, Value = self.__CheckKey(Parameter, Index)

			if ParameterCache:
				self.__ParametersLocks[Index] = True
				Keys[ParameterCache] = Value
				continue

			#---> Проверка аргументов.
			#==========================================================================================#
			Arguments.append(self.__CheckArgument(Parameter, Index))

		return Flags, Keys, Arguments

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, parameters: Iterable[str] | None = None, free_mode: bool = False):
		"""
		Обработчик консольных параметров.

		:param parameters: Набор параметров. По умолчанию берётся из аргументов запуска скрипта.
		:type parameters: Iterable[str] | None
		:param free_mode: Включает свободный режим анализатора, в котором не используются индикаторы ключей и флагов.
		:type free_mode: bool
		"""

		self.__Parameters = parameters or sys.argv[1:]
		self.__FreeMode = free_mode

		self.__KeysIndicator = "--"
		self.__FlagsIndicator = "-"
		self.__CommandData = None
		self.__CommandName = None
		self.__Command: Command = None
		self.__ParametersLocks = None
		self.__PositionsLocks = dict()

		self.__Helper = Helper(self)

		self.__ValidableTypes = {
			ParametersTypes.Base64: validators.base64,
			ParametersTypes.Base64: validators.email,
			ParametersTypes.Base64: validators.ipv4,
			ParametersTypes.Base64: validators.ipv6,
			ParametersTypes.Base64: validators.url
		}

		self.set_source(self.__Parameters)

	def check_commands(self, commands: list[Command] | Command) -> ParsedCommandData | None:
		"""
		Проверяет каждое из переданных описаний команд на соответствие текущей. 

		:param commands: Описательные структуры команд или их JSON-конфигурация.
		:type commands: list[Command] | Command
		:return: При успешной проверке парсит данные команды и возвращает их.
		:rtype: ParsedCommandData | None
		"""

		self.__CommandData: ParsedCommandData = None
		self.__Command = None

		if type(commands) == Command: commands = [commands]

		if self.__Helper.is_enabled:
			Help = Command("help", self.__Helper.labels.COMMAND_DESCRIPTION, self.__Helper.category)
			Help.base.add_argument(description =  self.__Helper.labels.ARGUMENT_DESCRIPTION)
			commands.append(Help)

		for CurrentCommand in commands: self.__CheckCommand(CurrentCommand)

		if self.__Helper.is_enabled and self.__CommandData and self.__CommandData.name == "help":
			if self.__CommandData.arguments: self.__Helper.generate_help_command(commands, self.__CommandData.arguments[0])
			else: self.__Helper.generate_help_list(commands)
		
		return self.__CommandData

	def set_source(self, parameters: list[str]):
		"""
		Задаёт список параметров, из которых будут парситься данные команды.

		:param parameters: Cписок параметров. По умолчанию берётся из *sys.argv* скрипта.
		:type parameters: list[str]
		"""

		self.__Parameters = parameters
		self.__CommandName = self.__Parameters[0] if self.__Parameters else None

	def set_flags_indicator(self, indicator: str):
		"""
		Задаёт текстовый индикатор флагов.

		:param indicator: Индикатор флагов.
		:type indicator: str
		:raises IdenticalIndicators: Выбрасывается в случае установки идентичных идентификаторов флага и ключа.
		"""

		if indicator != self.__KeysIndicator:
			self.__FlagsIndicator = indicator

		else: raise IdenticalIndicators()

	def set_keys_indicator(self, indicator: str):
		"""
		Задаёт текстовый индикатор ключей.

		:param indicator: Индикатор ключей.
		:type indicator: str
		:raises IdenticalIndicators: Выбрасывается в случае установки идентичных идентификаторов флага и ключа.
		"""

		if indicator != self.__FlagsIndicator:
			self.__KeysIndicator = indicator

		else: raise IdenticalIndicators()