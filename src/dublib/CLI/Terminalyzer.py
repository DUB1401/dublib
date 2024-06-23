from ..CLI.StyledPrinter import Styles, TextStyler
from ..Methods.Data import MergeDictionaries
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

	All = None
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
	# >>>>> СВОЙСТВА ТОЛЬКО ДЛЯ ЧТЕНИЯ <<<<< #
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

	def __init__(self, type: ParametersTypes, important: bool, description: str | None):
		"""
		Аргумент команды.
			type – тип значения аргумента;
			important – указывает, является ли аргумент обязательным;
			description – описание аргумента.
		"""

		#---> Генерация динамических свойств.
		#==========================================================================================#
		# Тип значения аргумента.
		self.__Type = type
		# Описание аргумента.
		self.__Description = description
		# Состояние: является ли аргумент обязательным.
		self.__IsImportant = important

class Flag:
	"""Флаг команды."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА ТОЛЬКО ДЛЯ ЧТЕНИЯ <<<<< #
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

	def __init__(self, name: str, important: bool, description: str | None):
		"""
		Флаг команды.
			name – название флага;
			important – указывает, является ли флаг обязательным;
			description – описание флага.
		"""

		#---> Генерация динамических свойств.
		#==========================================================================================#
		# Название флага.
		self.__Name = name
		# Описание флага.
		self.__Description = description
		# Состояние: является ли флаг обязательным.
		self.__IsImportant = important

class Key:
	"""Ключ команды."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА ТОЛЬКО ДЛЯ ЧТЕНИЯ <<<<< #
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

	def __init__(self, name: str, type: ParametersTypes, important: bool, description: str | None):
		"""
		Ключ команды.
			name – название ключа;
			type – тип значения ключа;
			important – указывает, является ли ключ обязательным;
			description – описание ключа.
		"""

		#---> Генерация динамических свойств.
		#==========================================================================================#
		# Название ключа.
		self.__Name = name
		# Тип значения ключа.
		self.__Type = type
		# Описание ключа.
		self.__Description = description
		# Состояние: является ли ключ обязательным.
		self.__IsImportant = important

#==========================================================================================#
# >>>>> ВСПОМОГАТЕЛЬНЫЕ ТИПЫ ДАННЫХ <<<<< #
#==========================================================================================#
	
class Position:

	#==========================================================================================#
	# >>>>> СВОЙСТВА ТОЛЬКО ДЛЯ ЧТЕНИЯ <<<<< #
	#==========================================================================================#

	@property
	def argument(self) -> Argument:
		"""Аргумент."""

		return self.__Argument

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
			important – указывает, является ли позиция обязательной;
			name – название позиции;
			description – описание позиции.
		"""

		#---> Генерация динамических свойств.
		#==========================================================================================#
		# Название позиции.
		self.__Name = name
		# Описание позиции.
		self.__Description = description
		# Состояние: является ли позиция обязательной.
		self.__IsImportant = important
		# Списки параметров.
		self.__Argument = None
		self.__Flags = list()
		self.__Keys = list()
		
	def add_argument(self, type: ParametersTypes = ParametersTypes.All, important: bool = False, description: str | None = None):
		"""
		Добавляет аргумент на позицию.
			type – тип значения аргумента;
			important – указывает, является ли позиция обязательной;
			description – описание позиции.
		"""

		# Проверка обязательности позиции.
		if important: self.__IsImportant = True
		# Добавление аргумента.
		self.__Argument = Argument(type, important, description)

	def add_flag(self, name: str, important: bool = False, description: str | None = None):
		"""
		Добавляет флаг на позицию.
			name – название флага;
			important – указывает, является ли флаг обязательным;
			description – описание флага.
		"""

		# Проверка обязательности позиции.
		if important: self.__IsImportant = True
		# Добавление флага.
		self.__Flags.append(Flag(name, important, description))

	def add_key(self, name: str, type: ParametersTypes = ParametersTypes.All, important: bool = False, description: str | None = None):
		"""
		Добавляет ключ на позицию.
			name – название ключа;
			type – тип значения ключа;
			important – указывает, является ли ключ обязательным;
			description – описание ключа.
		"""

		# Проверка обязательности позиции.
		if important: self.__IsImportant = True
		# Добавление ключа.
		self.__Keys.append(Key(name, type, important, description))

class Command:
	"""Описание команды."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА ТОЛЬКО ДЛЯ ЧТЕНИЯ <<<<< #
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
	def keys(self) -> list[Key]:
		"""Список ключей команды без позиций."""

		return self.__Keys

	@property
	def max_parameters_count(self) -> int:
		"""Максимальное количество параметров."""

		# Максимальное количество параметров.
		MaxParametersCount = 0

		# Для каждого элемента команды.
		for Element in [self.__Positions, self.__Arguments, self.__Flags, self.__Keys]:

			# Для каждой части.
			for Part in Element: 
				# Подсчёт параметров.
				if type(Part) == Position and Part.keys: MaxParametersCount += 2
				elif type(Part) == Position and not Part.keys: MaxParametersCount += 1
				elif type(Part) == Key: MaxParametersCount += 2
				else: MaxParametersCount += 1

		return MaxParametersCount

	@property
	def min_parameters_count(self) -> int:
		"""Минимальное количество параметров."""

		# Минимальное количество параметров.
		MinParametersCount = 0

		# Для каждого элемента команды.
		for Element in [self.__Positions, self.__Arguments, self.__Flags, self.__Keys]:

			# Для каждой части.
			for Part in Element: 

				# Если часть обязательна.
				if Part.is_important: 
					# Подсчёт параметров.
					if type(Part) == Position and Part.keys: MinParametersCount += 2
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
			name – название команды;
			description – описание команды.
		"""

		#---> Генерация динамических свойств.
		#==========================================================================================#
		# Название команды.
		self.__Name = name
		# Описание команды.
		self.__Description = description
		# Список позиций.
		self.__Positions: list[Position] = list()
		# Списки параметров.
		self.__Arguments: list[Argument] = list()
		self.__Flags: list[Flag] = list()
		self.__Keys: list[Key] = list()

	def add_argument(self, type: ParametersTypes = ParametersTypes.All, important: bool = False, description: str | None = None):
		"""
		Добавляет аргумент команды.
			type – тип значения аргумента;
			important – указывает, является ли позиция обязательной;
			description – описание позиции.
		"""

		# Проверка обязательности позиции.
		if important: self.__IsImportant = True
		# Добавление аргумента.
		self.__Arguments.append(Argument(type, important, description))

	def add_flag(self, name: str, important: bool = False, description: str | None = None):
		"""
		Добавляет флаг команды.
			name – название флага;
			important – указывает, является ли флаг обязательным;
			description – описание флага.
		"""

		# Проверка обязательности позиции.
		if important: self.__IsImportant = True
		# Добавление флага.
		self.__Flags.append(Flag(name, important, description))

	def add_key(self, name: str, type: ParametersTypes = ParametersTypes.All, important: bool = False, description: str | None = None):
		"""
		Добавляет ключ команды.
			name – название ключа;
			type – тип значения ключа;
			important – указывает, является ли ключ обязательным;
			description – описание ключа.
		"""

		# Проверка обязательности позиции.
		if important: self.__IsImportant = True
		# Добавление ключа.
		self.__Keys.append(Key(name, type, important, description))

	def create_position(self, important: bool = False, name: str | None = None, description: str | None = None) -> Position:
		"""
		Создаёт позицию.
			important – указывает, является ли позиция обязательной;
			name – название позиции;
			description – описание позиции.
		"""

		# Создание позиции.
		NewPosition = Position(name, description, important)
		# Добавление позиции в команду.
		self.__Positions.append(NewPosition)

		return self.__Positions[-1]

class ParsedCommandData:
	"""Данные обработанной команды."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА ТОЛЬКО ДЛЯ ЧТЕНИЯ <<<<< #
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
			name – название команды;
			flags – список активированных флагов;
			keys – словарь активированных ключей и их значений;
			arguments – список аргументов.
		"""

		#---> Генерация динамических свойств.
		#==========================================================================================#
		# Список аргументов.
		self.__Arguments = arguments
		# Список активированных флагов.
		self.__Flags = flags
		# Словарь активированных ключей и их значений.
		self.__Keys = keys
		# Название команды.
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

		# Состояние: активирован ли флаг.
		IsActivated = False
		# Если флаг активирован, переключить состояние.
		if flag in self.__Flags: IsActivated = True

		return IsActivated
	
	def check_key(self, key: str) -> bool:
		"""
		Проверяет, активирован ли ключ.
			key – название ключа.
		"""

		# Состояние: активирован ли ключ.
		IsActivated = False
		# Если ключ активирован, переключить состояние.
		if key in self.__Keys.keys(): IsActivated = True

		return IsActivated
	
	def get_key_value(self, key: str, exception: bool = False) -> any:
		"""
		Возвращает значение активированного ключа.
			key – название ключа;
			exception – указывает, нужно ли выбросить исключение при отсутствии ключа.
		"""

		# Значение ключа.
		Value = None
		# Если ключ существует, записать его значение, иначе выбросить исключение.
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
		
		# Если название описания команды соответствует названию из параметров.
		if self.__ConfirmCommandName(command):
			# Список активированных флагов.
			Flags = list()
			# Словарь активированных ключей.
			Keys = dict()
			# Аргументы.
			Arguments = list()
			# Состояния блокировки параметров и позиций.
			self.__ParametersLocks = [False] * len(self.__Parameters)
			self.__PositionsLocks = [False] * len(command.positions)
			# Блокировка параметра с названием команды.
			self.__ParametersLocks[0] = True

			# Для каждого параметра.
			for Index in range(1, len(self.__Parameters)):
				# Парсинг флагов.
				Flags += self.__ParseFlags(Index, command)	
				# Парсинг ключей.
				Keys = MergeDictionaries(Keys, self.__ParseKeys(Index, command))

			# Для каждого параметра.
			for Index in range(1, len(self.__Parameters)):
				# Парсинг аргументов.
				Arguments += self.__ParseArguments(Index, command)

			print("Params: ", self.__ParametersLocks)
			print("Positions:", self.__PositionsLocks)
			# Проверка количества параметров.
			self.__CheckParametersCount(command)
			# Заполнение данных спаршенной команды.
			self.__CommandData = ParsedCommandData(command.name, Flags, Keys, Arguments)

	def __CheckParametersCount(self, command: Command):
		"""
		Проверяет соответвтсие количества параметров.
			command – описание команды.
		"""

		# Если аргументов слишком много, выбросить исключение.
		if len(self.__Parameters) - 1 > command.max_parameters_count: raise TooManyParameters(" ".join(self.__Parameters))
		# Если аргументов слишком мало, выбросить исключение.
		if len(self.__Parameters) - 1 < command.min_parameters_count: raise NotEnoughParameters(" ".join(self.__Parameters))

	def __ConfirmCommandName(self, command: Command) -> bool:
		"""
		Проверяет, соответствует ли название команды из описания текущему.
			command – описание команды.
		"""
		print(self.__CommandName)
		# Состояние: определена ли команда.
		IsDetermined = False
		# Если имя команды определено, переключить статус проверки.
		if command.name == self.__CommandName: IsDetermined = True
		
		return IsDetermined

	def __ConfirmParametrType(self, value: str, type_name: ParametersTypes = ParametersTypes.All) -> any:
		"""
		Проверяет и парсит значение параметра согласно его типу.
			value – значение параметра;
			type_name – тип параметра.
		"""
		
		# Если требуется проверить специфический тип аргумента.
		if type_name != ParametersTypes.All:

			# Если аргумент должен являться логическим состоянием.
			if type_name == ParametersTypes.Bool:
				# Приведение к нижнему регистру.
				value = value.lower()
				# Попытки преобразования значения.
				if value == "true": value = True
				elif value == "false": value = False
				elif value.isdigit(): value = bool(int(value))
				else: raise InvalidParameterType(value, ParametersTypes.Bool.value)

			# Если аргумент должен являться датой.
			if type_name == ParametersTypes.Date:

				try:
					# Парсинг даты.
					value = dateparser.parse(value).date()

				except: raise InvalidParameterType(value, ParametersTypes.Date.value)
			
			# Если аргумент должен являться числом.
			if type_name == ParametersTypes.Number:
				# Если вся строка, без учёта минуса, не является числом, выбросить исключение, иначе преобразовать в число.
				if not value.lstrip("-").isdigit(): raise InvalidParameterType(value, ParametersTypes.Number.value)
				else: value = int(value)
				
			# Если аргумент должен являться валидным путём.
			if type_name == ParametersTypes.ValidPath:
				# Если строка не является валидным путём, выбросить исключение.
				if not os.path.exists(value): raise InvalidParameterType(value, ParametersTypes.ValidPath.value)

			# Если аргумент должен являться набором буквенных символов.
			if type_name == ParametersTypes.Text:
				# Если строка содержит небуквенные символы, выбросить исключение.
				if not value.isalpha(): raise InvalidParameterType(value, ParametersTypes.Text.value)

			# Если аргумент должен являться URL.
			if type_name == ParametersTypes.URL:
				# Если строка не является URL, выбросить исключение.
				if not bool(urlparse(value).scheme): raise InvalidParameterType(value, ParametersTypes.URL.value)

		return value

	#==========================================================================================#
	# >>>>> ПРИВАТНЫЕ МЕТОДЫ ПАРСИНГА ПАРАМЕТРОВ <<<<< #
	#==========================================================================================#

	def __ParseArguments(self, parameter_index: int, command: Command) -> dict[str, any]:
		"""
		Возвращает список значений аргументов.
			parameter_index – индекс параметра;
			command – описание команды.
		"""
		
		# Список значений аргументов.
		Arguments = list()

		# Если параметр не блокирован.
		if not self.__ParametersLocks[parameter_index]:

			# Для каждой позиции.
			for PositionIndex in range(len(command.positions)):
				# Текущая позиция.
				CurrentPosition = command.positions[PositionIndex]

				# Если позиция имеет аргумент и не заблокирована.
				if CurrentPosition.argument and not self.__PositionsLocks[PositionIndex]:
					# Блокировка параметра.
					self.__ParametersLocks[parameter_index] = True
					# Добавление значения аргумента.
					Arguments.append(self.__ConfirmParametrType(self.__Parameters[parameter_index], CurrentPosition.argument.type))
					# Переход к следующей итерации.
					continue

			# Для каждого аргумента.
			for CurrentArgument in command.arguments:
				# Блокировка параметра.
				self.__ParametersLocks[parameter_index] = True
				# Добавление значения аргумента.
				Arguments.append(self.__ConfirmParametrType(self.__Parameters[parameter_index], CurrentArgument.type))
				# Переход к следующей итерации.
				continue
				
		return Arguments

	def __ParseFlags(self, parameter_index: int, command: Command) -> list[str]:
		"""
		Возвращает список активных флагов.
			parameter_index – индекс параметра;
			command – описание команды.
		"""

		# Список активированных флагов.
		Flags = list()
		# Обрабатываемый параметр.
		Parameter = self.__Parameters[parameter_index]

		# Если параметр начинается с индикатора флагов.
		if Parameter.startswith(self.__FlagsIndicator):
			# Обрезка идентификатора флагов.
			Parameter = Parameter[len(self.__FlagsIndicator):]

			# Для каждой позиции.
			for PositionIndex in range(len(command.positions)):
				# Текущая позиция.
				CurrentPosition = command.positions[PositionIndex]
				# Названия флагов позиции.
				PositionFlagsNames = list()
				# Получение названий флагов.
				for PositionFlag in CurrentPosition.flags: PositionFlagsNames.append(PositionFlag.name)
				
				# Если параметр является флагом позиции.
				if Parameter in PositionFlagsNames:
					# Если параметр не заблокирован, заблокировать, иначе выбросить исключение.
					if not self.__ParametersLocks[parameter_index]: self.__ParametersLocks[parameter_index] = True
					else: raise MutuallyExclusiveFlags(" ".join(self.__Parameters))
					# Если позиция не заблокирована, заблокировать, иначе выбросить исключение.
					if not self.__PositionsLocks[PositionIndex]: self.__PositionsLocks[PositionIndex] = True
					else: raise MutuallyExclusivePositions(" ".join(self.__Parameters))
					# Добавление активированного флага.
					Flags.append(Parameter)
					# Переход к следующей итерации.
					continue

			# Для каждого флага.
			for CurrentFlag in command.flags:

				# Если параметр является флагом.
				if Parameter == CurrentFlag.name: 
					# Если параметр не заблокирован, заблокировать, иначе выбросить исключение.
					if not self.__ParametersLocks[parameter_index]: self.__ParametersLocks[parameter_index] = True
					else: raise MutuallyExclusiveFlags(" ".join(self.__Parameters))
					# Добавление активированного флага.
					Flags.append(Parameter)
					# Переход к следующей итерации.
					continue

		return Flags

	def __ParseKeys(self, parameter_index: int, command: Command) -> dict[str, any]:
		"""
		Возвращает словарь активных ключей и их значений.
			parameter_index – индекс параметра;
			command – описание команды.
		"""

		# Словарь активированных ключей.
		Keys = dict()
		# Обрабатываемый параметр.
		Parameter = self.__Parameters[parameter_index]

		# Если параметр начинается с индикатора ключей.
		if Parameter.startswith(self.__KeysIndicator):
			# Обрезка идентификатора ключей.
			Parameter = Parameter[len(self.__KeysIndicator):]

			# Для каждой позиции.
			for PositionIndex in range(len(command.positions)):
				# Текущая позиция.
				CurrentPosition = command.positions[PositionIndex]
				
				# Для каждого ключа позиции.
				for PositionKey in CurrentPosition.keys:

					# Если параметр является ключом позиции.
					if Parameter == PositionKey.name:

						# Если параметр и следующий за ним не заблокированы.
						if not self.__ParametersLocks[parameter_index]:
							# Блокировка двух параметров.
							self.__ParametersLocks[parameter_index] = True
							self.__ParametersLocks[parameter_index + 1] = True

						else:
							# Выброс исключения.
							raise MutuallyExclusiveKeys(" ".join(self.__Parameters))

						# Если позиция не заблокирована, заблокировать, иначе выбросить исключение.
						if not self.__PositionsLocks[PositionIndex]: self.__PositionsLocks[PositionIndex] = True
						else: raise MutuallyExclusivePositions(" ".join(self.__Parameters))
						# Добавление активированного ключа и его значения.
						Keys[Parameter] = self.__ConfirmParametrType(self.__Parameters[parameter_index + 1], PositionKey.type)
						# Переход к следующей итерации.
						continue

			# Для каждого ключа.
			for CurrentKey in command.keys:

				# Если параметр является ключом.
				if Parameter == CurrentKey.name: 
						
						# Если параметр и следующий за ним не заблокированы.
						if not self.__ParametersLocks[parameter_index]:
							# Блокировка двух параметров.
							self.__ParametersLocks[parameter_index] = True
							self.__ParametersLocks[parameter_index + 1] = True

						else:
							# Выброс исключения.
							raise MutuallyExclusiveKeys(" ".join(self.__Parameters))

						# Добавление активированного ключа и его значения.
						Keys[Parameter] = self.__ConfirmParametrType(self.__Parameters[parameter_index + 1], CurrentKey.type)
						# Переход к следующей итерации.
						continue

		return Keys

	#==========================================================================================#
	# >>>>> ПРИВАТНЫЕ МЕТОДЫ ПОМОЩИ <<<<< #
	#==========================================================================================#

	def __CreateCommandHelp(self, commands: list[Command], command_name: str):
		"""
		Отправляет подробное описание команды в callback-фнкцию.
			commands – описательные структуры комманд;
			command_name – название команды, для которой требуется получить помощь.
		"""

		# Обрабатываемая команда.
		CommandForHelp = None

		# Для каждой команды.
		for CurrentCommand in commands:
			# Если найдена искомая команда, записать её данные.
			if CurrentCommand.name == command_name: CommandForHelp = CurrentCommand

		# Если команда определена.
		if CommandForHelp:
			# Текст помощи.
			Help = TextStyler(CommandForHelp.name, decorations = [Styles.Decorations.Bold])

			#---> Обработка слоёв.
			#==========================================================================================#

			# Для каждого слоя.
			for Layout in CommandForHelp.layouts: pass

			# Отправка помощи в callback-функцию.
			self.__HelpCallback(Help)

		else: 
			# Отправка сообщения об отсутствии команды в callback-функцию.
			self.__HelpCallback(f"Command \"{command_name}\" not found.")

	def __CreateHelpList(self, commands: list[Command]):
		"""
		Отправляет список команд с их описанием в callback-фнкцию.
			commands – описательные структуры комманд.
		"""

		#---> Получение данных.
		#==========================================================================================#
		# Таблица помощи.
		HelpTable = {
			"Command": [],
			"Description": []
		}

		# Для каждой команды.
		for CurrentCommand in commands:
			# Добавление данных команды в таблицу.
			HelpTable["Command"].append(CurrentCommand.name)
			HelpTable["Description"].append(CurrentCommand.description or "")

		#---> Генерация таблицы.
		#==========================================================================================#
		# Инициализация таблицы.
		TableObject = PrettyTable()
		TableObject.set_style(PLAIN_COLUMNS)

		# Для каждого столбца.
		for ColumnName in HelpTable.keys():
			# Буфер стилизации названия колонки.
			Buffer = TextStyler(ColumnName, decorations = [Styles.Decorations.Bold])
			# Парсинг столбца.
			TableObject.add_column(Buffer, HelpTable[ColumnName])

		# Установка стилей таблицы.
		TableObject.align = "l"
		# Отправка таблицы в callback-функцию.
		self.__HelpCallback(TableObject.get_string())

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, parameters: list[str] | None = None):
		"""
		Обработчик консольных параметров.
			parameters – список параметров (по умолчанию берётся из аргументов запуска скрипта).
		"""

		#---> Генерация динамических свойств.
		#==========================================================================================#
		# Индикатор ключей.
		self.__KeysIndicator = "--"
		# Индикатор флагов.
		self.__FlagsIndicator = "-"
		# Список задействованных позиций.
		self.__PositionsStatuses = list()
		# Список задействованных слоёв.
		self.__LayoutsStatuses = list()
		# Данные спаршенной команды.
		self.__CommandData = None
		# Переданные параметры.
		self.__Parameters = parameters or sys.argv[1:]
		# Название команды.
		self.__CommandName = self.__Parameters[0] if self.__Parameters else None
		# Состояние: используется ли помощь.
		self.__EnableHelp = False
		# Функция вывода помощи.
		self.__HelpCallback = print

		# Состояния блокировки параметров и позиций.
		self.__ParametersLocks = None
		self.__PositionsLocks = None

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

		# Если передана одна команда, преобразовать её в список.
		if type(commands) == Command: commands = [commands]

		# Если включена помощь.
		if self.__EnableHelp:
			# Генерация команды помощи.
			Help = Command("help", "Prints a list of supported commands. For details, add the name of the command as an argument.")
			Help.add_argument(description = "The name of command for which you want to see detailed help.")
			# Добавление команды в обработчик.
			commands.append(Help)

		# Проверка каждой команды из списка.
		for CurrentCommand in commands: self.__CheckCommand(CurrentCommand)

		# Если модуль помощи включен и вызван.
		if self.__EnableHelp and self.__CommandData and self.__CommandData.name == "help":
			
			# Если переданы аргументы.
			if self.__CommandData.arguments:
				# Вывод подробной помощи по команде.
				self.__CreateCommandHelp(commands, self.__CommandData.arguments[0])

			else:
				# Составление списка команд.
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

		# Если новый индикатор флага не повторяет индикатор ключа.
		if indicator != self.__KeysIndicator:
			# Установка нового индикатора.
			self.__FlagsIndicator = indicator

		else:
			# Выброс исключения.
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

		# Если новый индикатор ключа не повторяет индикатор флага.
		if indicator != self.__FlagsIndicator:
			# Установка нового индикатора.
			self.__KeysIndicator = indicator

		else:
			# Выброс исключения.
			raise IdenticalIndicators()