class UserAgentRedefining(Exception):
	"""Исключение: переопределение заголовка User-Agent."""

	def __init__(self):
		"""Исключение: переопределение заголовка User-Agent."""

		# Добавление данных в сообщение об ошибке.
		self.__Message = "Use only set_user_agent() to manage \"User-Agent\" header."
		# Обеспечение доступа к оригиналу наследованного конструктора.
		super().__init__(self.__Message)
			
	def __str__(self):
		return self.__Message