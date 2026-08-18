from .enums import Protocols

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
	