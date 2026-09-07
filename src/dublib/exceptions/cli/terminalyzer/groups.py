class CommandModelOverridingError(Exception):
	"""Исключение: переопределение модели команды."""

	def __init__(self, command_name: str):
		"""
		Исключение: переопределение модели команды.

		:param command_name: Название команды.
		:type command_name: str
		"""

		super().__init__(command_name) 