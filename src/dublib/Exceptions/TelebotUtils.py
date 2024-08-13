class IncorrectUserToUpdate(Exception):
	"""Исключение: использование данных другого пользователя для обновления."""

	def __init__(self):
		"""Исключение: использование данных другого пользователя для обновления."""

		self.__Message = "Current user ID and ID in updating method differ."
		super().__init__(self.__Message) 
			
	def __str__(self):
		return self.__Message