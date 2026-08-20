import base64
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from time import time

import jwt

from ...exceptions import web_requestor as Exceptions
from . import constants

#==========================================================================================#
# >>>>> ПЕРЕЧИСЛЕНИЯ <<<<< #
#==========================================================================================#

class AuthorizationSchemes(Enum):
	"""Схемы авторизации."""

	Basic = "Basic"
	Bearer = "Bearer"

#==========================================================================================#
# >>>>> СПОСОБЫ АВТОРИЗАЦИИ <<<<< #
#==========================================================================================#

class _BaseAuthorizationMethod(ABC):
	"""Базовый метод авторизации."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def value(self) -> str | None:
		"""Значение, используемое для авторизации."""

		return self._Value

	@property
	def scheme(self) -> str:
		"""Схема авторизации."""

		return self._Scheme.value

	#==========================================================================================#
	# >>>>> НАСЛЕДУЕМЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def _ClearScheme(self, token: str) -> str:
		"""
		Удаляет из токена схему.

		:param token: Токен.
		:type token: str
		:return: Обработанный токен.
		:rtype: str
		"""

		for Schema in AuthorizationSchemes:
			SchemaLength: int = len(Schema.value)

			if token.lower().startswith(Schema.value.lower()):
				return token[:SchemaLength * -1].strip()

		return token

	#==========================================================================================#
	# >>>>> ПЕРЕОПРЕДЕЛЯЕМЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	@abstractmethod
	def _ReturnScheme(self) -> AuthorizationSchemes:
		"""
		Возвращает тип схемы авторизации.

		:return: Тип схемы авторизации.
		:rtype: AuthorizationSchemes
		"""

		return AuthorizationSchemes.Basic

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self):
		"""Базовый метод авторизации."""

		self._Scheme: AuthorizationSchemes = self._ReturnScheme()
		self._Value: str | None = None

	def clear(self):
		"""Очищает данные авторизации."""

		self._Value = None

class Basic(_BaseAuthorizationMethod):
	"""Схема авторизации: Basic."""

	#==========================================================================================#
	# >>>>> ПЕРЕОПРЕДЕЛЯЕМЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def _ReturnScheme(self) -> AuthorizationSchemes:
		"""
		Возвращает тип схемы авторизации.

		:return: Тип схемы авторизации.
		:rtype: AuthorizationSchemes
		"""

		return AuthorizationSchemes.Basic

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def set_data(self, login: str, password: str) -> str:
		"""
		Задаёт данные авторизации и преобразует их в Base64-закодированную строку.

		:param login: Логин.
		:type login: str
		:param password: Пароль.
		:type password: str
		"""

		Credentials: str = f"{login}:{password}"
		CredentialsBytes: bytes = Credentials.encode()
		self._Value = base64.b64encode(CredentialsBytes).decode()

		return self._Value

class Bearer(_BaseAuthorizationMethod):
	"""Схема авторизации: Bearer."""

	#==========================================================================================#
	# >>>>> ПЕРЕОПРЕДЕЛЯЕМЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def _ReturnScheme(self) -> AuthorizationSchemes:
		"""
		Возвращает тип схемы авторизации.

		:return: Тип схемы авторизации.
		:rtype: AuthorizationSchemes
		"""

		return AuthorizationSchemes.Bearer
		
	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def is_jwt_expired(self, token: str, exception: bool = False) -> bool:
		"""
		Проверяет, устарел ли **JSON Web Token**.

		:param token: **JSON Web Token** со схемой или без.
		:type token: str
		:param exception: Указывает, выбрасывать ли исключение при устаревании токена.
		:type exception: bool
		:return: Возвращает `True`, если токен устарел.
		:rtype: bool
		:raises jwt.exceptions.DecodeError: Неверный формат токена.
		:raises TokenExpired: Токен устарел.
		"""

		token = self._ClearScheme(token)
		TokenData = jwt.decode(token, options = {"verify_signature": False})
		ExpiratonTimestamp: int = TokenData["exp"]
		IsExpired: bool = ExpiratonTimestamp < time()

		if exception and IsExpired:
			raise Exceptions.TokenExpired(datetime.fromtimestamp(ExpiratonTimestamp))

		return IsExpired

	def set_jwt(self, token: str, validate: bool = True):
		"""
		Задаёт для авторизации **JSON Web Token**.

		:param token: **JSON Web Token** со схемой или без.
		:type token: str
		:param validate: Переключает проверку срока действия токена.
		:type validate: bool
		:raises TokenExpired: Токен устарел.
		"""

		if validate: self.is_jwt_expired(token, exception = True)
		self._Value = self._ClearScheme(token)

	def set_token(self, token: str):
		"""
		Задаёт для авторизации непрозрачный токен.

		:param token: Токен со схемой или без.
		:type token: str
		"""

		self._Value = self._ClearScheme(token)

#==========================================================================================#
# >>>>> ОСНОВНОЙ КЛАСС <<<<< #
#==========================================================================================#

class Authorizator:
	"""Оператор авторизации."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def headers(self) -> dict:
		"""Словарь заголовков авторизации."""

		if not self.__IsEnabled or not self.__AuthorizationMethod:
			return {}

		return {constants.AUTHORIZATION_HEADER: f"{self.__AuthorizationMethod.scheme} {self.__AuthorizationMethod.value}"}

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self):
		"""Оператор авторизации посредством Bearer-токена."""

		self.__AuthorizationMethod: _BaseAuthorizationMethod | None = None
		self.__IsEnabled: bool = True

	def clear(self):
		"""Удаляет способ авторизации."""

		self.__AuthorizationMethod = None

	def disable(self):
		"""Отключает авторизацию."""

		self.set_using_status(False)

	def enable(self):
		"""Включает авторизацию."""

		self.set_using_status(True)

	def set_authorization_method(self, method: _BaseAuthorizationMethod):
		"""
		Устанавливает метод авторизации.

		:param method: Метод авторизации.
		:type method: _BaseAuthorizationMethod
		"""

		self.__AuthorizationMethod = method

	def set_using_status(self, status: bool):
		"""
		Задаёт статус использования авторизации.

		:param status: Статус использования авторизации.
		:type status: bool
		"""

		self.__IsEnabled = status
