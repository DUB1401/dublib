class UserAgentRedefining(Exception):
	"""Исключение: переопределение заголовка User-Agent."""

	def __init__(self):
		"""Исключение: переопределение заголовка User-Agent."""

		super().__init__("Use only set_user_agent() to manage \"User-Agent\" header.")