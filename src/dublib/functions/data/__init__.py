import copy
from typing import Any, Sequence, overload

import orjson

from . import dictionary as dictionary
from . import string as string

def Copy(data: Any) -> Any:
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

def StringifyFloat(number: float, round_factor: int = 2) -> str:
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

def StringToBool(value: str, literals: Sequence[str] = ("false", "0")) -> bool:
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

@overload
def ToSequence(value: Any, target_type: type[list]) -> list: ...

@overload
def ToSequence(value: Any, target_type: type[set]) -> set: ...

@overload
def ToSequence(value: Any, target_type: type[tuple] = ...) -> tuple: ...

def ToSequence(value: Any, target_type: type[list | set | tuple] = tuple) -> list | set | tuple:
	"""
	Преобразует значение в итерируемый контейнерн целевого типа.

	:param value: Обрабатываемое значение или итерируемый контейнер значений.
	:type value: Any
	:param target_type: Целевой тип итерируемого контейнера.
	:type target_type: type[list | set | tuple]
	:return: Приведённое к итерируемому контейнеру значение (единичные элементы упаковываются в контейнер, контейнеры преобразуются в целевой тип).
	:rtype: list | set | tuple
	"""

	if type(value) is target_type: return value
	if type(value) in (list, set, tuple): return target_type(value)
	
	return target_type((value,))

def Zerotify(value: Any) -> Any:
	"""
	Преобразует значения, логически интерпретируемые в `False`, в тип `None`.

	:param value: Проверяемое значение.
	:type value: Any
	:return: Возвращает `None` при возможности логической интерпретации значения в `False`. Иначе возвращает переданное значение.
	:rtype: Any
	"""

	return None if not value else value
