import logging
import random
from time import sleep
from typing import TYPE_CHECKING, Any, Callable, Sequence, cast

import httpx
import requests
from curl_cffi import ProxySpec
from curl_cffi import requests as curl_cffi_requests

from ..core import LOGS_HANDLER
from ..functions.data import ToSequence
from .config import WebConfig
from .enums import Protocols, RequestsTypes, WebLibs
from .proxy import Proxy
from .response import WebResponse

if TYPE_CHECKING:
	from requests.cookies import RequestsCookieJar

__all__ = ["Protocols", "WebConfig", "WebLibs", "WebRequestor", "WebResponse"]

#==========================================================================================#
# >>>>> ИНИЦИАЛИЗАЦИЯ СИСТЕМЫ ЛОГГИРОВАНИЯ <<<<< #
#==========================================================================================#

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(LOGS_HANDLER)
LOGGER.setLevel(logging.INFO)

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
			if AcceptCH: self.__Config.headers.accept_client_hints(AcceptCH)
			if CriricalCH: self.__Config.headers.accept_client_hints(CriricalCH)

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
			if headers: headers = self.__Config.headers.to_dict() | headers
			else: headers = self.__Config.headers.to_dict()

		return headers

	#==========================================================================================#
	# >>>>> ПРИАТНЫЕ МЕТОДЫ ЗАПРОСОВ БИБЛИОТЕКИ CURL_CFFI <<<<< #
	#==========================================================================================#

	def __curl_cffi_DELETE(self, response: WebResponse, url: str, proxy: Proxy | None = None, params: dict | None = None, headers: dict | None = None, cookies: dict | None = None, data: Any = None, json: dict | None = None) -> WebResponse:
		"""
		Отправляет DELETE запрос через библиотеку **curl_cffi**.

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
		:param json: Словарь для сериализации и передачи в качестве JSON. Игнорируется при передаче `data`.
		:type json: dict | None
		:return: Контейнер ответа от библиотеки **curl_cffi**.
		:rtype: WebResponse
		"""

		self.__Session = cast(curl_cffi_requests.Session, self.__Session)
		headers = self.__MergeHeaders(headers)

		response.parse_response(self.__Session.delete(
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
		:param json: Словарь для сериализации и передачи в качестве JSON. Игнорируется при передаче `data`.
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

	def __httpx_DELETE(self, response: WebResponse, url: str, proxy: Proxy | None = None, params: dict | None = None, headers: dict | None = None, cookies: dict | None = None, data: Any = None, json: dict | None = None) -> WebResponse:
		"""
		Отправляет DELETE запрос через библиотеку **httpx**.

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
		:param json: Словарь для сериализации и передачи в качестве JSON. Игнорируется при передаче `data`.
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

		response.parse_response(self.__Session.request("DELETE", url, data = data, json = json))

		return response

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
		:param json: Словарь для сериализации и передачи в качестве JSON. Игнорируется при передаче `data`.
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

	def __requests_DELETE(self, response: WebResponse, url: str, proxy: Proxy | None = None, params: dict | None = None, headers: dict | None = None, cookies: dict | None = None, data: Any = None, json: dict | None = None) -> WebResponse:
		"""
		Отправляет DELETE запрос через библиотеку **requests**.

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
		:param json: Словарь для сериализации и передачи в качестве JSON. Игнорируется при передаче `data`.
		:type json: dict | None
		:return: Контейнер ответа от библиотеки **requests**.
		:rtype: WebResponse
		"""
		
		self.__Session = cast(requests.Session, self.__Session)
		headers = self.__MergeHeaders(headers)

		response.parse_response(self.__Session.delete(
			url = url,
			params = params,
			data = data,
			headers = headers,
			cookies = cookies,
			proxies = proxy.to_dict() if proxy else None,
			allow_redirects = self.__Config.redirecting,
			verify = self.__Config.verify_ssl,
			json = json
		))

		return response

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
		:param json: Словарь для сериализации и передачи в качестве JSON. Игнорируется при передаче `data`.
		:type json: dict | None
		:return: Контейнер ответа от библиотеки **requests**.
		:rtype: WebResponse
		"""

		self.__Session = cast(requests.Session, self.__Session)
		headers = self.__MergeHeaders(headers)

		response.parse_response(self.__Session.post(
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
			RequestsTypes.DELETE: {
				WebLibs.curl_cffi: self.__curl_cffi_DELETE,
				WebLibs.httpx: self.__httpx_DELETE,
				WebLibs.requests: self.__requests_DELETE
			},
			RequestsTypes.GET: {
				WebLibs.curl_cffi: self.__curl_cffi_GET,
				WebLibs.httpx: self.__httpx_GET,
				WebLibs.requests: self.__requests_GET
			},
			RequestsTypes.POST: {
				WebLibs.curl_cffi: self.__curl_cffi_POST,
				WebLibs.httpx: self.__httpx_POST,
				WebLibs.requests: self.__requests_POST
			}
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
		if self.__Config.headers.auto_accept_ch: self.__AcceptHints(Response)

		return Response

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ ВЫПОЛНЕНИЯ ЗАПРОСОВ <<<<< #
	#==========================================================================================#	

	def delete(self, url: str, params: dict | None = None, headers: dict | None = None, cookies: dict | None = None, data: Any = None, json: dict | None = None) -> WebResponse:
		"""
		Отправляет DELETE-запрос.

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
		:param json: Словарь для сериализации и передачи в качестве JSON. Игнорируется при передаче `data`.
		:type json: dict | None
		:return: Унифицированный контейнер ответа на веб-запросы.
		:rtype: WebResponse
		"""

		return self.request(RequestsTypes.DELETE, url, params = params, headers = headers, cookies = cookies, data = data, json = json)

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