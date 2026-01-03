class IncorrectUserToUpdate(Exception):
	"""Исключение: использование данных другого пользователя для обновления."""

	def __init__(self, current_id: int, given_id: int):
		"""Исключение: использование данных другого пользователя для обновления."""

		super().__init__(f"Current user is {current_id}, but given {given_id}.")

class RefreshingBlocked(Exception):
	"""Исключение: считывание данных из локального файла заблокировано."""

	def __init__(self):
		"""Исключение: считывание данных из локального файла заблокировано."""

		super().__init__("While saving suppressed refreshing is blocked.") 

class SavingQueueBlocked(Exception):
	"""Исключение: очередь сохранения заблокирована."""

	def __init__(self):
		"""Исключение: очередь сохранения заблокирована."""

		super().__init__("Saving queue disabled. If task remained they will be completed.") 