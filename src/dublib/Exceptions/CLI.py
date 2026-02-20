#==========================================================================================#
# >>>>> Terminalyzer <<<<< #
#==========================================================================================#
	
class IdenticalArguments(Exception):
	"""Исключение: попытка установки нескольких аргументов одинаковых типов на одну позицию."""

	def __init__(self, type_name: str):
		"""
		Исключение: попытка установки нескольких аргументов одинаковых типов на одну позицию.

		:param type_name: Название типа аргумента.
		:type type_name: str
		"""

		super().__init__(f"Can't set same arguments \"{type_name}\" on position.") 

class IdenticalIndicators(Exception):
	"""Исключение: попытка установки одинаковых индикаторов ключей и флагов."""

	def __init__(self):
		"""Исключение: попытка установки одинаковых индикаторов ключей и флагов."""

		super().__init__("Cannot set same indicators for keys and flags.") 

class InvalidParameterType(Exception):
	"""Исключение: значение параметра не соответсвует ожидаемому типу."""

	def __init__(self, value: str, type_name: str):
		"""
		Исключение: значение параметра не соответсвует ожидаемому типу.

		:param value: Значение параметра.
		:type value: str
		:param type_name: Название ожидаемого типа.
		:type type_name: str
		"""

		super().__init__(f"\"{value}\" isn't \"{type_name}\".") 
	
class MutuallyExclusiveParameters(Exception):
	"""Исключение: переданы взаимоисключающие параметры."""

	def __init__(self, position: str, blocked_parameter: str, parameter: str): 
		"""
		Исключение: переданы взаимоисключающие параметры.

		:param position: Название позиции.
		:type position: str
		:param blocked_parameter: Блокирующий параметр.
		:type blocked_parameter: str
		:param parameter: Обрабатываемый параметр.
		:type parameter: str
		"""

		super().__init__(f"\"{blocked_parameter}\" blocked \"{parameter}\" on position \"{position}\".") 

class NotEnoughParameters(Exception):
	"""Исключение: недостаточно параметров."""

	def __init__(self, command: str):
		"""
		Исключение: недостаточно параметров.

		:param command: Все параметры команды через пробел.
		:type command: str
		"""

		super().__init__(f"\"{command}\".") 

class TooManyParameters(Exception):
	"""Исключение: слишком много параметров."""

	def __init__(self, command: str):
		"""
		Исключение: слишком много параметров.

		:param command: Все параметры команды через пробел.
		:type command: str
		"""

		super().__init__(f"\"{command}\".") 

class UnboundKey(Exception):
	"""Исключение: ключ не связан со значением."""

	def __init__(self, key: str):
		"""
		Исключение: ключ не связан со значением.

		:param key: Название ключа.
		:type key: str
		"""
		
		super().__init__(f"\"{key}\".") 

class UnknownFlag(Exception):
	"""Исключение: неизвестный флаг."""

	def __init__(self, flag: str):
		"""
		Исключение: неизвестный флаг.

		:param flag: Название флага.
		:type flag: str
		"""
		
		super().__init__(f"\"{flag}\".") 
	
class UnknownKey(Exception):
	"""Исключение: неизвестный ключ."""

	def __init__(self, key: str):
		"""
		Исключение: неизвестный ключ.

		:param key: Название ключа.
		:type key: str
		"""
		
		super().__init__(f"\"{key}\".") 

class UnknownCommand(Exception):
	"""Исключение: неизвестная комманда."""

	def __init__(self, command: str):
		"""
		Исключение: неизвестная комманда.

		:param command: Название команды.
		:type command: str
		"""
		
		super().__init__(f"\"{command}\".") 