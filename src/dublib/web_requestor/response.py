import httpx
import orjson
import requests
from curl_cffi import requests as curl_cffi_requests

from .config import WebConfig

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

		try: return orjson.loads(string)
		except Exception: pass

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
		self.__Text = response.text
		self.__JSON = self.__TryDeserialize(response.text) if parse_json else None

		self.set_headers(dict(response.headers))

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
