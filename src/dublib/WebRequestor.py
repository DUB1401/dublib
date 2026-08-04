import enum
import json
import logging
import random
from time import sleep
from typing import TYPE_CHECKING, Any, Callable, Sequence, cast, get_args

import httpx
import requests
import ua_generator
from curl_cffi import BrowserTypeLiteral, CurlHttpVersion, ProxySpec
from curl_cffi import requests as curl_cffi_requests
from ua_generator.user_agent import UserAgent

from .Core import LOGS_HANDLER
from .Exceptions import WebRequestor as Exceptions
from .Functions.Data import ToSequence

if TYPE_CHECKING:
	from requests.cookies import RequestsCookieJar

#==========================================================================================#
# >>>>> ИНИЦИАЛИЗАЦИЯ СИСТЕМЫ ЛОГГИРОВАНИЯ <<<<< #
#==========================================================================================#

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(LOGS_HANDLER)
LOGGER.setLevel(logging.INFO)

#==========================================================================================#
# >>>>> ПЕРЕЧИСЛЕНИЯ <<<<< #
#==========================================================================================#

class Protocols(enum.Enum):
	"""Перечисление типов протоколов."""
	
	SOCKS4 = "socks4"
	SOCKS5 = "socks5"
	HTTPS = "https"
	HTTP = "http"
	SFTP = "sftp"
	FTP = "ftp"

class RequestsTypes(enum.Enum):
	"""Перечисление типов поддерживаемыйх запросов."""
	
	GET = "get"
	POST = "post"

class WebLibs(enum.Enum):
	"""Перечисление поддерживаемых библиотек запросов."""

	curl_cffi = "curl_cffi"
	requests = "requests"
	httpx = "httpx"

#==========================================================================================#
# >>>>> ДОПОЛНИТЕЛЬНЫЕ КОНФИГУРАЦИИ БИБЛИОТЕК ЗАПРОСОВ <<<<< #
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
# >>>>> ВСПОМОГАТЕЛЬНЫЕ ТИПЫ ДАННЫХ <<<<< #
#==========================================================================================#

class Proxy:
	"""Данные прокси-сервера."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def protocol(self) -> Protocols:
		"""Тип протокола подключения."""

		return self.__Protocol
	
	@property
	def host(self) -> str | None:
		"""IP адрес или домен хоста."""

		return self.__Host
	
	@property
	def port(self) -> int | None:
		"""Номер порта."""

		return self.__Port
	
	@property
	def login(self) -> str | None:
		"""Логин."""

		return self.__Login
	
	@property
	def password(self) -> str | None:
		"""Пароль."""

		return self.__Password

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, protocol: Protocols = Protocols.HTTPS, host: str | None = None, port: int | None = None, login: str | None = None, password: str | None = None):
		"""
		Данные прокси-сервера.

		:param protocol: Тип протокола подключения.
		:type protocol: Protocols
		:param host: IP адрес или домен хоста.
		:type host: str | None
		:param port: Номер порта.
		:type port: int | None
		:param login: Логин.
		:type login: str | None
		:param password: Пароль.
		:type password: str | None
		"""

		self.__Protocol = protocol
		self.__Host = host
		self.__Port = port
		self.__Login = login
		self.__Password = password
	
	def parse(self, proxy: str) -> "Proxy":
		"""
		Парсит данные прокси из строки.

		:param proxy: Строка с данными прокси вида `protocol://username:password@host:port`.
		:type proxy: str
		:return: Текущий объект данных прокси-сервера.
		:rtype: Proxy
		"""

		ProtocolPart, ProxyPart = proxy.split("://")
		LoginPart, HostPart = (None, None)

		if "@" in ProxyPart: LoginPart, HostPart = ProxyPart.split("@")
		else: HostPart = ProxyPart

		Host, Port = HostPart.split(":")
		Login, Password = (None, None)

		if LoginPart: Login, Password = LoginPart.split(":")

		self.__Protocol = Protocols(ProtocolPart.lower())
		self.__Host = Host
		self.__Port = int(Port)
		self.__Login = Login
		self.__Password = Password

		return self

	def set_protocol(self, protocol: Protocols):
		"""
		Задаёт новый протокол для прокси.

		:param protocol: Тип протокола.
		:type protocol: Protocols
		"""

		self.__Protocol = protocol

	def to_dict(self, force_http: bool = True) -> dict[str, str]:
		"""
		Строит словарь для подключения прокси к **requests**-подобным библиотекам.

		:param force_http: Большинство прокси неверно работают при использовании протокола HTTPS. При включённом состоянии для HTTPS-соединения **requests** будет использоваться `http://{proxy}` соединение.
		:type force_http: bool
		:return: Словарь данных прокси для подключения к **requests**-подобным библиотекам.
		:rtype: dict[str, str]
		"""

		ProxyDict = {}

		if self.__Protocol.value.startswith("http"):
			ProxyDict["http"] = self.to_string()
			if self.__Protocol == Protocols.HTTPS: ProxyDict["https"] = self.to_string(force_http)

		else: ProxyDict = {self.__Protocol.value: self.to_string(force_http = False)}

		return ProxyDict

	def to_string(self, force_http: bool = True) -> str:
		"""
		Возвращает данные прокси в виде строки.

		:param force_http: Большинство прокси неверно работают при использовании протокола HTTPS. При включённом состоянии для HTTPS-соединения **requests** будет использоваться `http://{proxy}` соединение.
		:type force_http: bool
		:return: Строка с данными прокси вида `protocol://username:password@host:port`
		:rtype: str
		"""

		Authorization = f"{self.__Login}:{self.__Password}@" if self.__Login and self.__Password else ""
		ProxyString = f"{self.__Protocol.value}://{Authorization}{self.__Host}:{self.__Port}"
		if force_http and ProxyString.startswith("https"): ProxyString = "http" + ProxyString[5:]

		return ProxyString
		
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
	def auto_accept_ch(self) -> bool:
		"""Указывает, необходимо ли автоматическое разрешение **Client Hints** при выполнении запросов."""

		return self.__AutoAcceptCH

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
	def headers(self) -> dict:
		"""Словарь заголвоков, приоритетно применяемых ко всем запросам."""

		Headers = self.__Headers.copy()
		if self.__UserAgent: Headers |= self.__UserAgent.headers.get()

		return Headers

	@property
	def lib(self) -> WebLibs:
		"""Тип используемой библиотеки."""

		return self.__UsedLib

	@property
	def retries(self):
		"""Количество повторов запроса при неудачном выполнении."""

		return self.__Retries

	@property
	def user_agent(self) -> str | None:
		"""Значение заголовка *User-Agent*."""

		return self.__UserAgent.text if self.__UserAgent else None

	@property
	def good_codes(self) -> tuple[int | None, ...]:
		"""Список кодов, означающих успешное выполнение запроса."""

		return self.__GoodCodes

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self):
		"""Конфигурация оператора запросов."""
		
		self.__SwitchProtocol = False
		self.__UsedLib = WebLibs.requests
		self.__EnableRedirecting = True
		self.__EnableLogging = True
		self.__UserAgent: UserAgent | None = None
		self.__Headers: dict[str, str] = {}
		self.__Retries: int = 0
		self.__GoodCodes: tuple[int | None, ...] = (200,)
		self.__Delay: float = 0.25
		self.__VerifySSL: bool = True
		self.__AutoAcceptCH: bool = True

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

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ УПРАВЛЕНИЯ ЗАГОЛОВКАМИ <<<<< #
	#==========================================================================================#
	
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

	def add_header(self, name: str, value: str | int):
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
		
		self.set_header(name, value)

	def set_header(self, name: str, value: str | int):
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

	def generate_user_agent(self, device: Sequence[str] | None = None, platform: Sequence[str] | None = None, browsers: Sequence[str] | None = None):
		"""
		Генерирует случайное значение заголовка *User-Agent* и данные **Client Hints** при помощи библиотеки [ua-generator](https://github.com/iamdual/ua-generator).

		Фильтры для спецификации параметров заголовка доступны в документации используемой библиотеки.

		:param device: Типы устройств.
		:type device: Sequence[str] | None
		:param platform: Платформы.
		:type platform: Sequence[str] | None
		:param browsers: Браузеры.
		:type browsers: Sequence[str] | None
		"""

		self.__UserAgent = ua_generator.generate(
			tuple(device) if device else None,
			tuple(platform) if platform else None,
			tuple(browsers) if browsers else None,
		)

	def remove_header(self, name: str, exception: bool = False):
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

class WebResponse:
	"""Унифицированный контейнер ответа на веб-запросы."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def content(self) -> bytes | None:
		"""Бинарное представление ответа."""

		return self.__Content

	@property
	def exceptions(self) -> tuple[Exception, ...]:
		"""Набор возникших во время выполнения запросов исключений."""

		return tuple(self.__Exceptions)

	@property
	def headers(self) -> dict:
		"""Словарь заголовков ответа."""

		return self.__Headers

	@property
	def json(self) -> dict | None:
		"""Десериализованное в словарь из JSON представление ответа."""

		return self.__JSON

	@property
	def ok(self) -> bool:
		"""Состояние: можно ли считать запрос успешным."""

		return self.status_code in self.__GoodCodes

	@property
	def status_code(self) -> int | None:
		"""Код ответа."""

		return self.__StatusCode

	@property
	def text(self) -> str | None:
		"""Текстовое представление ответа."""

		return self.__Text

	#==========================================================================================#
	# >>>>> ПРИВАТНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __TryDeserialize(self, string: str) -> dict | None:
		"""
		Производит попытку десериализации JSON в словарь.

		:param string: Строковые данные.
		:type string: str
		:return: Словарное представление JSON или `None` при невозможности десериализации.
		:rtype: dict | None
		"""

		try: return json.loads(string)
		except json.JSONDecodeError: pass

		return None

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, config: WebConfig | None = None):
		"""
		Унифицированный контейнер ответа на веб-запросы.

		:param config: Конфигурация оператора запросов. Используется для определения кодов, означающих успешное выполнение запроса.
		:type config: WebConfig | None
		"""

		self.__GoodCodes: tuple[int | None, ...] = config.good_codes if config else WebConfig().good_codes

		self.__StatusCode: int | None = None
		self.__Content: bytes | None = None
		self.__JSON: dict | None = None
		self.__Text: str | None = None
		self.__Headers: dict = {}
		self.__Exceptions: list[Exception] = []

	def __bool__(self) -> bool:
		"""Интерпретирует ответ в логическое значение: успешен ли запрос."""

		return self.ok

	def __str__(self) -> str:
		"""Интерпретирует ответ в строку."""

		return f"<WebResponse [{self.status_code}]>"

	def parse_response(self, response: requests.Response | httpx.Response | curl_cffi_requests.Response, parse_json: bool = True):
		"""
		Парсит ответ библиотеки в унифицированный формат.

		:param response: Ответ от библиотеки.
		:type response: requests.Response | httpx.Response | curl_cffi_requests.Response
		:param parse_json: Указывает, следует ли произвести попытку десериализации данных в JSON.
		:type parse_json: bool
		"""

		self.__StatusCode = response.status_code
		self.__Content = response.content
		self.__Text = None
		self.__JSON = None

		self.set_text(response.text, parse_json)
		self.set_headers(dict(response.headers))

		if parse_json:
			self.__JSON = self.__TryDeserialize(response.text)

	def push_exception(self, exception: Exception):
		"""
		Добавляет исключение во внутреннее хранилище ответа.

		:param exception: Возникшее во время запроса исключение.
		:type exception: Exception
		"""

		self.__Exceptions.append(exception)

	def set_headers(self, headers: dict):
		"""
		Задаёт словарь заголовков. Приводит все ключи к нижнему регистру.

		:param headers: Словарь заголовков.
		:type headers: dict
		"""

		self.__Headers = {Key.lower(): Value for Key, Value in headers.items()}

	def set_status_code(self, code: int | None):
		"""
		Задаёт HTTP код ответа.

		:param code: HTTP код ответа или `None` при отсутствии такового.
		:type code: int | None
		"""

		self.__StatusCode = code

	def set_text(self, text: str | None, parse_json: bool = True):
		"""
		Задаёт строкове представление ответа, также интерпретируемое в набор байтов.

		:param text: Строковое представление ответа или `None` при отсутствии такового.
		:type text: str | None
		:param parse_json: Указывает, следует ли произвести попытку десериализации строки в JSON.
		:type parse_json: bool
		"""

		self.__Text = text

		if text:
			if parse_json: self.__JSON = self.__TryDeserialize(text)
			self.__Content = text.encode()

#==========================================================================================#
# >>>>> ОСНОВНОЙ КЛАСС <<<<< #
#==========================================================================================#

class WebRequestor:
	"""Оператор запросов."""

	# Определение типов на уровне класса исключает ошибку типизации [no-redef].
	__Session: curl_cffi_requests.Session | requests.Session | httpx.Client | None

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#
	
	@property
	def config(self) -> WebConfig:
		"""Конфигурация оператора запросов."""

		return self.__Config

	@property
	def cookies(self) -> dict | None:
		"""Словарь установленных cookies."""

		if self.__Session is None: return None
		Cookies = None
		if self.__Config.lib in (WebLibs.curl_cffi, WebLibs.requests):
			CookiesSource = cast("curl_cffi_requests.cookies.Cookies | RequestsCookieJar", self.__Session.cookies)
			Cookies = CookiesSource.get_dict()
		elif self.__Config.lib == WebLibs.httpx: Cookies = dict(self.__Session.cookies)

		return Cookies

	#==========================================================================================#
	# >>>>> ПРИВАТНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __Request(self, request_type: RequestsTypes, url: str, **kwargs) -> WebResponse:
		"""
		Базовый обработчик запроса.

		:param request_type: Тип запроса.
		:type request_type: RequestsTypes
		:param url: Адрес запроса.
		:type url: str
		:param kwargs: Дополнительные аргументы, соответствующие таковым именованным аргументам у конкретных методов запросов.
		:return: Унифицированный контейнер ответа на веб-запросы.
		:rtype: WebResponse
		"""

		tries = 1 + self.__Config.retries
		Response = WebResponse(self.__Config)
		Try = 0

		while Try < tries and not Response.ok:
			if Try > 0: sleep(self.__Config.delay)
			Try += 1
			
			try:
				CurrentProxy = random.choice(self.__Proxies) if self.__Proxies else None
				self.__RequestsMethods[request_type][self.__Config.lib](Response, url, CurrentProxy, **kwargs)
				
				#---> Переключение HTTP/HTTPS протоколов прокси при неудачном запросе.
				#==========================================================================================#
				if Response.status_code not in self.__Config.good_codes and CurrentProxy and self.__Config.switch_proxy_protocol and CurrentProxy.protocol:

					if CurrentProxy.protocol in (Protocols.HTTP, Protocols.HTTPS):
						sleep(self.__Config.delay)

						match CurrentProxy.protocol:
							case Protocols.HTTP: CurrentProxy.set_protocol(Protocols.HTTPS)
							case Protocols.HTTPS: CurrentProxy.set_protocol(Protocols.HTTP)

						NewResponse = WebResponse(self.__Config)
						self.__RequestsMethods[request_type][self.__Config.lib](NewResponse, url, CurrentProxy, **kwargs)
						if NewResponse.status_code in self.__Config.good_codes: Response = NewResponse

			except Exception as ExceptionData:
				Response.push_exception(ExceptionData)
				if self.__Config.logging: LOGGER.error(f"[{self.__Config.lib.value}-{request_type.name}] {ExceptionData}")

		return Response

	def __AcceptHints(self, response: WebResponse):
		"""
		Обрабатывает разрешение **Client Hints** на основе заголовков ответа.

		:param response: Контейнер ответа.
		:type response: WebResponse
		"""

		ResponseHeaders: dict[str, str] = response.headers

		if ResponseHeaders:
			AcceptCH: str | None = ResponseHeaders.get("accept-ch")
			CriricalCH: str | None = ResponseHeaders.get("critical-ch")
			if AcceptCH: self.__Config.accept_client_hints(AcceptCH)
			if CriricalCH: self.__Config.accept_client_hints(CriricalCH)

	def __Initialize(self):
		"""Инициализирует сессию."""

		match self.__Config.lib:

			case WebLibs.curl_cffi:
				self.__Session = curl_cffi_requests.Session(
					allow_redirects = self.__Config.redirecting,
					impersonate = self.__Config.curl_cffi.fingerprint,
					http_version = self.__Config.curl_cffi.http_version
				)

			case WebLibs.httpx: self.__Session = httpx.Client(http2 = self.__Config.httpx.http2)
			case WebLibs.requests: self.__Session = requests.Session()

	def __MergeHeaders(self, headers: dict | None) -> dict | None:
		"""Объединяет заголовки конфигурации и параметров запроса."""

		if self.__Config.headers:
			if headers: headers = self.__Config.headers | headers
			else: headers = self.__Config.headers

		return headers

	#==========================================================================================#
	# >>>>> ПРИАТНЫЕ МЕТОДЫ ЗАПРОСОВ БИБЛИОТЕКИ CURL_CFFI <<<<< #
	#==========================================================================================#

	def __curl_cffi_GET(self, response: WebResponse, url: str, proxy: Proxy | None = None, params: dict | None = None, headers: dict | None = None, cookies: dict | None = None) -> WebResponse:
		"""
		Отправляет GET запрос через библиотеку **curl_cffi**.

		:param response: Контейнер ответа.
		:type response: WebResponse
		:param url: Адрес запроса.
		:type url: str
		:param proxy: Данные прокси.
		:type proxy: Proxy | None
		:param params: Словарь параметров запроса.
		:type params: dict | None
		:param headers: Словарь заголовков.
		:type headers: dict | None
		:param cookies: Словарь cookies.
		:type cookies: dict | None
		:return: Контейнер ответа от библиотеки **curl_cffi**.
		:rtype: WebResponse
		"""

		self.__Session = cast(curl_cffi_requests.Session, self.__Session)
		headers = self.__MergeHeaders(headers)

		response.parse_response(self.__Session.get(
			url = url,
			params = params,
			headers = headers,
			cookies = cookies,
			proxies = cast(ProxySpec, proxy.to_dict()) if proxy else None,
			verify = self.__Config.verify_ssl
		))

		return response

	def __curl_cffi_POST(self, response: WebResponse, url: str, proxy: Proxy | None = None, params: dict | None = None, headers: dict | None = None, cookies: dict | None = None, data: Any = None, json: dict | None = None) -> WebResponse:
		"""
		Отправляет POST запрос через библиотеку **curl_cffi**.

		:param response: Контейнер ответа.
		:type response: WebResponse
		:param url: Адрес запроса.
		:type url: str
		:param proxy: Данные прокси.
		:type proxy: Proxy | None
		:param params: Словарь параметров запроса.
		:type params: dict | None
		:param headers: Словарь заголовков.
		:type headers: dict | None
		:param cookies: Словарь cookies.
		:type cookies: dict | None
		:param data: Данные запроса.
		:type data: Any
		:param json: Словарь для сериализации и передачи в качестве JSON.
		:type json: dict | None
		:return: Контейнер ответа от библиотеки **curl_cffi**.
		:rtype: WebResponse
		"""

		self.__Session = cast(curl_cffi_requests.Session, self.__Session)
		headers = self.__MergeHeaders(headers)

		response.parse_response(self.__Session.post(
			url = url,
			params = params,
			headers = headers,
			cookies = cookies,
			data = data,
			json = json,
			proxies = cast(ProxySpec, proxy.to_dict()) if proxy else None,
			verify = self.__Config.verify_ssl
		))

		return response
	
	#==========================================================================================#
	# >>>>> ПРИВАТНЫЕ МЕТОДЫ ЗАПРОСОВ БИБЛИОТЕКИ HTTPX <<<<< #
	#==========================================================================================#

	def __httpx_GET(self, response: WebResponse, url: str, proxy: Proxy | None = None, params: dict | None = None, headers: dict | None = None, cookies: dict | None = None) -> WebResponse:
		"""
		Отправляет GET запрос через библиотеку **httpx**.

		:param response: Контейнер ответа.
		:type response: WebResponse
		:param url: Адрес запроса.
		:type url: str
		:param proxy: Данные прокси.
		:type proxy: Proxy | None
		:param params: Словарь параметров запроса.
		:type params: dict | None
		:param headers: Словарь заголовков.
		:type headers: dict | None
		:param cookies: Словарь cookies.
		:type cookies: dict | None
		:return: Контейнер ответа от библиотеки **httpx**.
		:rtype: WebResponse
		"""

		headers = self.__MergeHeaders(headers)
		CurrentCookies = self.cookies or {}
		cookies = cookies or {}

		self.__Session = httpx.Client(
			params = params,
			headers = headers,
			cookies = CurrentCookies | cookies,
			proxy = proxy.to_string() if proxy else None,
			http2 = self.__Config.httpx.http2,
			follow_redirects = self.__Config.redirecting,
			verify = self.__Config.verify_ssl
		)

		response.parse_response(self.__Session.get(url))

		return response

	def __httpx_POST(self, response: WebResponse, url: str, proxy: Proxy | None = None, params: dict | None = None, headers: dict | None = None, cookies: dict | None = None, data: Any = None, json: dict | None = None) -> WebResponse:
		"""
		Отправляет POST запрос через библиотеку **httpx**.

		:param response: Контейнер ответа.
		:type response: WebResponse
		:param url: Адрес запроса.
		:type url: str
		:param proxy: Данные прокси.
		:type proxy: Proxy | None
		:param params: Словарь параметров запроса.
		:type params: dict | None
		:param headers: Словарь заголовков.
		:type headers: dict | None
		:param cookies: Словарь cookies.
		:type cookies: dict | None
		:param data: Данные запроса.
		:type data: Any
		:param json: Словарь для сериализации и передачи в качестве JSON.
		:type json: dict | None
		:return: Контейнер ответа от библиотеки **httpx**.
		:rtype: WebResponse
		"""

		headers = self.__MergeHeaders(headers)
		CurrentCookies = self.cookies or {}
		cookies = cookies or {}
		
		self.__Session = httpx.Client(
			params = params,
			headers = headers,
			cookies = CurrentCookies | cookies,
			proxy = proxy.to_string() if proxy else None,
			http2 = self.__Config.httpx.http2,
			follow_redirects = self.__Config.redirecting,
			verify = self.__Config.verify_ssl
		)

		response.parse_response(self.__Session.post(url, data = data, json = json))

		return response
	
	#==========================================================================================#
	# >>>>> ПРИВАТНЫЕ МЕТОДЫ ЗАПРОСОВ БИБЛИОТЕКИ REQUESTS <<<<< #
	#==========================================================================================#

	def __requests_GET(self, response: WebResponse, url: str, proxy: Proxy | None = None, params: dict | None = None, headers: dict | None = None, cookies: dict | None = None) -> WebResponse:
		"""
		Отправляет GET запрос через библиотеку **requests**.

		:param response: Контейнер ответа.
		:type response: WebResponse
		:param url: Адрес запроса.
		:type url: str
		:param proxy: Данные прокси.
		:type proxy: Proxy | None
		:param params: Словарь параметров запроса.
		:type params: dict | None
		:param headers: Словарь заголовков.
		:type headers: dict | None
		:param cookies: Словарь cookies.
		:type cookies: dict | None
		:return: Контейнер ответа от библиотеки **requests**.
		:rtype: WebResponse
		"""
		
		self.__Session = cast(requests.Session, self.__Session)
		headers = self.__MergeHeaders(headers)

		response.parse_response(self.__Session.get(
			url = url,
			params = params,
			headers = headers,
			cookies = cookies,
			proxies = proxy.to_dict() if proxy else None,
			allow_redirects = self.__Config.redirecting,
			verify = self.__Config.verify_ssl
		))

		return response
	
	def __requests_POST(self, response: WebResponse, url: str, proxy: Proxy | None = None, params: dict | None = None, headers: dict | None = None, cookies: dict | None = None, data: Any = None, json: dict | None = None) -> WebResponse:
		"""
		Отправляет POST запрос через библиотеку **requests**.

		:param response: Контейнер ответа.
		:type response: WebResponse
		:param url: Адрес запроса.
		:type url: str
		:param proxy: Данные прокси.
		:type proxy: Proxy | None
		:param params: Словарь параметров запроса.
		:type params: dict | None
		:param headers: Словарь заголовков.
		:type headers: dict | None
		:param cookies: Словарь cookies.
		:type cookies: dict | None
		:param data: Данные запроса.
		:type data: Any
		:param json: Словарь для сериализации и передачи в качестве JSON.
		:type json: dict | None
		:return: Контейнер ответа от библиотеки **requests**.
		:rtype: WebResponse
		"""

		self.__Session = cast(requests.Session, self.__Session)
		headers = self.__MergeHeaders(headers)

		response.parse_response(self.__Session.get(
			url = url,
			params = params,
			headers = headers,
			cookies = cookies,
			data = data,
			json = json,
			proxies = proxy.to_dict() if proxy else None,
			allow_redirects = self.__Config.redirecting,
			verify = self.__Config.verify_ssl
		))

		return response
		
	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, config: WebConfig | None = None):
		"""
		Оператор запросов.

		:param config: Конфигурация библиотеки запросов.
		:type config: WebConfig | None
		"""

		self.__Proxies: tuple[Proxy, ...] = ()
		self.__Config = config or WebConfig()
		self.__Session = None

		self.__RequestsMethods: dict[RequestsTypes, dict[WebLibs, Callable]] = {
			RequestsTypes.GET: {
				WebLibs.curl_cffi: self.__curl_cffi_GET,
				WebLibs.httpx: self.__httpx_GET,
				WebLibs.requests: self.__requests_GET
			},
			RequestsTypes.POST: {
				WebLibs.curl_cffi: self.__curl_cffi_POST,
				WebLibs.httpx: self.__httpx_POST,
				WebLibs.requests: self.__requests_POST
			},
		}

		self.__Initialize()

	def close(self):
		"""Закрывает менеджер запросов."""
			
		if self.__Session is not None: 
			self.__Session.close()
			self.__Session = None
			
	def add_proxies(self, proxies: Sequence[Proxy] | Proxy):
		"""
		Добавляет прокси в систему ротации.

		:param proxy: Набор данных прокси-серверов.
		:type proxy: Sequence[Proxy] | Proxy
		"""
		
		if proxies:
			ProxiesList = ToSequence(proxies, list)
			Buffer = list(self.__Proxies)
			Buffer += ProxiesList
			self.__Proxies = tuple(Buffer)
	
	def remove_proxies(self):
		"""Удаляет данные используемых прокси."""

		self.__Proxies = ()

	def request(self, request_type: RequestsTypes, url: str, **kwargs) -> WebResponse:
		"""
		Базовый обработчик запроса.

		:param request_type: Тип запроса.
		:type request_type: RequestsTypes
		:param url: Адрес запроса.
		:type url: str
		:param kwargs: Дополнительные аргументы, соответствующие таковым именованным аргументам у конкретных методов запросов.
		:return: Унифицированный контейнер ответа на веб-запросы.
		:rtype: WebResponse
		"""

		Response: WebResponse = self.__Request(request_type, url, **kwargs)
		if self.__Config.auto_accept_ch: self.__AcceptHints(Response)

		return Response

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ ВЫПОЛНЕНИЯ ЗАПРОСОВ <<<<< #
	#==========================================================================================#	

	def get(self, url: str, params: dict | None = None, headers: dict | None = None, cookies: dict | None = None) -> WebResponse:
		"""
		Отправляет GET-запрос.

		:param url: Адрес запроса.
		:type url: str
		:param params: Словарь параметров запроса.
		:type params: dict | None
		:param headers: Словарь заголовков.
		:type headers: dict | None
		:param cookies: Словарь cookies.
		:type cookies: dict | None
		:return: Унифицированный контейнер ответа на веб-запросы.
		:rtype: WebResponse
		"""
		
		return self.request(RequestsTypes.GET, url, params = params, headers = headers, cookies = cookies)
	
	def post(self, url: str, params: dict | None = None, headers: dict | None = None, cookies: dict | None = None, data: Any = None, json: dict | None = None) -> WebResponse:
		"""
		Отправляет POST-запрос.

		:param url: Адрес запроса.
		:type url: str
		:param params: Словарь параметров запроса.
		:type params: dict | None
		:param headers: Словарь заголовков.
		:type headers: dict | None
		:param cookies: Словарь cookies.
		:type cookies: dict | None
		:param data: Данные запроса.
		:type data: Any
		:param json: Словарь для сериализации и передачи в качестве JSON.
		:type json: dict | None
		:return: Унифицированный контейнер ответа на веб-запросы.
		:rtype: WebResponse
		"""

		return self.request(RequestsTypes.POST, url, params = params, headers = headers, cookies = cookies, data = data, json = json)