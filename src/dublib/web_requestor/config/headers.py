from typing import Sequence, cast

import ua_generator
from ua_generator.user_agent import UserAgent

from ...exceptions import web_requestor as Exceptions
from ...functions.data import to_sequence
from . import constants
from .authorization import Authorizator

class ImportantHeaders:
	"""Оператор приоритетных заголовков."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def auto_accept_ch(self) -> bool:
		"""Указывает, необходимо ли автоматическое разрешение **Client Hints** при выполнении запросов."""

		return self.__AutoAcceptCH

	@property
	def authorization(self) -> Authorizator:
		"""Оператор авторизаци."""

		return self.__Authorizator

	@property
	def user_agent(self) -> str | None:
		"""Значение заголовка *User-Agent*."""

		return self.__UserAgent.text if self.__UserAgent else None

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self):
		"""Оператор приоритетных заголовков."""

		self.__Headers: dict[str, str] = {}
		self.__Authorizator: Authorizator = Authorizator()
		self.__UserAgent: UserAgent | None = None
		self.__AutoAcceptCH: bool = True
	
	def automatically_accept_client_hints(self, status: bool):
		"""
		Переключает автоматическое разрешение **Client Hints** при выполнении запросов.

		:param status: Статус активации.
		:type status: bool
		"""

		self.__AutoAcceptCH = status

	def accept_client_hints(self, hints: str):
		"""
		Добавляет в заголовки запроса данные, запрашиваемые **Client Hints**.

		:param hits: Строка, содержащая **Client Hints**, разделённые запятой.
		:type hits: str
		"""

		if not self.__UserAgent:
			self.generate_user_agent()
			self.__UserAgent = cast(UserAgent, self.__UserAgent)

		self.__UserAgent.headers.accept_ch(hints)

	def add(self, name: str, value: str | int):
		"""
		Добавляет постоянный заголовок ко всем производимым запросам. Запрещает переопределение заголовков.

		:param name: Имя заголовка.
		:type name: str
		:param value: Значение заголовка.
		:type value: str | int
		:raises UserAgentRedefining: Переопределение заголовка *User-Agent*. Используйте `generate_user_agent()` вместо этого метода.
		:raises HeaderRedefining: Переопределение заголовка.
		"""

		name = name.lower()

		if name in self.__Headers:
			raise Exceptions.HeaderRedefining(name)
		
		self.set(name, value)

	def set(self, name: str, value: str | int):
		"""
		Задаёт постоянный заголовок ко всем производимым запросам.

		:param name: Имя заголовка.
		:type name: str
		:param value: Значение заголовка.
		:type value: str | int
		:raises AuthorizationRedefining: Переопределение заголовка _Authorization_.
		:raises UserAgentRedefining: Gереопределение заголовков User-Agent или Sec-CH-*.
		"""

		name = name.lower()

		if name == constants.USER_AGENT_HEADER or name.startswith("sec-ch"):
			raise Exceptions.UserAgentRedefining()

		if name == constants.AUTHORIZATION_HEADER:
			raise Exceptions.AuthorizationRedefining()
		
		self.__Headers[name] = value if type(value) is str else str(value)

	def generate_user_agent(self, device: Sequence[str] | str | None = None, platform: Sequence[str] | str | None = None, browsers: Sequence[str] | str | None = None):
		"""
		Генерирует случайное значение заголовка *User-Agent* и данные **Client Hints** при помощи библиотеки [ua-generator](https://github.com/iamdual/ua-generator).

		Фильтры для спецификации параметров заголовка доступны в документации используемой библиотеки.

		:param device: Типы устройств.
		:type device: Sequence[str] | str | None
		:param platform: Платформы.
		:type platform: Sequence[str] | str | None
		:param browsers: Браузеры.
		:type browsers: Sequence[str] | str | None
		"""

		self.__UserAgent = ua_generator.generate(
			to_sequence(device) if device else None,
			to_sequence(platform) if platform else None,
			to_sequence(browsers) if browsers else None
		)

	def remove(self, name: str, exception: bool = False):
		"""
		Удаляет постоянный заголовок.

		:param name: Имя заголовка.
		:type name: str
		:param exception: Указывает, нужно ли выбрасывать исключение при попытке удаления несуществующего заголовка.
		:type exception: bool
		:raises UserAgentRedefining: Выбрасывается при попытке удаления заголовка *User-Agent*. Используйте `set_user_agent()` вместо этого метода.
		:raises KeyError: Заголовк не существует.
		"""

		name = name.lower()

		if name == "user-agent":
			raise Exceptions.UserAgentRedefining()

		if name in self.__Headers:
			del self.__Headers[name]
		elif exception:
			raise KeyError(name)

	def to_dict(self) -> dict[str, str]:
		"""
		Возвращает словарь заголовков. Ключи представлены в нижнем регистре.

		:return: Словарь заголовков.
		:rtype: dict[str, str]
		"""

		Headers = self.__Headers.copy()

		if self.__UserAgent: Headers.update(self.__UserAgent.headers.get())
		if self.__Authorizator: Headers.update(self.__Authorizator.headers)

		return Headers
