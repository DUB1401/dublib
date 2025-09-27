from typing import Any, Type, Iterable

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
	except: return copy.deepcopy(data)

def ToIterable(value: Any, iterable_type: Type[Iterable] = tuple, exclude: tuple[Type[Iterable], ...] = (bytes, str)) -> Iterable:
	"""
	Преобразует значение в итерируемый тип.

	:param value: Обрабатываемое значение.
	:type value: Any
	:param iterable_type: Целевой тип итерируемого контейнера. По умолчанию `tuple`.
	:type iterable_type: Type[Iterable]
	:param exclude: Типы-исключения, условно считающиеся неитерируемыми. По умолчанию `bytes`, `str`.
	:type exclude: tuple[Type[Iterable], ...]
	:return: Приведённое к итерируемому типу значению.
	:rtype: Iterable
	"""

	if isinstance(value, Iterable) and not isinstance(value, exclude): return value
	
	return iterable_type([value])

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

def MultipleReplace(string: str, values: Iterable[str], new_value: str) -> str:
	"""
	Поочердёно выполняет замену подстрок в строке на новое значение.

	:param string: Обрабатываемая строка.
	:type string: str
	:param values: Последовательность заменяемых значений.
	:type values: Iterable[str]
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

def CheckForCyrillic(text: str) -> bool:
	"""
	Проверяет, имеются ли кирилические символы в строке.

	:param text: Проверяемая строка.
	:type text: str
	:return: Возвращает `True`, если строка содержит хотя бы один кирилический символ.
	:rtype: bool
	"""
	
	Alphabet = set("абвгдеёжзийклмнопрстуфхцчшщъыьэюя")
	
	return any(Char in Alphabet for Char in text.lower())

def IsNotAlpha(text: str) -> bool:
	"""
	Проверяет, состоит ли строка целиком из небуквенных символов.

	:param text: Проверяемая строка.
	:type text: str
	:return: Возвращает `True` для строки, каждый символ которой при проверке `isalpha()` считается небуквенным.
	:rtype: bool
	"""

	return not any(Char.isalpha() for Char in text)

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