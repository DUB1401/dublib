from .... import Exceptions

from typing import Iterable, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
	from .Definition import _Flag, _Key, Command

#==========================================================================================#
# >>>>> ПРЕДСТАВЛЕНИЯ ОБРАБОТАННЫХ ПАРАМЕТРОВ <<<<< #
#==========================================================================================#

class _ParsedArgument:
	"""Представление обработанного аргумента."""

	@property
	def value(self) -> bool | float | int | str | datetime:
		"""Значение ключа."""

		return self.__Value

	def __init__(self, value: bool | float | int | str | datetime):
		"""
		Представление обработанного аргумента.

		:param value: Значение ключа.
		:type value: bool | float | int | str | datetime
		"""

		self.__Value = value

class _ParsedFlag:
	"""Представление обработанного флага."""

	@property
	def aliases(self) -> list[str]:
		"""Список псевдонимов."""

		return self.__Flag.aliases

	@property
	def name(self) -> str:
		"""Имя флага."""

		return self.__Flag.name

	def __init__(self, flag: "_Flag"):
		"""
		Представление обработанного флага.

		:param name: Флаг.
		:type name: _Flag
		"""

		self.__Flag = flag

class _ParsedKey:
	"""Представление обработанного ключа."""

	@property
	def aliases(self) -> list[str]:
		"""Список псевдонимов."""

		return self.__Key.aliases

	@property
	def name(self) -> str:
		"""Имя ключа."""

		return self.__Key.name

	@property
	def value(self) -> bool | float | int | str | datetime:
		"""Значение ключа."""

		return self.__Value

	def __init__(self, key: "_Key", value: bool | float | int | str | datetime):
		"""
		Представление обработанного ключа.

		:param key: Ключ.
		:type key: _Key
		:param value: Значение ключа.
		:type value: bool | float | int | str | datetime
		"""

		self.__Key = key
		self.__Value = value

class _ParsedCommandParameters:

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def arguments(self) -> tuple[_ParsedArgument]:
		"""Последовательность представлений аргументов."""

		return self.__GetParametersType(_ParsedArgument)
	
	@property
	def flags(self) -> tuple[_ParsedFlag]:
		"""Последовательность представлений флагов."""

		return self.__GetParametersType(_ParsedFlag)
	
	@property
	def keys(self) -> tuple[_ParsedKey]:
		"""Последовательность представлений ключей."""

		return self.__GetParametersType(_ParsedKey)
	
	@property
	def positions(self) -> dict[str, _ParsedArgument | _ParsedFlag | _ParsedKey | None]:
		"""Словарь параеметров позиций."""

		return self.__Positions.copy()

	#==========================================================================================#
	# >>>>> ПРИВАТНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __GetParametersType(self, requred_type: _ParsedArgument | _ParsedFlag | _ParsedKey) -> tuple[type]:
		"""
		Возвращает последовательность представлений параметров определённого типа.

		:param requred_type: Требуемый тип.
		:type requred_type: _ParsedArgument | _ParsedFlag | _ParsedKey
		:return: Последовательность представлений параметров определённого типа.
		:rtype: tuple[type]
		"""

		Result = list()

		for Sequence in (self.__Positions.values(), self.__BasePosition):
			for Parameter in Sequence:
				if type(Parameter) == requred_type: Result.append(Parameter)

		return tuple(Result)

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self):
		"""Данные о спаршенных параметрах команды."""

		self.__Positions: dict[str, _ParsedArgument | _ParsedFlag | _ParsedKey | None] = dict()
		self.__BasePosition: list[_ParsedArgument | _ParsedFlag | _ParsedKey] = list()

	def add_base_parameter(self, parameter: _ParsedArgument | _ParsedFlag | _ParsedKey):
		"""
		Добавляет представление параметра на базовую позицию.

		:param parameter: Представление параметра.
		:type parameter: _ParsedArgument | _ParsedFlag | _ParsedKey
		"""

		self.__BasePosition.append(parameter)

	def set_positional_parameter(self, position_name: str, parameter: _ParsedArgument | _ParsedFlag | _ParsedKey):
		"""
		Устанавливает представление параметра на позицию.

		:param position_name: Имя позиции.
		:type position_name: str
		:param parameter: Представление параметра.
		:type parameter: _ParsedArgument | _ParsedFlag | _ParsedKey
		:raises Exceptions.CLI.Terminalyzer.MultipleParametersOnPosition: Попытка установки нескольких параметров для одной позиции.
		"""

		if position_name in self.__Positions: raise Exceptions.CLI.Terminalyzer.MultipleParametersOnPosition(position_name)
		self.__Positions[position_name] = parameter

#==========================================================================================#
# >>>>> ДАННЫЕ ОБРАБОТАННОЙ КОМАНДЫ <<<<< #
#==========================================================================================#

class ParsedCommandData:
	"""Данные обработанной команды."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def arguments(self) -> tuple[bool | float | int | str | datetime]:
		"""Последовательность значений аргументов."""

		return tuple(Element.value for Element in self.__ParsedData.arguments)
	
	@property
	def flags(self) -> tuple[_ParsedFlag]:
		"""Последовательность активированных флагов."""

		return self.__ParsedData.flags
	
	@property
	def keys(self) -> tuple[str, bool | float | int | str | datetime]:
		"""Cловарь имён активированных ключей и их значений."""

		return self.__ParsedData.keys
	
	@property
	def name(self) -> str:
		"""Название команды."""

		return self.__Name

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, name: str, parsed_data: _ParsedCommandParameters):

		self.__Name = name
		self.__ParsedData = parsed_data

	def __str__(self) -> str:
		"""
		Возвращает строковое представление данных команды.

		:return: Строковое представление данных команды.
		:rtype: str
		"""

		return str(self.to_dict())

	def check_flag(self, flag: str) -> bool:
		"""
		Проверяет, активирован ли флаг.
		
		:param flag: Название флага.
		:type flag: str
		:return: Состояние проверки.
		:rtype: bool
		"""

		for CurrentFlag in self.__ParsedData.flags:
			if flag == CurrentFlag.name or flag in CurrentFlag.aliases: return True

		return False
	
	def check_key(self, key: str) -> bool:
		"""
		Проверяет, активирован ли ключ.
		
		:param flag: Название ключа.
		:type flag: str
		:return: Состояние проверки.
		:rtype: bool
		"""

		for CurrentKey in self.__ParsedData.keys:
			if key == CurrentKey.name or key in CurrentKey.aliases: return True

		return False
	
	def get_key_value(self, key: str, exception: bool = False) -> bool | float | int | str | datetime:
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

		for CurrentKey in self.__ParsedData.keys:
			if key == CurrentKey.name or key in CurrentKey.aliases: return CurrentKey.value

		if exception: raise KeyError(key)

	def get_position_parameter(self, position_name: str) -> _ParsedArgument | _ParsedFlag | _ParsedKey | None:
		"""
		Возвращает параметр позиции.

		:param position_name: Имя позиции.
		:type position_name: str
		:return: Параметр позиции или `None` при пустой позиции.
		:rtype: _ParsedArgument | _ParsedFlag | _ParsedKey | None
		:raises KeyError: Позиция не обнаружена.
		"""

		return self.__ParsedData.positions[position_name]
	
	def get_position_value(self, position_name: str) -> bool | float | int | str | datetime | None:
		"""
		Для аргументов и ключей на позиции возвращает значение, для флагов – `True` при активации.

		:param position_name: Имя позиции.
		:type position_name: str
		:return: Параметр позиции или `None` при пустой позиции.
		:rtype: bool | float | int | str | datetime | None
		:raises KeyError: Позиция не обнаружена.
		"""

		ParsedParameter = self.get_position_parameter(position_name)
		if not ParsedParameter: return

		if type(ParsedParameter) == _ParsedFlag: return True
		else: return ParsedParameter.value

	def to_dict(self) -> dict[str, list[bool | float | int | str | datetime] | str]:
		"""
		Возвращает словарное представление объекта.

		:return: Словарное представление объекта.
		:rtype: dict[str, list[bool | float | int | str | datetime] | str]
		"""

		return {
			"name": self.__Name, 
			"arguments": self.arguments,
			"flags": list(self.__ParsedData.flags), 
			"keys": {Key.name: Key.value for Key in self.__ParsedData.keys}
		}

#==========================================================================================#
# >>>>> ОСНОВНОЙ КЛАСС <<<<< #
#==========================================================================================#

class _CommandParser:
	"""Парсер команды."""

	#==========================================================================================#
	# >>>>> ПРИВАТНЫЕ МЕТОДЫ ВАЛИДАЦИИ <<<<< #
	#==========================================================================================#

	def __CheckImportantPositionsLocks(self):
		"""
		Проверяет, все ли обязательные позиции заблокированы.

		:raises ImportantPositionEmpty: Для обязательной позиции не задан параметр.
		"""

		for CurrentPosition in self.__Command.positions:
			if CurrentPosition.is_important and not self.__PositionsLocks[CurrentPosition.name]:
				raise Exceptions.CLI.Terminalyzer.ImportantPositionEmpty(CurrentPosition.name)

	def __CheckParametersCount(self):
		"""
		Проверяет соответвтсие количества параметров.
		
		:raises TooManyParameters: Слишком много параметров.
		:raises NotEnoughParameters: Недостаточно параметров.
		"""
		
		ParametersCount = len(self.__Parameters)
		if ParametersCount > self.__Command.max_parameters_count: raise Exceptions.CLI.Terminalyzer.TooManyParameters(self.__Command.max_parameters_count, ParametersCount)
		if ParametersCount < self.__Command.min_parameters_count: raise Exceptions.CLI.Terminalyzer.NotEnoughParameters(self.__Command.min_parameters_count, ParametersCount)

	#==========================================================================================#
	# >>>>> ПРИВАТНЫЕ МЕТОДЫ ПАРСИНГА <<<<< #
	#==========================================================================================#

	def __CatchParameterForPositions(self, index: str):
		"""
		Поочерёдно проверяет позиции и пытается заполнить их параметрами соответствующего типа.

		:param index: Индекс проверяемого параметра.
		:type index: str
		"""

		Parameter = self.__Parameters[index]

		for CurrentPosition in self.__Command.positions:
			
			for CurrentFlag in CurrentPosition.flags:
				if Parameter in [CurrentFlag.name] + CurrentFlag.aliases:
					self.__ParametersLocks[index] = True
					self.__IsPositionLocked(CurrentPosition.name, exception = True)
					self.__PositionsLocks[CurrentPosition.name] = _ParsedFlag(CurrentFlag)
					return
			
			for CurrentKey in CurrentPosition.keys:
				if Parameter == CurrentKey.name or Parameter in CurrentKey.aliases:
					self.__ParametersLocks[index] = True
					if len(self.__Parameters) < index + 2 or self.__ParametersLocks[index + 1]: raise Exceptions.CLI.Terminalyzer.UnboundKey(Parameter)
					self.__ParametersLocks[index + 1] = True

					self.__IsPositionLocked(CurrentPosition.name, exception = True)
					Value = CurrentKey.type.value.parse(self.__Parameters[index + 1])
					self.__PositionsLocks[CurrentPosition.name] = _ParsedKey(CurrentKey, Value)
					return
				
			if CurrentPosition.argument and not self.__IsPositionLocked(CurrentPosition.name):
				Value = CurrentPosition.argument.type.value.parse(self.__Parameters[index])
				self.__ParametersLocks[index] = True
				self.__PositionsLocks[CurrentPosition.name] = _ParsedArgument(Value)
				return

	def __IsPositionLocked(self, position_name: str, exception: bool = False) -> bool:
		"""
		Проверяет, заблокирована ли позиция параметром.

		:param position_name: Имя позиции.
		:type position_name: str
		:param exception: Указывает, выбрасывать ли исключение в случае подтверждения блокировки позиции.
		:type exception: bool
		:raises Exceptions.CLI.Terminalyzer.MultipleParametersOnPosition: Позиция заблокирована.
		:return: Возвращает `True`, если позиция заблокирована и выброс исключения отключён.
		:rtype: bool
		"""

		if self.__PositionsLocks[position_name] and exception: raise Exceptions.CLI.Terminalyzer.MultipleParametersOnPosition(position_name)

		return bool(self.__PositionsLocks[position_name])

	def __ParseBasePositionParameters(self, index: str):
		"""
		Проверяет возможность заполнения базовой позиции остаточными параметрами.

		:param index: Индекс проверяемого параметра.
		:type index: str
		"""

		Parameter = self.__Parameters[index]
		BasePosition = self.__Command.base

		for CurrentFlag in BasePosition.flags:
			if Parameter in [CurrentFlag.name] + CurrentFlag.aliases:
				self.__ParametersLocks[index] = True
				self.__BaseParameters.append(_ParsedFlag(CurrentFlag))
				return
		
		for CurrentKey in BasePosition.keys:
			if Parameter == CurrentKey.name or Parameter in CurrentKey.aliases:
				self.__ParametersLocks[index] = True
				if len(self.__Parameters) < index + 2 or self.__ParametersLocks[index + 1]: raise Exceptions.CLI.Terminalyzer.UnboundKey(Parameter)
				self.__ParametersLocks[index + 1] = True
				Value = CurrentKey.type.value.parse(self.__Parameters[index + 1])
				self.__BaseParameters.append(_ParsedKey(CurrentKey, Value))
				return
			
		for CurrentArgument in BasePosition.arguments:
			Value = CurrentArgument.type.value.parse(self.__Parameters[index])
			self.__ParametersLocks[index] = True
			self.__BaseParameters.append(_ParsedArgument(Value))
			return

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, command: "Command", parameters: Iterable[str]):
		"""
		Парсер команды.

		:param command: Данные команды.
		:type command: Command
		:param parameters: Последовательность строковых параметров команды (не включает имя самой команды).
		:type parameters: Iterable[str]
		"""

		self.__Command = command
		self.__Parameters = tuple(parameters)

		self.__ParametersLocks = [False for _ in self.__Parameters]
		self.__PositionsLocks = {CurrentPosition.name: None for CurrentPosition in self.__Command.positions}
		self.__BaseParameters = list()

	def parse(self) -> ParsedCommandData:
		"""
		Разбирает параметры команды и типизирует значения.

		:return: Данные обработанной команды.
		:rtype: ParsedCommandData
		"""

		ParsedData = _ParsedCommandParameters()

		for Index in range(len(self.__Parameters)):
			if self.__ParametersLocks[Index]: continue
			self.__CatchParameterForPositions(Index)

		for Index in range(len(self.__Parameters)):
			if self.__ParametersLocks[Index]: continue
			self.__ParseBasePositionParameters(Index)

		for PositionName in self.__PositionsLocks: ParsedData.set_positional_parameter(PositionName, self.__PositionsLocks[PositionName])
		for Parameter in self.__BaseParameters: ParsedData.add_base_parameter(Parameter)

		self.__CheckImportantPositionsLocks()
		self.__CheckParametersCount()

		return ParsedCommandData(self.__Command.name, ParsedData)