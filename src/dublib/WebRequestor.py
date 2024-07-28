from .Exceptions.WebRequestor import *

from curl_cffi import requests as curl_cffi_requests
from curl_cffi import CurlHttpVersion
from fake_useragent import UserAgent
from time import sleep

import requests
import logging
import random
import httpx
import enum
import json

#==========================================================================================#
# >>>>> ИНИЦИАЛИЗАЦИЯ СИСТЕМЫ ЛОГГИРОВАНИЯ <<<<< #
#==========================================================================================#

# Инициализация модуля ведения логов.
Logger = logging.getLogger(__name__)
Logger.addHandler(logging.NullHandler())
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
		# Версия используемого протокола HTTP.
		self.__HttpVersion = CurlHttpVersion.V1_1
		# Используемый отпечаток.
		self.__Fingerprint = None
		# Состояние автоматического переключения HTTP/HTTPS версий протокола при ошибках.
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
		# Состояние использования протокола HTTP/2 для запросов.
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
		# Состояние автоматического переключения HTTP/HTTPS версий протокола прокси при ошибках.
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
		# Результат десериализации.
		Result = None

		try:
			# Попытка десериализации.
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
		# Статус ответа.
		self.__status_code = None
		# Бинарное представление ответа.
		self.__content = None
		# Десериализованное в словарь из JSON представление ответа.
		self.__json = None
		# Текстовое представление ответа.
		self.__text = None

	def generate_by_text(self, text: str | None):
		"""
		Генерирует интерпретации ответа на основе текста.
			text – текстовое представление ответа.
		"""

		# Если запрос успешен.
		if text:
			# Установка интерпретаций.
			self.__status_code = None
			self.__text = text
			self.__content = bytes(text, encoding = "utf-8")
			self.__json = self.__TryDeserialize(text)

	def parse_response(self, response: requests.Response | httpx.Response | curl_cffi_requests.Response):
		"""
		Парсит ответ библиотеки в унифицированный формат.
			response – ответ библиотеки.
		"""

		# Установка кода ответа.
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

		# Проверка и установка типов значений.
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

		# Возвращаемый словарь заголовков.
		Headers = self.__Headers

		# Если установлено значение User-Agent.
		if self.__UserAgent:
			# Если заголовки не определены, привести их к словарному типу.
			if not Headers: Headers = dict()
			# Добавление заголовка User-Agent.
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
	def tries(self):
		"""Количество повторов запроса при неудачном выполнении."""

		return self.__Tries

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

		# Если указан нужный тип, сохранить, иначе выбросить исключение.
		if type(new_good_statusses) == list: self.__GoodStatusses = new_good_statusses
		else: raise TypeError("list() required.")

	#==========================================================================================#
	# >>>>> МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self):
		"""Конфигурация запросчика."""

		#---> Генерация публичных динамических свойств.
		#==========================================================================================#
		# Дополнительные конфигурации библиотек.
		self.curl_cffi = _curl_cffi_config()
		self.httpx = _httpx_config()
		self.requests = _requests_config()

		#---> Генерация приватных динамических свойств.
		#==========================================================================================#
		# Тип используемой библиотеки.
		self.__UsedLib = WebLibs.requests
		# Состояние режима автоматического перенаправления запросов.
		self.__EnableRedirecting = True
		# Статус ведения логов при помощи стандартного модуля.
		self.__EnableLogging = True
		# Значение заголовка User-Agent.
		self.__UserAgent = None
		# Словарь заголвоков, приоритетно применяемых ко всем запросам.
		self.__Headers = None
		# Количество повторов неуспешных запросов.
		self.__Tries = 1
		# Список статусов, считающихся результатом успешного выполнения запроса.
		self.__GoodStatusses = [200, 404]
		# Интервал времени между повторами запросов.
		self.__Delay = 0.25

	def add_header(self, name: str, value: int | bool | dict | str):
		"""
		Добавляет заголовок, приоритетно применяемый ко всем запросам.
			name – название заголовка;\n
			value – значение заголовка.
		"""

		# Если задаётся заголовок User-Agent, выбросить исключение.
		if name.lower() == "user-agent": raise UserAgentRedefining()
		# Если заголовки не объявлены, привести их к словарному типу.
		if self.__Headers == None: self.__Headers = dict()
		# Добавление заголовка.
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
		os: list[str] | str = ["windows", "macos", "linux"],
		browsers: list[str] | str = ["chrome", "edge", "firefox", "safari"],
		platforms: list[str] | str = ["pc", "mobile", "tablet"]
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

		# Если задаётся заголовок User-Agent, выбросить исключение.
		if name.lower() == "user-agent": raise UserAgentRedefining()
		# Удаление заголовка.
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

	def set_tries_count(self, tries_count: int):
		"""
		Задаёт количество повторов запроса при неудачном выполнении.
			tries_count – количество повторов.
		"""

		self.__Tries = tries_count

	def set_user_agent(self, user_agent: str | None):
		"""
		Задаёт значение заголовка UserAgent.
			user_agent – значение заголовка.
		"""

		self.__UserAgent = user_agent

class WebRequestor:
	"""Менеджер запросов."""
	
	#==========================================================================================#
	# >>>>> ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __Initialize(self):
		"""Инициализирует сессию."""

		# Если используется библиотека curl_cffi.	
		if self.__Config.lib == WebLibs.curl_cffi:
			# Инициализация сессии.
			self.__Session = curl_cffi_requests.Session(
				allow_redirects = self.__Config.redirecting,
				impersonate = self.__Config.curl_cffi.fingerprint,
				http_version = self.__Config.curl_cffi.http_version
			)

		# Если используется библиотека httpx.	
		if self.__Config.lib == WebLibs.httpx:
			# Инициализация сессии.
			self.__Session = httpx.Client(http2 = self.__Config.httpx.http2, proxies = self.__GetProxy())
					
		# Если используется библиотека requests.		
		if self.__Config.lib == WebLibs.requests:
			# Инициализация сессии.
			self.__Session = requests.Session()
		
	def __GetProxy(self, switch: bool = False) -> dict | None:
		"""
		Возвращает объект прокси для использования конкретной библиотекой.
			switch – переключает использование шифрования в протоколе HTTP.
		"""
		
		# Объект прокси.
		Proxy = None
		
		# Если задан хотя бы один прокси..
		if len(self.__Proxies) > 0:
			# Случайный выбор прокси.
			Proxy = random.choice(self.__Proxies)
			# Данные авторизации.
			Auth = ""
			# Если указаны логин и пароль, составить авторизационные данные.
			if Proxy["login"] != None and Proxy["password"] != None: Auth = Proxy["login"] + ":" + Proxy["password"] + "@"
					
			# Если используется библиотека curl_cffi или requests.
			if self.__Config.lib in [WebLibs.curl_cffi, WebLibs.requests]:
				# Идентификатор протокола.
				Protocol = Proxy["protocol"]

				# Если включено изменение протокола, подставить альтернативную версию.
				if switch and Protocol == "https": Protocol = "http"
				elif switch and Protocol == "http": Protocol = "https"

				# Создание объекта прокси.
				Proxy = {
					Protocol: Protocol.replace("https", "http") + "://" + Auth + Proxy["host"] + ":" + Proxy["port"]
				}
			
			# Если используется библиотека httpx.	
			if self.__Config.lib == WebLibs.httpx:
				# Создание объекта прокси.
				Proxy = {
					Proxy["protocol"] + "://": Proxy["protocol"].replace("https", "http") + "://" + Auth + Proxy["host"] + ":" + Proxy["port"]
				}
			
		return Proxy

	def __MergeHeaders(self, headers: dict | None) -> dict | None:
		"""Объединяет заголовки конфигурации и параметров запроса."""

		# Если конфигурация содержит заголовки.
		if self.__Config.headers:

			# Если переданы заголовки.
			if headers: 
				# Объединение заголовков с приоритетом конфигурационным.
				headers = self.__Config.headers | headers
				
			else:
				# Установка словаря заголовков из конфигурации.
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

		# Эмуляция ответа.
		Response = WebResponse()
		# Обработка заголовков.
		headers = self.__MergeHeaders(headers)
		# Статусы подмены HTTP/S протокола прокси.
		SwitchHTTP = set([False, self.__Config.requests.switch_proxy_protocol])

		try:

			# Для каждого статуса подмены.
			for SwitchProtocol in SwitchHTTP:
				# Выполнение запроса.
				Response.parse_response(self.__Session.get(
					url = url,
					params = params,
					headers = headers,
					cookies = cookies,
					proxies = self.__GetProxy(SwitchProtocol)
				))

				# Если запрос успешен, прервать выполнение.
				if Response.status_code in self.__Config.good_statusses: break
				# Иначе, если переключался протокол, вернуть оригинальный ответ.
				elif SwitchProtocol: Response = FirstResponse
				# Иначе, если включено переключение протоколов.
				elif len(SwitchHTTP) > 1:
					# Запоминание первого ответа.
					FirstResponse = Response
					# Выжидание интервала.
					sleep(self.__Config.delay)
		
		except Exception as ExceptionData:
			# Установка значений ответа.
			Response.generate_by_text(str(ExceptionData))

		return Response

	def __curl_cffi_POST(self, url: str, params: dict | None = None, headers: dict | None = None, cookies: dict | None = None, data: any = None, json: dict | None = None) -> curl_cffi_requests.Response:
		"""
		Отправляет POST запрос через библиотеку curl_cffi.
			url – адрес запроса;\n
			params – словарь параметров запроса;\n
			headers – словарь заголовков;\n
			cookies – словарь куков;\n
			data – данные запроса;\n
			json – сериализованное тело запроса.
		"""

		# Эмуляция ответа.
		Response = WebResponse()
		# Обработка заголовков.
		headers = self.__MergeHeaders(headers)
		# Статусы подмены HTTP/S протокола прокси.
		SwitchHTTP = set([False, self.__Config.requests.switch_proxy_protocol])

		try:

			# Для каждого статуса подмены.
			for SwitchProtocol in SwitchHTTP:
				# Выполнение запроса.
				Response.parse_response(self.__Session.post(
					url = url,
					params = params,
					headers = headers,
					cookies = cookies,
					data = data,
					json = json,
					proxies = self.__GetProxy(SwitchProtocol)
				))

				# Если запрос успешен, прервать выполнение.
				if Response.status_code in self.__Config.good_statusses: break
				# Иначе, если переключался протокол, вернуть оригинальный ответ.
				elif SwitchProtocol: Response = FirstResponse
				# Иначе, если включено переключение протоколов.
				elif len(SwitchHTTP) > 1:
					# Запоминание первого ответа.
					FirstResponse = Response
					# Выжидание интервала.
					sleep(self.__Config.delay)
		
		except Exception as ExceptionData:
			# Установка значений ответа.
			Response.generate_by_text(str(ExceptionData))

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

		# Эмуляция ответа.
		Response = WebResponse()
		# Обработка заголовков.
		headers = self.__MergeHeaders(headers)

		try:
			# Выполнение запроса.
			Response.parse_response(self.__Session.get(
				uel = url,
				params = params,
				headers = headers,
				cookies = cookies,
				follow_redirects = self.__Config.redirecting
			))
		
		except Exception as ExceptionData:
			# Установка значений ответа.
			Response.generate_by_text(str(ExceptionData))

		return Response

	def __httpx_POST(self, url: str, params: dict | None = None, headers: dict | None = None, cookies: dict | None = None, data: any = None, json: dict | None = None) -> httpx.Response:
		"""
		Отправляет POST запрос через библиотеку httpx.
			url – адрес запроса;\n
			params – словарь параметров запроса;\n
			headers – словарь заголовков;\n
			cookies – словарь куков;\n
			data – данные запроса;\n
			json – сериализованное тело запроса.
		"""

		# Эмуляция ответа.
		Response = WebResponse()
		# Обработка заголовков.
		headers = self.__MergeHeaders(headers)

		try:
			# Выполнение запроса.
			Response.parse_response(self.__Session.post(
				url = url,
				params = params,
				headers = headers,
				cookies = cookies,
				data = data,
				json = json,
				follow_redirects = self.__Config.redirecting
			))

		except Exception as ExceptionData:
			# Установка значений ответа.
			Response.generate_by_text(str(ExceptionData))

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
		
		# Эмуляция ответа.
		Response = WebResponse()
		# Обработка заголовков.
		headers = self.__MergeHeaders(headers)
		# Статусы подмены HTTP/S протокола прокси.
		SwitchHTTP = set([False, self.__Config.requests.switch_proxy_protocol])
		# Результат первого запроса.
		FirstResponse = None

		try:

			# Для каждого статуса подмены.
			for SwitchProtocol in SwitchHTTP:
				# Выполнение запроса.
				Response.parse_response(self.__Session.get(
					url = url,
					params = params,
					headers = headers,
					cookies = cookies,
					proxies = self.__GetProxy(SwitchProtocol),
					allow_redirects = self.__Config.redirecting
				))

				# Если запрос успешен, прервать выполнение.
				if Response.status_code in self.__Config.good_statusses: break
				# Иначе, если переключался протокол, вернуть оригинальный ответ.
				elif SwitchProtocol: Response = FirstResponse
				# Иначе, если включено переключение протоколов.
				elif len(SwitchHTTP) > 1:
					# Запоминание первого ответа.
					FirstResponse = Response
					# Выжидание интервала.
					sleep(self.__Config.delay)
		
		except Exception as ExceptionData:
			# Установка значений ответа.
			Response.generate_by_text(str(ExceptionData))

		return Response
	
	def __requests_POST(self, url: str, params: dict | None = None, headers: dict | None = None, cookies: dict | None = None, data: any = None, json: dict | None = None) -> requests.Response:
		"""
		Отправляет POST запрос через библиотеку requests.
			url – адрес запроса;\n
			params – словарь параметров запроса;\n
			headers – словарь заголовков;\n
			cookies – словарь куков;\n
			data – данные запроса;\n
			json – сериализованное тело запроса.
		"""
		
		# Эмуляция ответа.
		Response = WebResponse()
		# Обработка заголовков.
		headers = self.__MergeHeaders(headers)
		# Статусы подмены HTTP/S протокола прокси.
		SwitchHTTP = set([False, self.__Config.requests.switch_proxy_protocol])

		try:

			# Для каждого статуса подмены.
			for SwitchProtocol in SwitchHTTP:
				# Выполнение запроса.
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

				# Если запрос успешен, прервать выполнение.
				if Response.status_code in self.__Config.good_statusses: break
				# Иначе, если переключался протокол, вернуть оригинальный ответ.
				elif SwitchProtocol: Response = FirstResponse
				# Иначе, если включено переключение протоколов.
				elif len(SwitchHTTP) > 1:
					# Запоминание первого ответа.
					FirstResponse = Response
					# Выжидание интервала.
					sleep(self.__Config.delay)
		
		except Exception as ExceptionData:
			# Установка значений ответа.
			Response.generate_by_text(str(ExceptionData))

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
		# Список прокси.
		self.__Proxies = list()
		# Конфигурация.
		self.__Config = config
		# Сессия запросов.
		self.__Session = None

		# Инициализация сессии.
		self.__Initialize()

	def close(self):
		"""Закрывает менеджер запросов."""
			
		# Закрытие и обнуление сессии.
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
		
		# Добавление прокси в список.
		self.__Proxies.append({
			"protocol": protocol.value,
			"host": host,
			"port": str(port),
			"login": login,
			"password": password
		})
		# Если используется библиотека httpx, реинициализировать сессию.
		if self.__Config.lib == WebLibs.httpx: self.__Initialize()
	
	def remove_proxies(self):
		"""Удаляет данные используемых прокси."""

		# Очистка данных.
		self.__Proxies = list()
		# Если используется библиотека httpx, реинициализировать сессию.
		if self.__Config.lib == WebLibs.httpx: self.__Initialize()

	#==========================================================================================#
	# >>>>> ЗАПРОСЫ <<<<< #
	#==========================================================================================#	
	
	def get(self, url: str, params: dict | None = None, headers: dict | None = None, cookies: dict | None = None, tries: int | None = None) -> WebResponse:
		"""
		Отправляет GET запрос.
			url – адрес запроса;\n
			params – словарь параметров запроса;\n
			headers – словарь заголовков;\n
			cookies – словарь куков;\n
			tries – количество попыток повтора при неудачном выполнении.
		"""

		# Если не указано количество повторов, использовать оное из конфигурации.
		if tries == None: tries = self.__Config.tries
		# Ответ.
		Response = WebResponse()
		# Индекс попытки.
		Try = 0
		# Название библиотеки.
		LibName = None
		
		# Пока не превышено количество попыток.
		while Try < tries and Response.status_code not in self.__Config.good_statusses:
			# Если не первая попытка, выждать интервал.
			if Try > 0: sleep(self.__Config.delay)
			# Инкремент повтора.
			Try += 1
			
			try:

				# Если используется библиотека curl_cffi.
				if self.__Config.lib == WebLibs.curl_cffi:
					# Установка имени библиотеки.
					LibName = "CURL_CFFI"
					# Выполнение запроса.
					Response = self.__curl_cffi_GET(url, params, headers, cookies)

				# Если используется библиотека httpx.
				if self.__Config.lib == WebLibs.httpx:
					# Установка имени библиотеки.
					LibName = "HTTPX"
					# Выполнение запроса.
					Response = self.__httpx_GET(url, params, headers, cookies)
				
				# Если используется библиотека requests.
				if self.__Config.lib == WebLibs.requests:
					# Установка имени библиотеки.
					LibName = "REQUESTS"
					# Выполнение запроса.
					Response = self.__requests_GET(url, params, headers, cookies)

			except Exception as ExceptionData:
				# Запись в лог ошибки: не удалось выполнить запрос.
				if self.__Config.logging: Logger.error(f"[{LibName}-GET] Description: \"" + str(ExceptionData) + "\".")
		
		return Response
	
	def post(self, url: str, params: dict | None = None, headers: dict | None = None, cookies: dict | None = None, data: any = None, json: dict | None = None, tries: int | None = None) -> WebResponse:
		"""
		Отправляет POST запрос.
			url – адрес запроса;\n
			params – словарь параметров запроса;\n
			headers – словарь заголовков;\n
			cookies – словарь куков;\n
			data – отправляемые данные;\n
			json – сериализованное тело запроса;\n
			tries – количество попыток повтора при неудачном выполнении.
		"""

		# Если не указано количество повторов, использовать оное из конфигурации.
		if tries == None: tries = self.__Config.tries
		# Ответ.
		Response = WebResponse()
		# Индекс попытки.
		Try = 0
		# Название библиотеки.
		LibName = None
		
		# Пока не превышено количество попыток.
		while Try < tries and Response.status_code not in self.__Config.good_statusses:
			# Если не первая попытка, выждать интервал.
			if Try > 0: sleep(self.__Config.delay)
			# Инкремент повтора.
			Try += 1
			
			try:
				
				# Если используется библиотека curl_cffi.
				if self.__Config.lib == WebLibs.curl_cffi:
					# Установка имени библиотеки.
					LibName = "CURL_CFFI"
					# Выполнение запроса.
					Response = self.__curl_cffi_POST(url, params, headers, cookies, data, json)

				# Если используется библиотека httpx.
				if self.__Config.lib == WebLibs.httpx:
					# Установка имени библиотеки.
					LibName = "HTTPX"
					# Выполнение запроса.
					Response = self.__httpx_POST(url, params, headers, cookies, data, json)
				
				# Если используется библиотека requests.
				if self.__Config.lib == WebLibs.requests:
					# Установка имени библиотеки.
					LibName = "REQUESTS"
					# Выполнение запроса.
					Response = self.__requests_POST(url, params, headers, cookies, data, json)
				
			except Exception as ExceptionData:
				# Запись в лог ошибки: не удалось выполнить запрос.
				if self.__Config.logging: Logger.error(f"[{LibName}-POST] Description: \"" + str(ExceptionData) + "\".")
		
		return Response