class ConfigRequired(Exception):
	"""
	Исключение: не задана конфигурация.
	"""

	# Конструктор: вызывается при обработке исключения.
	def __init__(self):
		"""
		Исключение: не задана конфигурация.
		"""

		# Добавление данных в сообщение об ошибке.
		self.__Message = "Any requests library config required."
		# Обеспечение доступа к оригиналу наследованного свойства.
		super().__init__(self.__Message)
			
	# Преобразователь: представляет содержимое класса как строку.
	def __str__(self):
		return self.__Message

class SeleniumRequired(Exception):
	"""
	Исключение: не инициализирован или не установлен Selenium.
	"""

	# Конструктор: вызывается при обработке исключения.
	def __init__(self):
		"""
		Исключение: не инициализирован или не установлен Selenium.
		"""

		# Добавление данных в сообщение об ошибке.
		self.__Message = "Selenium webdriver initialization required or lib not installed."
		# Обеспечение доступа к оригиналу наследованного свойства.
		super().__init__(self.__Message)
			
	# Преобразователь: представляет содержимое класса как строку.
	def __str__(self):
		return self.__Message