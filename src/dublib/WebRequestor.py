from fake_useragent import UserAgent as UserAgentGenerator
from dublib.Exceptions.WebRequestor import *

import importlib
import requests
import logging
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

class RequestsConfig:
	"""
	Конфигурация библиотеки requests.
	"""

	def __init__(self):
		"""
		Конфигурация библиотеки requests.
		"""
		
		#---> Генерация динамических свойств.
		#==========================================================================================#
		# Заголовки запросов.
		self.Headers = {
			"User-Agent": str(UserAgentGenerator.chrome)
		}
		
	def addHeader(self, Key: str, Value: int | str):
		"""
		Добавляет пользовательский заголовок запроса.
			Key – ключ заголовка;
			Value – значение заголовка.
		"""

		# Запись заголовка.
		self.Headers[Key] = Value
		
	def setReferer(self, Referer: str):
		"""
		Задаёт пользовательское значение заголовка Referer.
			Referer – новое значение заголовка.
		"""

		self.Headers["Referer"] = Referer
		
	def setUserAgent(self, UserAgent: str):
		"""
		Задаёт пользовательское значение заголовка User-Agent.
			UserAgent – новое значение заголовка.
		"""

		self.Headers["User-Agent"] = UserAgent
	
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

	def __CheckConfigPresence(self) -> bool:
		"""
		Возвращает состояние: задана ли конфигурация.
		"""

		# Состояние: задана ли конфигурация.
		IsConfigSet = False if self.__Session == None and self.__Browser == None else True
		
		return IsConfigSet
	
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
		if self.__SeleniumConfig.Headless == True: ChromeOptions.add_argument("--headless=new")
		# Инициализация браузера.
		self.__Browser = self.selenium.webdriver.Chrome(service = self.Service.Service(self.ChromeDriverManager.ChromeDriverManager().install()), options = ChromeOptions)
		# Установка размера окна браузера на FullHD для корректной работы сайтов.
		self.__Browser.set_window_size(self.__SeleniumConfig.WindowWidth, self.__SeleniumConfig.WindowHeight)
		# Установка максимального времени загрузки страницы и выполнения скрипта.
		self.__Browser.set_page_load_timeout(self.__SeleniumConfig.PageLoadTimeout)
		self.__Browser.set_script_timeout(self.__SeleniumConfig.ScriptTimeout)
		
	def __GetByRequests(self, URL: str) -> WebResponse:
		"""
		Запрашивает страницу при помощи библиотеки requests.
		"""

		# Ответ.
		Response = self.__Session.get(URL, headers = self.__RequestsConfig.Headers)
		
		return Response
	
	def __GetBySelenium(self, URL: str) -> WebResponse:
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
		# Конфигурация requests.
		self.__RequestsConfig = RequestsConfig()
		# Конфигурация Selenium.
		self.__SeleniumConfig = SeleniumConfig()
		# Сессия запросов.
		self.__Session = None
		# Состояние: используется ли Selenium.
		self.__IsSeleniumUsed = False
		# Экземпляр веб-браузера.
		self.__Browser = None
		# Состояние: вести ли логи.
		self.__Logging = Logging
		
	def close(self):
		"""
		Закрывает запросчик.
		"""

		# Если для запросов используется Selenium.
		if self.__IsSeleniumUsed == True:
			
			try:
				# Закрытие браузера.
				self.__Browser.close()
				self.__Browser.quit()
				# Обнуление экземпляра.
				self.__Browser = None
			
			except Exception:
				pass
			
		else:
			# Закрытие сессии.
			self.__Session.close()
			# Обнуление сессии.
			self.__Session = None
		
	def executeJavaScript(self, Script: str, Async: bool = False, TriesCount: int = 1) -> WebResponse:
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
		
	def get(self, URL: str, TriesCount: int = 3) -> WebResponse:
		"""
		Получает HTML код страницы.
			URL – адрес страницы;
			TriesCount – количество попыток повтора при неудачном выполнении.
		"""

		# Ответ.
		Response = WebResponse()
		# Индекс попытки.
		Try = 0
		
		# Если задана конфигурация.
		if self.__CheckConfigPresence() == True:
			
			# Пока не превышено количество попыток.
			while Try < TriesCount and Response.status_code != 200:
				# Инкремент повтора.
				Try += 1
				
				try:
					# Выполнение запроса.
					Response = self.__GetBySelenium(URL) if self.__IsSeleniumUsed == True else self.__GetByRequests(URL)
					
				except Exception as ExceptionData:
					# Запись в лог ошибки: не удалось выполнить запрос.
					if self.__Logging == True: logging.error("Some error occured during request: \"" + str(ExceptionData).split('\n')[0] + "\".")
			
		else:
			# Выброс исключения.
			raise ConfigRequired()
			
		return Response
	
	def getBrowserHandler(self) -> any:
		"""
		Возвращает дескриптор экземпляра браузера.
			URL – адрес страницы;
			TriesCount – количество попыток повтора при неудачном выполнении.
			Требуется инициализация библиотеки Selenium!
		"""

		# Если веб-драйвер не инициализирован, выбросить исключение.
		if self.__Browser == None:
			raise SeleniumRequired()
		
		return self.__Browser
			
	def initialize(self, Config: RequestsConfig | SeleniumConfig = RequestsConfig()):
		"""
		Задаёт конфигурацию и инициализирует модуль запросов.
			Config – конфигурация.
		"""

		# Если задана конфигурация Selenium.
		if type(Config) == SeleniumConfig:
			# Переключение состояния Selenium.
			self.__IsSeleniumUsed = True
			# Сохранение конфигурации.
			self.__SeleniumConfig = Config
			
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
		elif type(Config) == RequestsConfig:
			# Переключение состояния Selenium.
			self.__IsSeleniumUsed = False
			# Сохранение конфигурации.
			self.__RequestsConfig = Config
			# Инициализация сессии.
			self.__Session = requests.Session()