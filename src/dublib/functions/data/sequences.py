from typing import Any, overload

from . import dictionary as dictionary
from . import string as string

@overload
def to_sequence(value: Any, target_type: type[list]) -> list: ...
@overload
def to_sequence(value: Any, target_type: type[set]) -> set: ...
@overload
def to_sequence(value: Any, target_type: type[tuple] = ...) -> tuple: ...

def to_sequence(value: Any, target_type: type[list | set | tuple] = tuple) -> list | set | tuple:
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
