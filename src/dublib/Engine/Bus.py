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
	def data(self) -> dict:
		"""Копия словаря дополнительных данных."""

		return self._Data.copy()

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
		"""Вложенное возвращаемое значение."""

		return self._Value

	#==========================================================================================#
	# >>>>> МЕТОДЫ УСТАНОВКИ ЗНАЧЕНИЙ СВОЙСТВ <<<<< #
	#==========================================================================================#

	@code.setter
	def code(self, new_code: int):
		"""Код выполнения."""

		self._Code = int(new_code)

	@message.setter
	def message(self, new_message: str | None):
		"""Сообщение."""

		self._Message = str(new_message) if new_message else None
	
	@type.setter
	def type(self, new_type: StatussesTypes):
		"""Тип отчёта."""

		self._Type = new_type
	
	@value.setter
	def value(self, new_value: any):
		"""Вложенное возвращаемое значение."""

		self._Value = new_value

	#==========================================================================================#
	# >>>>> МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, code: int, message: str | None = None, value: str | None = None, type: StatussesTypes = StatussesTypes.Normal):
		"""
		Отчёт о выполнении.
			code – код выполнения;\n
			message – сообщение;\n
			value – вложенное возвращаемое значение;\n
			data – словарь дополнительных данных;\n
			type – тип отчёта.
		"""

		#---> Генерация динамичкских свойств.
		#==========================================================================================#
		self._Code = code
		self._Message = message
		self._Value = value
		self._Data = dict()
		self._Type = StatussesTypes.Normal

	def __getitem__(self, key: str) -> any:
		"""
		Возвращает значение поля дополнительных данных.
			key – ключ.
		"""

		return self._Data[key]
	
	def __setitem__(self, key: str, value: any):
		"""
		Задаёт значение поля дополнительных данных.
			key – ключ;\n
			value – значение.
		"""

		self._Data[key] = value

	def check_data(self, key: str) -> bool:
		"""
		Проверяет, заполнено ли поле данных с указанным ключём.
			key – ключ.
		"""

		IsSuccess = False
		if key in self._Data.keys(): IsSuccess = True

		return IsSuccess 

class ExecutionWarning(ExecutionStatus):
	"""Отчёт о предупреждении выполнения."""

	def __init__(self, code: int, message: str | None = None, value: str | None = None):
		"""
		Отчёт о предупреждении выполнения.
			code – код выполнения;\n
			message – сообщение;\n
			value – вложенное возвращаемое значение.
		"""

		#---> Генерация динамичкских свойств.
		#==========================================================================================#
		self._Type = StatussesTypes.Warning
		self._Code = code
		self._Message = message
		self._Value = value
		self._Data = dict()

class ExecutionError(ExecutionStatus):
	"""Отчёт об ошибке выполнения."""

	def __init__(self, code: int, message: str | None = None, value: str | None = None):
		"""
		Отчёт об ошибке выполнения.
			code – код выполнения;\n
			message – сообщение;\n
			value – вложенное возвращаемое значение.
		"""
		
		#---> Генерация динамичкских свойств.
		#==========================================================================================#
		self._Code = code
		self._Message = message
		self._Value = value
		self._Data = dict()
		self._Type = StatussesTypes.Error

class ExecutionCritical(ExecutionStatus):
	"""Отчёт о критической ошибке выполнения."""

	def __init__(self, code: int, message: str | None = None, value: str | None = None):
		"""
		Отчёт о критической ошибке выполнения.
			code – код выполнения;\n
			message – сообщение;\n
			value – вложенное возвращаемое значение.
		"""

		#---> Генерация динамичкских свойств.
		#==========================================================================================#
		self._Type = StatussesTypes.Critical
		self._Code = code
		self._Message = message
		self._Value = value
		self._Data = dict()