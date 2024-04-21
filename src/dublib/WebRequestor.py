from .Exceptions.WebRequestor import *

from curl_cffi import requests as curl_cffi_requests
from fake_useragent import UserAgent

import importlib
import requests
import logging
import random
import httpx
import enum
import json

#==========================================================================================#
# >>>>> ДОПОЛНИТЕЛЬНЫЕ КОНФИГУРАЦИИ БИБЛИОТЕК ЗАПРОСОВ <<<<< #
#==========================================================================================#

class _curl_cffi_config:
	"""Дополнительная конфигурация библиотеки curl_cffi."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА ТОЛЬКО ДЛЯ ЧТЕНИЯ <<<<< #
	#==========================================================================================#

	@property
	def fingerprint(self) -> str | None:
		"""Отпечаток браузера."""

		return self.__Fingerprint

	@property
	def http2(self) -> bool:
		"""Состояние использования протокола HTTP/2 для запросов."""

		return self.__EnableHTTP2

	#==========================================================================================#
	# >>>>> МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self):
		"""Дополнительная конфигурация библиотеки curl_cffi."""

		#---> Генерация динамических свойств.
		#==========================================================================================#
		# Состояние использования протокола HTTP/2 для запросов.
		self.__EnableHTTP2 = False
		# Используемый отпечаток.
		self.__Fingerprint = None
	
	def enable_http2(self, status: bool):
		"""
		Переключает режим использования протокола HTTP/2 для запросов.
			status – состояние режима.
		"""

		self.__EnableHTTP2 = status

	def select_fingerprint(self, fingerprint: str | None):
		"""Выбирает используемый отпечаток браузера."""

		self.__Fingerprint = fingerprint

class _httpx_config:
	"""Дополнительная конфигурация библиотеки httpx."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА ТОЛЬКО ДЛЯ ЧТЕНИЯ <<<<< #
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

		#---> Генерация динамических свойств.
		#==========================================================================================#
		# Состояние использования протокола HTTP/2 для запросов.
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

class Protocols(enum.Enum):
	"""Перечисление типов протоколов."""
	
	SOCKS = "socks"
	HTTPS = "https"
	HTTP = "http"
	FTP = "ftp"

class WebLibs(enum.Enum):
	"""Перечисление поддерживаемых библиотек запросов."""

	curl_cffi = "curl_cffi"
	requests = "requests"
	httpx = "httpx"
		
class WebResponse:
	"""Унифицированная объектная структура ответа библиотек запросов."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА ТОЛЬКО ДЛЯ ЧТЕНИЯ <<<<< #
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

		#---> Генерация динамических свойств.
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
			self.__status_code = 200
			self.__text = text
			self.__content = bytes(text)
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
			status_code – код ответа;
			text – текстовое представление ответа;
			content – бинарное представление ответа;
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
	# >>>>> СВОЙСТВА ТОЛЬКО ДЛЯ ЧТЕНИЯ <<<<< #
	#==========================================================================================#

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

	@property
	def user_agent(self) -> str | None:
		"""Значение User-Agent."""

		return self.__UserAgent

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

		#---> Генерация приватных динамических свойств.
		#==========================================================================================#
		# Тип используемой библиотеки.
		self.__UsedLib = WebLibs.requests
		# Состояние режима автоматического перенаправления запросов.
		self.__EnableRedirecting = True
		# Статус ведения логов при помощи стандартного модуля.
		self.__EnableLogging = True
		# Значение заголовка UserAgent.
		self.__UserAgent = None
		# Словарь заголвоков, приоритетно применяемых ко всем запросам.
		self.__Headers = None

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

	def generate_user_agent(self, platform: str):
		"""
		Генерирует случайное значение User-Agent при помощи библиотеки fake_useragent.
			platform – тип платформы.
		"""

		self.__UserAgent = UserAgent(platforms = platform).random

	def remove_header(self, key: str):
		"""
		Удаляет заголовок, приоритетно применяемый ко всем запросам.
			key – название заголовка.
		"""

		# Если задаётся заголовок User-Agent, выбросить исключение.
		if key.lower() == "user-agent": raise UserAgentRedefining()
		# Удаление заголовка.
		del self.__Headers[key]

	def select_lib(self, lib: WebLibs):
		"""
		Задаёт тип используемой библиотеки.
			lib – тип библиотеки.
		"""

		self.__UsedLib = lib

	def set_header(self, key: str, value: int | bool | dict | str):
		"""
		Добавляет заголовок, приоритетно применяемый ко всем запросам.
			key – название заголовка;
			value – значение заголовка.
		"""

		# Если задаётся заголовок User-Agent, выбросить исключение.
		if key.lower() == "user-agent": raise UserAgentRedefining()
		# Если заголовки не объявлены, привести их к словарному типу.
		if self.__Headers == None: self.__Headers = dict()
		# Добавление заголовка.
		self.__Headers[key] = value

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
			self.__Session = curl_cffi_requests.Session(allow_redirects = self.__Config.redirecting)

		# Если используется библиотека httpx.	
		if self.__Config.lib == WebLibs.httpx:
			# Инициализация сессии.
			self.__Session = httpx.Client(http2 = self.__Config.httpx.http2, proxies = self.__GetProxy())
					
		# Если используется библиотека requests.		
		if self.__Config.lib == WebLibs.requests:
			# Инициализация сессии.
			self.__Session = requests.Session()
		
	def __GetProxy(self) -> dict | None:
		"""Возвращает объект прокси для использования конкретной библиотекой."""
		
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
				# Создание объекта прокси.
				Proxy = {
					Proxy["protocol"]: Proxy["protocol"].replace("https", "http") + "://" + Auth + Proxy["host"] + ":" + Proxy["port"]
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
			url – адрес запроса;
			params – словарь параметров запроса;
			headers – словарь заголовков;
			cookies – словарь куков.
		"""

		# Эмуляция ответа.
		Response = WebResponse()
		# Обработка заголовков.
		headers = self.__MergeHeaders(headers)
		# Выполнение запроса.
		Response.parse_response(self.__Session.get(url, params = params, headers = headers, cookies = cookies, proxies = self.__GetProxy()))

		return Response

	def __curl_cffi_POST(self, url: str, params: dict | None = None, headers: dict | None = None, cookies: dict | None = None, data: any = None, json: dict | None = None) -> curl_cffi_requests.Response:
		"""
		Отправляет POST запрос через библиотеку curl_cffi.
			url – адрес запроса;
			params – словарь параметров запроса;
			headers – словарь заголовков;
			cookies – словарь куков;
			data – данные запроса;
			json – сериализованное тело запроса.
		"""

		# Эмуляция ответа.
		Response = WebResponse()
		# Обработка заголовков.
		headers = self.__MergeHeaders(headers)
		# Выполнение запроса.
		Response.parse_response(self.__Session.post(url, params = params, headers = headers, cookies = cookies, data = data, json = json, proxies = self.__GetProxy()))
		
		return Response
	
	#==========================================================================================#
	# >>>>> МЕТОДЫ ЗАПРОСОВ БИБЛИОТЕКИ HTTPX <<<<< #
	#==========================================================================================#

	def __httpx_GET(self, url: str, params: dict | None = None, headers: dict | None = None, cookies: dict | None = None) -> httpx.Response:
		"""
		Отправляет GET запрос через библиотеку httpx.
			url – адрес запроса;
			params – словарь параметров запроса;
			headers – словарь заголовков;
			cookies – словарь куков.
		"""

		# Эмуляция ответа.
		Response = WebResponse()
		# Обработка заголовков.
		headers = self.__MergeHeaders(headers)
		# Выполнение запроса.
		Response.parse_response(self.__Session.get(url, params = params, headers = headers, cookies = cookies, follow_redirects = self.__Config.redirecting))

		return Response

	def __httpx_POST(self, url: str, params: dict | None = None, headers: dict | None = None, cookies: dict | None = None, data: any = None, json: dict | None = None) -> httpx.Response:
		"""
		Отправляет POST запрос через библиотеку httpx.
			url – адрес запроса;
			params – словарь параметров запроса;
			headers – словарь заголовков;
			cookies – словарь куков;
			data – данные запроса;
			json – сериализованное тело запроса.
		"""

		# Эмуляция ответа.
		Response = WebResponse()
		# Обработка заголовков.
		headers = self.__MergeHeaders(headers)
		# Выполнение запроса.
		Response.parse_response(self.__Session.post(url, params = params, headers = headers, cookies = cookies, data = data, json = json, follow_redirects = self.__Config.redirecting))
		
		return Response
	
	#==========================================================================================#
	# >>>>> МЕТОДЫ ЗАПРОСОВ БИБЛИОТЕКИ REQUESTS <<<<< #
	#==========================================================================================#

	def __requests_GET(self, url: str, params: dict | None = None, headers: dict | None = None, cookies: dict | None = None) -> requests.Response:
		"""
		Отправляет GET запрос через библиотеку requests.
			url – адрес запроса;
			params – словарь параметров запроса;
			headers – словарь заголовков;
			cookies – словарь куков.
		"""
		
		# Эмуляция ответа.
		Response = WebResponse()
		# Обработка заголовков.
		headers = self.__MergeHeaders(headers)
		
		try:
			# Выполнение запроса.
			Response.parse_response(self.__Session.get(url, params = params, headers = headers, cookies = cookies, proxies = self.__GetProxy(), allow_redirects = self.__Config.redirecting))

		except requests.exceptions.ProxyError as ExceptionData:
			# Установка значений ответа.
			Response.generate_by_text(str(ExceptionData))
			Response.set_data(status_code = 407)

		return Response
	
	def __requests_POST(self, url: str, params: dict | None = None, headers: dict | None = None, cookies: dict | None = None, data: any = None, json: dict | None = None) -> requests.Response:
		"""
		Отправляет POST запрос через библиотеку requests.
			url – адрес запроса;
			params – словарь параметров запроса;
			headers – словарь заголовков;
			cookies – словарь куков;
			data – данные запроса;
			json – сериализованное тело запроса.
		"""
		
		# Эмуляция ответа.
		Response = WebResponse()
		# Обработка заголовков.
		headers = self.__MergeHeaders(headers)

		try:
			# Выполнение запроса.
			Response.parse_response(self.__Session.post(url, params = params, headers = headers, cookies = cookies, data = data, json = json, proxies = self.__GetProxy(), allow_redirects = self.__Config.redirecting))
		
		except requests.exceptions.ProxyError as ExceptionData:
			# Установка значений ответа.
			Response.generate_by_text(str(ExceptionData))
			Response.set_data(status_code = 407)

		return Response
		
	#==========================================================================================#
	# >>>>> ОБЩИЕ МЕТОДЫ <<<<< #
	#==========================================================================================#
		
	def __init__(self, config: WebConfig):
		"""
		Менеджер запросов.
			config – конфигурация библиотеки запросов.
		"""

		#---> Генерация динамических свойств.
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
		Добавляет прокси для использования в запросах. Не работает с Selenium.
			protocol – протокол прокси-соединения;
			host – IP или адрес хоста;
			port – порт сервера;
			login – логин для авторизации;
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
	
	#==========================================================================================#
	# >>>>> ЗАПРОСЫ <<<<< #
	#==========================================================================================#	
	
	def get(self, url: str, params: dict | None = None, headers: dict | None = None, cookies: dict | None = None, tries: int = 1) -> WebResponse:
		"""
		Отправляет GET запрос.
			url – адрес запроса;
			params – словарь параметров запроса;
			headers – словарь заголовков;
			cookies – словарь куков;
			tries – количество попыток повтора при неудачном выполнении.
		"""

		# Ответ.
		Response = WebResponse()
		# Индекс попытки.
		Try = 0
		# Название библиотеки.
		LibName = None
		
		# Пока не превышено количество попыток.
		while Try < tries and Response.status_code != 200:
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
				if self.__Config.logging: logging.error(f"[{LibName}-GET] Description: \"" + str(ExceptionData) + "\".")
		
		return Response
	
	def post(self, url: str, params: dict | None = None, headers: dict | None = None, cookies: dict | None = None, data: any = None, json: dict | None = None, tries: int = 1) -> WebResponse:
		"""
		Отправляет POST запрос.
			url – адрес запроса;
			params – словарь параметров запроса;
			headers – словарь заголовков;
			cookies – словарь куков;
			data – отправляемые данные;
			json – сериализованное тело запроса;
			tries – количество попыток повтора при неудачном выполнении.
		"""

		# Ответ.
		Response = WebResponse()
		# Индекс попытки.
		Try = 0
		# Название библиотеки.
		LibName = None
		
		# Пока не превышено количество попыток.
		while Try < tries and Response.status_code != 200:
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
				if self.__Config.logging: logging.error(f"[{LibName}-POST] Description: \"" + str(ExceptionData) + "\".")
		
		return Response