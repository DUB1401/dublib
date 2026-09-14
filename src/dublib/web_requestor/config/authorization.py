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
	def scheme(self) -> AuthorizationSchemes:
		"""Схема авторизации."""

		return self._Scheme

	#==========================================================================================#
	# >>>>> НАСЛЕДУЕМЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def _remove_scheme(self, data: str) -> str:
		"""
		Удаляет из данных авторизации схему.

		:param data: Данные авторизации.
		:type data: str
		:return: Очищенные данные.
		:rtype: str
		"""

		scheme_length: int = len(self._Scheme.value)

		if data.lower().startswith(self._Scheme.value.lower()):
			return data[:scheme_length * -1].strip()

		return data

	#==========================================================================================#
	# >>>>> ПЕРЕОПРЕДЕЛЯЕМЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	@abstractmethod
	def _export_scheme(self) -> AuthorizationSchemes:
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

		self._Scheme: AuthorizationSchemes = self._export_scheme()
		self._Value: str | None = None

	def clear(self):
		"""Очищает данные авторизации."""

		self._Value = None

class Basic(_BaseAuthorizationMethod):
	"""Схема авторизации: Basic."""

	#==========================================================================================#
	# >>>>> ПЕРЕОПРЕДЕЛЯЕМЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def _export_scheme(self) -> AuthorizationSchemes:
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

	def _export_scheme(self) -> AuthorizationSchemes:
		"""
		Возвращает тип схемы авторизации.

		:return: Тип схемы авторизации.
		:rtype: AuthorizationSchemes
		"""

		return AuthorizationSchemes.Bearer
		
	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def get_jwt_expiration_date(self, token: str) -> datetime:
		"""
		Определяет дату и время истечения токена.

		:param token: **JSON Web Token** со схемой или без.
		:type token: str
		:return: Дата и время истечения токена.
		:rtype: datetime
		"""

		token = self._remove_scheme(token)
		token_data: dict = jwt.decode(token, options = {"verify_signature": False})
		expiration_timestamp: int = token_data["exp"]

		return datetime.fromtimestamp(expiration_timestamp)

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
		:raises TokenExpiredError: Токен устарел.
		"""

		expiration_date = self.get_jwt_expiration_date(token)
		is_expired: bool = expiration_date.timestamp() < time()

		if exception and is_expired:
			raise Exceptions.TokenExpiredError(expiration_date)

		return is_expired

	def set_jwt(self, token: str, validate: bool = True):
		"""
		Задаёт для авторизации **JSON Web Token**.

		:param token: **JSON Web Token** со схемой или без.
		:type token: str
		:param validate: Переключает проверку срока действия токена.
		:type validate: bool
		:raises TokenExpiredError: Токен устарел.
		"""

		if validate: self.is_jwt_expired(token, exception = True)
		self._Value = self._remove_scheme(token)

	def set_token(self, token: str):
		"""
		Задаёт для авторизации непрозрачный токен.

		:param token: Токен со схемой или без.
		:type token: str
		"""

		self._Value = self._remove_scheme(token)

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

		return {constants.AUTHORIZATION_HEADER: f"{self.__AuthorizationMethod.scheme.value} {self.__AuthorizationMethod.value}"}

	@property
	def method(self) -> _BaseAuthorizationMethod | None:
		"""Используемый метод авторизации."""

		return self.__AuthorizationMethod

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
