from enum import Enum

#==========================================================================================#
# >>>>> ПЕРЕЧИСЛЕНИЯ <<<<< #
#==========================================================================================#

class Protocols(Enum):
	"""Перечисление типов протоколов."""
	
	SOCKS4 = "socks4"
	SOCKS5 = "socks5"
	HTTPS = "https"
	HTTP = "http"
	SFTP = "sftp"
	FTP = "ftp"

class RequestsTypes(Enum):
	"""Перечисление типов поддерживаемыйх запросов."""
	
	DELETE = "delete"
	GET = "get"
	POST = "post"

class WebLibs(Enum):
	"""Перечисление поддерживаемых библиотек запросов."""

	curl_cffi = "curl_cffi"
	requests = "requests"
	httpx = "httpx"

