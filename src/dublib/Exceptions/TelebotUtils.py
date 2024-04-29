class UpdateByOtherUser(Exception):
	"""Исключение: использование данных другого пользователя для обновления."""

	def __init__(self):
		"""Исключение: использование данных другого пользователя для обновления."""

		# Добавление данных в сообщение об ошибке.
		self.__Message = "Current user ID and ID in updating method differ."
		# Обеспечение доступа к оригиналу наследованного свойства.
		super().__init__(self.__Message) 
			
	def __str__(self):
		return self.__Message