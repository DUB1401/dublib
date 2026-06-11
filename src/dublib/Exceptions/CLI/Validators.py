class ValidationError(Exception):
	"""Исключение: ошибка приведения строки к определённому типу."""

	def __init__(self, value: str, target_type: type):
		"""
		Исключение: ошибка приведения строки к определённому типу.

		:param value: Значение.
		:type value: str
		:param target_type: Тип, к которому происходило приведение.
		:type target_type: type
		"""

		target_type = target_type.__name__.split("_", maxsplit = 1)[-1]

		super().__init__(f"Unable convert \"{value}\" to \"{target_type}\" type.")