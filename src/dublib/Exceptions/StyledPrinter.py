class DuplicatedStyles(Exception):
	"""
	Исключение: использованы оба способа указания стилей.
	"""

	# Конструктор: вызывается при обработке исключения.
	def __init__(self):
		"""
		Исключение: использованы оба способа указания стилей.
		"""
		
		# Добавление данных в сообщение об ошибке.
		self.__Message = "Use only StyledGroup() or arguments styles."
		# Обеспечение доступа к оригиналу наследованного свойства.
		super().__init__(self.__Message)
			
	# Преобразователь: представляет содержимое класса как строку.
	def __str__(self):
		return self.__Message