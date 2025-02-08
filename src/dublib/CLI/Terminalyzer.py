from .TextStyler import TextStyler
from ..Exceptions.CLI import *

from prettytable import PLAIN_COLUMNS, PrettyTable
from urllib.parse import urlparse
from typing import Any, Callable
from datetime import datetime
from functools import reduce

import dateparser
import enum
import sys
import os

#==========================================================================================#
# >>>>> ПЕРЕЧИСЛЕНИЯ ТИПОВ <<<<< #
#==========================================================================================#

class ParametersTypes(enum.Enum):
	"""Перечисление типов значений параметров."""

	All = "All"
	Bool = "Bool"
	Date = "Date"
	Number = "Number"
	ValidPath = "ValidPath"
	Text = "Text"
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
			type – тип значения аргумента;\n
			description – описание аргумента;\n
			important – указывает, является ли аргумент обязательным.
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
			name – название флага;\n
			description – описание флага;\n
			important – указывает, является ли флаг обязательным.
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
			name – название ключа;\n
			type – тип значения ключа;\n
			description – описание ключа;\n
			important – указывает, является ли ключ обязательным.
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
		Объектное представление позиции команды.
			important – указывает, является ли позиция обязательной;\n
			name – название позиции;\n
			description – описание позиции.
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
			type – тип значения аргумента;\n
			description – описание позиции;\n
			important – указывает, является ли позиция обязательной.
		"""

		if important: self.__IsImportant = True
		self.__Arguments.append(Argument(type, description, important))

	def add_flag(self, name: str, description: str | None = None, important: bool = False):
		"""
		Добавляет флаг на позицию.
			name – название флага;\n
			description – описание флага;\n
			important – указывает, является ли флаг обязательным.
		"""

		if important: self.__IsImportant = True
		self.__Flags.append(Flag(name, description, important))

	def add_key(self, name: str, type: ParametersTypes = ParametersTypes.All, description: str | None = None, important: bool = False):
		"""
		Добавляет ключ на позицию.
			name – название ключа;\n
			type – тип значения ключа;\n
			description – описание ключа;\n
			important – указывает, является ли ключ обязательным.
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
	def has_important_argument(self) -> bool:
		"""Состояние: имеет ли команда обязательный важный аргумент."""

		return self.__HasImportantArgument

	@property
	def has_important_flag(self) -> bool:
		"""Состояние: имеет ли команда обязательный важный флаг."""

		return self.__HasImportantFlag

	@property
	def has_important_key(self) -> bool:
		"""Состояние: имеет ли команда обязательный важный ключ."""

		return self.__HasImportantKey

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

	def __init__(self, name: str, description: str | None = None, check_parameters_count: bool = True):
		"""
		Структура описания команды.
			name – название команды;\n
			description – описание команды;\n
			check_parameters_count – указывает, нужно ли проверять количество переданных параметров.
		"""

		#---> Генерация динамических атрибутов.
		#==========================================================================================#
		self.__ChackParametersCount = check_parameters_count

		self.__BasePosition = Position(name = name, description = description, is_base = True)
		self.__Positions: list[Position] = list()

		self.__HasImportantArgument = False
		self.__HasImportantFlag = False
		self.__HasImportantKey = False

		self.__MinParametersCount = None
		self.__MaxParametersCount = None

	def add_argument(self, type: ParametersTypes = ParametersTypes.All, description: str | None = None, important: bool = False):
		"""
		Добавляет аргумент команды.
			type – тип значения аргумента;\n
			description – описание позиции;\n
			important – указывает, является ли позиция обязательной.
		"""

		if important: self.__HasImportantArgument = True
		self.__BasePosition.add_argument(type, description, important)

	def add_flag(self, name: str, description: str | None = None, important: bool = False):
		"""
		Добавляет флаг команды.
			name – название флага;\n
			description – описание флага;\n
			important – указывает, является ли флаг обязательным.
		"""

		if important: self.__HasImportantFlag = True
		self.__BasePosition.add_flag(name, description, important)

	def add_key(self, name: str, type: ParametersTypes = ParametersTypes.All, description: str | None = None, important: bool = False):
		"""
		Добавляет ключ команды.
			name – название ключа;\n
			type – тип значения ключа;\n
			description – описание ключа;\n
			important – указывает, является ли ключ обязательным.
		"""

		if important: self.__HasImportantKey = True
		self.__BasePosition.add_key(name, type, description, important)

	def create_position(self, name: str | None = None, description: str | None = None, important: bool = False) -> Position:
		"""
		Создаёт позицию.
			name – название позиции;\n
			description – описание позиции;\n
			important – указывает, является ли позиция обязательной.
		"""

		NewPosition = Position(name, description, important)
		self.__Positions.append(NewPosition)

		return self.__Positions[-1]
	
	def set_max_parameters_count(self, count: int | None):
		"""
		Задаёт максимальное количество параметров команды.
			count – количество параметров или None для автоматического подсчёта.
		"""

		self.__MaxParametersCount = count

	def set_min_parameters_count(self, count: int | None):
		"""
		Задаёт минимальное количество параметров команды.
			count – количество параметров или None для автоматического подсчёта.
		"""

		self.__MinParametersCount = count

class HelpTranslation:
	"""Модуль поддержки локализаций помощью."""

	#==========================================================================================#
	# >>>>> ВСПОМОГАТЕЛЬНЫЕ ТИПЫ ДАННЫХ <<<<< #
	#==========================================================================================#

	def __init__(self):
		"""Настройки модуля помощи."""

		#---> Генерация динамических атрибутов.
		#==========================================================================================#
		self.command_description = "Print list of supported commands. For details, add name of command as argument."
		self.argument_description = "The name of command for which you want to see detailed help."
		self.important_note = "Important parameters marked with * symbol."
		self.no_command = "Command \"%c\" not found."

class ParsedCommandData:
	"""Данные обработанной команды."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def arguments(self) -> list[str]:
		"""Список аргументов."""

		return self.__Arguments
	
	@property
	def flags(self) -> list[str]:
		"""Список активированных флагов."""

		return self.__Flags
	
	@property
	def keys(self) -> dict[str, any]:
		"""Cловарь активированных ключей и их значений."""

		return self.__Keys.copy()
	
	@property
	def name(self) -> str:
		"""Название команды."""

		return self.__Name

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, name: str, flags: list[str], keys: dict[str, any], arguments: list[str]):
		"""
		Данные обработанной команды.
			name – название команды;\n
			flags – список активированных флагов;\n
			keys – словарь активированных ключей и их значений;\n
			arguments – список аргументов.
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
			flag – название флага.
		"""

		IsActivated = False
		if flag in self.__Flags: IsActivated = True

		return IsActivated
	
	def check_key(self, key: str) -> bool:
		"""
		Проверяет, активирован ли ключ.
			key – название ключа.
		"""

		IsActivated = False
		if key in self.__Keys.keys(): IsActivated = True

		return IsActivated
	
	def get_key_value(self, key: str, exception: bool = False) -> Any:
		"""
		Возвращает значение активированного ключа.
			key – название ключа;\n
			exception – указывает, нужно ли выбросить исключение при отсутствии ключа.
		"""

		Value = None
		if key in self.__Keys.keys(): Value = self.__Keys[key]
		elif exception: raise KeyError(key)

		return Value

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
	def help_translation(self) -> HelpTranslation:
		"""Настройки локализации помощи."""

		return self.__HelpTranslationObject

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

	def __ConfirmParameterType(self, value: str, type_name: ParametersTypes = ParametersTypes.All, raise_exception: bool = True) -> bool | int | str | datetime:
		"""
		Проверяет и парсит значение параметра согласно его типу.
			value – значение параметра;\n
			type_name – тип параметра;\n
			raise_exception – указывает, нужно ли выбрасывать исключение при ошибке проверки типа.
		"""
		
		Value = None

		if type_name != ParametersTypes.All:

			if type_name == ParametersTypes.Bool:
				Buffer = value.lower()
				if Buffer == "true": Value = True
				elif Buffer == "false": Value = False

			elif type_name == ParametersTypes.Date:
				try: Value = dateparser.parse(value).date()
				except: pass
			
			elif type_name == ParametersTypes.Number:
				if value.lstrip("-").isdigit(): Value = int(value)
				
			elif type_name == ParametersTypes.ValidPath:
				if os.path.exists(value): Value = value

			elif type_name == ParametersTypes.Text:
				if value.isalpha(): Value = value

			elif type_name == ParametersTypes.URL:
				if bool(urlparse(value).scheme): Value = value 

		else: Value = value

		if Value == None and raise_exception: raise InvalidParameterType(value, type_name.value)

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
	# >>>>> МЕТОДЫ ГЕНЕРАЦИИ ПОМОЩИ <<<<< #
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
		MSG_Name = TextStyler(self.__FlagsIndicator + flag.name).decorate.bold
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
		MSG_Name = TextStyler(self.__KeysIndicator + key.name).decorate.bold
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

		Help += TextStyler(f"\n{PositionName}").decorate.bold + Description
		
		for CurrentArgument in position.arguments: Help += self.__BuildArgumentDescription(CurrentArgument, Indent)
		for CurrentFlag in position.flags: Help += self.__BuildFlagDescription(CurrentFlag, Indent)
		for CurrentKey in position.keys: Help += self.__BuildKeyDescription(CurrentKey, Indent)

		return Help

	def __CreateCommandHelp(self, commands: list[Command], command_name: str):
		"""
		Отправляет подробное описание команды в callback-фнкцию.
			commands – описательные структуры комманд;\n
			command_name – название команды, для которой требуется получить помощь.
		"""

		CommandForHelp = None

		for CurrentCommand in commands:
			if CurrentCommand.name == command_name: CommandForHelp = CurrentCommand

		if CommandForHelp:
			Help = TextStyler(CommandForHelp.name).decorate.bold
			Help += self.__GenerateCommandMap(CommandForHelp)
			if CommandForHelp.description: Help += "\n" + TextStyler(CommandForHelp.description).decorate.italic
			for Position in CommandForHelp.positions: Help += self.__BuildPositionDescription(Position)
			if any((CommandForHelp.has_important_flag, CommandForHelp.has_important_key, CommandForHelp.has_important_argument)) and self.__HelpTranslationObject.important_note: Help += "\n" + self.__HelpTranslationObject.important_note or ""
			self.__HelpCallback(Help)

		else: self.__HelpCallback(self.__HelpTranslationObject.no_command.replace(r"%c", command_name))

	def __CreateHelpList(self, commands: list[Command]):
		"""
		Отправляет список команд с их описанием в callback-фнкцию.
			commands – описательные структуры комманд.
		"""

		#---> Получение данных.
		#==========================================================================================#
		HelpTable = {
			"Command": [],
			"Description": []
		}

		for CurrentCommand in commands:
			HelpTable["Command"].append(CurrentCommand.name)
			HelpTable["Description"].append(CurrentCommand.description or "")

		#---> Генерация таблицы.
		#==========================================================================================#
		TableObject = PrettyTable()
		TableObject.set_style(PLAIN_COLUMNS)

		for ColumnName in HelpTable.keys():
			Buffer = TextStyler(ColumnName).decorate.bold
			TableObject.add_column(Buffer, HelpTable[ColumnName])

		TableObject.align = "l"
		self.__HelpCallback(TableObject.get_string())

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

	def __init__(self, parameters: list[str] | None = None, free_mode: bool = False):
		"""
		Обработчик консольных параметров.
			parameters – список параметров (по умолчанию берётся из аргументов запуска скрипта);\n
			free_mode – включает свободный режим анализатора, в котором не используются индикаторы ключей и флагов.
		"""

		#---> Генерация динамических атрибутов.
		#==========================================================================================#
		self.__Parameters = parameters or sys.argv[1:]
		self.__FreeMode = free_mode

		self.__KeysIndicator = "--"
		self.__FlagsIndicator = "-"
		self.__CommandData = None
		self.__CommandName = None
		self.__Command: Command = None
		self.__ParametersLocks = None
		self.__PositionsLocks = dict()

		self.__EnableHelp = False
		self.__HelpCallback = print

		self.__HelpTranslationObject = HelpTranslation()

		self.set_source(self.__Parameters)

	def enable_help(self, status: bool = True):
		"""
		Переключает использование модуля помощи.
			status – состояние использования модуля помощи.
		"""

		self.__EnableHelp = status

	def check_commands(self, commands: list[Command] | Command) -> ParsedCommandData | None:
		"""
		Выполняет проверку соответствия списку команд.
			commands – описательные структуры комманд или их JSON-конфигурация.
		"""

		self.__CommandData = None
		self.__Command = None

		if type(commands) == Command: commands = [commands]

		if self.__EnableHelp:
			Help = Command("help", self.__HelpTranslationObject.command_description)
			Help.add_argument(description = self.__HelpTranslationObject.argument_description)
			commands.append(Help)

		for CurrentCommand in commands: self.__CheckCommand(CurrentCommand)

		if self.__EnableHelp and self.__CommandData and self.__CommandData.name == "help":
			if self.__CommandData.arguments: self.__CreateCommandHelp(commands, self.__CommandData.arguments[0])
			else: self.__CreateHelpList(commands)
		
		return self.__CommandData

	def set_source(self, parameters: list[str]):
		"""
		Задаёт список параметров.
			parameters – список параметров (по умолчанию берётся из параметров скрипта).
		"""

		self.__Parameters = parameters
		self.__CommandName = self.__Parameters[0] if self.__Parameters else None

	def set_flags_indicator(self, indicator: str):
		"""
		Задаёт индикатор флагов.
			indicator – индикатор флагов.
		"""

		if indicator != self.__KeysIndicator:
			self.__FlagsIndicator = indicator

		else:
			raise IdenticalIndicators()

	def set_help_callback(self, callback: Callable):
		"""
		Задаёт функцию, в которую будет передан вывод помощи.
			callback – функция, принимающая строку в качестве аргумента.
		"""

		self.__HelpCallback = callback

	def set_keys_indicator(self, indicator: str):
		"""
		Задаёт индикатор ключей.
			indicator – индикатор ключей.
		"""

		if indicator != self.__FlagsIndicator:
			self.__KeysIndicator = indicator

		else:
			raise IdenticalIndicators()