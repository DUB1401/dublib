from typing import Any, overload, Sequence
import copy

import orjson

#==========================================================================================#
# >>>>> ФУНКЦИИ ПРЕОБРАЗОВАНИЯ ТИПОВ ДАННЫХ <<<<< #
#==========================================================================================#

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
	:param literals: Набор строк, интерпретируемых как `False`.
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

#==========================================================================================#
# >>>>> ФУНКЦИИ РАБОТЫ СО СТРОКАМИ <<<<< #
#==========================================================================================#

def CheckForCyrillic(text: str) -> bool:
	"""
	Проверяет, имеются ли кирилические символы в строке.

	:param text: Проверяемая строка.
	:type text: str
	:return: Возвращает `True`, если строка содержит хотя бы один кирилический символ.
	:rtype: bool
	"""
	
	Alphabet = set("абвгдеёжзийклмнопрстуфхцчшщъыьэюя")

	for Char in text.lower():
		if Char in Alphabet: return True
	
	return False

def СontainsAlpha(text: str) -> bool:
	"""
	Проверяет, содержит ли строка хотя бы один буквенный символ.

	:param text: Проверяемая строка.
	:type text: str
	:return: Возвращает `True` для строки, в которой хотя бы один символ проходит проверку `isalpha()`.
	:rtype: bool
	"""

	for Char in text:
		if Char.isalpha(): return True

	return False

def MultipleReplace(string: str, values: Sequence[str], new_value: str) -> str:
	"""
	Поочердёно выполняет замену подстрок в строке на новое значение.

	:param string: Обрабатываемая строка.
	:type string: str
	:param values: Последовательность заменяемых значений.
	:type values: Sequence[str]
	:param new_value: Новое значение для подстановки.
	:type new_value: str
	:return: Обработанная строка.
	:rtype: str
	"""
	
	for Value in values: string = string.replace(Value, new_value)

	return string

def RemoveRecurringSubstrings(string: str, substring: str) -> str:
	"""
	Удаляет из строки подряд идущие повторяющиеся подстроки.

	:param string: Обрабатываемая строка.
	:type string: str
	:param substring: Удаляемая подстрока.
	:type substring: str
	:return: Обработанная строка.
	:rtype: str
	"""

	while substring + substring in string: string = string.replace(substring + substring, substring)

	return string

def StripAlpha(text: str) -> str:
	"""
	Удаляет из строки начальные и конечные небуквенные символы.

	:param text: Обрабатываемая строка.
	:type text: str
	:return: Обработанная строка.
	:rtype: str
	"""

	Start, End = 0, len(text)
	while Start < End and not text[Start].isalpha(): Start += 1
	while End > Start and not text[End - 1].isalpha(): End -= 1
  
	return text[Start:End]

#==========================================================================================#
# >>>>> ФУНКЦИИ РАБОТЫ СО СЛОВАРЯМИ <<<<< #
#==========================================================================================#

def MergeDictionaries(base_dictionary: dict, mergeable_dictionary: dict, overwrite: bool = False) -> dict:
	"""
	Объединяет словари.

	:param base_dictionary: Словарь, в который выполняется копирование.
	:type base_dictionary: dict
	:param mergeable_dictionary: Словарь, из котрого выполняется копирование.
	:type mergeable_dictionary: dict
	:param overwrite: Указывает, нужно ли перезаписывать значения конфликтующих ключей базового словаря. По умолчанию `False`.
	:type overwrite: bool
	:return: Словарь, образованный слиянием двух переданных словарей.
	:rtype: dict
	"""
 
	for key, value in mergeable_dictionary.items():
		if overwrite or key not in base_dictionary:
			base_dictionary[key] = value
			
	return base_dictionary

def ReplaceDictionaryKey(dictionary: dict, old_key: Any, new_key: Any) -> dict:
	"""
	Заменяет ключ в словаре, сохраняя исходный порядок элементов.

	:param dictionary: Обрабатываемый словарь.
	:type dictionary: dict
	:param old_key: Старый ключ.
	:type old_key: Any
	:param new_key: Новый ключ.
	:type new_key: Any
	:raises KeyError: Выбрасывается при отсутствии старого ключа в словаре.
	:return: Обработанный словарь.
	:rtype: dict
	"""
	
	Result = dict()
	if old_key not in dictionary.keys(): raise KeyError(old_key)

	for Key in dictionary.keys():
		if Key == old_key: Result[new_key] = dictionary[old_key]
		else: Result[Key] = dictionary[Key]

	return Result