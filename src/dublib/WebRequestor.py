from .Exceptions.WebRequestor import *

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

# Инициализация модуля ведения логов.
Logger = logging.getLogger(__name__)
Logger.addHandler(logging.StreamHandler().setFormatter(logging.Formatter("[%(name)s] %(levelname)s: %(message)s")))
Logger.setLevel(logging.INFO)

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

	@property
	def switch_proxy_protocol(self) -> bool:
		"""Состояние автоматического переключения HTTP/HTTPS версий протокола прокси при ошибках."""

		return self.__SwitchProtocol

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
			version – версия.
		"""

		self.__HttpVersion = version

	def select_fingerprint(self, fingerprint: str | None):
		"""Выбирает используемый отпечаток браузера."""

		self.__Fingerprint = fingerprint

	def enable_proxy_protocol_switching(self, status: bool):
		"""
		Переключает режим автоматической смены HTTP/HTTPS версий протокола прокси при ошибках.
			status – состояние режима.
		"""

		self.__SwitchProtocol = status

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

class _requests_config:
	"""Дополнительная конфигурация библиотеки requests."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def switch_proxy_protocol(self) -> bool:
		"""Состояние автоматического переключения HTTP/HTTPS версий протокола прокси при ошибках."""

		return self.__SwitchProtocol

	#==========================================================================================#
	# >>>>> МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self):
		"""Дополнительная конфигурация библиотеки requests."""

		#---> Генерация динамических атрибутов.
		#==========================================================================================#
		self.__SwitchProtocol = False
	
	def enable_proxy_protocol_switching(self, status: bool):
		"""
		Переключает режим автоматической смены HTTP/HTTPS версий протокола прокси при ошибках.
			status – состояние режима.
		"""

		self.__SwitchProtocol = status

#==========================================================================================#
# >>>>> ВСПОМОГАТЕЛЬНЫЕ ТИПЫ ДАННЫХ <<<<< #
#==========================================================================================#

class Protocols(enum.Enum):
	"""Перечисление типов протоколов."""
	
	SOCKS4 = "socks4"
	SOCKS5 = "socks5"
	HTTPS = "https"
	HTTP = "http"
	SFTP = "sftp"
	FTP = "ftp"

class WebLibs(enum.Enum):
	"""Перечисление поддерживаемых библиотек запросов."""

	curl_cffi = "curl_cffi"
	requests = "requests"
	httpx = "httpx"
		
class WebResponse:
	"""Унифицированная объектная структура ответа библиотек запросов."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def content(self) -> bytes | None:
		"""Бинарное представление ответа."""

		return self.__content

	@property
	def json(self) -> dict | None:
		"""Десериализованное в словарь из JSON представление ответа."""

		return self.__json

	@property
	def status_code(self) -> int | None:
		"""Код ответа."""

		return self.__status_code

	@property
	def text(self) -> str | None:
		"""Текстовое представление ответа."""

		return self.__text

	#==========================================================================================#
	# >>>>> ПРИВАТНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __TryDeserialize(self, text: str) -> dict | None:
		Result = None

		try:
			Result = json.loads(text)

		except: pass

		return Result

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self):
		"""Унифицированная объектная структура ответа библиотек запросов."""

		#---> Генерация динамических атрибутов.
		#==========================================================================================#
		self.__status_code = None
		self.__content = None
		self.__json = None
		self.__text = None

	def generate_by_text(self, text: str | None):
		"""
		Генерирует интерпретации ответа на основе текста.
			text – текстовое представление ответа.
		"""

		if text:
			self.__status_code = None
			self.__text = text
			self.__content = bytes(text, encoding = "utf-8")
			self.__json = self.__TryDeserialize(text)

	def parse_response(self, response: requests.Response | httpx.Response | curl_cffi_requests.Response):
		"""
		Парсит ответ библиотеки в унифицированный формат.
			response – ответ библиотеки.
		"""

		self.__status_code = response.status_code
		self.__text = response.text
		self.__content = response.content
		self.__json = self.__TryDeserialize(response.text)

	def set_data(self, status_code: int | None = None, text: str | None = None, content: bytes | None = None, json: dict | None = None):
		"""
		Присваивает значения интерпретациям ответа.
			status_code – код ответа;\n
			text – текстовое представление ответа;\n
			content – бинарное представление ответа;\n
			json – десериализованное в словарь из JSON представление ответа.
		"""

		if status_code: self.__status_code = status_code
		if text: self.__text = text
		if content: self.__content = content
		if json: self.__json = json

#==========================================================================================#
# >>>>> ОСНОВНЫЕ КЛАССЫ <<<<< #
#==========================================================================================#

class WebConfig:
	"""Конфигурация запросчика."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def delay(self) -> float:
		"""# Интервал времени между повторами запросов."""

		return self.__Delay

	@property
	def headers(self) -> dict | None:
		"""Словарь заголвоков, приоритетно применяемых ко всем запросам."""

		Headers = self.__Headers

		if self.__UserAgent:
			if not Headers: Headers = dict()
			Headers["User-Agent"] = self.__UserAgent

		return Headers

	@property
	def lib(self) -> WebLibs:
		"""Тип используемой библиотеки."""

		return self.__UsedLib

	@property
	def logging(self) -> bool:
		"""Статус ведения логов при помощи стандартного модуля."""

		return self.__EnableLogging

	@property
	def redirecting(self) -> bool:
		"""Состояние режима автоматического перенаправления запросов."""

		return self.__EnableRedirecting

		"""Количество повторов неуспешных запросов."""

		return self.__Tries

	@property
	def retries(self):
		"""Количество повторов запроса при неудачном выполнении."""

		return self.__Retries

	@property
	def user_agent(self) -> str | None:
		"""Значение заголовка User-Agent."""

		return self.__UserAgent

	@property
	def good_statusses(self) -> list[int, None]:
		"""Список статусов, считающихся результатом успешного выполнения запроса."""

		return self.__GoodStatusses

	#==========================================================================================#
	# >>>>> МЕТОДЫ УСТАНОВКИ ЗНАЧЕНИЙ СВОЙСТВ <<<<< #
	#==========================================================================================#

	@good_statusses.setter
	def good_statusses(self, new_good_statusses: list[int, None]):
		"""Список статусов, считающихся результатом успешного выполнения запроса."""

		if type(new_good_statusses) == list: self.__GoodStatusses = new_good_statusses
		else: raise TypeError("list() required.")

	#==========================================================================================#
	# >>>>> МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self):
		"""Конфигурация запросчика."""

		#---> Генерация публичных динамических свойств.
		#==========================================================================================#
		self.curl_cffi = _curl_cffi_config()
		self.httpx = _httpx_config()
		self.requests = _requests_config()

		#---> Генерация приватных динамических свойств.
		#==========================================================================================#
		self.__UsedLib = WebLibs.requests
		self.__EnableRedirecting = True
		self.__EnableLogging = True
		self.__UserAgent = None
		self.__Headers = None
		self.__Retries = 0
		self.__GoodStatusses = [200, 404]
		self.__Delay = 0.25

	def add_header(self, name: str, value: int | bool | dict | str):
		"""
		Добавляет заголовок, приоритетно применяемый ко всем запросам.
			name – название заголовка;\n
			value – значение заголовка.
		"""

		if name.lower() == "user-agent": raise UserAgentRedefining()
		if self.__Headers == None: self.__Headers = dict()
		self.__Headers[name] = value

	def enable_logging(self, status: bool):
		"""
		Переключает ведение логов при помощи стандартного модуля.
			status – состояние режима.
		"""

		self.__EnableLogging = status

	def enable_redirecting(self, status: bool):
		"""
		Переключает режим автоматического перенаправления запросов.
			status – состояние режима.
		"""

		self.__EnableRedirecting = status

	def generate_user_agent(self,
		os: Iterable[str] = ("Windows", "Linux", "Ubuntu", "Chrome OS", "Mac OS X", "Android", "iOS"),
		browsers: Iterable[str] = ("Google", "Chrome", "Firefox", "Edge", "Opera"," Safari", "Android", "Yandex Browser", "Samsung Internet", "Opera Mobile", "Mobile Safari", "Firefox Mobile", "Firefox iOS", "Chrome Mobile", "Chrome Mobile iOS", "Mobile Safari UI/WKWebView", "Edge Mobile", "DuckDuckGo Mobile", "MiuiBrowser", "Whale", "Twitter", "Facebook", "Amazon Silk"),
		platforms: Iterable[str] = ("desktop", "mobile", "tablet")
	):
		"""
		Генерирует случайное значение User-Agent при помощи библиотеки fake_useragent.
			os – операционные системы;\n
			browsers – браузеры;\n
			platforms – типы платформ.
		"""

		self.__UserAgent = UserAgent(
			os = os,
			browsers = browsers,
			platforms = platforms
		).random

	def remove_header(self, name: str):
		"""
		Удаляет заголовок, приоритетно применяемый ко всем запросам.
			name – название заголовка.
		"""

		if name.lower() == "user-agent": raise UserAgentRedefining()
		del self.__Headers[name]

	def select_lib(self, lib: WebLibs):
		"""
		Задаёт тип используемой библиотеки.
			lib – тип библиотеки.
		"""

		self.__UsedLib = lib

	def set_delay(self, delay: float):
		"""
		Задаёт интервал времени между повторами запросов.
			delay – интервал.
		"""

		self.__Delay = delay

	def set_retries_count(self, retries: int):
		"""
		Задаёт количество повторов запроса при неудачном выполнении.
			retries – количество повторов.
		"""

		self.__Retries = retries

	def set_user_agent(self, user_agent: str | None):
		"""
		Задаёт значение заголовка UserAgent.
			user_agent – значение заголовка.
		"""

		self.__UserAgent = user_agent

class WebRequestor:
	"""Менеджер запросов."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#
	
	@property
	def cookies(self) -> dict | None:
		"""Словарь установленных Cookies."""

		Cookies = None
		if self.__Config.lib in [WebLibs.curl_cffi, WebLibs.requests]: Cookies = self.__Session.cookies.get_dict()
		elif self.__Config.lib == WebLibs.httpx: Cookies = dict(self.__Session.cookies)

		return Cookies

	#==========================================================================================#
	# >>>>> ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __Initialize(self):
		"""Инициализирует сессию."""

		if self.__Config.lib == WebLibs.curl_cffi:
			self.__Session = curl_cffi_requests.Session(
				allow_redirects = self.__Config.redirecting,
				impersonate = self.__Config.curl_cffi.fingerprint,
				http_version = self.__Config.curl_cffi.http_version
			)

		if self.__Config.lib == WebLibs.httpx:
			self.__Session = httpx.Client(http2 = self.__Config.httpx.http2, proxies = self.__GetProxy())
					
		if self.__Config.lib == WebLibs.requests:
			self.__Session = requests.Session()
		
	def __GetProxy(self, switch: bool = False) -> dict | None:
		"""
		Возвращает объект прокси для использования конкретной библиотекой.
			switch – переключает использование шифрования в протоколе HTTP.
		"""
		
		Proxy = None
		
		if len(self.__Proxies) > 0:
			Proxy = random.choice(self.__Proxies)
			Auth = ""
			if Proxy["login"] != None and Proxy["password"] != None: Auth = Proxy["login"] + ":" + Proxy["password"] + "@"
					
			if self.__Config.lib in [WebLibs.curl_cffi, WebLibs.requests]:
				Protocol = Proxy["protocol"]

				if switch and Protocol == "https": Protocol = "http"
				elif switch and Protocol == "http": Protocol = "https"

				Proxy = {
					Protocol: Protocol.replace("https", "http") + "://" + Auth + Proxy["host"] + ":" + Proxy["port"]
				}
			
			if self.__Config.lib == WebLibs.httpx:
				Proxy = {
					Proxy["protocol"] + "://": Proxy["protocol"].replace("https", "http") + "://" + Auth + Proxy["host"] + ":" + Proxy["port"]
				}
			
		return Proxy

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

	def __curl_cffi_GET(self, url: str, params: dict | None = None, headers: dict | None = None, cookies: dict | None = None) -> curl_cffi_requests.Response:
		"""
		Отправляет GET запрос через библиотеку curl_cffi.
			url – адрес запроса;\n
			params – словарь параметров запроса;\n
			headers – словарь заголовков;\n
			cookies – словарь куков.
		"""

		Response = WebResponse()
		headers = self.__MergeHeaders(headers)
		SwitchHTTP = set([False, self.__Config.requests.switch_proxy_protocol])

		for SwitchProtocol in SwitchHTTP:
			Response.parse_response(self.__Session.get(
				url = url,
				params = params,
				headers = headers,
				cookies = cookies,
				proxies = self.__GetProxy(SwitchProtocol)
			))

			if Response.status_code in self.__Config.good_statusses: break
			elif SwitchProtocol: Response = FirstResponse
			elif len(SwitchHTTP) > 1:
				FirstResponse = Response
				sleep(self.__Config.delay)

		return Response

	def __curl_cffi_POST(self, url: str, params: dict | None = None, headers: dict | None = None, cookies: dict | None = None, data: Any = None, json: dict | None = None) -> curl_cffi_requests.Response:
		"""
		Отправляет POST запрос через библиотеку curl_cffi.
			url – адрес запроса;\n
			params – словарь параметров запроса;\n
			headers – словарь заголовков;\n
			cookies – словарь куков;\n
			data – данные запроса;\n
			json – сериализованное тело запроса.
		"""

		Response = WebResponse()
		headers = self.__MergeHeaders(headers)
		SwitchHTTP = set([False, self.__Config.requests.switch_proxy_protocol])

		for SwitchProtocol in SwitchHTTP:
			Response.parse_response(self.__Session.post(
				url = url,
				params = params,
				headers = headers,
				cookies = cookies,
				data = data,
				json = json,
				proxies = self.__GetProxy(SwitchProtocol)
			))

			if Response.status_code in self.__Config.good_statusses: break
			elif SwitchProtocol: Response = FirstResponse
			elif len(SwitchHTTP) > 1:
				FirstResponse = Response
				sleep(self.__Config.delay)

		return Response
	
	#==========================================================================================#
	# >>>>> МЕТОДЫ ЗАПРОСОВ БИБЛИОТЕКИ HTTPX <<<<< #
	#==========================================================================================#

	def __httpx_GET(self, url: str, params: dict | None = None, headers: dict | None = None, cookies: dict | None = None) -> httpx.Response:
		"""
		Отправляет GET запрос через библиотеку httpx.
			url – адрес запроса;\n
			params – словарь параметров запроса;\n
			headers – словарь заголовков;\n
			cookies – словарь куков.
		"""

		Response = WebResponse()
		headers = self.__MergeHeaders(headers)

		Response.parse_response(self.__Session.get(
			url = url,
			params = params,
			headers = headers,
			cookies = cookies,
			follow_redirects = self.__Config.redirecting
		))

		return Response

	def __httpx_POST(self, url: str, params: dict | None = None, headers: dict | None = None, cookies: dict | None = None, data: Any = None, json: dict | None = None) -> httpx.Response:
		"""
		Отправляет POST запрос через библиотеку httpx.
			url – адрес запроса;\n
			params – словарь параметров запроса;\n
			headers – словарь заголовков;\n
			cookies – словарь куков;\n
			data – данные запроса;\n
			json – сериализованное тело запроса.
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
			follow_redirects = self.__Config.redirecting
		))

		return Response
	
	#==========================================================================================#
	# >>>>> МЕТОДЫ ЗАПРОСОВ БИБЛИОТЕКИ REQUESTS <<<<< #
	#==========================================================================================#

	def __requests_GET(self, url: str, params: dict | None = None, headers: dict | None = None, cookies: dict | None = None) -> requests.Response:
		"""
		Отправляет GET запрос через библиотеку requests.
			url – адрес запроса;\n
			params – словарь параметров запроса;\n
			headers – словарь заголовков;\n
			cookies – словарь куков.
		"""
		
		Response = WebResponse()
		headers = self.__MergeHeaders(headers)
		SwitchHTTP = set([False, self.__Config.requests.switch_proxy_protocol])
		FirstResponse = None

		for SwitchProtocol in SwitchHTTP:
			Response.parse_response(self.__Session.get(
				url = url,
				params = params,
				headers = headers,
				cookies = cookies,
				proxies = self.__GetProxy(SwitchProtocol),
				allow_redirects = self.__Config.redirecting
			))

			if Response.status_code in self.__Config.good_statusses: break
			elif SwitchProtocol: Response = FirstResponse
			elif len(SwitchHTTP) > 1:
				FirstResponse = Response
				sleep(self.__Config.delay)

		return Response
	
	def __requests_POST(self, url: str, params: dict | None = None, headers: dict | None = None, cookies: dict | None = None, data: Any = None, json: dict | None = None) -> requests.Response:
		"""
		Отправляет POST запрос через библиотеку requests.
			url – адрес запроса;\n
			params – словарь параметров запроса;\n
			headers – словарь заголовков;\n
			cookies – словарь куков;\n
			data – данные запроса;\n
			json – сериализованное тело запроса.
		"""
		
		Response = WebResponse()
		headers = self.__MergeHeaders(headers)
		SwitchHTTP = set([False, self.__Config.requests.switch_proxy_protocol])

		for SwitchProtocol in SwitchHTTP:
			Response.parse_response(self.__Session.post(
				url = url,
				params = params,
				headers = headers,
				cookies = cookies,
				data = data,
				json = json,
				proxies = self.__GetProxy(SwitchProtocol),
				allow_redirects = self.__Config.redirecting
			))

			if Response.status_code in self.__Config.good_statusses: break
			elif SwitchProtocol: Response = FirstResponse
			elif len(SwitchHTTP) > 1:
				FirstResponse = Response
				sleep(self.__Config.delay)

		return Response
		
	#==========================================================================================#
	# >>>>> ОБЩИЕ МЕТОДЫ <<<<< #
	#==========================================================================================#
		
	def __init__(self, config: WebConfig):
		"""
		Менеджер запросов.
			config – конфигурация библиотеки запросов.
		"""

		#---> Генерация динамических атрибутов.
		#==========================================================================================#
		self.__Proxies = list()
		self.__Config = config
		self.__Session = None

		self.__Initialize()

	def close(self):
		"""Закрывает менеджер запросов."""
			
		self.__Session.close()
		self.__Session = None
			
	def add_proxy(self, protocol: Protocols, host: str, port: int | str, login: str | None = None, password: str | None = None):
		"""
		Добавляет прокси для использования в запросах. Для библиотеки httpx реинициализирует сессию!
			protocol – протокол прокси-соединения;\n
			host – IP или адрес хоста;\n
			port – порт сервера;\n
			login – логин для авторизации;\n
			password – пароль для авторизации.
		"""
		
		self.__Proxies.append({
			"protocol": protocol.value,
			"host": host,
			"port": str(port),
			"login": login,
			"password": password
		})
		if self.__Config.lib == WebLibs.httpx: self.__Initialize()
	
	def remove_proxies(self):
		"""Удаляет данные используемых прокси."""

		self.__Proxies = list()
		if self.__Config.lib == WebLibs.httpx: self.__Initialize()

	#==========================================================================================#
	# >>>>> ЗАПРОСЫ <<<<< #
	#==========================================================================================#	
	
	def get(self, url: str, params: dict | None = None, headers: dict | None = None, cookies: dict | None = None) -> WebResponse:
		"""
		Отправляет GET запрос.
			url – адрес запроса;\n
			params – словарь параметров запроса;\n
			headers – словарь заголовков;\n
			cookies – словарь куков.
		"""

		tries = 1 + self.__Config.retries
		Response = WebResponse()
		Try = 0
		LibName = None
		
		while Try < tries and Response.status_code not in self.__Config.good_statusses:
			if Try > 0: sleep(self.__Config.delay)
			Try += 1
			
			try:

				if self.__Config.lib == WebLibs.curl_cffi:
					LibName = "CURL_CFFI"
					Response = self.__curl_cffi_GET(url, params, headers, cookies)

				if self.__Config.lib == WebLibs.httpx:
					LibName = "HTTPX"
					Response = self.__httpx_GET(url, params, headers, cookies)
				
				if self.__Config.lib == WebLibs.requests:
					LibName = "REQUESTS"
					Response = self.__requests_GET(url, params, headers, cookies)

			except Exception as ExceptionData:
				Response.generate_by_text(str(ExceptionData))
				if self.__Config.logging: Logger.error(f"[{LibName}-GET] Description: \"" + str(ExceptionData) + "\".")
		
		return Response
	
	def post(self, url: str, params: dict | None = None, headers: dict | None = None, cookies: dict | None = None, data: Any = None, json: dict | None = None) -> WebResponse:
		"""
		Отправляет POST запрос.
			url – адрес запроса;\n
			params – словарь параметров запроса;\n
			headers – словарь заголовков;\n
			cookies – словарь куков;\n
			data – отправляемые данные;\n
			json – сериализованное тело запроса.
		"""

		tries = 1 + self.__Config.retries
		Response = WebResponse()
		Try = 0
		LibName = None
		
		while Try < tries and Response.status_code not in self.__Config.good_statusses:
			if Try > 0: sleep(self.__Config.delay)
			Try += 1
			
			try:
				
				if self.__Config.lib == WebLibs.curl_cffi:
					LibName = "CURL_CFFI"
					Response = self.__curl_cffi_POST(url, params, headers, cookies, data, json)

				if self.__Config.lib == WebLibs.httpx:
					LibName = "HTTPX"
					Response = self.__httpx_POST(url, params, headers, cookies, data, json)
				
				if self.__Config.lib == WebLibs.requests:
					LibName = "REQUESTS"
					Response = self.__requests_POST(url, params, headers, cookies, data, json)
				
			except Exception as ExceptionData:
				Response.generate_by_text(str(ExceptionData))
				if self.__Config.logging: Logger.error(f"[{LibName}-POST] Description: \"" + str(ExceptionData) + "\".")
		
		return Response