class IdenticalIndicators(Exception):
	"""
	Исключение: попытка установки одинаковых индикаторов ключей и флагов.
	"""

	def __init__(self):
		"""
		Исключение: попытка установки одинаковых индикаторов ключей и флагов.
		"""

		# Добавление данных в сообщение об ошибке.
		self.__Message = "Cannot set same indicators for keys and flags."
		# Обеспечение доступа к оригиналу наследованного свойства.
		super().__init__(self.__Message) 
			
	def __str__(self):
		return self.__Message

class InvalidArgumentType(Exception):
	"""
	Исключение: неверное значение аргумента.
	"""

	def __init__(self, value: str, type_name: str):
		"""
		Исключение: неверное значение аргумента.
			value – значение аргумента;
			type_name – название ожидаемого типа.
		"""

		# Добавление данных в сообщение об ошибке.
		self.__Message = "\"" + value + "\" isn't \"" + type_name + "\"."
		# Обеспечение доступа к оригиналу наследованного свойства.
		super().__init__(self.__Message) 
			
	def __str__(self):
		return self.__Message

class MutuallyExclusiveFlags(Exception):
	"""
	Исключение: активированы взаимоисключающие флаги.
	"""

	def __init__(self, command: str):
		"""
		Исключение: активированы взаимоисключающие флаги.
			command – команда, вызвавшая исключение.
		"""

		# Добавление данных в сообщение об ошибке.
		self.__Message = "\"" + command + "\"."
		# Обеспечение доступа к оригиналу наследованного свойства.
		super().__init__(self.__Message) 
			
	def __str__(self):
		return self.__Message

class MutuallyExclusiveKeys(Exception):
	"""
	Исключение: активированы взаимоисключающие ключи.
	"""

	def __init__(self, command: str):
		"""
		Исключение: активированы взаимоисключающие ключи.
			command – команда, вызвавшая исключение.
		"""

		# Добавление данных в сообщение об ошибке.
		self.__Message = "\"" + command + "\"."
		# Обеспечение доступа к оригиналу наследованного свойства.
		super().__init__(self.__Message) 
		
			
	def __str__(self):
		return self.__Message
	
class MutuallyExclusivePositions(Exception):
	"""
	Исключение: активированы разные позиции на одном слое.
	"""

	def __init__(self, command: str): 
		"""
		Исключение: активированы разные позиции на одном слое.
			command – команда, вызвавшая исключение.
		"""

		# Добавление данных в сообщение об ошибке.
		self.__Message = "\"" + command + "\"."
		# Обеспечение доступа к оригиналу наследованного свойства.
		super().__init__(self.__Message) 
		
	def __str__(self):
		return self.__Message

class NotEnoughArguments(Exception):
	"""
	Исключение: недостаточно аргументов.
	"""

	def __init__(self, command: str):
		"""
		Исключение: недостаточно аргументов.
			command – команда, вызвавшая исключение.
		"""

		# Добавление данных в сообщение об ошибке.
		self.__Message = "\"" + command + "\"."
		# Обеспечение доступа к оригиналу наследованного свойства.
		super().__init__(self.__Message) 

	def __str__(self):
		return self.__Message

class TooManyArguments(Exception):
	"""
	Исключение: слишком много аргументов.
	"""

	def __init__(self, command: str):
		"""
		Исключение: слишком много аргументов.
			command – команда, вызвавшая исключение.
		"""

		# Добавление данных в сообщение об ошибке.
		self.__Message = "\"" + command + "\"."
		# Обеспечение доступа к оригиналу наследованного свойства.
		super().__init__(self.__Message) 
			
	def __str__(self):
		return self.__Message

class UnknownCommand(Exception):
	"""
	Исключение: неизвестная комманда.
	"""

	def __init__(self, command: str):
		"""
		Исключение: неизвестная комманда.
			command – команда, вызвавшая исключение.
		"""
		
		# Добавление данных в сообщение об ошибке.
		self.__Message = "\"" + command + "\"."
		# Обеспечение доступа к оригиналу наследованного свойства.
		super().__init__(self.__Message) 
		
	def __str__(self):
		return self.__Message