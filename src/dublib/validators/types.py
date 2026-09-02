from datetime import datetime
from pathlib import Path as PathlibPath
from typing import cast, override

import dateparser
import validators
from pathvalidate import is_valid_filepath

from .base import BaseValidator

class All(BaseValidator[str]):

	@override
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
	
	@override
	@staticmethod
	def validate(value: str) -> bool:
		"""
		Проверяет, соответствует ли строка критериям валидируемого типа.

		:param value: Проверяемая строка.
		:type value: str
		:return: Возвращает `True`, если строка является валидным значением типа.
		:rtype: bool
		"""

		value # type: ignore

		return True
	
class Alpha(BaseValidator[str]):

	@override
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
	
	@override
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
	
class Base64(BaseValidator[str]):

	@override
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
	
	@override
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
			Result = validators.base64(value)
			if type(Result) is bool: return Result
		except validators.ValidationError: pass

		return False

class Bool(BaseValidator[bool]):

	@override
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
	
	@override
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

class Datetime(BaseValidator[datetime]):

	@override
	@staticmethod
	def convert(value: str) -> datetime:
		"""
		Конвертирует строку в значение определённого типа.

		:param value: Конвертируемая строка.
		:type value: str
		:return: Конвертированное значение.
		:rtype: datetime
		"""

		return cast(datetime, dateparser.parse(value))
	
	@override
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
		except (ValueError, TypeError): pass

		return False

class Domain(BaseValidator[str]):

	@override
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
	
	@override
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
			Result = validators.domain(value)
			if type(Result) is bool: return Result
		except validators.ValidationError: pass

		return False

class Email(BaseValidator[str]):

	@override
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
	
	@override
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
			Result = validators.email(value)
			if type(Result) is bool: return Result
		except validators.ValidationError: pass

		return False

class Float(BaseValidator[float]):

	@override
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
	
	@override
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

class Integer(BaseValidator[int]):

	@override
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
	
	@override
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

class IPv4(BaseValidator[str]):

	@override
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
	
	@override
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
			Result = validators.ipv4(value)
			if type(Result) is bool: return Result
		except validators.ValidationError: pass

		return False

class IPv6(BaseValidator[str]):

	@override
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
	
	@override
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
			Result = validators.ipv6(value)
			if type(Result) is bool: return Result
		except validators.ValidationError: pass

		return False

class Number(BaseValidator[float | int]):

	@override
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
	
	@override
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

class Path(BaseValidator[PathlibPath]):

	@override
	@staticmethod
	def convert(value: str) ->  PathlibPath:
		"""
		Конвертирует строку в значение определённого типа.

		:param value: Конвертируемая строка.
		:type value: str
		:return: Конвертированное значение.
		:rtype: pathlib.Path
		"""

		return PathlibPath(value)
	
	@override
	@staticmethod
	def validate(value: str) -> bool:
		"""
		Проверяет, соответствует ли строка критериям валидируемого типа.

		:param value: Проверяемая строка.
		:type value: str
		:return: Возвращает `True`, если строка является валидным значением типа.
		:rtype: bool
		"""

		return is_valid_filepath(value)

class UnsignedInteger(BaseValidator[int]):

	@override
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
	
	@override
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
	
class URL(BaseValidator[str]):

	@override
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
	
	@override
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
			Result = validators.url(value)
			if type(Result) is bool: return Result
		except validators.ValidationError: pass

		return False

class ValidPath(BaseValidator[PathlibPath]):

	@override
	@staticmethod
	def convert(value: str) ->  PathlibPath:
		"""
		Конвертирует строку в значение определённого типа.

		:param value: Конвертируемая строка.
		:type value: str
		:return: Конвертированное значение.
		:rtype: pathlib.Path
		"""

		return PathlibPath(value)
	
	@override
	@staticmethod
	def validate(value: str) -> bool:
		"""
		Проверяет, соответствует ли строка критериям валидируемого типа.

		:param value: Проверяемая строка.
		:type value: str
		:return: Возвращает `True`, если строка является валидным значением типа.
		:rtype: bool
		"""

		return PathlibPath(value).exists()