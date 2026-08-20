from .enums import MessagesTypes

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

	def __init__(self, text: str, message_type: MessagesTypes | None = None, origin: str | None = None):
		"""
		Сообщение процесса выполнения.

		:param text: Текст сообщения.
		:type text: str
		:param message_type: Тип сообщения.
		:type message_type: MessagesTypes | None
		:param origin: Источник сообщения.
		:type origin: str | None
		"""

		self._Text = text
		self._Type = message_type
		self._Origin = origin

	def check_origin(self, origin: str | None) -> bool:
		"""
		Проверяет совпадение источника сообщения.

		:param origin: Идентификатор источника сообщения.
		:type origin: str | None
		:return: Возвращает `True`, если переданный источник совпадает с заданным в самом сообщении.
		:rtype: bool
		"""

		return origin == self._Origin

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

		self.__Messages: list[ExecutionMessage] = []
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

		self.__Messages = []
		self.__HasErrors = False
		self.__HasWarnings = False

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

	def push_debug(self, text: str, origin: str | None = None):
		"""
		Добавляет сообщение типа **Debug**.

		:param text: Текст сообщения.
		:type text: str
		:param origin: Идентификатор источника сообщения.
		:type origin: str | None
		"""

		self.add_message(ExecutionMessage(text, MessagesTypes.Debug, origin))

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
