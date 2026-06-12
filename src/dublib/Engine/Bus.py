from ..CLI.Templates.Bus import GenerateMessage, MessagesTypes, PrintMessage
from ..Exceptions.Engine import Bus as BusExceptions
from ..CLI.TextStyler import Codes, TextStyler

from typing import Any, Sequence

#==========================================================================================#
# >>>>> СИСТЕМА СООБЩЕНИЙ <<<<< #
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

class MessagesContainer:
	"""Контейнер сообщений."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def count(self) -> int:
		"""Количество сообщений."""

		return len(self.__Messages)

	@property
	def has_errors(self) -> bool:
		"""Состояние: имеются ли сообщения-ошибки."""

		return self.__HasErrors
	
	@property
	def has_warnings(self) -> bool:
		"""Состояние: имеются ли сообщения-предупреждения."""

		return self.__HasWarnings

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self):
		"""Контейнер сообщений."""

		self.__Messages: list[ExecutionMessage] = list()
		self.__HasErrors = False
		self.__HasWarnings = False

	def add_message(self, message: ExecutionMessage):
		"""
		Добавляет сообщение в контейнер.

		:param message: Сообщение.
		:type message: ExecutionMessage
		"""

		self.__Messages.append(message)
		
		match message.type:
			case MessagesTypes.Error: self.__HasErrors = True
			case MessagesTypes.Warning: self.__HasWarnings = True 

	def as_list(self) -> list[ExecutionMessage]:
		"""
		Возвращает копию списка сообщений.

		:return: Список сообщений.
		:rtype: list[ExecutionMessage]
		"""

		return self.__Messages.copy()

	def clear(self):
		"""Удаляет сообщения."""

		self.__Messages = list()
		self.__HasErrors = False
		self.__HasWarnings = False

	def print(self, character: str = " ", indent: int = 0):
		"""
		Выводит в консоль все сообщения.
		
		:param character: Символ для реализации отступа.
		:type character: str
		:param indent: Количество символов отстутпа перед сообщением.
		:type indent: int
		"""
		
		for Message in self.__Messages:
			if character and indent: print(character * int(indent), end = "")
			Message.print()

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ СОЗДАНИЯ КОНКРЕТНЫХ ТИПОВ СООБЩЕНИЙ <<<<< #
	#==========================================================================================#

	def push_critical(self, text: str, origin: str | None = None):
		"""
		Добавляет сообщение типа **Critical**.

		:param text: Текст сообщения.
		:type text: str
		:param origin: Идентификатор источника сообщения.
		:type origin: str | None
		"""

		self.add_message(ExecutionMessage(text, MessagesTypes.Critical, origin))

	def push_error(self, text: str, origin: str | None = None):
		"""
		Добавляет сообщение типа **Error**.

		:param text: Текст сообщения.
		:type text: str
		:param origin: Идентификатор источника сообщения.
		:type origin: str | None
		"""

		self.add_message(ExecutionMessage(text, MessagesTypes.Error, origin))

	def push_info(self, text: str, origin: str | None = None):
		"""
		Добавляет сообщение типа **Info**.

		:param text: Текст сообщения.
		:type text: str
		:param origin: Идентификатор источника сообщения.
		:type origin: str | None
		"""

		self.add_message(ExecutionMessage(text, MessagesTypes.Info, origin))

	def push_warning(self, text: str, origin: str | None = None):
		"""
		Добавляет сообщение типа **Warning**.

		:param text: Текст сообщения.
		:type text: str
		:param origin: Идентификатор источника сообщения.
		:type origin: str | None
		"""

		self.add_message(ExecutionMessage(text, MessagesTypes.Warning, origin))

#==========================================================================================#
# >>>>> КОНТЕЙНЕР ПРАВИЛ <<<<< #
#==========================================================================================#

class LogicalRule:
	"""Логическое правило взаимодействия."""

	def __init__(self):
		"""Логическое правило взаимодействия."""

		self.__IsEnabled = True

	def __bool__(self) -> bool:
		"""
		Возвращает статус правила.

		:return: Статус правила.
		:rtype: bool
		"""

		return self.__IsEnabled

	def disable(self):
		"""Отключает правило."""

		self.set_status(False)

	def enable(self):
		"""Включает правило."""

		self.set_status(True)

	def set_status(self, status: bool):
		"""
		Устанавливает статус активации правила.

		:param status: Статус правила.
		:type status: bool
		"""

		self.__IsEnabled = status

class RulesContainer:
	"""Хранилище правил взаимодействия."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def allowed_data_keys(self) -> tuple[Any]:
		"""Последовательность доступных для использования в качестве ключей значений."""

		return self.__AllowedKeys

	@property
	def require_value_initialization(self) -> LogicalRule:
		"""Правило: требуется ли обязательная инициализация значения."""

		return self.__ValueInitializationRule

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	def __init__(self):
		"""Хранилище правил взаимодействия."""

		self.__ValueInitializationRule = LogicalRule()
		self.__AllowedKeys = tuple()

	def set_allowed_keys(self, keys: Sequence[Any]):
		"""
		Задаёт последовательность ключей, для которых можно задавать значения в словаре дополнительных данных.

		Если последовательность не указана, разрешаются любые варианты.

		:param keys: Последовательность ключей.
		:type keys: Sequence[Any]
		"""

		self.__AllowedKeys = tuple(keys)

#==========================================================================================#
# >>>>> ОСНОВНЫЕ КЛАССЫ <<<<< #
#==========================================================================================#

class ExecutionResult:
	"""Контейнер результата выполнения."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def code(self) -> int | None:
		"""Целочисленный код."""

		return self._Code

	@property
	def data(self) -> dict:
		"""Копия словаря дополнительных данных."""

		return self._Data.copy()

	@property
	def is_value_setted(self) -> bool:
		"""Состояние: вызывался ли метод установки значения у данного контейнера."""

		return self._IsValueSetted

	@property
	def messages(self) -> MessagesContainer:
		"""Контейнер сообщений."""

		return self._Messages
	
	@property
	def rules(self) -> RulesContainer:
		"""Набор правил взаимодействия."""

		return self._Rules

	@property
	def value(self) -> Any:
		"""
		Вложенное возвращаемое значение.

		:raises ValueNotInintialized: Включено правило проверки инициализации значения.
		"""

		if self._Rules.require_value_initialization and not self._IsValueSetted: raise BusExceptions.ValueNotInintialized()

		return self._Value

	#==========================================================================================#
	# >>>>> МЕТОДЫ УСТАНОВКИ ЗНАЧЕНИЙ СВОЙСТВ <<<<< #
	#==========================================================================================#

	@code.setter
	def code(self, new_code: int | None):
		"""Код выполнения."""

		self._Code = new_code
	
	@value.setter
	def value(self, new_value: Any) -> Any:
		"""Вложенное возвращаемое значение."""

		self.set_value(new_value)

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
		"""Контейнер результата выполнения."""

		self._Code = None
		self._Messages = MessagesContainer()
		self._Rules = RulesContainer()
		self._Value = None
		self._Data = dict()

		self._IsValueSetted = False

		self._PostInitMethod()

	def __bool__(self) -> bool:
		"""
		Приводит вложенное значение к логическому типу.

		:return: Возвращает `True`, если значение в контейнере возможно привести к таковому.
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
	
	def __iadd__(self, status: "ExecutionResult") -> "ExecutionResult":
		"""
		Выполняет слияние другого контейнера с текущим, объединяя списки сообщений. 

		:param status: Контейнер результата для слияния.
		:type status: ExecutionResult
		:param overwrite: Если включено, дополнительные данные, код и значение другого контейнера перезупишут текущие.
		:type overwrite: bool, optional
		:raises TypeError: Выбрасывается при попытке слияния с объектом другого типа.
		"""

		if isinstance(status, ExecutionResult): self.merge(status)
		else: raise TypeError("Can only concatenate ExecutionResult objects.")

		return self

	def __setitem__(self, key: Any, value: Any):
		"""
		Устанавливает значение в словарь дополнительных данных.

		:param key: Ключ.
		:type key: Any
		:param value: Значение.
		:type value: Any
		:raises KeyNotAllowed: Ключ не может быть использован из-за правила взаимодействия.
		"""

		if self._Rules.allowed_data_keys and key not in self._Rules.allowed_data_keys: raise BusExceptions.KeyNotAllowed()
		self._Data[key] = value

	def __str__(self) -> str:
		"""Возвращает текстовое представление результата."""

		Status = str()
		Bolder = TextStyler(Codes.Decorations.Bold)
		Status += Bolder.get_styled_text("Code:") + f" {self._Code}\n"
		Status += Bolder.get_styled_text("Value:") + f" {self._Value}\n"

		if self._Data: Status += Bolder.get_styled_text("Data:") + "\n"
		for Key in self._Data: Status += f"    {Key}: " + str(self._Data[Key]) + "\n"
		if self._Messages: Status += Bolder.get_styled_text("Messages:") + "\n"
		for Message in self._Messages: Status += f"    {Message}\n"

		return Status.rstrip()

	def check_data(self, key: Any) -> bool:
		"""
		Проверяет существование значения в словаре дополнительных данных.

		:param key: Ключ для проверки.
		:type key: Any
		:return: Возвращает `True`, если значение по переданному ключу найдено.
		:rtype: bool
		"""

		return key in self._Data

	def merge(self, result: "ExecutionResult", overwrite: bool = True):
		"""
		Выполняет слияние другого контейнера с текущим, объединяя списки сообщений. 

		:param status: Контейнер результата для слияния.
		:type status: ExecutionResult
		:param overwrite: Если включено, дополнительные данные, код и значение другого контейнера перезупишут текущие.
		:type overwrite: bool, optional
		"""

		if overwrite:
			if result.code: self._Code = result.code
			if result.is_value_setted: self._Value = result.value

		for Key in result.data.keys():
			if Key in self._Data and overwrite or Key not in self._Data: self._Data[Key] = result.data[Key]
		
		for Element in result.messages.as_list(): self._Messages.add_message(Element)

	def delete_value(self):
		"""Удаляет значение."""

		self._IsValueSetted = False
		self._Value = None

	def set_code(self, code: int | None):
		"""
		Задаёт целочисленный код.

		:param code: Целочисленный код.
		:type code: int | None
		"""

		self._Code = code

	def set_value(self, value: Any):
		"""
		Задаёт результат выполнения.

		:param value: Результат выполнения.
		:type value: Any
		"""

		self._IsValueSetted = True
		self._Value = value