from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Sequence, TypeVar, cast, overload

from .... import exceptions

if TYPE_CHECKING:
	from .definition import Command, _Flag, _Key
	
#==========================================================================================#
# >>>>> ПЕРЕМЕННЫЕ ТИПОВ <<<<< #
#==========================================================================================#

_EXPECTED_TYPE = TypeVar("_EXPECTED_TYPE", bool, float, int, Path, str, datetime)

#==========================================================================================#
# >>>>> ПРЕДСТАВЛЕНИЯ ОБРАБОТАННЫХ ПАРАМЕТРОВ <<<<< #
#==========================================================================================#

class _ParsedArgument:
	"""Представление обработанного аргумента."""

	@property
	def value(self) -> bool | float | int | Path | str | datetime:
		"""Значение ключа."""

		return self.__Value

	def __init__(self, value: bool | float | int | Path | str | datetime):
		"""
		Представление обработанного аргумента.

		:param value: Значение ключа.
		:type value: bool | float | int | Path | str | datetime
		"""

		self.__Value = value

class _ParsedFlag:
	"""Представление обработанного флага."""

	@property
	def aliases(self) -> list[str]:
		"""Список псевдонимов."""

		return self.__Flag.aliases.copy()

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

		return self.__Key.aliases.copy()

	@property
	def name(self) -> str:
		"""Имя ключа."""

		return self.__Key.name

	@property
	def value(self) -> bool | float | int | Path | str | datetime:
		"""Значение ключа."""

		return self.__Value

	def __init__(self, key: "_Key", value: bool | float | int | Path | str | datetime):
		"""
		Представление обработанного ключа.

		:param key: Ключ.
		:type key: _Key
		:param value: Значение ключа.
		:type value: bool | float | int | Path | str | datetime
		"""

		self.__Key = key
		self.__Value = value

class _ParsedCommandParameters:

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def arguments(self) -> tuple[_ParsedArgument, ...]:
		"""Последовательность представлений аргументов."""

		return self.__GetParametersType(_ParsedArgument)
	
	@property
	def flags(self) -> tuple[_ParsedFlag, ...]:
		"""Последовательность представлений флагов."""

		return self.__GetParametersType(_ParsedFlag)
	
	@property
	def keys(self) -> tuple[_ParsedKey, ...]:
		"""Последовательность представлений ключей."""

		return self.__GetParametersType(_ParsedKey)
	
	@property
	def positions(self) -> dict[str, _ParsedArgument | _ParsedFlag | _ParsedKey | None]:
		"""Словарь параеметров позиций."""

		return self.__Positions.copy()

	#==========================================================================================#
	# >>>>> ПРИВАТНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __GetParametersType(self, required_type: type[_ParsedArgument | _ParsedFlag | _ParsedKey]) -> tuple:
		"""
		Возвращает последовательность представлений параметров определённого типа.

		:param requred_type: Требуемый тип.
		:type requred_type: type[_ParsedArgument | _ParsedFlag | _ParsedKey]
		:return: Последовательность представлений параметров определённого типа.
		:rtype: tuple
		"""

		Result = []

		for CurrentSequence in (self.__Positions.values(), self.__BasePosition):
			for Parameter in CurrentSequence:
				if type(Parameter) is required_type: Result.append(Parameter)

		return tuple(Result)

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self):
		"""Данные о спаршенных параметрах команды."""

		self.__Positions: dict[str, _ParsedArgument | _ParsedFlag | _ParsedKey | None] = {}
		self.__ImportantPositions: list[str] = []
		self.__BasePosition: list[_ParsedArgument | _ParsedFlag | _ParsedKey] = []

	def add_base_parameter(self, parameter: _ParsedArgument | _ParsedFlag | _ParsedKey):
		"""
		Добавляет представление параметра на базовую позицию.

		:param parameter: Представление параметра.
		:type parameter: _ParsedArgument | _ParsedFlag | _ParsedKey
		"""

		self.__BasePosition.append(parameter)

	def is_position_important(self, position_name: str) -> bool:
		"""
		Проверяет, описана ли позиция как обязательная.

		:param position_name: Имя позиции.
		:type position_name: str
		:return: Возвращает `True`, если позиция обязательна для заполнения.
		:rtype: bool
		:raises KeyError: Позиция не найдена.
		"""

		return position_name in self.__ImportantPositions

	def set_positional_parameter(self, position_name: str, parameter: _ParsedArgument | _ParsedFlag | _ParsedKey, is_important: bool):
		"""
		Устанавливает представление параметра на позицию.

		:param position_name: Имя позиции.
		:type position_name: str
		:param parameter: Представление параметра.
		:type parameter: _ParsedArgument | _ParsedFlag | _ParsedKey
		:param is_important: Состояние: обязательная ли позиция.
		:type is_important: bool
		:raises Exceptions.CLI.Terminalyzer.MultipleParametersOnPosition: Попытка установки нескольких параметров для одной позиции.
		"""

		if position_name in self.__Positions:
			raise exceptions.cli.terminalyzer.MultipleParametersOnPosition(position_name)
		
		self.__Positions[position_name] = parameter

		if is_important:
			self.__ImportantPositions.append(position_name)

#==========================================================================================#
# >>>>> ДАННЫЕ ОБРАБОТАННОЙ КОМАНДЫ <<<<< #
#==========================================================================================#

class ParsedCommandData:
	"""Данные обработанной команды."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def arguments(self) -> tuple[bool | float | int | str | Path | datetime, ...]:
		"""Последовательность значений аргументов."""

		return tuple(Element.value for Element in self.__ParsedData.arguments)
	
	@property
	def flags(self) -> tuple[_ParsedFlag, ...]:
		"""Последовательность активированных флагов."""

		return self.__ParsedData.flags
	
	@property
	def keys(self) -> dict[str, bool | float | int | Path | str | datetime | None]:
		"""Cловарь имён активированных ключей и их значений."""

		return {CurrentKey.name: CurrentKey.value for CurrentKey in self.__ParsedData.keys}
	
	@property
	def name(self) -> str:
		"""Название команды."""

		return self.__Name

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, name: str, parsed_data: _ParsedCommandParameters):

		self.__Name: str = name
		self.__ParsedData: _ParsedCommandParameters = parsed_data

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
	
	@overload
	def get_key_value(self, key: str, expected_type: type[_EXPECTED_TYPE], exception: bool = False) -> _EXPECTED_TYPE | None: ...
	@overload
	def get_key_value(self, key: str, expected_type: None = None, exception: bool = False) -> bool | float | int | Path | str | datetime | None: ...

	def get_key_value(self, key: str, expected_type: type | None = None, exception: bool = False) -> bool | float | int | Path | str | datetime | None:
		"""
		Возвращает значение активированного ключа.

		:param key: Название ключа.
		:type key: str
		:param expected_type: Ожидаемый тип значения. Если тип не соответствует, будет выброшено исключение `TypeError`. Проверяются только значения, отличные от `None`.
		:type expected_type: type[bool | float | int | Path | str | datetime]
		:param exception: Указывает, нужно ли выбрасывать исключение при отсутствии ключа.
		:type exception: bool
		:return: Значение ключа или `None` при отсутствующем ключе.
		:rtype: bool | float | int | Path | str | datetime | None
		:raises KeyError: Ключ не найден. Отключается параметром `exception`.
		:raises TypeError: Ожидается другой тип данных.
		"""

		ValueToReturn: bool | float | int | Path | str | datetime | None = None
		IsKeyFound: bool = False

		for CurrentKey in self.__ParsedData.keys:
			if key == CurrentKey.name or key in CurrentKey.aliases:
				ValueToReturn = CurrentKey.value
				IsKeyFound = True
				break

		if not IsKeyFound:
			if exception:
				raise KeyError(key)
			else: 
				return None
		
		if expected_type and ValueToReturn is not None:
			ReturnedType = type(ValueToReturn)
			if not isinstance(ReturnedType, expected_type):
				raise TypeError(f"Expected \"{expected_type}\", but on key {ReturnedType}.")

		return ValueToReturn

	def get_position_named_parameter(self, position_name: str) -> _ParsedFlag | _ParsedKey | None:
		"""
		Возвращает именованный параметр позиции (флаг или ключ).

		:param position_name: Имя позиции.
		:type position_name: str
		:return: Именованный параметр позиции или `None` при пустой позиции.
		:rtype: _ParsedArgument | _ParsedFlag | _ParsedKey | None
		:raises KeyError: Позиция не обнаружена.
		:raises TypeError: На позиции находится аргумент, а не именованный параметр.
		"""

		Parameter = self.get_position_parameter(position_name)

		if isinstance(Parameter, _ParsedArgument):
			raise TypeError("Expected named parameter (flag or key), found argument.")
		
		return Parameter

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

	def get_important_position_parameter(self, position_name: str) -> _ParsedArgument | _ParsedFlag | _ParsedKey:
		"""
		Возвращает параметр обязательной позиции.

		:param position_name: Имя позиции.
		:type position_name: str
		:return: Параметр обязательной позиции.
		:rtype: _ParsedArgument | _ParsedFlag | _ParsedKey
		"""

		Parameter = self.get_position_parameter(position_name)

		if Parameter is None:
			raise exceptions.cli.terminalyzer.ImportantPositionEmpty(position_name)

		return Parameter

	def get_important_position_named_parameter(self, position_name: str) -> _ParsedFlag | _ParsedKey:
		"""
		Возвращает именованный параметр обязательной позиции (флаг или ключ).

		:param position_name: Имя позиции.
		:type position_name: str
		:return: Именованный параметр обязательной позиции.
		:rtype: _ParsedFlag | _ParsedKey
		"""

		Parameter = self.get_important_position_parameter(position_name)

		if isinstance(Parameter, _ParsedArgument):
			raise TypeError("Expected named parameter (flag or key), found argument.")

		return Parameter

	@overload
	def get_important_position_value(self, position_name: str, expected_type: type[_EXPECTED_TYPE]) -> _EXPECTED_TYPE: ...
	@overload
	def get_important_position_value(self, position_name: str, expected_type: None = None) -> bool | float | int | Path | str | datetime: ...

	def get_important_position_value(self, position_name: str, expected_type: type[_EXPECTED_TYPE] | None = None) -> bool | float | int | Path | str | datetime:
		"""
		Для аргументов и ключей на позиции возвращает значение, для флагов – основое имя флага. Позиция не может быть пустой.

		:param position_name: Имя позиции.
		:type position_name: str
		:param expected_type: Ожидаемый тип значения.
		:type expected_type: type[_EXPECTED_TYPE]
		:return: Значение позиции или основное имя флага.
		:rtype: bool | float | int | Path | str | datetime
		:raises Exceptions.CLI.Terminalyzer.ImportantPositionEmpty: Обязательная позиция пуста.
		:raises Exceptions.CLI.Terminalyzer.PositionOptional: Позиция не обязательна.
		"""

		if not self.__ParsedData.is_position_important(position_name):
			raise exceptions.cli.terminalyzer.PositionOptional(position_name)

		ValueToReturn = self.get_position_value(position_name, expected_type)

		if ValueToReturn is None:
			raise exceptions.cli.terminalyzer.ImportantPositionEmpty(position_name)

		return ValueToReturn

	@overload
	def get_position_value(self, position_name: str, expected_type: type[_EXPECTED_TYPE]) -> _EXPECTED_TYPE | None: ...
	@overload
	def get_position_value(self, position_name: str, expected_type: None = None) -> bool | float | int | Path | str | datetime | None: ...

	def get_position_value(self, position_name: str, expected_type: type | None = None) -> bool | float | int | Path | str | datetime | None:
		"""
		Для аргументов и ключей на позиции возвращает значение, для флагов – основное название флага.

		:param position_name: Имя позиции.
		:type position_name: str
		:param expected_type: Ожидаемый тип значения.
		:type expected_type: type[bool | float | int | Path | str | datetime] | None
		:return: Параметр позиции или `None` при пустой позиции. Для флага возвращает основное имя флага.
		:rtype: bool | float | int | Path | str | datetime | None
		:raises KeyError: Позиция не обнаружена.
		:raises TypeError: Позиция не пуста и ожидается другой тип данных.
		"""

		ParsedParameter = self.get_position_parameter(position_name)
		ValueToReturn: bool | float | int | Path | str | datetime | None = None

		if not ParsedParameter:
			ValueToReturn = None
		elif type(ParsedParameter) is _ParsedFlag:
			ValueToReturn = ParsedParameter.name
		else:
			ParsedParameter = cast(_ParsedArgument | _ParsedKey, ParsedParameter)
			ValueToReturn = ParsedParameter.value

		if expected_type:
			ReturnedType = type(ValueToReturn)
			if ReturnedType is not expected_type and ValueToReturn is not None:
				raise TypeError(f"Expected \"{expected_type}\", but on position {ReturnedType}.")
			
		return ValueToReturn

	def to_dict(self) -> dict:
		"""
		Возвращает словарное представление объекта.

		:return: Словарное представление объекта.
		:rtype: dict
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

class CommandParser:
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
				raise exceptions.cli.terminalyzer.ImportantPositionEmpty(CurrentPosition.name)

	def __CheckParametersCount(self):
		"""
		Проверяет соответвтсие количества параметров.
		
		:raises TooManyParameters: Слишком много параметров.
		:raises NotEnoughParameters: Недостаточно параметров.
		"""
		
		ParametersCount = len(self.__Parameters)
		if ParametersCount > self.__Command.max_parameters_count: raise exceptions.cli.terminalyzer.TooManyParameters(self.__Command.max_parameters_count, ParametersCount)
		if ParametersCount < self.__Command.min_parameters_count: raise exceptions.cli.terminalyzer.NotEnoughParameters(self.__Command.min_parameters_count, ParametersCount)

	def __CheckUnboundParameters(self):
		"""
		Проверяет, все ли параметры в команде использованы.

		:raises UnboundParameter: Параметр не используется.
		"""

		if False in self.__ParametersLocks:
			UnboundParameterIndex: int = self.__ParametersLocks.index(False)
			Parameter: str = self.__Parameters[UnboundParameterIndex]
			raise exceptions.cli.terminalyzer.UnboundParameter(Parameter)

	#==========================================================================================#
	# >>>>> ПРИВАТНЫЕ МЕТОДЫ ПАРСИНГА <<<<< #
	#==========================================================================================#

	def __CatchParameterForPositions(self, index: int):
		"""
		Поочерёдно проверяет позиции и пытается заполнить их параметрами соответствующего типа.

		:param index: Индекс проверяемого параметра.
		:type index: int
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
					if len(self.__Parameters) < index + 2 or self.__ParametersLocks[index + 1]: raise exceptions.cli.terminalyzer.UnboundKey(Parameter)
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

		if self.__PositionsLocks[position_name] and exception: raise exceptions.cli.terminalyzer.MultipleParametersOnPosition(position_name)

		return bool(self.__PositionsLocks[position_name])

	def __ParseBasePositionParameters(self, index: int):
		"""
		Проверяет возможность заполнения базовой позиции остаточными параметрами.

		:param index: Индекс проверяемого параметра.
		:type index: int
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
				if len(self.__Parameters) < index + 2 or self.__ParametersLocks[index + 1]: raise exceptions.cli.terminalyzer.UnboundKey(Parameter)
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

	def __init__(self, command: "Command", parameters: Sequence[str]):
		"""
		Парсер команды.

		:param command: Данные команды.
		:type command: Command
		:param parameters: Последовательность строковых параметров команды (не включает имя самой команды).
		:type parameters: Sequence[str]
		"""

		self.__Command = command
		self.__Parameters: tuple[str, ...] = tuple(parameters)

		self.__ParametersLocks: list[bool] = [False for _ in self.__Parameters]
		self.__PositionsLocks: dict = {CurrentPosition.name: None for CurrentPosition in self.__Command.positions}
		self.__BaseParameters: list = []

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

		for PositionName in self.__PositionsLocks:
			ParsedData.set_positional_parameter(PositionName, self.__PositionsLocks[PositionName], self.__Command.get_position(PositionName).is_important)

		for Parameter in self.__BaseParameters:
			ParsedData.add_base_parameter(Parameter)

		self.__CheckImportantPositionsLocks()
		self.__CheckParametersCount()
		self.__CheckUnboundParameters()

		return ParsedCommandData(self.__Command.name, ParsedData)