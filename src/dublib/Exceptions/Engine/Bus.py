class KeyNotAllowed(Exception):
	"""Исключение: ключ не может быть использован."""

	def __init__(self):
		"""Исключение: ключ не может быть использован."""

		super().__init__("Key isn't allowed by rule.")

class ValueNotInintialized(Exception):
	"""Исключение: значение не инициализировано."""

	def __init__(self):
		"""Исключение: значение не инициализировано."""

		super().__init__("Enabled protection rule to value initialization.")