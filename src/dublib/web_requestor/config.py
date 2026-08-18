from typing import Sequence, cast, get_args

import ua_generator
from curl_cffi import BrowserTypeLiteral, CurlHttpVersion
from ua_generator.user_agent import UserAgent

from ..exceptions import web_requestor as Exceptions
from ..functions.data import ToSequence
from .enums import WebLibs

#==========================================================================================#
# >>>>> НАСТРОЙКИ КОНКРЕТНЫХ БИБЛИОТЕК <<<<< #
#==========================================================================================#

class _curl_cffi_config:
	"""Дополнительная конфигурация библиотеки curl_cffi."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def fingerprint(self) -> BrowserTypeLiteral | None:
		"""Отпечаток браузера."""

		return self.__Fingerprint

	@property
	def http_version(self) -> CurlHttpVersion:
		"""Версия используемого протокола HTTP."""

		return self.__HttpVersion

	#==========================================================================================#
	# >>>>> МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self):
		"""Дополнительная конфигурация библиотеки curl_cffi."""

		self.__HttpVersion = CurlHttpVersion.V1_1
		self.__Fingerprint: BrowserTypeLiteral | None = None
	
	def select_http_version(self, version: CurlHttpVersion):
		"""
		Указывает используемую версию протокола HTTP.
		
		:param version: Версия протокола HTTP.
		:type version: CurlHttpVersion
		"""

		self.__HttpVersion = version

	def select_fingerprint(self, fingerprint: str | None):
		"""
		Выбирает используемый отпечаток браузера.

		:param fingerprint: Строковый идентификатор отпечатка браузера или `None` для удаления. Список идентификаторов можно получить на [странице](https://github.com/lexiforest/curl_cffi?tab=readme-ov-file#supported-impersonate-browsers) библиотеки.
		:type fingerprint: str | None
		:raises ValueError: 
		"""

		if fingerprint not in get_args(BrowserTypeLiteral): raise ValueError(fingerprint)
		self.__Fingerprint = cast(BrowserTypeLiteral | None, fingerprint)

class _httpx_config:
	"""Дополнительная конфигурация библиотеки httpx."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def http2(self) -> bool:
		"""Состояние использования протокола HTTP/2 для запросов."""

		return self.__EnableHTTP2

	#==========================================================================================#
	# >>>>> МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self):
		"""Дополнительная конфигурация библиотеки curl_cffi."""

		self.__EnableHTTP2 = False
	
	def enable_http2(self, status: bool):
		"""
		Переключает режим использования протокола HTTP/2 для запросов.
			status – состояние режима.
		"""

		self.__EnableHTTP2 = status

#==========================================================================================#
# >>>>> СЕКЦИИ КОНФИГУРАЦИИ <<<<< #
#==========================================================================================#
	
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
	def user_agent(self) -> str | None:
		"""Значение заголовка *User-Agent*."""

		return self.__UserAgent.text if self.__UserAgent else None

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self):
		"""Оператор приоритетных заголовков."""

		self.__Headers: dict[str, str] = {}
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
		:raises UserAgentRedefining: Переопределение заголовка *User-Agent*. Используйте `generate_user_agent()` вместо этого метода.
		"""

		name = name.lower()

		if name == "user-agent" or name.startswith("sec-ch"):
			raise Exceptions.UserAgentRedefining()
		
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
			ToSequence(device) if device else None,
			ToSequence(platform) if platform else None,
			ToSequence(browsers) if browsers else None
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

		if self.__UserAgent:
			Headers.update(self.__UserAgent.headers.get())

		return Headers

#==========================================================================================#
# >>>>> ОСНОВНОЙ КЛАСС <<<<< #
#==========================================================================================#

class WebConfig:
	"""Конфигурация оператора запросов."""

	#==========================================================================================#
	# >>>>> КОНТЕЙНЕРЫ ПАРАМЕТРОВ ОТЕДЛЬНЫХ БИБЛИОТЕК <<<<< #
	#==========================================================================================#

	@property
	def curl_cffi(self) -> _curl_cffi_config:
		"""Дополнительная конфигурация библиотеки **curl_cffi**."""

		return self.__curl_cffi

	@property
	def httpx(self) -> _httpx_config:
		"""Дополнительная конфигурация библиотеки **httpx**."""

		return self.__httpx

	#==========================================================================================#
	# >>>>> СОСТОЯНИЯ <<<<< #
	#==========================================================================================#

	@property
	def logging(self) -> bool:
		"""Указывает, требуется ли вести логи при помощи стандартного модуля **Python**."""

		return self.__EnableLogging
	
	@property
	def redirecting(self) -> bool:
		"""Указывает, следует ли выполнять автоматическую переадресацию."""

		return self.__EnableRedirecting

	@property
	def switch_proxy_protocol(self) -> bool:
		"""Указывает, следует ли автоматически переключаться между HTTP/HTTPS версиями протокола прокси при ошибках запроса."""

		return self.__SwitchProtocol

	@property
	def verify_ssl(self) -> bool:
		"""Указывает, необходимо ли проводить верификацию SSL."""

		return self.__VerifySSL
	
	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def delay(self) -> float:
		"""Интервал времени между повторами запросов."""

		return self.__Delay

	@property
	def headers(self) -> ImportantHeaders:
		"""Оператор приоритетных заголовков."""

		return self.__Headers

	@property
	def lib(self) -> WebLibs:
		"""Тип используемой библиотеки."""

		return self.__UsedLib

	@property
	def retries(self):
		"""Количество повторов запроса при неудачном выполнении."""

		return self.__Retries

	@property
	def good_codes(self) -> tuple[int | None, ...]:
		"""Список кодов, означающих успешное выполнение запроса."""

		return self.__GoodCodes

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self):
		"""Конфигурация оператора запросов."""
		
		self.__Retries: int = 0
		self.__UsedLib = WebLibs.requests
		self.__GoodCodes: tuple[int | None, ...] = (200,)
		self.__Delay: float = 0.25

		self.__SwitchProtocol: bool = False
		self.__EnableRedirecting: bool = True
		self.__EnableLogging: bool = True
		self.__VerifySSL: bool = True

		self.__Headers: ImportantHeaders = ImportantHeaders()

		self.__curl_cffi = _curl_cffi_config()
		self.__httpx = _httpx_config()

	def select_lib(self, lib: WebLibs):
		"""
		Задаёт тип используемой библиотеки запросов.

		:param lib: Тип библиотеки.
		:type lib: WebLibs
		"""

		self.__UsedLib = lib

	def set_delay(self, delay: float | int):
		"""
		Задаёт интервал ожидания между повторными запросами.

		:param delay: Интервал в секундах.
		:type delay: float | int
		"""

		self.__Delay = float(delay)

	def set_good_codes(self, good_codes: Sequence[int | None]):
		"""
		Задаёт набор кодов HTTP, означающих успешное выполнение запроса.

		:param good_codes: Набор кодов HTTP. Расширяется значением `None`, которое возникает при обработке внутреннего исключения.
		:type good_codes: Sequence[int | None]
		"""

		self.__GoodCodes = tuple(good_codes)

	def set_retries_count(self, retries: int):
		"""
		Задаёт количество повторов запроса при неудачном выполнении.

		:param retries: Количество повторов. Первый запрос не учитывается в подсчёте.
		:type retries: int
		"""

		self.__Retries = retries

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ УСТАНОВКИ ЛОГИЧЕСКИХ ПЕРЕКЛЮЧАТЕЛЕЙ <<<<< #
	#==========================================================================================#

	def enable_logging(self, status: bool):
		"""
		Переключает ведение логов при помощи стандартного модуля Python.

		:param status: Состояние активации.
		:type status: bool
		"""

		self.__EnableLogging = status

	def enable_proxy_protocol_switching(self, status: bool):
		"""
		Переключает режим автоматической смены HTTP/HTTPS версий протокола прокси при ошибках. Может привести к значительному увеличению времени запроса.

		:param status: Состояние активации.
		:type status: bool
		"""

		self.__SwitchProtocol = status

	def enable_redirecting(self, status: bool):
		"""
		Переключает автоматическую переадресацию.

		:param status: Состояние активации.
		:type status: bool
		"""

		self.__EnableRedirecting = status

	def enable_ssl_verification(self, status: bool):
		"""
		Переключает верификацию SSL.

		:param status: Состояние активации.
		:type status: bool
		"""

		self.__VerifySSL = status
