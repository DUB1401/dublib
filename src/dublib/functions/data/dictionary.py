from typing import Any

import more_itertools

def insert_after_ley(base_dictionary: dict, insertable_dictionary: dict, target_key: Any, overwrite: bool = False) -> dict:
	"""
	Вставляет словарь после определённого ключа. При конфликте ключей приоритет расположения отдаётся порядку ключей из вставляемого словаря.

	:param base_dictionary: Исходный словарь. Не изменяется.
	:type base_dictionary: dict
	:param insertable_dictionary: Вставляемый словарь.
	:type insertable_dictionary: dict
	:param target_key: Целевой ключ, после которого производится вставка.
	:type target_key: Any
	:param overwrite: Указывает, нужно ли перезаписать значения при конфликте ключей.
	:type overwrite: bool
	:return: Объединённые словари.
	:rtype: dict
	:raises KeyError: Целевой ключ не найден.
	"""

	BaseKeys: list = list(base_dictionary.keys())

	if target_key not in BaseKeys:
		raise KeyError(target_key)

	FirstPart, SecondPart = more_itertools.split_after(BaseKeys, lambda element: element == target_key, maxsplit = 1)
	Result: dict = {}

	for FirstPartKey in FirstPart: Result[FirstPartKey] = base_dictionary[FirstPartKey]
	for InsertableKey in insertable_dictionary.keys(): Result[InsertableKey] = insertable_dictionary[InsertableKey]

	for SecondPartKey in SecondPart:

		if SecondPartKey in Result:
			if not overwrite: Result[SecondPartKey] = base_dictionary[SecondPartKey]

		else: Result[SecondPartKey] = base_dictionary[SecondPartKey]

	return Result

def lower_keys(data: dict) -> dict:
	"""
	Приводит все строковые ключи словаря в нижний регистр.

	:param data: Обрабатываемый словарь.
	:type data: dict
	:return: Обработанный словарь.
	:rtype: dict
	"""

	return {Key.lower() if type(Key) is str else Key: Value for Key, Value in data.items()}

def replace_key(dictionary: dict, old_key: Any, new_key: Any) -> dict:
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
	
	Result = {}
	if old_key not in dictionary:
		raise KeyError(old_key)

	for Key in dictionary.keys():
		if Key == old_key: Result[new_key] = dictionary[old_key]
		else: Result[Key] = dictionary[Key]

	return Result