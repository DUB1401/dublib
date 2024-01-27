from fake_useragent import UserAgent as UserAgentGenerator
from dublib.Exceptions.WebRequestor import *

import importlib
import requests
import logging
import random
import httpx
import enum

#==========================================================================================#
# >>>>> ВСПОМОГАТЕЛЬНЫЕ ТИПЫ ДАННЫХ <<<<< #
#==========================================================================================#

class Browsers(enum.Enum):
	"""
	Перечисление типов поддерживаемых браузеров.
	"""

	Chrome = "Google Chrome"
	#Firefox = "Mozilla Firefox"
	#Edge = "Microsoft Edge"

class Protocols(enum.Enum):
	"""
	Перечисление типов протоколов.
	"""
	
	FTP = "ftp"
	HTTP = "http"
	HTTPS = "https"
	SOCKS = "socks"

class HttpxConfig:
	"""
	Конфигурация библиотеки httpx.
	"""
	
	#==========================================================================================#
	# >>>>> СВОЙСТВА ТОЛЬКО ДЛЯ ЧТЕНИЯ <<<<< #
	#==========================================================================================#
	
	@property
	def headers(self) -> dict:
		return self.__Headers.copy()
	
	@property
	def http2(self) -> bool:
		return self.__HTTP2
	
	@property
	def redirecting(self) -> bool:
		return self.__Redirecting
	
	#==========================================================================================#
	# >>>>> МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, auto_user_agent: bool = True):
		"""
		Конфигурация библиотеки httpx.
			auto_user_agent – переключает автоматическую генерацию заголовка User-Agent.
		"""
		
		#---> Генерация динамических свойств.
		#==========================================================================================#
		# Заголовки запросов.
		self.__Headers = dict()
		# Состояние: выполнять ли переадресацию.
		self.__Redirecting = True
		# Состояние: использовать ли HTTP2.0.
		self.__HTTP2 = True
		
		# Если указано, сгенерировать заголовок User-Agent.
		if auto_user_agent == True: self.__Headers = {"User-Agent": UserAgentGenerator().chrome}
		
	def add_header(self, key: str, value: int | str):
		"""
		Добавляет пользовательский заголовок запроса.
			key – ключ заголовка;
			value – значение заголовка.
		"""

		# Запись заголовка.
		self.__Headers[key] = value
		
	def enable_http2(self, status: bool):
		"""
		Переключает использование протокола HTTP2.0.
			status – статус использования протокола.
		"""
		
		self.__HTTP2 = status
		
	def enable_redirecting(self, status: bool):
		"""
		Переключает автоматическое перенаправление HTTP.
			status – статус перенаправления.
		"""
		
		self.__Redirecting = status
		
	def set_referer(self, referer: str):
		"""
		Задаёт пользовательское значение заголовка Referer.
			referer – новое значение заголовка.
		"""

		self.__Headers["Referer"] = referer
		
	def set_user_agent(self, user_agent: str):
		"""
		Задаёт пользовательское значение заголовка User-Agent.
			user_agent – новое значение заголовка.
		"""

		self.__Headers["User-Agent"] = user_agent

class RequestsConfig:
	"""
	Конфигурация библиотеки requests.
	"""
	
	#==========================================================================================#
	# >>>>> СВОЙСТВА ТОЛЬКО ДЛЯ ЧТЕНИЯ <<<<< #
	#==========================================================================================#
	
	@property
	def headers(self) -> dict:
		return self.__Headers.copy()
	
	@property
	def redirecting(self) -> bool:
		return self.__Redirecting
	
	#==========================================================================================#
	# >>>>> МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, auto_user_agent: bool = True):
		"""
		Конфигурация библиотеки requests.
			auto_user_agent – переключает автоматическую генерацию заголовка User-Agent.
		"""
		
		#---> Генерация динамических свойств.
		#==========================================================================================#
		# Заголовки запросов.
		self.__Headers = dict()
		# Состояние: выполнять ли переадресацию.
		self.__Redirecting = True
		
		# Если указано, сгенерировать заголовок User-Agent.
		if auto_user_agent == True: self.__Headers = {"User-Agent": UserAgentGenerator().chrome}
		
	def add_header(self, key: str, value: int | str):
		"""
		Добавляет пользовательский заголовок запроса.
			key – ключ заголовка;
			value – значение заголовка.
		"""

		# Запись заголовка.
		self.__Headers[key] = Value
		
	def enable_redirecting(self, status: bool):
		"""
		Переключает автоматическое перенаправление HTTP.
			status – статус перенаправления.
		"""
		
		self.__Redirecting = status
		
	def set_referer(self, referer: str):
		"""
		Задаёт пользовательское значение заголовка Referer.
			referer – новое значение заголовка.
		"""

		self.__Headers["Referer"] = referer
		
	def set_user_agent(self, user_agent: str):
		"""
		Задаёт пользовательское значение заголовка User-Agent.
			user_agent – новое значение заголовка.
		"""

		self.__Headers["User-Agent"] = user_agent
	
class SeleniumConfig:
	"""
	Конфигурация библиотеки Selenium.
	"""
	
	def __init__(
			self,
			browser_type: Browsers = Browsers.Chrome,
			headless: bool = False,
			page_load_timeout: int = 75,
			script_timeout: int = 75,
			window_width: int = 1920,
			WindowHeight: int = 1080
		):
		"""
		Конфигурация библиотеки Selenium.
			browser_type – наименование используемого браузера;
			headless – переключатель безоконного режима;
			page_load_timeout – тайм-аут загрузки страницы;
			script_timeout – тайм-аут выполнения JavaScript;
			window_width – ширина окна;
			window_height – высота окна.
		"""
		
		#---> Генерация динамических свойств.
		#==========================================================================================#
		# Тип используемого браузера.
		self.BrowserType = browser_type
		# Состояние: активен ли безрабочный режим.
		self.Headless = headless
		# Тайм-аут загрузки страницы.
		self.PageLoadTimeout = page_load_timeout
		# Тайм-аут выполнения JavaScript.
		self.ScriptTimeout = script_timeout
		# Ширина окна.
		self.WindowWidth = window_width
		# Высота окна.
		self.WindowHeight = window_height
		
	def set_browser_type(self, browser_type: Browsers):
		"""
		Задаёт используемый браузер.
			BrowserType – браузер.
		"""

		self.BrowserType = browser_type
		
	def set_headless(self, status: bool):
		"""
		Переключает отображение окна браузера.
			status – состояние отображение окна браузера.
		"""

		self.Headless = status
		
	def set_page_load_timeout(self, page_load_timeout: int):
		"""
		Задаёт тайм-аут загрузки страницы.
			page_load_timeout – тайм-аут загрузки страницы в секундах.
		"""

		self.PageLoadTimeout = page_load_timeout
		
	def set_script_timeout(self, script_timeout: int):
		"""
		Задаёт тайм-аут выполнения JavaScript.
			script_timeout – тайм-аут выполнения JavaScript в секундах.
		"""

		self.ScriptTimeout = script_timeout
		
	def set_window_size(self, width: int, height: int):
		"""
		Задаёт размер окна браузера.
			width – ширина окна в пикселях;
			height – высота окна в пикселях.
		"""

		self.WindowWidth = width
		self.WindowHeight = height
		
class WebResponse:
	"""
	Эмуляция структуры ответа библиотеки requests.
	"""

	def __init__(self):
		"""
		Эмуляция структуры ответа библиотеки requests.
		"""

		#---> Генерация динамических свойств.
		#==========================================================================================#
		# Статус ответа.
		self.status_code = None
		# Бинарное представление ответа.
		self.content = None
		# Текстовое представление ответа.
		self.text = None
		
#==========================================================================================#
# >>>>> ОСНОВНОЙ КЛАСС <<<<< #
#==========================================================================================#

class WebRequestor:
	"""
	Запросчик HTML кода веб-страниц.
	"""
	
	#==========================================================================================#
	# >>>>> ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __CheckConfig(self):
		"""
		Выбрасывает исключение при отсутствии конфигурации.
		"""

		# Если конфигурация не задана, выбросить исключение.
		if self.__Config == None: raise ConfigRequired()
		
	def __GetProxy(self) -> dict | None:
		"""
		Возвращает объект прокси для запроса.
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
					
			# Если задана конфигурация requests.		
			if type(self.__Config) == RequestsConfig:
				# Создание объекта прокси.
				Proxy = {
					Proxy["protocol"]: Proxy["protocol"].replace("https", "http") + "://" + Auth + Proxy["host"] + ":" + Proxy["port"]
				}
			
			# Если задана конфигурация httpx.		
			if type(self.__Config) == HttpxConfig:
				# Создание объекта прокси.
				Proxy = {
					Proxy["protocol"] + "://": Proxy["protocol"].replace("https", "http") + "://" + Auth + Proxy["host"] + ":" + Proxy["port"]
				}
			
		return Proxy
	
	def __InitializeChrome(self):
		"""
		Инициализирует браузер Google Chrome.
		"""

		# Закрытие браузера.
		self.close()
		# Опции веб-браузера.
		ChromeOptions = self.Options.Options()
		# Установка опций.
		ChromeOptions.add_argument("--no-sandbox")
		ChromeOptions.add_argument("--disable-dev-shm-usage")
		ChromeOptions.add_argument("--disable-gpu")
		ChromeOptions.add_experimental_option("excludeSwitches", ["enable-logging"])
		# При отключённом режиме отладки скрыть окно браузера.
		if self.__Config.Headless == True: ChromeOptions.add_argument("--headless=new")
		# Инициализация браузера.
		self.__Browser = self.selenium.webdriver.Chrome(service = self.Service.Service(self.ChromeDriverManager.ChromeDriverManager().install()), options = ChromeOptions)
		# Установка размера окна браузера на FullHD для корректной работы сайтов.
		self.__Browser.set_window_size(self.__Config.WindowWidth, self.__Config.WindowHeight)
		# Установка максимального времени загрузки страницы и выполнения скрипта.
		self.__Browser.set_page_load_timeout(self.__Config.PageLoadTimeout)
		self.__Browser.set_script_timeout(self.__Config.ScriptTimeout)

	def __ProcessHeaders(self, headers: dict | None) -> dict | None:
		"""
		Обрабатывает заголовки перед выполнением запроса.
		"""

		# Если переданы заголовки.
		if headers != None:
			# Объединение словарей заголовков из конфигурации и аргументов.
			headers = self.__Config.headers | headers
			
		else:
			# Установка словаря заголовков из конфигурации.
			headers = self.__Config.headers

		return headers
		
	#==========================================================================================#
	# >>>>> МЕТОДЫ ЗАПРОСОВ <<<<< #
	#==========================================================================================#

	def __httpx_GET(self, url: str, params: dict | None = None, headers: dict | None = None, cookies: dict | None = None) -> httpx.Response:
		"""
		Отправляет GET запрос через библиотеку httpx.
			url – адрес запроса;
			params – словарь параметров запроса;
			headers – словарь заголовков;
			cookies – словарь куков.
		"""

		# Обработка заголовков.
		headers = self.__ProcessHeaders(headers)
		# Ответ.
		Response = self.__Client.get(url, params = params, headers = headers, cookies = cookies, follow_redirects = self.__Config.redirecting)
		
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
		
		# Обработка заголовков.
		headers = self.__ProcessHeaders(headers)
		# Ответ.
		Response = self.__Client.post(url, params = params, headers = headers, cookies = cookies, data = data, json = json, follow_redirects = self.__Config.redirecting)
		
		return Response
		
	def __requests_GET(self, url: str, params: dict | None = None, headers: dict | None = None, cookies: dict | None = None) -> requests.Response:
		"""
		Отправляет GET запрос через библиотеку requests.
			url – адрес запроса;
			params – словарь параметров запроса;
			headers – словарь заголовков;
			cookies – словарь куков.
		"""
		
		# Обработка заголовков.
		headers = self.__ProcessHeaders(headers)
		# Ответ.
		Response = self.__Session.get(url, params = params, headers = headers, cookies = cookies, proxies = self.__GetProxy(), allow_redirects = self.__Config.redirecting)
		
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
		
		# Обработка заголовков.
		headers = self.__ProcessHeaders(headers)
		# Ответ.
		Response = self.__Session.post(url, params = params, headers = headers, cookies = cookies, data = data, json = json, proxies = self.__GetProxy(), allow_redirects = self.__Config.redirecting)
		
		return Response
	
	def __selenium_LOAD(self, url: str) -> WebResponse:
		"""
		Загружает страницу при помощи библиотеки Selenium.
			URL – адрес страницы.
		"""

		# Ответ.
		Response = WebResponse()
		
		try:
			# Запрос страницы.
			self.__Browser.get(url)
			
		except self.TimeoutException.TimeoutException:
			# Установка свойств ответа.
			Response.status_code = 408
			
		except Exception:
			# Установка свойств ответа.
			Response.status_code = 499
			
		else:
			# Установка свойств ответа.
			Response.status_code = 200
			Response.text = self.__Browser.execute_script("return document.body.innerHTML;")
			Response.content = bytes(Response.text)
		
		return Response
			
	def __init__(self, logging: bool = False):
		"""
		Запросчик HTML кода веб-страниц.
			logging – переключает ведение логов при помощи стандартного модуля.
		"""

		#---> Генерация динамических свойств.
		#==========================================================================================#
		# Конфигурация.
		self.__Config = None
		# Сессия запросов httpx.
		self.__Session = None
		# Клиент запросов httpx.
		self.__Client = None
		# Экземпляр веб-браузера Selenium.
		self.__Browser = None
		# Состояние: вести ли логи.
		self.__Logging = logging
		# Список прокси.
		self.__Proxies = list()
		
	#==========================================================================================#
	# >>>>> ОБЩИЕ МЕТОДЫ <<<<< #
	#==========================================================================================#
		
	def close(self):
		"""
		Закрывает запросчик.
		"""

		# Если задана конфигурация Selenium.
		if type(self.__Config) == SeleniumConfig:
			
			try:
				# Закрытие браузера.
				self.__Browser.close()
				self.__Browser.quit()
				# Обнуление экземпляра.
				self.__Browser = None
			
			except Exception:
				pass
			
		# Если задана конфигурация requests.
		if type(self.__Config) == RequestsConfig:
			# Закрытие сессии.
			self.__Session.close()
			# Обнуление сессии.
			self.__Session = None
			
		# Если задана конфигурация httpx.
		if type(self.__Config) == HttpxConfig:
			# Закрытие клиента.
			self.__Client.close()
			# Обнуление клиента.
			self.__Client = None
			
	def add_proxy(self, protocol: Protocols, host: str, port: int | str, login: str | None = None, password: str | None = None):
		"""
		Добавляет прокси для использования в запросах. Не работает с Selenium.
			protocol – протокол прокси-соединения;
			host – IP или адрес хоста;
			port – порт сервера;
			login – логин для авторизации;
			password – пароль для авторизации.
		"""
		
		# Добавление прокси.
		self.__Proxies.append({
			"protocol": protocol.value,
			"host": host,
			"port": str(port),
			"login": login,
			"password": password
		})
			
	def initialize(self, config: HttpxConfig | RequestsConfig | SeleniumConfig = RequestsConfig()):
		"""
		Задаёт конфигурацию и инициализирует модуль запросов. Вызывать после всех настроек.
			config – конфигурация.
		"""

		# Если задана конфигурация Selenium.
		if type(config) == SeleniumConfig:
			# Сохранение конфигурации.
			self.__Config = config
			
			try:
				# Динамический импорт пакетов.
				self.Options = importlib.import_module("selenium.webdriver.chrome.option")
				self.Service = importlib.import_module("selenium.webdriver.chrome.service")
				self.ChromeDriverManager = importlib.import_module("webdriver_manager.chrome")
				self.TimeoutException = importlib.import_module("selenium.common.exceptions")
				
			except:
				raise SeleniumRequired()
			
			# Инициализация выбранного браузера.
			match config.BrowserType:
				
				case Browsers.Chrome: self.__InitializeChrome()
					
		# Если задана конфигурация requests.		
		if type(config) == RequestsConfig:
			# Сохранение конфигурации.
			self.__Config = config
			# Инициализация сессии.
			self.__Session = requests.Session()
			
		# Если задана конфигурация httpx.		
		if type(config) == HttpxConfig:
			# Сохранение конфигурации.
			self.__Config = config
			# Инициализация клиента.
			self.__Client = httpx.Client(http2 = config.http2, proxies = self.__GetProxy())
	
	#==========================================================================================#
	# >>>>> SELENIUM <<<<< #
	#==========================================================================================#

	def execute_script(self, script: str, use_async: bool = False, tries: int = 3) -> WebResponse:
		"""
		Выполняет JavaScript на текущей странице браузера. Требуется инициализация библиотеки Selenium!
			script – исполняемый код;
			use_async – указывает, необходимо ли выполнить скрипт асинхронно;
			tries – количество попыток повтора при неудачном выполнении.
		Примечание:
			Требуется инициализация библиотеки Selenium!
		"""

		# Ответ.
		Response = WebResponse()
		
		# Если веб-драйвер инициализирован.
		if self.__Browser != None:
			# Результат выполнения скрипта.
			Result = None
			# Количество повторов.
			CurrentTry = 0
			# Состояние: вернул ли скрипт ответ.
			IsLoaded = False
		
			# Повторять, пока скрипт не вернёт ответ.
			while IsLoaded == False:
				
				try:
					# Выполнение скрипта и запись результата.
					Result = self.__Browser.execute_async_script(script) if use_async == True else self.__Browser.execute_script(script)
				
				except self.TimeoutException.TimeoutException:
					# Установка свойств ответа.
					Response.status_code = 408
					
				except Exception:
					# Инкремент количества повторов.
					CurrentTry += 1
					# Установка свойств ответа.
					Response.status_code = 400
					
					# Если достигнуто максимальное количество повторов, остановить повторные запросы.
					if CurrentTry == tries:
						break
			
				else:
					# Переключение статуса выполнения скрипта.
					IsLoaded = True
					# Установка свойств ответа.
					Response.status_code = 200
					Response.text = Result
					Response.content = bytes(Result)
					
			else:
				# Выброс исключения.
				raise SeleniumRequired()
				
		return Response
	
	def get_browser_handler(self) -> any:
		"""
		Возвращает дескриптор экземпляра браузера.
			URL – адрес страницы;
			TriesCount – количество попыток повтора при неудачном выполнении.
		Примечание:
			Требуется инициализация библиотеки Selenium!
		"""

		# Если веб-драйвер не инициализирован, выбросить исключение.
		if self.__Browser == None: raise SeleniumRequired()
		
		return self.__Browser
	
	def load(self, url: str, tries: int = 3) -> WebResponse:
		"""
		Загружает HTML код страницы через Selenium.
			url – адрес запроса;
			tries – количество попыток повтора при неудачном выполнении.
		Примечание:
			Требуется инициализация библиотеки Selenium!
		"""

		# Ответ.
		Response = WebResponse()
		# Индекс попытки.
		Try = 0
		# Проверка наличия конфигурации.
		self.__CheckConfig()
		
		# Пока не превышено количество попыток.
		while Try < tries and Response.status_code != 200:
			# Инкремент повтора.
			Try += 1
			
			try:
				# Выполнение запроса.
				Response = self.__selenium_LOAD(url)
				
			except Exception as ExceptionData:
				# Запись в лог ошибки: не удалось выполнить запрос.
				if self.__Logging == True: logging.error("[SELENIUM-LOAD] Description: \"" + str(ExceptionData).split("\n")[0] + "\".")
		
		return Response
	
	#==========================================================================================#
	# >>>>> ЗАПРОСЫ <<<<< #
	#==========================================================================================#	
	
	def get(self, url: str, params: dict | None = None, headers: dict | None = None, cookies: dict | None = None, tries: int = 3) -> requests.Response | httpx.Response:
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
		# Проверка наличия конфигурации.
		self.__CheckConfig()

		# Название библиотеки.
		LibName = None
		
		# Пока не превышено количество попыток.
		while Try < tries and Response.status_code != 200:
			# Инкремент повтора.
			Try += 1
			
			try:
				
				# Если установлена конфигурация библиотеки requests.
				if type(self.__Config) == RequestsConfig:
					# Установка имени библиотеки.
					LibName = "REQUESTS"
					# Выполнение запроса.
					Response = self.__requests_GET(url, params, headers, cookies)
					
				# Если установлена конфигурация библиотеки httpx.
				if type(self.__Config) == HttpxConfig:
					# Установка имени библиотеки.
					LibName = "HTTPX"
					# Выполнение запроса.
					Response = self.__httpx_GET(url, params, headers, cookies)
				
			except Exception as ExceptionData:
				# Запись в лог ошибки: не удалось выполнить запрос.
				if self.__Logging == True: logging.error(f"[{LibName}-GET] Description: \"" + str(ExceptionData).split("\n")[0] + "\".")
		
		return Response
	
	def post(self, url: str, params: dict | None = None, headers: dict | None = None, cookies: dict | None = None, data: any = None, json: dict | None = None, tries: int = 3) -> requests.Response | httpx.Response:
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
		# Проверка наличия конфигурации.
		self.__CheckConfig()
		# Название библиотеки.
		LibName = None
		
		# Пока не превышено количество попыток.
		while Try < tries and Response.status_code != 200:
			# Инкремент повтора.
			Try += 1
			
			try:
				
				# Если установлена конфигурация библиотеки requests.
				if type(self.__Config) == RequestsConfig:
					# Установка имени библиотеки.
					LibName = "REQUESTS"
					# Выполнение запроса.
					Response = self.__requests_POST(url, params, headers, cookies, data, json)
					
				# Если установлена конфигурация библиотеки httpx.
				if type(self.__Config) == HttpxConfig:
					# Установка имени библиотеки.
					LibName = "HTTPX"
					# Выполнение запроса.
					Response = self.__httpx_POST(url, params, headers, cookies, data, json)
				
			except Exception as ExceptionData:
				# Запись в лог ошибки: не удалось выполнить запрос.
				if self.__Logging == True: logging.error(f"[{LibName}-POST] Description: \"" + str(ExceptionData).split("\n")[0] + "\".")
		
		return Response