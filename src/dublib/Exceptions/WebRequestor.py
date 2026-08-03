class HeaderRedefining(Exception):
	"""Исключение: переопределение заголовка."""

	def __init__(self, header: str):
		"""
		Исключение: переопределение заголовка.

		:param header: Заголовок.
		:type header: str
		"""

		super().__init__(header)

class UserAgentRedefining(Exception):
	"""Исключение: переопределение заголовка User-Agent."""

	def __init__(self):
		"""Исключение: переопределение заголовка User-Agent."""

		super().__init__("Use only set_user_agent() to manage \"User-Agent\" header.")