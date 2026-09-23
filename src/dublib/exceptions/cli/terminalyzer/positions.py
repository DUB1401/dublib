class EmptyPositionError(Exception):
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

class ImportantPositionEmptyError(Exception):
	"""Исключение: для обязательной позиции не задан параметр."""

	def __init__(self, position_name: str):
		"""
		Исключение: для обязательной позиции не задан параметр.

		:param position_name: Имя позиции.
		:type position_name: str
		"""

		super().__init__(position_name) 

class MultipleParametersOnPositionError(Exception):
	"""Исключение: попытка установить несколько параметров для одной позиции."""

	def __init__(self, position_name: str): 
		"""
		Исключение: попытка установить несколько параметров для одной позиции.

		:param position_name: Название позиции.
		:type position_name: str
		"""

		super().__init__(f"On position \"{position_name}\" set more than 1 parameter.") 

class PositionAlreadyExistsError(Exception):
	"""Исключение: позиция уже существует."""

	def __init__(self, position_name: str):
		"""
		Исключение: позиция уже существует.

		:param position_name: Имя позиции.
		:type position_name: str
		"""

		super().__init__(position_name) 

class PositionDescriptionOverridingError(Exception):
	"""Исключение: переопределение описания позиции."""

	def __init__(self, command_name: str, position_name: str):
		"""
		Исключение: переопределение описания позиции.

		:param command_name: Имя команды.
		:type command_name: str
		:param position_name: Имя позиции.
		:type position_name: str
		"""

		super().__init__(f"Parameter overrides description for position \"{command_name}\" in model \"{position_name}\".") 

class PositionNotFoundError(Exception):
	"""Исключение: позиция не найдена."""

	def __init__(self, position_name: str):
		"""
		Исключение: позиция не найдена.

		:param position_name: Имя позиции.
		:type position_name: str
		"""

		super().__init__(position_name)

class PositionOptionalError(Exception):
	"""Исключение: позиция является необязательной."""

	def __init__(self, position_name: str):
		"""
		Исключение: позиция является необязательной.

		:param position_name: Имя позиции.
		:type position_name: str
		"""

		super().__init__(position_name) 
