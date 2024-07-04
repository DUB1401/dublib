import enum

#==========================================================================================#
# >>>>> ВСПОМОГАТЕЛЬНЫЕ СТРУКТУРЫ ДАННЫХ <<<<< #
#==========================================================================================#

class StatussesTypes(enum.Enum):
	Normal = ""
	Warning = "warning"
	Error = "error"
	Critical = "critical"

#==========================================================================================#
# >>>>> ОСНОВНЫЕ КЛАССЫ <<<<< #
#==========================================================================================#

class ExecutionStatus:
	"""Отчёт о выполнении."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def code(self) -> int:
		"""Код выполнения."""

		return self._Code

	@property
	def data(self) -> any:
		"""Данные отладки."""

		return self._Data

	@property
	def message(self) -> str | None:
		"""Сообщение."""

		return self._Message
	
	@property
	def type(self) -> StatussesTypes:
		"""Тип отчёта."""

		return self._Type
	
	@property
	def value(self) -> any:
		"""Значение."""

		return self._Value

	#==========================================================================================#
	# >>>>> МЕТОДЫ УСТАНОВКИ ЗНАЧЕНИЙ СВОЙСТВ <<<<< #
	#==========================================================================================#

	@code.setter
	def code(self, new_code: int):
		"""Код выполнения."""

		self._Code = int(new_code)

	@data.setter
	def data(self, new_data):
		"""Данные отладки."""

		self._Data = new_data

	@message.setter
	def message(self, new_message):
		"""Сообщение."""

		self._Message = str(new_message) if new_message else None
	
	@type.setter
	def type(self, new_type: StatussesTypes):
		"""Тип отчёта."""

		self._Type = new_type
	
	@value.setter
	def value(self, new_value: any):
		"""Значение."""

		self._Value = new_value

	#==========================================================================================#
	# >>>>> МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, code: int, message: str | None = None, value: str | None = None, data: any = None, type: StatussesTypes = StatussesTypes.Normal):
		"""
		Отчёт о выполнении.
			code – код выполнения;
			message – сообщение;
			value – значение;
			data – данные отладки;
			type – тип отчёта.
		"""

		#---> Генерация динамичкских свойств.
		#==========================================================================================#
		# Код выполнения.
		self._Code = code
		# Сообщение.
		self._Message = message
		# Зачение.
		self._Value = value
		# Словарь дополнительных данных.
		self._Data = data
		# Тип сообщения.
		self._Type = StatussesTypes.Normal

class ExecutionWarning(ExecutionStatus):
	"""Отчёт о предупреждении выполнения."""

	def __init__(self, code: int, message: str | None = None, value: str | None = None, data: any = None):
		"""
		Отчёт о предупреждении выполнения.
			code – код выполнения;
			message – сообщение;
			value – значение;
			data – данные отладки.
		"""

		#---> Генерация динамичкских свойств.
		#==========================================================================================#
		# Тип сообщения.
		self._Type = StatussesTypes.Warning
		# Код выполнения.
		self._Code = code
		# Сообщение.
		self._Message = message
		# Зачение.
		self._Value = value
		# Словарь дополнительных данных.
		self._Data = data

class ExecutionError(ExecutionStatus):
	"""Отчёт об ошибке выполнения."""

	def __init__(self, code: int, message: str | None = None, value: str | None = None, data: any = None):
		"""
		Отчёт об ошибке выполнения.
			code – код выполнения;
			message – сообщение;
			value – значение;
			data – данные отладки.
		"""
		
		#---> Генерация динамичкских свойств.
		#==========================================================================================#
		# Код выполнения.
		self._Code = code
		# Сообщение.
		self._Message = message
		# Зачение.
		self._Value = value
		# Словарь дополнительных данных.
		self._Data = data
		# Тип сообщения.
		self._Type = StatussesTypes.Error

class ExecutionCritical(ExecutionStatus):
	"""Отчёт о критической ошибке выполнения."""

	def __init__(self, code: int, message: str | None = None, value: str | None = None, data: any = None):
		"""
		Отчёт о критической ошибке выполнения.
			code – код выполнения;
			message – сообщение;
			value – значение;
			data – данные отладки.
		"""

		#---> Генерация динамичкских свойств.
		#==========================================================================================#
		# Тип сообщения.
		self._Type = StatussesTypes.Critical
		# Код выполнения.
		self._Code = code
		# Краткое описание.
		self._Message = message
		# Зачение.
		self._Value = value
		# Словарь дополнительных данных.
		self._Data = data