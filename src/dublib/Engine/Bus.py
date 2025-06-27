from ..CLI.Templates.Bus import GenerateMessage, MessagesTypes, PrintMessage
from ..CLI.TextStyler import TextStyler

from typing import Any

#==========================================================================================#
# >>>>> ВСПОМОГАТЕЛЬНЫЕ СТРУКТУРЫ ДАННЫХ <<<<< #
#==========================================================================================#

class ExecutionMessage:
	"""Сообщение процесса выполнения."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def text(self) -> str:
		"""Текст сообщения."""

		return self._Text

	@property
	def type(self) -> MessagesTypes | None:
		"""Тип сообщения."""

		return self._Type
	
	@property
	def origin(self) -> str | None:
		"""Строка идентификации источника сообщения."""

		return self._Origin

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, text: str, type: MessagesTypes | None = None, origin: str | None = None):
		"""
		Сообщение процесса выполнения.

		:param text: Текст сообщения.
		:type text: str
		:param type: Тип сообщения.
		:type type: MessagesTypes | None
		:param origin: Источник сообщения.
		:type origin: str | None
		"""

		self._Text = text
		self._Type = type
		self._Origin = origin

	def __str__(self) -> str:
		"""Возвращает строковое представление сообщения."""

		return GenerateMessage(self._Text, self._Type, self._Origin)

	def check_origin(self, origin: str | None) -> bool:
		"""
		Проверяет совпадение источника сообщения.

		:param origin: Идентификатор источника сообщения.
		:type origin: str | None
		:return: Возвращает `True`, если переданный источник совпадает с заданным в самом сообщении.
		:rtype: bool
		"""

		return origin == self._Origin

	def print(self):
		"""Выводит в консоль форматированное сообщение."""

		PrintMessage(self._Text, self._Type, self._Origin)

#==========================================================================================#
# >>>>> ОСНОВНЫЕ КЛАССЫ <<<<< #
#==========================================================================================#

class ExecutionStatus:
	"""Отчёт о выполнении."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def code(self) -> int | None:
		"""Код выполнения."""

		return self._Code

	@property
	def data(self) -> dict:
		"""Копия словаря дополнительных данных."""

		return self._Data.copy()

	@property
	def has_errors(self) -> bool:
		"""Состояние: имеются ли ошибки."""

		return self._HasErrors
	
	@property
	def has_warnings(self) -> bool:
		"""Состояние: имеются ли предупреждения."""

		return self._HasWarnings

	@property
	def messages(self) -> tuple[ExecutionMessage]:
		"""Сообщение."""

		return tuple(self._Messages)
	
	@property
	def value(self) -> Any:
		"""Вложенное возвращаемое значение."""

		return self._Value

	#==========================================================================================#
	# >>>>> МЕТОДЫ УСТАНОВКИ ЗНАЧЕНИЙ СВОЙСТВ <<<<< #
	#==========================================================================================#

	@code.setter
	def code(self, new_code: int):
		"""Код выполнения."""

		self._Code = int(new_code)
	
	@value.setter
	def value(self, new_value: Any) -> Any:
		"""Вложенное возвращаемое значение."""

		self._Value = new_value

	#==========================================================================================#
	# >>>>> ПЕРЕОПРЕДЕЛЯЕМЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def _PostInitMethod(self):
		"""Метод, срабатывающий после инициализации объекта."""

		pass

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self):
		"""Отчёт о выполнении."""

		self._Code = None
		self._Messages: list[ExecutionMessage] = list()
		self._Value = None
		self._Data = dict()

		self._HasErrors = False
		self._HasWarnings = False

		self._PostInitMethod()

	def __bool__(self) -> bool:
		"""
		Приводит вложенное значение к логическому типу.

		:return: Возвращает `True`, если значение в статусе возможно привести к таковому.
		:rtype: bool
		"""

		return bool(self._Value)

	def __getitem__(self, key: Any) -> Any:
		"""
		Возвращает значение из словаря дополнительных данных.

		:param key: Ключ к словарю дополнительных данных.
		:type key: Any
		:return: Значение из словаря дополнительных данных.
		:rtype: Any
		"""

		return self._Data[key]
	
	def __iadd__(self, status: "ExecutionStatus") -> "ExecutionStatus":
		"""
		Выполняет слияние другого статуса с текущим объектом, объединяя списки сообщений и перезаписывая данные. 

		:param status: Статус для слияния.
		:type status: ExecutionStatus
		:raises TypeError: Выбрасывается при попытке слияния с объектом другого типа.
		:return: Результирующий отчёт о выполнении.
		:rtype: ExecutionStatus
		"""

		if isinstance(status, ExecutionStatus): self.merge(status)
		else: raise TypeError("can only concatenate ExecutionStatus")

		return self

	def __setitem__(self, key: Any, value: Any):
		"""
		Задаёт значение в словаре дополнительных данных.
			key – ключ;\n
			value – значение.
		"""

		self._Data[key] = value

	def __str__(self) -> str:
		"""Возвращает текстовое представление статуса."""

		Status = str()
		Status += TextStyler("Code:").decorate.bold + " " + str(self._Code) + "\n"
		Status += TextStyler("Value:").decorate.bold + " " + str(self._Value) + "\n"

		if self._Data: Status += TextStyler("Data:").decorate.bold + "\n"
		for Key in self._Data: Status += "    " + str(Key) + ": " + str(self._Data[Key]) + "\n"

		if self._Messages: Status += TextStyler("Messages:").decorate.bold + "\n"

		for Message in self._Messages: Status += "    " + str(Message) + "\n"

		return Status.rstrip()

	def check_data(self, key: Any) -> bool:
		"""
		Проверяет, существует ли значение в словаре дополнительных данных.
			key – ключ.
		"""

		return key in self._Data.keys()

	def merge(self, status: "ExecutionStatus", overwrite: bool = True):
		"""
		Выполняет слияние другого статуса с текущим объектом, объединяя списки сообщений и перезаписывая данные. 
			status – статус для слиянитя;\n
			overwrite – переключает перезапись данных статуса.
		"""

		if overwrite:
			self._Code = status.code
			self._Value = status.value

		for Key in status.data.keys():
			if Key in self._Data and overwrite or Key not in self._Data: self._Data[Key] = status.data[Key]
		
		self._Messages += status.messages

	def set_code(self, code: int | None):
		"""
		Задаёт код выполнения.
			code – код выполнения.
		"""

		self._Code = code

	def set_value(self, value: Any, force: bool = False):
		"""
		Устанавливает значение, которое необходимо вернуть в результате выполнения.
			value – значение;\n
			force – указывает, что нужно перезаписать существующее значение.
		"""

		self._Value = value

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ РАБОТЫ С СООБЩЕНИЯМИ <<<<< #
	#==========================================================================================#

	def print_messages(self, indent: int = 0):
		"""
		Выводит в консоль все сообщения.
			indent – количество пробелов перед выводом сообщения.
		"""
		
		for Message in self._Messages:
			if indent: print(" " * int(indent), end = "")
			Message.print()

	def push_critical(self, text: str, origin: str | None = None):
		"""
		Добавляет сообщение типа Critical.
			text – текст сообщения;\n
			origin – строка идентификации источника сообщения.
		"""

		self.push_message(text, MessagesTypes.Critical, origin)
		self._HasErrors = True

	def push_error(self, text: str, origin: str | None = None):
		"""
		Добавляет сообщение типа Error.
			text – текст сообщения;\n
			origin – строка идентификации источника сообщения.
		"""

		self.push_message(text, MessagesTypes.Error, origin)
		self._HasErrors = True

	def push_info(self, text: str, origin: str | None = None):
		"""
		Добавляет сообщение типа Info.
			text – текст сообщения;\n
			origin – строка идентификации источника сообщения.
		"""

		self.push_message(text, MessagesTypes.Info, origin)

	def push_message(self, text: str, type: MessagesTypes | None = None, origin: str | None = None):
		"""
		Добавляет сообщение.
			text – текст сообщения;\n
			type – тип сообщения;\n
			origin – строка идентификации источника сообщения.
		"""

		self._Messages.append(ExecutionMessage(text, type, origin))

	def push_warning(self, text: str, origin: str | None = None):
		"""
		Добавляет сообщение типа Warning.
			text – текст сообщения;\n
			origin – строка идентификации источника сообщения.
		"""

		self.push_message(text, MessagesTypes.Warning, origin)
		self._HasWarnings = True