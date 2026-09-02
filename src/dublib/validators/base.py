from abc import ABC, abstractmethod

from ..exceptions.validators import ValidationError

class BaseValidator[T](ABC):
	"""Базовый валидатор строки."""

	@staticmethod
	@abstractmethod
	def convert(value: str) -> T:
		"""
		Конвертирует строку в значение определённого типа без проведения валидации.

		:param value: Конвертируемая строка.
		:type value: str
		:return: Конвертированное значение.
		:rtype: Any
		"""

		pass

	@classmethod
	def parse(cls, value: str) -> T:
		"""
		Проводит валидацию строки и преобразует её в целевой тип.

		:param value: Обрабатываемая строка.
		:type value: str
		:return: Результат преобразования.
		:rtype: Any
		:raises ValidationError: Ошибка валидации.
		"""

		if not cls.validate(value): raise ValidationError(value, cls)

		return cls.convert(value)

	@staticmethod
	@abstractmethod
	def validate(value: str) -> bool:
		"""
		Проверяет, соответствует ли строка критериям валидируемого типа.

		:param value: Проверяемая строка.
		:type value: str
		:return: Возвращает `True`, если строка является валидным значением типа.
		:rtype: bool
		"""

		pass
