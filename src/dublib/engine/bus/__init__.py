from typing import Any, Sequence

from ...cli.text_styler import TextStyler, codes
from ...exceptions.engine import bus as BusExceptions
from .messages import MessagesContainer

#==========================================================================================#
# >>>>> КОНТЕЙНЕРЫ ПРАВИЛ <<<<< #
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
	def allowed_data_keys(self) -> tuple:
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
		self.__AllowedKeys: tuple = ()

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
	
	@code.setter
	def code(self, new_code: int | None):
		"""Код выполнения."""

		self._Code = new_code

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
		self._Data = {}

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
		Bolder = TextStyler(codes.Decorations.Bold)
		Status += Bolder.get_styled_text("Code:") + f" {self._Code}\n"
		Status += Bolder.get_styled_text("Value:") + f" {self._Value}\n"

		if self._Data: Status += Bolder.get_styled_text("Data:") + "\n"
		for Key in self._Data: Status += f"    {Key}: " + str(self._Data[Key]) + "\n"
		if self._Messages: Status += Bolder.get_styled_text("Messages:") + "\n"
		for Message in self._Messages.as_list(): Status += f"    {Message}\n"

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