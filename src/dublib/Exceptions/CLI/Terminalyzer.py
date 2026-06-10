#==========================================================================================#
# >>>>> ИСКЛЮЧЕНИЯ ВАЛИДАТОРА <<<<< #
#==========================================================================================#

class EmptyPosition(Exception):
	"""Исключение: для позиции не описан ни один параметр."""

	def __init__(self, command_name: str, position: str):
		"""
		Исключение: для позиции не описан ни один параметр.

		:param command_name: Имя команды.
		:type command_name: str
		:param position: Имя позиции.
		:type position: str
		"""

		super().__init__(f"Position \"{position}\" on command \"{command_name}\".") 

class MultipleCommandDefinition(Exception):
	"""Исключение: множественное определение команды."""

	def __init__(self, command: str):
		"""
		Исключение: множественное определение команды.

		:param command: Название команды.
		:type command: str
		"""

		super().__init__(command) 

#==========================================================================================#
# >>>>> ИСКЛЮЧЕНИЯ ВРЕМЕНИ ВЫПОЛНЕНИЯ <<<<< #
#==========================================================================================#

class ImportantPositionEmpty(Exception):
	"""Исключение: для обязательной позиции не задан параметр."""

	def __init__(self, position: str):
		"""
		Исключение: для обязательной позиции не задан параметр.

		:param position: Имя позиции.
		:type position: str
		"""

		super().__init__(position) 

class MultipleParametersOnPosition(Exception):
	"""Исключение: попытка установить несколько параметров для одной позиции."""

	def __init__(self, position_name: str): 
		"""
		Исключение: попытка установить несколько параметров для одной позиции.

		:param position_name: Название позиции.
		:type position_name: str
		"""

		super().__init__(f"On positioin \"{position_name}\" setted more than 1 parameter.") 

class NotEnoughParameters(Exception):
	"""Исключение: недостаточно параметров."""

	def __init__(self, minimal: int, given: int):
		"""
		Исключение: недостаточно параметров.

		:param minimal: Минимальное количество параметров команды.
		:type minimal: int
		:param given: Переданное количество параметров.
		:type given: int
		"""

		super().__init__(f"Minimal parameters count is {minimal}. Given {given}.") 

class TooManyParameters(Exception):
	"""Исключение: слишком много параметров."""

	def __init__(self, maximal: int, given: int):
		"""
		Исключение: слишком много параметров.

		:param maximal: Максимальное количество параметров команды.
		:type maximal: int
		:param given: Переданное количество параметров.
		:type given: int
		"""

		super().__init__(f"Maximal parameters count is {maximal}. Given {given}.") 

class UnboundKey(Exception):
	"""Исключение: ключ не связан со значением."""

	def __init__(self, key: str):
		"""
		Исключение: ключ не связан со значением.

		:param key: Название ключа.
		:type key: str
		"""
		
		super().__init__(f"\"{key}\".") 