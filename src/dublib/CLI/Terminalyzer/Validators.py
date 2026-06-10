from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from datetime import datetime
from pathlib import Path
from enum import Enum

import dateparser
import validators

#==========================================================================================#
# >>>>> БАЗОВЫЙ КЛАСС <<<<< #
#==========================================================================================#

_PARSED_VALUE = TypeVar("PARSED_VALUE")

class ValidationError(Exception):
	"""Исключение: ошибка приведения строки к определённому типу."""

	def __init__(self, value: str, target_type: "ValidableValuesTypes"):
		"""
		Исключение: ошибка приведения строки к определённому типу.

		:param value: Значение.
		:type value: str
		:param target_type: Тип, к которому происходило приведение.
		:type target_type: ValidableValuesTypes
		"""

		super().__init__(f"Unable convert \"{value}\" to \"{target_type.__name__}\" type.")

class BaseValidator(ABC, Generic[_PARSED_VALUE]):
	"""Базовый валидатор строки."""

	@abstractmethod
	@staticmethod
	def convert(value: str) -> _PARSED_VALUE:
		"""
		Конвертирует строку в значение определённого типа.

		:param value: Конвертируемая строка.
		:type value: str
		:return: Конвертированное значение.
		:rtype: Any
		"""

		pass

	@classmethod
	def parse(cls, value: str) -> _PARSED_VALUE:
		"""
		Проводит валидацию строки и преобразует её в целевой тип.

		:param value: Обрабатываемая строка.
		:type value: str
		:return: Результат преобразования.
		:rtype: Any
		"""

		if not cls.validate(value): raise ValidationError(value, ValidableValuesTypes(cls))

		return cls.convert(value)

	@abstractmethod
	@staticmethod
	def validate(value: str) -> bool:
		"""
		Проверяет, соответствует ли строка критериям валидируемого типа.

		:param value: Проверяемая строка.
		:type value: str
		:return: Возвращает `True`, если строка является валидным значением типа.
		:rtype: bool
		"""

		pass

#==========================================================================================#
# >>>>> ВАЛИДАТОРЫ <<<<< #
#==========================================================================================#

class Validator_All(BaseValidator[str]):

	@staticmethod
	def convert(value: str) -> str:
		"""
		Конвертирует строку в значение определённого типа.

		:param value: Конвертируемая строка.
		:type value: str
		:return: Конвертированное значение.
		:rtype: str
		"""

		return value
	
	@staticmethod
	def validate(value: str) -> bool:
		"""
		Проверяет, соответствует ли строка критериям валидируемого типа.

		:param value: Проверяемая строка.
		:type value: str
		:return: Возвращает `True`, если строка является валидным значением типа.
		:rtype: bool
		"""

		return True
	
class Validator_Alpha(BaseValidator[str]):

	@staticmethod
	def convert(value: str) -> str:
		"""
		Конвертирует строку в значение определённого типа.

		:param value: Конвертируемая строка.
		:type value: str
		:return: Конвертированное значение.
		:rtype: str
		"""

		return value
	
	@staticmethod
	def validate(value: str) -> bool:
		"""
		Проверяет, соответствует ли строка критериям валидируемого типа.

		:param value: Проверяемая строка.
		:type value: str
		:return: Возвращает `True`, если строка является валидным значением типа.
		:rtype: bool
		"""

		return value.isalpha()
	
class Validator_Base64(BaseValidator[str]):

	@staticmethod
	def convert(value: str) -> str:
		"""
		Конвертирует строку в значение определённого типа.

		:param value: Конвертируемая строка.
		:type value: str
		:return: Конвертированное значение.
		:rtype: str
		"""

		return value
	
	@staticmethod
	def validate(value: str) -> bool:
		"""
		Проверяет, соответствует ли строка критериям валидируемого типа.

		:param value: Проверяемая строка.
		:type value: str
		:return: Возвращает `True`, если строка является валидным значением типа.
		:rtype: bool
		"""

		try: return validators.base64(value)
		except validators.ValidationError: return False

class Validator_Bool(BaseValidator[bool]):

	@staticmethod
	def convert(value: str) -> bool:
		"""
		Конвертирует строку в значение определённого типа.

		:param value: Конвертируемая строка.
		:type value: str
		:return: Конвертированное значение.
		:rtype: bool
		"""

		value = value.lower()
		if value in ("true",): return True

		return False
	
	@staticmethod
	def validate(value: str) -> bool:
		"""
		Проверяет, соответствует ли строка критериям валидируемого типа.

		:param value: Проверяемая строка.
		:type value: str
		:return: Возвращает `True`, если строка является валидным значением типа.
		:rtype: bool
		"""

		Buffer = value.lower()

		return Buffer in ("true", "false")

class Validator_Datetime(BaseValidator[datetime]):

	@staticmethod
	def convert(value: str) -> datetime:
		"""
		Конвертирует строку в значение определённого типа.

		:param value: Конвертируемая строка.
		:type value: str
		:return: Конвертированное значение.
		:rtype: datetime
		"""

		return dateparser.parse(value)
	
	@staticmethod
	def validate(value: str) -> bool:
		"""
		Проверяет, соответствует ли строка критериям валидируемого типа.

		:param value: Проверяемая строка.
		:type value: str
		:return: Возвращает `True`, если строка является валидным значением типа.
		:rtype: bool
		"""

		try: 
			dateparser.parse(value)
			return True
		except: pass

		return False

class Validator_Email(BaseValidator[str]):

	@staticmethod
	def convert(value: str) -> str:
		"""
		Конвертирует строку в значение определённого типа.

		:param value: Конвертируемая строка.
		:type value: str
		:return: Конвертированное значение.
		:rtype: str
		"""

		return value
	
	@staticmethod
	def validate(value: str) -> bool:
		"""
		Проверяет, соответствует ли строка критериям валидируемого типа.

		:param value: Проверяемая строка.
		:type value: str
		:return: Возвращает `True`, если строка является валидным значением типа.
		:rtype: bool
		"""

		try: return validators.email(value)
		except validators.ValidationError: return False

class Validator_Float(BaseValidator[float]):

	@staticmethod
	def convert(value: str) -> float:
		"""
		Конвертирует строку в значение определённого типа.

		:param value: Конвертируемая строка.
		:type value: str
		:return: Конвертированное значение.
		:rtype: float
		"""

		return float(value)
	
	@staticmethod
	def validate(value: str) -> bool:
		"""
		Проверяет, соответствует ли строка критериям валидируемого типа.

		:param value: Проверяемая строка.
		:type value: str
		:return: Возвращает `True`, если строка является валидным значением типа.
		:rtype: bool
		"""

		return value.count("-") <= 1 and value.count(".") == 1 and value.replace(".", "").lstrip("-").isdigit()

class Validator_Integer(BaseValidator[int]):

	@staticmethod
	def convert(value: str) -> int:
		"""
		Конвертирует строку в значение определённого типа.

		:param value: Конвертируемая строка.
		:type value: str
		:return: Конвертированное значение.
		:rtype: int
		"""

		return int(value)
	
	@staticmethod
	def validate(value: str) -> bool:
		"""
		Проверяет, соответствует ли строка критериям валидируемого типа.

		:param value: Проверяемая строка.
		:type value: str
		:return: Возвращает `True`, если строка является валидным значением типа.
		:rtype: bool
		"""

		return value.count("-") <= 1 and value.lstrip("-").isdigit()

class Validator_IPv4(BaseValidator[str]):

	@staticmethod
	def convert(value: str) -> str:
		"""
		Конвертирует строку в значение определённого типа.

		:param value: Конвертируемая строка.
		:type value: str
		:return: Конвертированное значение.
		:rtype: str
		"""

		return value
	
	@staticmethod
	def validate(value: str) -> bool:
		"""
		Проверяет, соответствует ли строка критериям валидируемого типа.

		:param value: Проверяемая строка.
		:type value: str
		:return: Возвращает `True`, если строка является валидным значением типа.
		:rtype: bool
		"""

		try: return validators.ipv4(value)
		except validators.ValidationError: return False

class Validator_IPv6(BaseValidator[str]):

	@staticmethod
	def convert(value: str) -> str:
		"""
		Конвертирует строку в значение определённого типа.

		:param value: Конвертируемая строка.
		:type value: str
		:return: Конвертированное значение.
		:rtype: str
		"""

		return value
	
	@staticmethod
	def validate(value: str) -> bool:
		"""
		Проверяет, соответствует ли строка критериям валидируемого типа.

		:param value: Проверяемая строка.
		:type value: str
		:return: Возвращает `True`, если строка является валидным значением типа.
		:rtype: bool
		"""

		try: return validators.ipv6(value)
		except validators.ValidationError: return False

class Validator_Number(BaseValidator[float | int]):

	@staticmethod
	def convert(value: str) -> float | int:
		"""
		Конвертирует строку в значение определённого типа.

		:param value: Конвертируемая строка.
		:type value: str
		:return: Конвертированное значение.
		:rtype: float | int
		"""

		return float(value) if "." in value else int(value)
	
	@staticmethod
	def validate(value: str) -> bool:
		"""
		Проверяет, соответствует ли строка критериям валидируемого типа.

		:param value: Проверяемая строка.
		:type value: str
		:return: Возвращает `True`, если строка является валидным значением типа.
		:rtype: bool
		"""

		if "." in value:
			try: 
				float(value)
				return True
			except ValueError: return False

		else:
			try:
				int(value)
				return True
			except ValueError: return False

class Validator_Path(BaseValidator[Path]):

	@staticmethod
	def convert(value: str) ->  Path:
		"""
		Конвертирует строку в значение определённого типа.

		:param value: Конвертируемая строка.
		:type value: str
		:return: Конвертированное значение.
		:rtype: Path
		"""

		return Path(value)
	
	@staticmethod
	def validate(value: str) -> bool:
		"""
		Проверяет, соответствует ли строка критериям валидируемого типа.

		:param value: Проверяемая строка.
		:type value: str
		:return: Возвращает `True`, если строка является валидным значением типа.
		:rtype: bool
		"""

		try: 
			Path(value)
			return True
		except: return False

class Validator_UnsignedInteger(BaseValidator[int]):

	@staticmethod
	def convert(value: str) ->  int:
		"""
		Конвертирует строку в значение определённого типа.

		:param value: Конвертируемая строка.
		:type value: str
		:return: Конвертированное значение.
		:rtype: int
		"""

		return int(value)
	
	@staticmethod
	def validate(value: str) -> bool:
		"""
		Проверяет, соответствует ли строка критериям валидируемого типа.

		:param value: Проверяемая строка.
		:type value: str
		:return: Возвращает `True`, если строка является валидным значением типа.
		:rtype: bool
		"""

		return value.isdigit()
	
class Validator_URL(BaseValidator[str]):

	@staticmethod
	def convert(value: str) ->  str:
		"""
		Конвертирует строку в значение определённого типа.

		:param value: Конвертируемая строка.
		:type value: str
		:return: Конвертированное значение.
		:rtype: str
		"""

		return value
	
	@staticmethod
	def validate(value: str) -> bool:
		"""
		Проверяет, соответствует ли строка критериям валидируемого типа.

		:param value: Проверяемая строка.
		:type value: str
		:return: Возвращает `True`, если строка является валидным значением типа.
		:rtype: bool
		"""

		try: return validators.url(value)
		except validators.ValidationError: return False

class Validator_ValidPath(BaseValidator[Path]):

	@staticmethod
	def convert(value: str) ->  Path:
		"""
		Конвертирует строку в значение определённого типа.

		:param value: Конвертируемая строка.
		:type value: str
		:return: Конвертированное значение.
		:rtype: Path
		"""

		return Path(value)
	
	@staticmethod
	def validate(value: str) -> bool:
		"""
		Проверяет, соответствует ли строка критериям валидируемого типа.

		:param value: Проверяемая строка.
		:type value: str
		:return: Возвращает `True`, если строка является валидным значением типа.
		:rtype: bool
		"""

		try: return Path(value).exists()
		except: return False

#==========================================================================================#
# >>>>> ПЕРЕЧИСЛЕНИЕ ВАЛИДАТОРОВ <<<<< #
#==========================================================================================#

class ValidableValuesTypes(Enum):
	"""Перечисление типов валидаторов."""

	All = Validator_All
	Alpha = Validator_Alpha
	Base64 = Validator_Base64
	Bool = Validator_Bool
	Datetime = Validator_Datetime
	Email = Validator_Email
	Float = Validator_Float
	Integer = Validator_Integer
	IPv4 = Validator_IPv4
	IPv6 = Validator_IPv6
	Number = Validator_Number
	Path = Validator_Path
	UnsignedInteger = Validator_UnsignedInteger
	URL = Validator_URL
	ValidPath = Validator_ValidPath