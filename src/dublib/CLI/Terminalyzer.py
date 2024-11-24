from ..Methods.Data import MergeDictionaries
from .TextStyler import TextStyler
from ..Exceptions.CLI import *

from prettytable import PLAIN_COLUMNS, PrettyTable
from urllib.parse import urlparse

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
	def is_important(self) -> bool:
		"""Состояние: является ли позиция обязательной."""

		return self.__IsImportant

	@property
	def keys(self) -> list[Key]:
		"""Список ключей."""

		return self.__Keys

	@property
	def name(self) -> str | None:
		"""Название позиции."""

		return self.__Name

	#==========================================================================================#
	# >>>>> МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, important: bool = False, name: str | None = None, description: str | None = None):
		"""
		Объектное представление позиции команды.
			important – указывает, является ли позиция обязательной;\n
			name – название позиции;\n
			description – описание позиции.
		"""

		#---> Генерация динамических атрибутов.
		#==========================================================================================#
		self.__Name = name
		self.__Description = description
		self.__IsImportant = important
		self.__Arguments = list()
		self.__Flags = list()
		self.__Keys = list()
		
	def add_argument(self, type: ParametersTypes = ParametersTypes.All, description: str | None = None, important: bool = False):
		"""
		Добавляет аргумент на позицию.
			type – тип значения аргумента;\n
			description – описание позиции;\n
			important – указывает, является ли позиция обязательной.
		"""

		if important: self.__IsImportant = True

		for CurrentArgument in self.__Arguments: 
			if CurrentArgument.type == type: raise IdenticalArguments(type.value)

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
		"""Список аргументов команды без позиций."""

		return self.__Arguments

	@property
	def description(self) -> str:
		"""Описание команды."""

		return self.__Description

	@property
	def flags(self) -> list[Flag]:
		"""Список флагов команды без позиций."""

		return self.__Flags

	@property
	def has_important_argument(self) -> bool:
		"""Состояние: имеет ли команда обязательный важный аргумент."""

		return self.__HasImportantArgument

	@property
	def has_important_flag(self) -> bool:
		"""Состояние: имеет ли команда обязательный важный аргумент."""

		return self.__HasImportantFlag

	@property
	def has_important_key(self) -> bool:
		"""Состояние: имеет ли команда обязательный важный аргумент."""

		return self.__HasImportantKey

	@property
	def keys(self) -> list[Key]:
		"""Список ключей команды без позиций."""

		return self.__Keys

	@property
	def max_parameters_count(self) -> int:
		"""Максимальное количество параметров."""

		MaxParametersCount = 0

		for Element in [self.__Positions, self.__Arguments, self.__Flags, self.__Keys]:

			for Part in Element: 
				if type(Part) == Position and Part.keys: MaxParametersCount += 2
				elif type(Part) == Position and not Part.keys: MaxParametersCount += 1
				elif type(Part) == Key: MaxParametersCount += 2
				else: MaxParametersCount += 1

		return MaxParametersCount

	@property
	def min_parameters_count(self) -> int:
		"""Минимальное количество параметров."""

		MinParametersCount = 0

		for Element in [self.__Positions, self.__Arguments, self.__Flags, self.__Keys]:

			for Part in Element: 

				if Part.is_important: 

					if type(Part) == Position:
						if Part.keys and not Part.flags and not Part.arguments: MinParametersCount += 2
						else: MinParametersCount += 1

					elif type(Part) == Position and Part.keys: MinParametersCount += 2
					elif type(Part) == Position and not Part.keys: MinParametersCount += 1
					elif type(Part) == Key: MinParametersCount += 2
					else: MinParametersCount += 1

		return MinParametersCount

	@property
	def name(self) -> str:
		"""Название команды."""

		return self.__Name

	@property
	def positions(self) -> list[Position]:
		"""Список позиций."""

		return self.__Positions

	#==========================================================================================#
	# >>>>> МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, name: str, description: str | None = None):
		"""
		Описание команды.
			name – название команды;\n
			description – описание команды.
		"""

		#---> Генерация динамических атрибутов.
		#==========================================================================================#
		self.__Name = name
		self.__Description = description
		self.__Positions: list[Position] = list()
		self.__Arguments: list[Argument] = list()
		self.__Flags: list[Flag] = list()
		self.__Keys: list[Key] = list()
		self.__HasImportantArgument = False
		self.__HasImportantFlag = False
		self.__HasImportantKey = False

	def add_argument(self, type: ParametersTypes = ParametersTypes.All, description: str | None = None, important: bool = False):
		"""
		Добавляет аргумент команды.
			type – тип значения аргумента;\n
			description – описание позиции;\n
			important – указывает, является ли позиция обязательной.
		"""

		if important: self.__HasImportantArgument = True
		self.__Arguments.append(Argument(type, description, important))

	def add_flag(self, name: str, description: str | None = None, important: bool = False):
		"""
		Добавляет флаг команды.
			name – название флага;\n
			description – описание флага;\n
			important – указывает, является ли флаг обязательным.
		"""

		if important: self.__HasImportantFlag = True
		self.__Flags.append(Flag(name, description, important))

	def add_key(self, name: str, type: ParametersTypes = ParametersTypes.All, description: str | None = None, important: bool = False):
		"""
		Добавляет ключ команды.
			name – название ключа;\n
			type – тип значения ключа;\n
			description – описание ключа;\n
			important – указывает, является ли ключ обязательным.
		"""

		if important: self.__HasImportantKey = True
		self.__Keys.append(Key(name, type, description, important))

	def create_position(self, name: str | None = None, description: str | None = None, important: bool = False) -> Position:
		"""
		Создаёт позицию.
			name – название позиции;\n
			description – описание позиции;\n
			important – указывает, является ли позиция обязательной.
		"""

		NewPosition = Position(important, name, description)
		self.__Positions.append(NewPosition)

		return self.__Positions[-1]

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
	
	def get_key_value(self, key: str, exception: bool = False) -> any:
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
			self.__ParametersLocks = [False] * len(self.__Parameters)
			self.__PositionsLocks = [False] * len(command.positions)
			self.__ParametersLocks[0] = True

			for Index in range(1, len(self.__Parameters)):
				Flags += self.__ParseFlags(Index, command)	
				Keys = MergeDictionaries(Keys, self.__ParseKeys(Index, command))

			for Index in range(1, len(self.__Parameters)):
				Arguments += self.__ParseArguments(Arguments, Index, command)

			self.__CheckUnlockedParameters(self.__ParametersLocks)
			self.__CheckParametersCount(command)
			self.__CommandData = ParsedCommandData(command.name, Flags, Keys, Arguments)

	def __CheckParametersCount(self, command: Command):
		"""
		Проверяет соответвтсие количества параметров.
			command – описание команды.
		"""

		if len(self.__Parameters) - 1 > command.max_parameters_count: raise TooManyParameters(" ".join(self.__Parameters))
		if len(self.__Parameters) - 1 < command.min_parameters_count: raise NotEnoughParameters(" ".join(self.__Parameters))

	def __CheckUnlockedParameters(self, parameters_locks: list[bool]):
		"""
		Проверяет незаблокированные параметры.
			parameters_locks – список состояний блокировки параметров.
		"""

		IndicatorsOrder = [self.flags_indicator, self.keys_indicator]
		ExceptionsOrder = [UnknownFlag, UnknownKey]

		if len(self.keys_indicator) > len(self.flags_indicator):
			IndicatorsOrder.reverse()
			ExceptionsOrder.reverse()

		for Index in range(1, len(self.__Parameters)):

			if not parameters_locks[Index]:

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

	def __ConfirmParametrType(self, value: str, type_name: ParametersTypes = ParametersTypes.All, raise_exception: bool = True) -> any:
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

				try:
					Value = dateparser.parse(value).date()

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

		if Value == None and raise_exception: raise InvalidParameterType(value, ParametersTypes.URL.value)

		return Value

	#==========================================================================================#
	# >>>>> МЕТОДЫ ПАРСИНГА ПАРАМЕТРОВ <<<<< #
	#==========================================================================================#

	def __ParseArguments(self, arguments: list[any], parameter_index: int, command: Command) -> dict[str, any]:
		"""
		Возвращает список значений аргументов.
			arguments – список значений аргументов;\n
			parameter_index – индекс параметра;\n
			command – описание команды.
		"""
		
		Arguments = list()

		for PositionIndex in range(len(command.positions)):

			if not self.__ParametersLocks[parameter_index]:
				CurrentPosition = command.positions[PositionIndex]

				if CurrentPosition.arguments and not self.__PositionsLocks[PositionIndex]:
					self.__ParametersLocks[parameter_index] = True

					for Argument in CurrentPosition.arguments:
						Value = self.__ConfirmParametrType(self.__Parameters[parameter_index], Argument.type, raise_exception = False)

						if Value:
							Arguments.append(Value)
							break

						elif Argument == CurrentPosition.arguments[-1]: 
							Types = list()
							for Argument in CurrentPosition.arguments: Types.append(Argument.type.value)
							raise InvalidPositionalArgumentTypes(self.__Parameters[parameter_index], Types)
					
					continue

				else: break

		if len(arguments) < len(command.arguments):

			for CurrentArgument in command.arguments:

				if not self.__ParametersLocks[parameter_index]:
					self.__ParametersLocks[parameter_index] = True
					Arguments.append(self.__ConfirmParametrType(self.__Parameters[parameter_index], CurrentArgument.type))
					continue

				else: break
				
		return Arguments

	def __ParseFlags(self, parameter_index: int, command: Command) -> list[str]:
		"""
		Возвращает список активных флагов.
			parameter_index – индекс параметра;\n
			command – описание команды.
		"""

		Flags = list()
		Parameter = self.__Parameters[parameter_index]

		if Parameter.startswith(self.__FlagsIndicator):
			Parameter = Parameter[len(self.__FlagsIndicator):]

			for PositionIndex in range(len(command.positions)):
				CurrentPosition = command.positions[PositionIndex]
				PositionFlagsNames = list()
				for PositionFlag in CurrentPosition.flags: PositionFlagsNames.append(PositionFlag.name)
				
				if Parameter in PositionFlagsNames:
					if not self.__ParametersLocks[parameter_index]: self.__ParametersLocks[parameter_index] = True
					else: raise MutuallyExclusiveFlags(" ".join(self.__Parameters))
					if not self.__PositionsLocks[PositionIndex]: self.__PositionsLocks[PositionIndex] = True
					else: raise MutuallyExclusivePositions(" ".join(self.__Parameters))
					Flags.append(Parameter)
					continue

			for CurrentFlag in command.flags:

				if Parameter == CurrentFlag.name: 
					if not self.__ParametersLocks[parameter_index]: self.__ParametersLocks[parameter_index] = True
					else: raise MutuallyExclusiveFlags(" ".join(self.__Parameters))
					Flags.append(Parameter)
					continue

		return Flags

	def __ParseKeys(self, parameter_index: int, command: Command) -> dict[str, any]:
		"""
		Возвращает словарь активных ключей и их значений.
			parameter_index – индекс параметра;\n
			command – описание команды.
		"""

		Keys = dict()
		Parameter = self.__Parameters[parameter_index]

		if Parameter.startswith(self.__KeysIndicator):
			Parameter = Parameter[len(self.__KeysIndicator):]

			for PositionIndex in range(len(command.positions)):
				CurrentPosition = command.positions[PositionIndex]
				
				for PositionKey in CurrentPosition.keys:

					if Parameter == PositionKey.name:

						if not self.__ParametersLocks[parameter_index]:
							self.__ParametersLocks[parameter_index] = True
							self.__ParametersLocks[parameter_index + 1] = True

						else:
							raise MutuallyExclusiveKeys(" ".join(self.__Parameters))

						if not self.__PositionsLocks[PositionIndex]: self.__PositionsLocks[PositionIndex] = True
						else: raise MutuallyExclusivePositions(" ".join(self.__Parameters))
						Keys[Parameter] = self.__ConfirmParametrType(self.__Parameters[parameter_index + 1], PositionKey.type)
						continue

			for CurrentKey in command.keys:

				if Parameter == CurrentKey.name: 
						
						if not self.__ParametersLocks[parameter_index]:
							self.__ParametersLocks[parameter_index] = True
							self.__ParametersLocks[parameter_index + 1] = True

						else:
							raise MutuallyExclusiveKeys(" ".join(self.__Parameters))

						Keys[Parameter] = self.__ConfirmParametrType(self.__Parameters[parameter_index + 1], CurrentKey.type)
						continue

		return Keys

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
		MSG_Name = TextStyler("Argument").decorate.bold
		MSG_Type = f" ({argument.type.value})"
		MSG_Description = f": {argument.description}" if argument.description else ""
		Description = f"\n{MSG_Indent}    • {MSG_Name}{MSG_Type}{MSG_Description}"

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
		Description = f"\n{MSG_Indent}    • {MSG_Name}{MSG_Description}"

		return Description
	
	def __BuildKeyDescription(self, key: Key, indent: str | None = None) -> str:
		"""
		Строит описание для ключа.
			key – ключ;\n
			indent – отступ, добавляемый к каждой строке.
		"""

		MSG_Indent = indent or "  "
		MSG_Name = TextStyler(self.__KeysIndicator + key.name).decorate.bold
		MSG_Type = f" ({key.type.value})"
		MSG_Description = f": {key.description}" if key.description else ""
		Description = f"\n{MSG_Indent}    • {MSG_Name}{MSG_Type}{MSG_Description}"

		return Description

	def __BuildPositionDescription(self, position: Command | Position, index: int | None = None) -> str:
		"""
		Строит описание позиции или свободных параметров команды.
			position – позиция или описание команды;\n
			index – индекс обрабатываемой позиции.
		"""

		Help = ""
		Indent = ""
		IsPosition = False

		if type(index) == int:
			Indent = "  "
			IsPosition = True
			PositionName = f"{Indent}{position.name}" if position.name else f"{Indent}POSITION_{index + 1}"
			MSG_Description = f": {position.description}" if position.description else ""
			Help += TextStyler(f"\n{PositionName}").decorate.bold + MSG_Description

		if position.arguments and IsPosition: Help += f"\n{Indent}  ARGUMENTS:"
		elif position.arguments: Help += f"\n{Indent}  " + TextStyler("ARGUMENTS:").decorate.bold
		for CurrentArgument in position.arguments:
			Help += self.__BuildArgumentDescription(CurrentArgument, Indent)

		if position.flags and IsPosition: Help += f"\n{Indent}  FLAGS:"
		elif position.flags: Help += f"\n{Indent}  " + TextStyler("FLAGS:").decorate.bold
		for CurrentFlag in position.flags:
			Help += self.__BuildFlagDescription(CurrentFlag, Indent)

		if position.keys and IsPosition: Help += f"\n{Indent}  KEYS:"
		elif position.keys: Help += f"\n{Indent}  " + TextStyler("KEYS:").decorate.bold
		for CurrentKey in position.keys:
			Help += self.__BuildKeyDescription(CurrentKey, Indent)

		return Help

	def __CreateCommandHelp(self, commands: list[Command], command_name: str):
		"""
		Отправляет подробное описание команды в callback-фнкцию.
			commands – описательные структуры комманд;\n
			command_name – название команды, для которой требуется получить помощь.
		"""

		HelpCommand = None

		for CurrentCommand in commands:
			if CurrentCommand.name == command_name: HelpCommand = CurrentCommand

		if HelpCommand:
			Help = TextStyler(HelpCommand.name).decorate.bold
			Help += self.__GenerateCommandMap(HelpCommand)

			if HelpCommand.description:
				Description = TextStyler(HelpCommand.description).decorate.bold
				Help += f"\n{Description}"

			for PositionIndex in range(len(HelpCommand.positions)):
				Help += self.__BuildPositionDescription(HelpCommand.positions[PositionIndex], PositionIndex)

			Help += self.__BuildPositionDescription(HelpCommand)

			if "*" in Help.split("\n")[0]: Help += f"\n{self.__HelpTranslationObject.important_note}" if self.__HelpTranslationObject.important_note else ""
			self.__HelpCallback(Help)

		else: 
			self.__HelpCallback(self.__HelpTranslationObject.no_command.replace(r"%c", command_name))

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
		Positions = command.positions
		Map = ""

		for Index in range(len(Positions)):
			MSG_Name = f"{Positions[Index].name}" if Positions[Index].name else f"POSITION_{Index + 1}"
			MSG_Important = "*" if Positions[Index].is_important else ""
			Map += f" [{MSG_Name}{MSG_Important}]"

		IsArgumentsImportant = "*" if command.has_important_argument else ""
		IsFlagsImportant = "*" if command.has_important_flag else ""
		IsKeysImportant = "*" if command.has_important_key else ""
		if command.arguments: Map += f" {{ARGUMENTS{IsArgumentsImportant}}}"
		if command.flags: Map += f" {{FLAGS{IsFlagsImportant}}}"
		if command.keys: Map += f" {{KEYS{IsKeysImportant}}}"

		return Map

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, parameters: list[str] | None = None):
		"""
		Обработчик консольных параметров.
			parameters – список параметров (по умолчанию берётся из аргументов запуска скрипта).
		"""

		#---> Генерация динамических атрибутов.
		#==========================================================================================#
		self.__KeysIndicator = "--"
		self.__FlagsIndicator = "-"
		self.__CommandData = None
		self.__Parameters = parameters or sys.argv[1:]
		self.__CommandName = self.__Parameters[0] if self.__Parameters else None
		self.__EnableHelp = False
		self.__HelpCallback = print
		self.__ParametersLocks = None
		self.__PositionsLocks = None
		self.__HelpTranslationObject = HelpTranslation()

	def enable_help(self, status: bool):
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

		if type(commands) == Command: commands = [commands]

		if self.__EnableHelp:
			Help = Command("help", self.__HelpTranslationObject.command_description)
			Help.add_argument(description = self.__HelpTranslationObject.argument_description)
			commands.append(Help)

		for CurrentCommand in commands: self.__CheckCommand(CurrentCommand)

		if self.__EnableHelp and self.__CommandData and self.__CommandData.name == "help":
			
			if self.__CommandData.arguments:
				self.__CreateCommandHelp(commands, self.__CommandData.arguments[0])

			else:
				self.__CreateHelpList(commands)
		
		return self.__CommandData

	def set_source(self, parameters: list[str]):
		"""
		Задаёт список параметров.
			parameters – список параметров (по умолчанию берётся из параметров скрипта).
		"""

		self.__Parameters = parameters

	def set_flags_indicator(self, indicator: str):
		"""
		Задаёт индикатор флагов.
			indicator – индикатор флагов.
		"""

		if indicator != self.__KeysIndicator:
			self.__FlagsIndicator = indicator

		else:
			raise IdenticalIndicators()

	def set_help_callback(self, callback: any):
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