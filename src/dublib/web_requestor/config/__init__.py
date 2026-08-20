from typing import Sequence, cast, get_args

from curl_cffi import BrowserTypeLiteral, CurlHttpVersion

from ..enums import WebLibs
from .headers import ImportantHeaders

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
