import copy
from typing import Any, Sequence

import orjson

from . import dictionary as dictionary
from . import string as string
from .sequences import to_sequence

__all__ = [
	"deep_copy",
	"stringify_float",
	"string_to_bool",
	"to_sequence",
	"zerotify"
]

def deep_copy(data: Any) -> Any:
	"""
	Выполняет глубокое копирование объекта с автоматическим определением наилучшего метода.
	
	Объекты, которые могут быть сериализованы в JSON (`dict`, `list`, `tuple`), копируются с помощью десериализации/сериализации библиотекой **orjson**. В остальных случаях вызывается `copy.deepcopy()`.

	:param data: Копируемый объект.
	:type data: Any
	:return: Копия объекта.
	:rtype: Any
	"""
	
	try: return orjson.loads(orjson.dumps(data))
	except (orjson.JSONDecodeError, orjson.JSONEncodeError): return copy.deepcopy(data)

def stringify_float(number: float, round_factor: int = 2) -> str:
	"""
	Преобразует число с плавающей запятой в строку, отсекая `.0` в конце при наличии.

	:param number: Преобразуемое число.
	:type number: float
	:param round_factor: Оставляемое количество символов после запятой.
	:type round_factor: int
	:return: Полученная строка.
	:rtype: str
	"""

	String = str(round(number, round_factor))
	if String.endswith(".0"): String = String[:-2]

	return String

def string_to_bool(value: str, literals: Sequence[str] = ("false", "0")) -> bool:
	"""
	Преобразует строку в логический тип, учитывая её содержимое.
	
	Например, `"false"` будет приведено к `False`, в отличие от стандартной реализации.

	:param value: Преобразуемая строка.
	:type value: str
	:param literals: Набор строк, интерпретируемых как `False`. Нечувствителен к регистру.
	:type literals: Sequence[str]
	:return: Результирующее значение.
	:rtype: bool
	"""

	if value.lower() in literals: return False

	return bool(value)

def zerotify(value: Any) -> Any:
	"""
	Преобразует значения, логически интерпретируемые в `False`, в тип `None`.

	:param value: Проверяемое значение.
	:type value: Any
	:return: Возвращает `None` при возможности логической интерпретации значения в `False`. Иначе возвращает переданное значение.
	:rtype: Any
	"""

	return None if not value else value
