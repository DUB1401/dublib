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
	# >>>>> СВОЙСТВА ТОЛЬКО ДЛЯ ЧТЕНИЯ <<<<< #
	#==========================================================================================#

	@property
	def code(self) -> int:
		"""Код выполнения."""

		return self._Code

	@property
	def data(self) -> dict | None:
		"""Словарь дополнительных данных."""

		return self._Data

	@property
	def description(self) -> str | None:
		"""Краткое описание."""

		return self._Description
	
	@property
	def type(self) -> StatussesTypes:
		"""Тип отчёта."""

		return self._Type
	
	@property
	def value(self) -> str | None:
		"""Значение."""

		return self._Value

	#==========================================================================================#
	# >>>>> МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, code: int, description: str | None = None, value: str | None = None, data: dict | None = None, type: StatussesTypes = StatussesTypes.Normal):
		"""
		Отчёт о выполнении.
			code – код выполнения;
			description – краткое описание;
			value – значение;
			data – словарь дополнительных данных;
			type – тип отчёта.
		"""

		#---> Генерация динамичкских свойств.
		#==========================================================================================#
		# Код выполнения.
		self._Code = code
		# Краткое описание.
		self._Description = description
		# Зачение.
		self._Value = value
		# Словарь дополнительных данных.
		self._Data = data
		# Тип сообщения.
		self._Type = StatussesTypes.Normal

class ExecutionWarning(ExecutionStatus):
	"""Отчёт о предупреждении выполнения."""

	def __init__(self, code: int, description: str | None = None, value: str | None = None, data: dict | None = None):
		"""
		Отчёт о предупреждении выполнения.
			code – код выполнения;
			description – краткое описание;
			value – значение;
			data – словарь дополнительных данных.
		"""

		#---> Генерация динамичкских свойств.
		#==========================================================================================#
		# Тип сообщения.
		self._Type = StatussesTypes.Warning
		# Код выполнения.
		self._Code = code
		# Краткое описание.
		self._Description = description
		# Зачение.
		self._Value = value
		# Словарь дополнительных данных.
		self._Data = data

class ExecutionError(ExecutionStatus):
	"""Отчёт об ошибке выполнения."""

	def __init__(self, code: int, description: str | None = None, value: str | None = None, data: dict | None = None):
		"""
		Отчёт об ошибке выполнения.
			code – код выполнения;
			description – краткое описание;
			value – значение;
			data – словарь дополнительных данных.
		"""
		
		#---> Генерация динамичкских свойств.
		#==========================================================================================#
		# Код выполнения.
		self._Code = code
		# Краткое описание.
		self._Description = description
		# Зачение.
		self._Value = value
		# Словарь дополнительных данных.
		self._Data = data
		# Тип сообщения.
		self._Type = StatussesTypes.Error

class ExecutionCritical(ExecutionStatus):
	"""Отчёт о критической ошибке выполнения."""

	def __init__(self, code: int, description: str | None = None, value: str | None = None, data: dict | None = None):
		"""
		Отчёт о критической ошибке выполнения.
			code – код выполнения;
			description – краткое описание;
			value – значение;
			data – словарь дополнительных данных.
		"""

		#---> Генерация динамичкских свойств.
		#==========================================================================================#
		# Тип сообщения.
		self._Type = StatussesTypes.Critical
		# Код выполнения.
		self._Code = code
		# Краткое описание.
		self._Description = description
		# Зачение.
		self._Value = value
		# Словарь дополнительных данных.
		self._Data = data