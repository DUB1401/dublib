from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from ....cli.terminalyzer.commands.identificator import CommandIdentificator

class KeyMissingError(Exception):
	"""Исключение: ключ не активирован."""

	def __init__(self, key: str):
		"""
		Исключение: ключ не активирован.

		:param key: Имя ключа.
		:type key: str
		"""

		super().__init__(key) 

class NamedParameterMissingInModelError(Exception):
	"""Исключение: именованный параметр отсутствует в модели команды."""

	def __init__(self, command_name: str, parameter_name: str):
		"""
		Исключение: именованный параметр отсутствует в модели команды.

		:param command_name: Имя команды.
		:type command_name: str
		:param parameter_name: Имя параметра.
		:type parameter_name: str
		"""

		super().__init__(f"Named parameter \"{parameter_name}\" missing in model \"{command_name}\".") 

class NotEnoughParametersError(Exception):
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

class TooManyParametersError(Exception):
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

class UnboundKeyError(Exception):
	"""Исключение: ключ не связан со значением."""

	def __init__(self, key: str):
		"""
		Исключение: ключ не связан со значением.

		:param key: Название ключа.
		:type key: str
		"""
		
		super().__init__(f"\"{key}\".")

class UnboundParameterError(Exception):
	"""Исключение: параметр не используется."""

	def __init__(self, parameter: str):
		"""
		Исключение: параметр не используется.

		:param parameter: Параметр.
		:type parameter: str
		"""

		super().__init__(parameter)

class UnfamiliarParametersError(Exception):
	"""Исключение: обрабатываемые параметры не соответствуют идентификатору модели."""

	def __init__(self, identificator: "CommandIdentificator"):
		"""
		Исключение: обрабатываемые параметры не соответствуют идентификатору модели.

		:param identificator: Идентификатор команды.
		:type identificator: CommandIdentificator
		"""

		super().__init__(identificator.as_str()) 