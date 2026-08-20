from datetime import datetime

class AuthorizationRedefining(Exception):
	"""Исключение: переопределение заголовка _Authorization_."""

	def __init__(self):
		"""Исключение: переопределение заголовка _Authorization_"""

		super().__init__("Generate \"Authorization\" by headers subsystem.")

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
	"""Исключение: переопределение заголовков _User-Agent_ или _Sec-CH-*_."""

	def __init__(self):
		"""Исключение: переопределение заголовков _User-Agent_ или _Sec-CH-*_."""

		super().__init__("Generate \"User-Agent\" and \"Sec-CH-*\" by headers subsystem.")