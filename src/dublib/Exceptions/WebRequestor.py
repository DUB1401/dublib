class UserAgentRedefining(Exception):
	"""Исключение: переопределение заголовка User-Agent."""

	def __init__(self):
		"""Исключение: переопределение заголовка User-Agent."""

		self.__Message = "Use only set_user_agent() to manage \"User-Agent\" header."
		super().__init__(self.__Message)
			
	def __str__(self):
		return self.__Message