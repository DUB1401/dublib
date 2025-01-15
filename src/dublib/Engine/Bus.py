from ..CLI.TextStyler import Colors, TextStyler

from typing import Any

import enum

#==========================================================================================#
# >>>>> ВСПОМОГАТЕЛЬНЫЕ СТРУКТУРЫ ДАННЫХ <<<<< #
#==========================================================================================#

class MessagesTypes(enum.Enum):
	"""Перечисление типов сообщений."""

	Info = "info"
	Warning = "warning"
	Error = "error"
	Critical = "critical"

class ExecutionMessage:
	"""Сообщение процесса выполнения."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def text(self) -> str:
		"""Текст сообщения."""

		return self.__Text

	@property
	def type(self) -> MessagesTypes | None:
		"""Тип сообщения."""

		return self.__Type
	
	@property
	def origin(self) -> str | None:
		"""Строка идентификации источника сообщения."""

		return self.__Origin

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, text: str, type: MessagesTypes = MessagesTypes.Info, origin: str | None = None):
		"""
		Сообщение процесса выполнения.
			text – текст сообщения;\n
			type – тип сообщения;\n
			origin – строка идентификации источника сообщения.
		"""

		#---> Генерация динамичкских атрибутов.
		#==========================================================================================#
		self.__Text = text
		self.__Type = type
		self.__Origin = origin

	def __str__(self) -> str:
		"""Возвращает строковое представление форматированного сообщения."""

		Origin = ""
		Type = ""
		if self.__Origin: Origin = f"{self.__Origin}:"
		if self.__Type: Type = f"[{Origin}{self.__Type.name.upper()}] "
		ColorsDict = {
			MessagesTypes.Info: Colors.White,
			MessagesTypes.Error: Colors.Red,
			MessagesTypes.Warning: Colors.Yellow,
			MessagesTypes.Critical: Colors.Red,
			None: Colors.White
		}
		Message = TextStyler(f"{Type}{self.__Text}", text_color = ColorsDict[self.__Type]).text

		return Message

	def check_origin(self, origin: str | None) -> bool:
		"""
		Проверяет, совпадает ли источник сообщения.
			origin – строка идентификации источника сообщения.
		"""

		return origin == self.__Origin

	def print(self):
		"""Выводит в консоль сообщение."""

		print(str(self))

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

		return self.__Code

	@property
	def data(self) -> dict:
		"""Копия словаря дополнительных данных."""

		return self.__Data.copy()

	@property
	def messages(self) -> tuple[ExecutionMessage]:
		"""Сообщение."""

		return tuple(self.__Messages)
	
	@property
	def value(self) -> Any:
		"""Вложенное возвращаемое значение."""

		return self.__Value

	#==========================================================================================#
	# >>>>> МЕТОДЫ УСТАНОВКИ ЗНАЧЕНИЙ СВОЙСТВ <<<<< #
	#==========================================================================================#

	@code.setter
	def code(self, new_code: int):
		"""Код выполнения."""

		self.__Code = int(new_code)
	
	@value.setter
	def value(self, new_value: Any) -> Any:
		"""Вложенное возвращаемое значение."""

		self.__Value = new_value

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self):
		"""Отчёт о выполнении."""

		#---> Генерация динамичкских атрибутов.
		#==========================================================================================#
		self.__Code = None
		self.__Messages: list[ExecutionMessage] = list()
		self.__Value = None
		self.__Data = dict()

	def __bool__(self) -> bool:
		"""Приводит вложенное значение к логическому типу."""

		return bool(self.__Value)

	def __getitem__(self, key: Any) -> Any:
		"""
		Возвращает значение из словаря дополнительных данных.
			key – ключ.
		"""

		return self.__Data[key]
	
	def __setitem__(self, key: Any, value: Any):
		"""
		Задаёт значение в словаре дополнительных данных.
			key – ключ;\n
			value – значение.
		"""

		self.__Data[key] = value

	def __str__(self) -> str:
		"""Возвращает текстовое представление статуса."""

		Status = str()
		Status += TextStyler("Code:").decorate.bold + " " + str(self.__Code) + "\n"
		Status += TextStyler("Value:").decorate.bold + " " + str(self.__Value) + "\n"

		if self.__Data: Status += TextStyler("Data:").decorate.bold + "\n"
		for Key in self.__Data: Status += "    " + str(Key) + ": " + str(self.__Data[Key]) + "\n"

		if self.__Messages: Status += TextStyler("Messages:").decorate.bold + "\n"

		for Message in self.__Messages: Status += "    " + str(Message) + "\n"

		return Status.rstrip()

	def check_data(self, key: Any) -> bool:
		"""
		Проверяет, существует ли значение в словаре дополнительных данных.
			key – ключ.
		"""

		return key in self.__Data.keys()

	def merge(self, status: "ExecutionStatus", overwrite: bool = True):
		"""
		Выполняет слияние другого статуса с текущим объектом, объединяя списки сообщений и перезаписывая данные. 
			status – статус для слиянитя;\n
			overwrite – переключает перезапись данных статуса.
		"""

		if overwrite:
			self.__Code = status.code
			self.__Value = status.value

		for Key in status.data.keys():
			if Key in self.__Data and overwrite or Key not in self.__Data: self.__Data[Key] = status.data[Key]
		
		self.__Messages += status.messages

	def set_code(self, code: int | None):
		"""
		Задаёт код выполнения.
			code – код выполнения.
		"""

		self.__Code = code

	def set_value(self, value: Any, force: bool = False):
		"""
		Устанавливает значение, которое необходимо вернуть в результате выполнения.
			value – значение;\n
			force – указывает, что нужно перезаписать существующее значение.
		"""

		self.__Value = value

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ РАБОТЫ С СООБЩЕНИЯМИ <<<<< #
	#==========================================================================================#

	def print_messages(self, indent: int = 0):
		"""
		Выводит в консоль все сообщения.
			indent – количество пробелов перед выводом сообщения.
		"""
		
		for Message in self.__Messages:
			if indent: print(" " * int(indent), end = "")
			Message.print()

	def push_critical(self, text: str, origin: str | None = None):
		"""
		Добавляет сообщение типа Critical.
			text – текст сообщения;\n
			origin – строка идентификации источника сообщения.
		"""

		self.push_message(text, MessagesTypes.Critical, origin)

	def push_error(self, text: str, origin: str | None = None):
		"""
		Добавляет сообщение типа Error.
			text – текст сообщения;\n
			origin – строка идентификации источника сообщения.
		"""

		self.push_message(text, MessagesTypes.Error, origin)

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

		self.__Messages.append(ExecutionMessage(text, type, origin))

	def push_warning(self, text: str, origin: str | None = None):
		"""
		Добавляет сообщение типа Warning.
			text – текст сообщения;\n
			origin – строка идентификации источника сообщения.
		"""

		self.push_message(text, MessagesTypes.Warning, origin)