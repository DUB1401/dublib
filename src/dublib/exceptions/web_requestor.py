from datetime import datetime

class HeaderRedefining(Exception):
	"""Исключение: переопределение заголовка."""

	def __init__(self, header: str):
		"""
		Исключение: переопределение заголовка.

		:param header: Заголовок.
		:type header: str
		"""

		super().__init__(header)

class TokenExpired(Exception):
	"""Исключение: токен устарел."""

	def __init__(self, expiration_date: datetime):
		"""
		Исключение: токен устарел.

		:param expiration_date: Дата устаревания токена.
		:type expiration_date: datetime
		"""

		super().__init__(expiration_date.strftime("%Y-%m-%d %H:%M:%S"))

class UserAgentRedefining(Exception):
	"""Исключение: переопределение заголовка User-Agent."""

	def __init__(self):
		"""Исключение: переопределение заголовка User-Agent."""

		super().__init__("Use only set_user_agent() to manage \"User-Agent\" header.")