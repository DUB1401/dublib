#==========================================================================================#
# >>>>> Terminalyzer <<<<< #
#==========================================================================================#
	
class IdenticalArguments(Exception):
	"""Исключение: попытка установки одинаковых аргументов на одну позицию."""

	def __init__(self, type_name: str):
		"""Исключение: попытка установки одинаковых аргументов на одну позицию."""

		self.__Message = f"Can't set same arguments \"{type_name}\" on position."
		super().__init__(self.__Message) 
			
	def __str__(self):
		return self.__Message

class IdenticalIndicators(Exception):
	"""Исключение: попытка установки одинаковых индикаторов ключей и флагов."""

	def __init__(self):
		"""Исключение: попытка установки одинаковых индикаторов ключей и флагов."""

		self.__Message = "Cannot set same indicators for keys and flags."
		super().__init__(self.__Message) 
			
	def __str__(self):
		return self.__Message

class InvalidParameterType(Exception):
	"""Исключение: неверное значение параметра."""

	def __init__(self, value: str, type_name: str):
		"""
		Исключение: неверное значение параметра.
			value – значение параметра;\n
			type_name – название ожидаемого типа.
		"""

		self.__Message = "\"" + value + "\" isn't \"" + type_name + "\"."
		super().__init__(self.__Message) 
			
	def __str__(self):
		return self.__Message
	
class InvalidPositionalArgumentTypes(Exception):
	"""Исключение: неверное значение аргумента."""

	def __init__(self, value: str, types_names: list[str]):
		"""
		Исключение: неверное значение аргумента.
			value – значение аргумента;\n
			types_names – список названий ожидаемых типов.
		"""

		self.__Message = "\"" + value + "\" isn't: " + ", ".join(types_names) + "."
		super().__init__(self.__Message) 
			
	def __str__(self):
		return self.__Message

class MutuallyExclusiveFlags(Exception):
	"""Исключение: активированы взаимоисключающие флаги."""

	def __init__(self, command: str):
		"""
		Исключение: активированы взаимоисключающие флаги.
			command – команда, вызвавшая исключение.
		"""

		self.__Message = "\"" + command + "\"."
		super().__init__(self.__Message) 
			
	def __str__(self):
		return self.__Message

class MutuallyExclusiveKeys(Exception):
	"""Исключение: активированы взаимоисключающие ключи."""

	def __init__(self, command: str):
		"""
		Исключение: активированы взаимоисключающие ключи.
			command – команда, вызвавшая исключение.
		"""

		self.__Message = "\"" + command + "\"."
		super().__init__(self.__Message) 
		
			
	def __str__(self):
		return self.__Message
	
class MutuallyExclusivePositions(Exception):
	"""Исключение: активированы разные позиции на одном слое."""

	def __init__(self, command: str): 
		"""
		Исключение: активированы разные позиции на одном слое.
			command – команда, вызвавшая исключение.
		"""

		self.__Message = "\"" + command + "\"."
		super().__init__(self.__Message) 
		
	def __str__(self):
		return self.__Message

class NotEnoughParameters(Exception):
	"""Исключение: недостаточно аргументов."""

	def __init__(self, command: str):
		"""
		Исключение: недостаточно аргументов.
			command – команда, вызвавшая исключение.
		"""

		self.__Message = "\"" + command + "\"."
		super().__init__(self.__Message) 

	def __str__(self):
		return self.__Message

class TooManyParameters(Exception):
	"""Исключение: слишком много аргументов."""

	def __init__(self, command: str):
		"""
		Исключение: слишком много аргументов.
			command – команда, вызвавшая исключение.
		"""

		self.__Message = "\"" + command + "\"."
		super().__init__(self.__Message) 
			
	def __str__(self):
		return self.__Message

class UnknownFlag(Exception):
	"""Исключение: неизвестный флаг."""

	def __init__(self, flag: str):
		"""
		Исключение: неизвестный флаг.
			flag – флаг.
		"""
		
		self.__Message = "\"" + flag + "\"."
		super().__init__(self.__Message) 
		
	def __str__(self):
		return self.__Message
	
class UnknownKey(Exception):
	"""Исключение: неизвестный ключ."""

	def __init__(self, key: str):
		"""
		Исключение: неизвестный ключ.
			key – ключ.
		"""
		
		self.__Message = "\"" + key + "\"."
		super().__init__(self.__Message) 
		
	def __str__(self):
		return self.__Message

class UnknownCommand(Exception):
	"""Исключение: неизвестная комманда."""

	def __init__(self, command: str):
		"""
		Исключение: неизвестная комманда.
			command – команда, вызвавшая исключение.
		"""
		
		self.__Message = "\"" + command + "\"."
		super().__init__(self.__Message) 
		
	def __str__(self):
		return self.__Message