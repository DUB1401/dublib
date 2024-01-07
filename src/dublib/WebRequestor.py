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
	# >>>>> СВОЙСТВА <<<<< #
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

	def __init__(self, AutoUserAgent: bool = True):
		"""
		Конфигурация библиотеки httpx.
			AutoUserAgent – переключает автоматическую генерацию заголовка User-Agent.
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
		if AutoUserAgent == True: self.__Headers = {"User-Agent": UserAgentGenerator().chrome}
		
	def addHeader(self, Key: str, Value: int | str):
		"""
		Добавляет пользовательский заголовок запроса.
			Key – ключ заголовка;
			Value – значение заголовка.
		"""

		# Запись заголовка.
		self.__Headers[Key] = Value
		
	def enableHTTP2(self, Value: bool):
		"""
		Переключает использование протокола HTTP2.0.
			Value – статус использования протокола.
		"""
		
		self.__HTTP2 = Value
		
	def enableRedirecting(self, Value: bool):
		"""
		Переключает автоматическое перенаправление HTTP.
			Value – статус перенаправления.
		"""
		
		self.__Redirecting = Value
		
	def setReferer(self, Referer: str):
		"""
		Задаёт пользовательское значение заголовка Referer.
			Referer – новое значение заголовка.
		"""

		self.__Headers["Referer"] = Referer
		
	def setUserAgent(self, UserAgent: str):
		"""
		Задаёт пользовательское значение заголовка User-Agent.
			UserAgent – новое значение заголовка.
		"""

		self.__Headers["User-Agent"] = UserAgent

class RequestsConfig:
	"""
	Конфигурация библиотеки requests.
	"""
	
	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
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

	def __init__(self, AutoUserAgent: bool = True):
		"""
		Конфигурация библиотеки requests.
			AutoUserAgent – переключает автоматическую генерацию заголовка User-Agent.
		"""
		
		#---> Генерация динамических свойств.
		#==========================================================================================#
		# Заголовки запросов.
		self.__Headers = dict()
		# Состояние: выполнять ли переадресацию.
		self.__Redirecting = True
		
		# Если указано, сгенерировать заголовок User-Agent.
		if AutoUserAgent == True: self.__Headers = {"User-Agent": UserAgentGenerator().chrome}
		
	def addHeader(self, Key: str, Value: int | str):
		"""
		Добавляет пользовательский заголовок запроса.
			Key – ключ заголовка;
			Value – значение заголовка.
		"""

		# Запись заголовка.
		self.__Headers[Key] = Value
		
	def enableRedirecting(self, Value: bool):
		"""
		Переключает автоматическое перенаправление HTTP.
			Value – статус перенаправления.
		"""
		
		self.__Redirecting = Value
		
	def setReferer(self, Referer: str):
		"""
		Задаёт пользовательское значение заголовка Referer.
			Referer – новое значение заголовка.
		"""

		self.__Headers["Referer"] = Referer
		
	def setUserAgent(self, UserAgent: str):
		"""
		Задаёт пользовательское значение заголовка User-Agent.
			UserAgent – новое значение заголовка.
		"""

		self.__Headers["User-Agent"] = UserAgent
	
class SeleniumConfig:
	"""
	Конфигурация библиотеки Selenium.
	"""
	
	def __init__(
			self,
			BrowserType: Browsers = Browsers.Chrome,
			Headless: bool = False,
			PageLoadTimeout: int = 75,
			ScriptTimeout: int = 75,
			WindowWidth: int = 1920,
			WindowHeight: int = 1080
		):
		"""
		Конфигурация библиотеки Selenium.
		"""
		
		#---> Генерация динамических свойств.
		#==========================================================================================#
		# Тип используемого браузера.
		self.BrowserType = BrowserType
		# Состояние: активен ли безрабочный режим.
		self.Headless = Headless
		# Тайм-аут загрузки страницы.
		self.PageLoadTimeout = PageLoadTimeout
		# Тайм-аут выполнения JavaScript.
		self.ScriptTimeout = ScriptTimeout
		# Ширина окна.
		self.WindowWidth = WindowWidth
		# Высота окна.
		self.WindowHeight = WindowHeight
		
	def setBrowserType(self, BrowserType: Browsers):
		"""
		Задаёт используемый браузер.
			BrowserType – браузер.
		"""

		self.BrowserType = BrowserType
		
	def setHeadless(self, Headless: bool):
		"""
		Переключает отображение окна браузера.
			Headless – состояние отображение окна браузера.
		"""

		self.Headless = Headless
		
	def setPageLoadTimeout(self, PageLoadTimeout: int):
		"""
		Задаёт тайм-аут загрузки страницы.
			PageLoadTimeout – тайм-аут загрузки страницы в секундах.
		"""

		self.PageLoadTimeout = PageLoadTimeout
		
	def setScriptTimeout(self, ScriptTimeout: int):
		"""
		Задаёт тайм-аут выполнения JavaScript.
			PageLoadTimeout – тайм-аут выполнения JavaScript в секундах.
		"""

		self.ScriptTimeout = ScriptTimeout
		
	def setWindowSize(self, Width: int, Height: int):
		"""
		Задаёт размер окна браузера.
			Width – ширина окна в пикселях;
			Height – высота окна в пикселях.
		"""

		self.WindowWidth = Width
		self.WindowHeight = Height
		
class WebResponse:
	"""
	Эмуляция структуры ответа библиотеки requests.
	"""

	#==========================================================================================#
	# >>>>> СТАТИЧЕСКИЕ СВОЙСТВА <<<<< #
	#==========================================================================================#

	# Статус ответа.
	status_code = None
	# Бинарное представление ответа.
	content = None
	# Текстовое представление ответа.
	text = None

	#==========================================================================================#
	# >>>>> МЕТОДЫ <<<<< #
	#==========================================================================================#
	
	# Конструктор.
	def __init__(self):
		"""
		Эмуляция структуры ответа библиотеки requests.
		"""

		#---> Генерация динамических свойств.
		#==========================================================================================#
		# Статус ответа.
		status_code = None
		# Бинарное представление ответа.
		content = None
		# Текстовое представление ответа.
		text = None
		
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
				print(Proxy)
			
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
		
	#==========================================================================================#
	# >>>>> МЕТОДЫ ЗАПРОСОВ <<<<< #
	#==========================================================================================#

	def __httpx_GET(self, URL: str, Params: dict | None = None, Headers: dict | None = None, Cookies: dict | None = None) -> httpx.Response:
		"""
		Отправляет GET запрос через библиотеку httpx.
			URL – адрес запроса;
			Params – словарь параметров запроса;
			Headers – словарь заголовков;
			Cookies – словарь куков.
		"""
		
		# Если переданы заголовки.
		if Headers != None:
			# Объединение словарей заголовков из конфигурации и аргументов.
			Headers = self.__Config.headers | Headers
			
		else:
			# Установка словаря заголовков из конфигурации.
			Headers = self.__Config.headers
		
		# Ответ.
		Response = self.__Client.get(URL, params = Params, headers = Headers, cookies = Cookies, follow_redirects = self.__Config.redirecting)
		
		return Response
	
	def __httpx_POST(self, URL: str, Params: dict | None = None, Headers: dict | None = None, Cookies: dict | None = None, Data: any = None, JSON: dict | None = None) -> httpx.Response:
		"""
		Отправляет POST запрос через библиотеку httpx.
			URL – адрес запроса;
			Params – словарь параметров запроса;
			Headers – словарь заголовков;
			Data – данные запроса;
			Cookies – словарь куков.
		"""
		
		# Если переданы заголовки.
		if Headers != None:
			# Объединение словарей заголовков из конфигурации и аргументов.
			Headers = self.__Config.headers | Headers
			
		else:
			# Установка словаря заголовков из конфигурации.
			Headers = self.__Config.headers
		
		# Ответ.
		Response = self.__Client.post(URL, params = Params, headers = Headers, cookies = Cookies, data = Data, json = JSON, follow_redirects = self.__Config.redirecting)
		
		return Response
		
	def __requests_GET(self, URL: str, Params: dict | None = None, Headers: dict | None = None, Cookies: dict | None = None) -> requests.Response:
		"""
		Отправляет GET запрос через библиотеку requests.
			URL – адрес запроса;
			Params – словарь параметров запроса;
			Headers – словарь заголовков;
			Cookies – словарь куков.
		"""
		
		# Если переданы заголовки.
		if Headers != None:
			# Объединение словарей заголовков из конфигурации и аргументов.
			Headers = self.__Config.headers | Headers
			
		else:
			# Установка словаря заголовков из конфигурации.
			Headers = self.__Config.headers

		# Ответ.
		Response = self.__Session.get(URL, params = Params, headers = Headers, cookies = Cookies, proxies = self.__GetProxy(), allow_redirects = self.__Config.redirecting)
		
		return Response
	
	def __requests_POST(self, URL: str, Params: dict | None = None, Headers: dict | None = None, Cookies: dict | None = None, Data: any = None, JSON: dict | None = None) -> requests.Response:
		"""
		Отправляет POST запрос через библиотеку requests.
			URL – адрес запроса;
			Params – словарь параметров запроса;
			Headers – словарь заголовков;
			Cookies – словарь куков;
			Data – данные запроса;
			JSON – тело запроса.
		"""
		
		# Если переданы заголовки.
		if Headers != None:
			# Объединение словарей заголовков из конфигурации и аргументов.
			Headers = self.__Config.headers | Headers
			
		else:
			# Установка словаря заголовков из конфигурации.
			Headers = self.__Config.headers
		
		# Ответ.
		Response = self.__Session.post(URL, params = Params, headers = Headers, cookies = Cookies, data = Data, json = JSON, proxies = self.__GetProxy(), allow_redirects = self.__Config.redirecting)
		
		return Response
	
	def __selenium_LOAD(self, URL: str) -> WebResponse:
		"""
		Запрашивает страницу при помощи библиотеки Selenium.
		"""

		# Ответ.
		Response = WebResponse()
		
		try:
			# Запрос страницы.
			self.__Browser.get(URL)
			
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
			
	def __init__(self, Logging: bool = False):
		"""
		Запросчик HTML кода веб-страниц.
			Logging – переключает ведение логов при помощи стандартного модуля logging.
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
		self.__Logging = Logging
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
			
	def addProxy(self, Protocol: Protocols, Host: str, Port: int | str, Login: str | None = None, Password: str | None = None):
		"""
		Добавляет прокси для использования в запросах. Не работает с Selenium.
			Protocol – протокол прокси-соединения;
			Host – IP или адрес хоста;
			Port – порт сервера;
			Login – логин для авторизации;
			Password – пароль для авторизации.
		"""
		
		# Добавление прокси.
		self.__Proxies.append({
			"protocol": Protocol.value,
			"host": Host,
			"port": str(Port),
			"login": Login,
			"password": Password
		})
			
	def initialize(self, Config: HttpxConfig | RequestsConfig | SeleniumConfig = RequestsConfig()):
		"""
		Задаёт конфигурацию и инициализирует модуль запросов. Вызывать после всех настроек.
			Config – конфигурация.
		"""

		# Если задана конфигурация Selenium.
		if type(Config) == SeleniumConfig:
			# Сохранение конфигурации.
			self.__Config = Config
			
			try:
				# Динамический импорт пакетов.
				self.Options = importlib.import_module("selenium.webdriver.chrome.option")
				self.Service = importlib.import_module("selenium.webdriver.chrome.service")
				self.ChromeDriverManager = importlib.import_module("webdriver_manager.chrome")
				self.TimeoutException = importlib.import_module("selenium.common.exceptions")
				
			except:
				raise SeleniumRequired()
			
			# Инициализация выбранного браузера.
			match Config.BrowserType:
				
				case Browsers.Chrome: self.__InitializeChrome()
					
		# Если задана конфигурация requests.		
		if type(Config) == RequestsConfig:
			# Сохранение конфигурации.
			self.__Config = Config
			# Инициализация сессии.
			self.__Session = requests.Session()
			
		# Если задана конфигурация httpx.		
		if type(Config) == HttpxConfig:
			# Сохранение конфигурации.
			self.__Config = Config
			# Инициализация клиента.
			self.__Client = httpx.Client(http2 = Config.http2, proxies = self.__GetProxy())
	
	#==========================================================================================#
	# >>>>> SELENIUM <<<<< #
	#==========================================================================================#

	def executeJavaScript(self, Script: str, Async: bool = False, TriesCount: int = 3) -> WebResponse:
		"""
		Выполняет JavaScript на текущей странице браузера.
			Script – исполняемый код;
			Async – указывает, необходимо ли выполнить скрипт асинхронно;
			TriesCount – количество попыток повтора при неудачном выполнении.
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
					Result = self.__Browser.execute_async_script(Script) if Async == True else self.__Browser.execute_script(Script)
				
				except self.TimeoutException.TimeoutException:
					# Установка свойств ответа.
					Response.status_code = 408
					
				except Exception:
					# Инкремент количества повторов.
					CurrentTry += 1
					# Установка свойств ответа.
					Response.status_code = 400
					
					# Если достигнуто максимальное количество повторов, остановить повторные запросы.
					if CurrentTry == TriesCount:
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
	
	def getBrowserHandler(self) -> any:
		"""
		Возвращает дескриптор экземпляра браузера.
			URL – адрес страницы;
			TriesCount – количество попыток повтора при неудачном выполнении.
			Требуется инициализация библиотеки Selenium!
		"""

		# Если веб-драйвер не инициализирован, выбросить исключение.
		if self.__Browser == None: raise SeleniumRequired()
		
		return self.__Browser
	
	def load(self, URL: str, TriesCount: int = 3) -> WebResponse:
		"""
		Загружает HTML код страницы через Selenium.
			URL – адрес запроса;
			TriesCount – количество попыток повтора при неудачном выполнении.
		"""

		# Ответ.
		Response = WebResponse()
		# Индекс попытки.
		Try = 0
		# Проверка наличия конфигурации.
		self.__CheckConfig()
		
		# Пока не превышено количество попыток.
		while Try < TriesCount and Response.status_code != 200:
			# Инкремент повтора.
			Try += 1
			
			try:
				# Выполнение запроса.
				Response = self.__selenium_LOAD(URL)
				
			except Exception as ExceptionData:
				# Запись в лог ошибки: не удалось выполнить запрос.
				if self.__Logging == True: logging.error("[SELENIUM-LOAD] Description: \"" + str(ExceptionData).split("\n")[0] + "\".")
		
		return Response
	
	#==========================================================================================#
	# >>>>> ЗАПРОСЫ <<<<< #
	#==========================================================================================#	
	
	def get(self, URL: str, Params: dict | None = None, Headers: dict | None = None, Cookies: dict | None = None, TriesCount: int = 3) -> requests.Response | httpx.Response:
		"""
		Отправляет GET запрос.
			URL – адрес запроса;
			Params – словарь параметров запроса;
			Headers – словарь заголовков;
			Cookies – словарь куков;
			TriesCount – количество попыток повтора при неудачном выполнении.
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
		while Try < TriesCount and Response.status_code != 200:
			# Инкремент повтора.
			Try += 1
			
			try:
				
				# Если установлена конфигурация библиотеки requests.
				if type(self.__Config) == RequestsConfig:
					# Установка имени библиотеки.
					LibName = "REQUESTS"
					# Выполнение запроса.
					Response = self.__requests_GET(URL, Params, Headers, Cookies)
					
				# Если установлена конфигурация библиотеки httpx.
				if type(self.__Config) == HttpxConfig:
					# Установка имени библиотеки.
					LibName = "HTTPX"
					# Выполнение запроса.
					Response = self.__httpx_GET(URL, Params, Headers, Cookies)
				
			except Exception as ExceptionData:
				# Запись в лог ошибки: не удалось выполнить запрос.
				if self.__Logging == True: logging.error(f"[{LibName}-GET] Description: \"" + str(ExceptionData).split("\n")[0] + "\".")
		
		return Response
	
	def post(self, URL: str, Params: dict | None = None, Headers: dict | None = None, Cookies: dict | None = None, Data: any = None, JSON: dict | None = None, TriesCount: int = 3) -> requests.Response | httpx.Response:
		"""
		Отправляет POST запрос.
			URL – адрес запроса;
			Params – словарь параметров запроса;
			Headers – словарь заголовков;
			Cookies – словарь куков;
			JSON – тело запроса;
			TriesCount – количество попыток повтора при неудачном выполнении.
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
		while Try < TriesCount and Response.status_code != 200:
			# Инкремент повтора.
			Try += 1
			
			try:
				
				# Если установлена конфигурация библиотеки requests.
				if type(self.__Config) == RequestsConfig:
					# Установка имени библиотеки.
					LibName = "REQUESTS"
					# Выполнение запроса.
					Response = self.__requests_POST(URL, Params, Headers, Cookies, Data, JSON)
					
				# Если установлена конфигурация библиотеки httpx.
				if type(self.__Config) == HttpxConfig:
					# Установка имени библиотеки.
					LibName = "HTTPX"
					# Выполнение запроса.
					Response = self.__httpx_POST(URL, Params, Headers, Cookies, Data, JSON)
				
			except Exception as ExceptionData:
				# Запись в лог ошибки: не удалось выполнить запрос.
				if self.__Logging == True: logging.error(f"[{LibName}-POST] Description: \"" + str(ExceptionData).split("\n")[0] + "\".")
		
		return Response