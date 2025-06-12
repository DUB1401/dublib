from .Exceptions.WebRequestor import *
from .Methods.Data import ToIterable

from typing import Any, Iterable
from time import sleep
import logging
import random
import enum
import json

from curl_cffi import requests as curl_cffi_requests
from curl_cffi import CurlHttpVersion
from fake_useragent import UserAgent
import requests
import httpx

#==========================================================================================#
# >>>>> ИНИЦИАЛИЗАЦИЯ СИСТЕМЫ ЛОГГИРОВАНИЯ <<<<< #
#==========================================================================================#

Logger = logging.getLogger(__name__)
Logger.addHandler(logging.StreamHandler().setFormatter(logging.Formatter("[%(name)s] %(levelname)s: %(message)s")))
Logger.setLevel(logging.INFO)

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
	def fingerprint(self) -> str | None:
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

		#---> Генерация динамических атрибутов.
		#==========================================================================================#
		self.__HttpVersion = CurlHttpVersion.V1_1
		self.__Fingerprint = None
		self.__SwitchProtocol = False
	
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
   		"""

		self.__Fingerprint = fingerprint

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

		#---> Генерация динамических атрибутов.
		#==========================================================================================#
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
	def protocol(self) -> Protocols | None:
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

	def __init__(self, protocol: Protocols | None = None, host: str | None = None, port: int | str | None = None, login: str | None = None, password: str | None = None):
		"""
		Данные прокси-сервера.

		:param protocol: Тип протокола подключения.
		:type protocol: Protocols | None
		:param host: IP адрес или домен хоста.
		:type host: str | None
		:param port: Номер порта.
		:type port: int | str | None
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

		ProxyDict = dict()

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
	def logging(self) -> bool:
		"""Указывает, требуется ли вести логи при помощи стандартного модуля Python."""

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
	# >>>>> СОСТОЯНИЯ <<<<< #
	#==========================================================================================#

	@property
	def delay(self) -> float:
		"""Интервал времени между повторами запросов."""

		return self.__Delay

	@property
	def headers(self) -> dict | None:
		"""Словарь заголвоков, приоритетно применяемых ко всем запросам, или `None` при отсутствии заголовков."""

		Headers = self.__Headers.copy()
		if self.__UserAgent: Headers["User-Agent"] = self.__UserAgent

		return Headers or None

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
		"""Значение заголовка User-Agent."""

		return self.__UserAgent

	@property
	def good_codes(self) -> tuple[int | None]:
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
		self.__UserAgent = None
		self.__Headers = dict()
		self.__Retries = 0
		self.__GoodCodes = (200, 404)
		self.__Delay = 0.25
		self.__VerifySSL = True

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

	def set_good_codes(self, good_codes: Iterable[int | None]):
		"""
		Задаёт набор кодов HTTP, означающих успешное выполнение запроса.

		:param good_codes: Набор кодов HTTP. Расширяется значением `None`, которое возникает при обработке внутреннего исключения.
		:type good_codes: Iterable[int | None]
		"""

		self.__GoodCodes = good_codes

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ УПРАВЛЕНИЯ ЗАГОЛОВКАМИ <<<<< #
	#==========================================================================================#
	
	def add_header(self, name: str, value: str | int):
		"""
		Добавляет постоянный заголовок ко всем производимым запросам.

		:param name: Имя заголовка.
		:type name: str
		:param value: Значение заголовка.
		:type value: str | int
		:raises UserAgentRedefining: Выбрасывается при попытке переопределения заголовка *User-Agent*. Используйте `set_user_agent()` вместо этого метода.
		"""

		if name.lower() == "user-agent": raise UserAgentRedefining()
		self.__Headers[name] = value

	def generate_user_agent(
		self,
		os: Iterable[str] = ("Windows", "Linux", "Ubuntu", "Chrome OS", "Mac OS X", "Android", "iOS"),
		browsers: Iterable[str] = ("Chrome", "Firefox", "Edge", "Opera"," Safari", "Android", "Yandex Browser", "Samsung Internet", "Opera Mobile", "Mobile Safari", "Firefox Mobile", "Firefox iOS", "Chrome Mobile", "Chrome Mobile iOS", "Mobile Safari UI/WKWebView", "Edge Mobile", "DuckDuckGo Mobile", "MiuiBrowser", "Whale", "Twitter", "Facebook", "Amazon Silk"),
		platforms: Iterable[str] = ("desktop", "mobile", "tablet")
	):
		"""
		Генерирует случайное значение заголовка *User-Agent* при помощи библиотеки **fake_useragent**.

		:param os: Операционные системы.
		:type os: Iterable[str]
		:param browsers: Браузеры.
		:type browsers: Iterable[str]
		:param platforms: Платформы.
		:type platforms: Iterable[str]
		"""

		self.__UserAgent = UserAgent(
			os = os,
			browsers = browsers,
			platforms = platforms
		).random

	def remove_header(self, name: str):
		"""
		Удаляет постоянный заголовок.

		:param name: Имя заголовка.
		:type name: str
		:raises UserAgentRedefining: Выбрасывается при попытке удаления заголовка *User-Agent*. Используйте `set_user_agent()` вместо этого метода.
		"""

		if name.lower() == "user-agent": raise UserAgentRedefining()
		del self.__Headers[name]

	def set_user_agent(self, user_agent: str | None):
		"""
		Задаёт значение заголовка *User-Agent*.

		:param user_agent: Значение заголовка или `None` для удаления.
		:type user_agent: str | None
		"""

		self.__UserAgent = user_agent

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
	def exceptions(self) -> tuple[Exception]:
		"""Набор возникших во время выполнения запросов исключений."""

		return tuple(self.__Exceptions)

	@property
	def json(self) -> dict | None:
		"""Десериализованное в словарь из JSON представление ответа."""

		return self.__JSON

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
		except: pass

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self):
		"""Унифицированный контейнер ответа на веб-запросы."""

		self.__StatusCode = None
		self.__Content = None
		self.__JSON = None
		self.__Text = None
		self.__Exceptions = list()

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
		self.__Text = response.text
		self.__Content = response.content
		self.__JSON = self.__TryDeserialize(response.text)

	def push_exception(self, exception: Exception):
		"""
		Добавляет исключение во внутреннее хранилище ответа.

		:param exception: Возникшее во время запроса исключение.
		:type exception: Exception
		"""

		self.__Exceptions.append(exception)

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
			self.__Content = bytes(text)

#==========================================================================================#
# >>>>> ОСНОВНОЙ КЛАСС <<<<< #
#==========================================================================================#

class WebRequestor:
	"""Оператор запросов."""

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

		Cookies = None
		if self.__Config.lib in (WebLibs.curl_cffi, WebLibs.requests): Cookies = self.__Session.cookies.get_dict()
		elif self.__Config.lib == WebLibs.httpx: Cookies = dict(self.__Session.cookies)

		return Cookies

	#==========================================================================================#
	# >>>>> ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

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

			if headers: 
				headers = self.__Config.headers | headers
				
			else:
				headers = self.__Config.headers

		return headers

	#==========================================================================================#
	# >>>>> МЕТОДЫ ЗАПРОСОВ БИБЛИОТЕКИ CURL_CFFI <<<<< #
	#==========================================================================================#

	def __curl_cffi_GET(self, url: str, proxy: Proxy | None = None, params: dict | None = None, headers: dict | None = None, cookies: dict | None = None) -> curl_cffi_requests.Response:
		"""
		Отправляет GET запрос через библиотеку **curl_cffi**.

		:param url: Адрес запроса.
		:type url: str
		:param proxy: Данные прокси.
		:type proxy: Proxy | None
		:param params: Словарь параметров запроса. По умолчанию `None`.
		:type params: dict | None
		:param headers: Словарь заголовков. По умолчанию `None`.
		:type headers: dict | None
		:param cookies: Словарь cookies. По умолчанию `None`.
		:type cookies: dict | None
		:return: Контейнер ответа от библиотеки **requests**.
		:rtype: requests.Response
		"""

		Response = WebResponse()
		headers = self.__MergeHeaders(headers)
			
		Response.parse_response(self.__Session.get(
			url = url,
			params = params,
			headers = headers,
			cookies = cookies,
			proxies = proxy.to_dict(),
			verify = self.__Config.verify_ssl
		))

		return Response

	def __curl_cffi_POST(self, url: str, proxy: Proxy | None = None, params: dict | None = None, headers: dict | None = None, cookies: dict | None = None, data: Any = None, json: dict | None = None) -> curl_cffi_requests.Response:
		"""
		Отправляет POST запрос через библиотеку **curl_cffi**.

		:param url: Адрес запроса.
		:type url: str
		:param proxy: Данные прокси.
		:type proxy: Proxy | None
		:param params: Словарь параметров запроса. По умолчанию `None`.
		:type params: dict | None
		:param headers: Словарь заголовков. По умолчанию `None`.
		:type headers: dict | None
		:param cookies: Словарь cookies. По умолчанию `None`.
		:type cookies: dict | None
		:param data: Данные запроса. По умолчанию `None`.
		:type data: Any
		:param json: Словарь для сериализации и передачи в качестве JSON. По умолчанию `None`.
		:type json: dict | None
		:return: Контейнер ответа от библиотеки **requests**.
		:rtype: requests.Response
		"""

		Response = WebResponse()
		headers = self.__MergeHeaders(headers)

		Response.parse_response(self.__Session.post(
			url = url,
			params = params,
			headers = headers,
			cookies = cookies,
			data = data,
			json = json,
			proxies = proxy.to_dict(),
			verify = self.__Config.verify_ssl
		))

		return Response
	
	#==========================================================================================#
	# >>>>> МЕТОДЫ ЗАПРОСОВ БИБЛИОТЕКИ HTTPX <<<<< #
	#==========================================================================================#

	def __httpx_GET(self, url: str, proxy: Proxy | None = None, params: dict | None = None, headers: dict | None = None, cookies: dict | None = None) -> httpx.Response:
		"""
		Отправляет GET запрос через библиотеку **httpx**.

		:param url: Адрес запроса.
		:type url: str
		:param proxy: Данные прокси.
		:type proxy: Proxy | None
		:param params: Словарь параметров запроса. По умолчанию `None`.
		:type params: dict | None
		:param headers: Словарь заголовков. По умолчанию `None`.
		:type headers: dict | None
		:param cookies: Словарь cookies. По умолчанию `None`.
		:type cookies: dict | None
		:return: Контейнер ответа от библиотеки **requests**.
		:rtype: requests.Response
		"""

		Response = WebResponse()
		headers = self.__MergeHeaders(headers)
		CurrentCookies = self.cookies or dict()
		cookies = cookies or dict()

		self.__Session = httpx.Client(
			params = params,
			headers = headers,
			cookies = CurrentCookies | cookies,
			proxy = proxy.to_string(),
			http2 = self.__Config.httpx.http2,
			follow_redirects = self.__Config.redirecting,
			verify = self.__Config.verify_ssl
		)

		Response.parse_response(self.__Session.get(url))

		return Response

	def __httpx_POST(self, url: str, proxy: Proxy | None = None, params: dict | None = None, headers: dict | None = None, cookies: dict | None = None, data: Any = None, json: dict | None = None) -> httpx.Response:
		"""
		Отправляет POST запрос через библиотеку **httpx**.

		:param url: Адрес запроса.
		:type url: str
		:param proxy: Данные прокси.
		:type proxy: Proxy | None
		:param params: Словарь параметров запроса. По умолчанию `None`.
		:type params: dict | None
		:param headers: Словарь заголовков. По умолчанию `None`.
		:type headers: dict | None
		:param cookies: Словарь cookies. По умолчанию `None`.
		:type cookies: dict | None
		:param data: Данные запроса. По умолчанию `None`.
		:type data: Any
		:param json: Словарь для сериализации и передачи в качестве JSON. По умолчанию `None`.
		:type json: dict | None
		:return: Контейнер ответа от библиотеки **requests**.
		:rtype: requests.Response
		"""

		Response = WebResponse()
		headers = self.__MergeHeaders(headers)
		CurrentCookies = self.cookies or dict()
		cookies = cookies or dict()
		
		self.__Session = httpx.Client(
			params = params,
			headers = headers,
			cookies = CurrentCookies | cookies,
			data = data,
			json = json,
			proxy = proxy.to_string(),
			http2 = self.__Config.httpx.http2,
			follow_redirects = self.__Config.redirecting,
			verify = self.__Config.verify_ssl
		)

		Response.parse_response(self.__Session.post(url, data = data, json = json))

		return Response
	
	#==========================================================================================#
	# >>>>> МЕТОДЫ ЗАПРОСОВ БИБЛИОТЕКИ REQUESTS <<<<< #
	#==========================================================================================#

	def __requests_GET(self, url: str, proxy: Proxy | None = None, params: dict | None = None, headers: dict | None = None, cookies: dict | None = None) -> requests.Response:
		"""
		Отправляет GET запрос через библиотеку **requests**.

		:param url: Адрес запроса.
		:type url: str
		:param proxy: Данные прокси.
		:type proxy: Proxy | None
		:param params: Словарь параметров запроса. По умолчанию `None`.
		:type params: dict | None
		:param headers: Словарь заголовков. По умолчанию `None`.
		:type headers: dict | None
		:param cookies: Словарь cookies. По умолчанию `None`.
		:type cookies: dict | None
		:return: Контейнер ответа от библиотеки **requests**.
		:rtype: requests.Response
		"""
		
		Response = WebResponse()
		headers = self.__MergeHeaders(headers)

		Response.parse_response(self.__Session.get(
			url = url,
			params = params,
			headers = headers,
			cookies = cookies,
			proxies = proxy.to_dict() if proxy else None,
			allow_redirects = self.__Config.redirecting,
			verify = self.__Config.verify_ssl
		))

		return Response
	
	def __requests_POST(self, url: str, proxy: Proxy | None = None, params: dict | None = None, headers: dict | None = None, cookies: dict | None = None, data: Any = None, json: dict | None = None) -> requests.Response:
		"""
		Отправляет POST запрос через библиотеку **requests**.

		:param url: Адрес запроса.
		:type url: str
		:param proxy: Данные прокси.
		:type proxy: Proxy | None
		:param params: Словарь параметров запроса. По умолчанию `None`.
		:type params: dict | None
		:param headers: Словарь заголовков. По умолчанию `None`.
		:type headers: dict | None
		:param cookies: Словарь cookies. По умолчанию `None`.
		:type cookies: dict | None
		:param data: Данные запроса. По умолчанию `None`.
		:type data: Any
		:param json: Словарь для сериализации и передачи в качестве JSON. По умолчанию `None`.
		:type json: dict | None
		:return: Контейнер ответа от библиотеки **requests**.
		:rtype: requests.Response
		"""

		Response = WebResponse()
		headers = self.__MergeHeaders(headers)

		Response.parse_response(self.__Session.get(
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

		return Response
		
	#==========================================================================================#
	# >>>>> ОБЩИЕ МЕТОДЫ <<<<< #
	#==========================================================================================#
		
	def __init__(self, config: WebConfig | None = None):
		"""
		Оператор запросов.

		:param config: Конфигурация библиотеки запросов.
		:type config: WebConfig | None
		"""

		self.__Proxies: tuple[Proxy] = tuple()
		self.__Config = config or WebConfig()
		self.__Session = None

		self.__RequestsMethods = {
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
			
		self.__Session.close()
		self.__Session = None
			
	def add_proxies(self, proxies: Iterable[Proxy] | Proxy):
		"""
		Добавляет прокси в систему ротации.

		:param proxy: Набор данных прокси-серверов.
		:type proxy: Iterable[Proxy] | Proxy
		"""
		
		if proxies:
			proxies = ToIterable(proxies, list)
			Buffer = list(self.__Proxies)
			Buffer += proxies
			self.__Proxies = tuple(Buffer)
	
	def remove_proxies(self):
		"""Удаляет данные используемых прокси."""

		self.__Proxies = tuple()

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

		tries = 1 + self.__Config.retries
		Response = WebResponse()
		Try = 0
		LibName = self.__Config.lib.value.upper()
		
		while Try < tries and Response.status_code not in self.__Config.good_codes:
			if Try > 0: sleep(self.__Config.delay)
			Try += 1
			
			try:
				CurrentProxy = random.choice(self.__Proxies) if self.__Proxies else None
				Response: WebResponse = self.__RequestsMethods[request_type][self.__Config.lib](url, CurrentProxy, **kwargs)
				
				#---> Переключение HTTP/HTTPS протоколов прокси при неудачном запросе.
				#==========================================================================================#
				if Response.status_code not in self.__Config.good_codes and CurrentProxy and self.__Config.switch_proxy_protocol and CurrentProxy.protocol:

					if CurrentProxy.protocol in (Protocols.HTTP, Protocols.HTTPS):
						sleep(self.__Config.delay)

						match CurrentProxy.protocol:
							case Protocols.HTTP: CurrentProxy.set_protocol(Protocols.HTTPS)
							case Protocols.HTTPS: CurrentProxy.set_protocol(Protocols.HTTP)

						NewResponse: WebResponse = self.__RequestsMethods[request_type][self.__Config.lib](url, CurrentProxy, **kwargs)
						if NewResponse.status_code in self.__Config.good_codes: Response = NewResponse

			except Exception as ExceptionData:
				Response.push_exception(ExceptionData)
				if self.__Config.logging: Logger.error(f"[{LibName}-{request_type.name}] {ExceptionData}")
		
		return Response

	#==========================================================================================#
	# >>>>> ТИПЫ ЗАПРОСОВ <<<<< #
	#==========================================================================================#	
	
	def get(self, url: str, params: dict | None = None, headers: dict | None = None, cookies: dict | None = None) -> WebResponse:
		"""
		Отправляет GET-запрос.

		:param url: Адрес запроса.
		:type url: str
		:param params: Словарь параметров запроса. По умолчанию `None`.
		:type params: dict | None
		:param headers: Словарь заголовков. По умолчанию `None`.
		:type headers: dict | None
		:param cookies: Словарь cookies. По умолчанию `None`.
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
		:param params: Словарь параметров запроса. По умолчанию `None`.
		:type params: dict | None
		:param headers: Словарь заголовков. По умолчанию `None`.
		:type headers: dict | None
		:param cookies: Словарь cookies. По умолчанию `None`.
		:type cookies: dict | None
		:param data: Данные запроса. По умолчанию `None`.
		:type data: Any
		:param json: Словарь для сериализации и передачи в качестве JSON. По умолчанию `None`.
		:type json: dict | None
		:return: Унифицированный контейнер ответа на веб-запросы.
		:rtype: WebResponse
		"""

		return self.request(RequestsTypes.POST, url, params = params, headers = headers, cookies = cookies, data = data, json = json)
