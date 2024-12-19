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
	
class MutuallyExclusiveParameters(Exception):
	"""Исключение: переданы взаимоисключающие параметры."""

	def __init__(self, position: str, blocked_parameter: str, parameter: str): 
		"""
		Исключение: активированы разные позиции на одном слое.
			command – команда, вызвавшая исключение.
		"""

		self.__Message = f"\"{blocked_parameter}\" blocked \"{parameter}\" on position \"{position}\"."
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

class UnboundKey(Exception):
	"""Исключение: ключ не связан со значением."""

	def __init__(self, key: str):
		"""
		Исключение: ключ не связан со значением.
			key – ключ.
		"""
		
		self.__Message = "\"" + key + "\"."
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