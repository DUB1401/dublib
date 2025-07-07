from .Decorators import deprecated

from typing import Any, Iterable

#==========================================================================================#
# >>>>> ФУНКЦИИ ПРОВЕРКИ ДАННЫХ <<<<< #
#==========================================================================================#

def CheckForCyrillic(text: str) -> bool:
	"""
	Проверяет, имеются ли кирилические символы в строке.
		text – проверяемая строка.
	"""
	alphabet = set("абвгдеёжзийклмнопрстуфхцчшщъыьэюя")
	return any(char in alphabet for char in text.lower())


def IsNotAlpha(text: str) -> bool:
	"""
	Проверяет, состоит ли строка целиком из небуквенных символов.
	"""

	return not any(char.isalpha() for char in text)

#==========================================================================================#
# >>>>> ФУНКЦИИ ОБРАБОТКИ ДАННЫХ <<<<< #
#==========================================================================================#

@deprecated(message = "Use itertools.batched() instead.")
def ChunkList(value: list, length: int) -> list[list]:
	"""
	Разделяет список на фрагменты фиксированной длинны.
		value – обрабатываемое значение;\n
		length – длина фрагментов.
	"""
	Result = list()
	CutIndex = 1
	Buffer = list()

	for Index in range(len(value)):

		if CutIndex == length:
			Result.append(Buffer)
			Buffer = list()

		else:
			Buffer.append(value[Index])

		CutIndex += 1

	if len(Buffer) > 0: Result.append(Buffer)

	return Result

def MergeDictionaries(base_dictionary: dict, mergeable_dictionary: dict, overwrite: bool = False) -> dict:
	"""
	Объединяет словари.
		base_dictionary – словарь, в который идёт копирование;\n
		mergeable_dictionary – словарь, из котрого идёт копирование;\n
		overwrite – указывает, нужно ли перезаписывать значения конфликтующих ключей базового словаря.
	"""
 
	for key, value in mergeable_dictionary.items():
		if overwrite or key not in base_dictionary:
			base_dictionary[key] = value
	return base_dictionary
    

def MultipleReplace(string: str, values: list[str], new_value: str) -> str:
	"""
	Поочердёно выполняет замену подстрок в строке на новое значение.
		string – обрабатываемая строка;\n
		values – список значений;\n
		new_value – значение для замены.
	"""
	
	for Value in values: string = string.replace(Value, new_value)

	return string

def RemoveRecurringSubstrings(string: str, substring: str) -> str:
	"""
	Удаляет из строки подряд идущие повторяющиеся подстроки.
		string – строка, из которой удаляются повторы;\n
		Substring – удаляемая подстрока.
	"""

	while substring + substring in string: string = string.replace(substring + substring, substring)

	return string

def ReplaceDictionaryKey(dictionary: dict, old_key, new_key) -> dict:
	"""
	Заменяет ключ в словаре, сохраняя исходный порядок элементов.
		dictionary – обрабатываемый словарь;\n
		old_key – старое название ключа;\n
		new_key – новое название ключа.
	"""
	
	Result = dict()
	if old_key not in dictionary.keys(): raise KeyError(str(old_key))

	for Key in dictionary.keys():

		if Key == old_key:
			Result[new_key] = dictionary[old_key]

		else:
			Result[Key] = dictionary[Key]

	return Result

def StripAlpha(text: str) -> str:
	"""
	Удаляет из строки начальные и конечные небуквенные символы.
		text – обрабатываемая строка.
	"""

	start, end = 0, len(text)
	while start < end and not text[start].isalpha():
		start += 1
	while end > start and not text[end - 1].isalpha():
		end -= 1
  
	return text[start:end]

def ToIterable(value: Any, iterable_type: type[Iterable] = tuple, exclude: tuple[Iterable] = (bytes, str)) -> Iterable:
	"""
	Преобразует значение в итерируемый тип.

	:param value: Обрабатываемое значение.
	:type value: Any
	:param iterable_type: Целевой тип итерируемого контейнера. По умолчанию `tuple`.
	:type iterable_type: type[Iterable]
	:param exclude: Типы-исключения, условно считающиеся неитерируемыми. По умолчанию `bytes`, `str`.
	:type exclude: tuple[Iterable]
	:return: Приведённое к итерируемому типу значению.
	:rtype: Iterable
	"""

	if isinstance(value, Iterable) and not isinstance(value, exclude): return value
	else: value = iterable_type([value])

	return value

def Zerotify(value: Any) -> Any:
	"""
	Преобразует значения, логически интерпретируемые в False, в тип None.
		value – обрабатываемое значение.
	"""

	if bool(value) == False: value = None

	return value
