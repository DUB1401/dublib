#==========================================================================================#
# >>>>> StyledPrinter <<<<< #
#==========================================================================================#

class DuplicatedStyles(Exception):
	"""Исключение: использованы оба способа указания стилей."""

	def __init__(self):
		"""Исключение: использованы оба способа указания стилей."""
		
		self.__Message = "Use only StyledGroup() or arguments styles."
		super().__init__(self.__Message)
			
	def __str__(self):
		return self.__Message
	
#==========================================================================================#
# >>>>> Terminalyzer <<<<< #
#==========================================================================================#
	
class IdenticalIndicators(Exception):
	"""Исключение: попытка установки одинаковых индикаторов ключей и флагов."""

	def __init__(self):
		"""Исключение: попытка установки одинаковых индикаторов ключей и флагов."""

		self.__Message = "Cannot set same indicators for keys and flags."
		super().__init__(self.__Message) 
			
	def __str__(self):
		return self.__Message

class InvalidParameterType(Exception):
	"""Исключение: неверное значение аргумента."""

	def __init__(self, value: str, type_name: str):
		"""
		Исключение: неверное значение аргумента.
			value – значение аргумента;\n
			type_name – название ожидаемого типа.
		"""

		self.__Message = "\"" + value + "\" isn't \"" + type_name + "\"."
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