from typing import Sequence

_CYRYLLIC_CHARACTERS: set = set("абвгдеёжзийклмнопрстуфхцчшщъыьэюя")

def CheckForCyrillic(text: str) -> bool:
	"""
	Проверяет, имеются ли кирилические символы в строке.

	:param text: Проверяемая строка.
	:type text: str
	:return: Возвращает `True`, если строка содержит хотя бы один кирилический символ.
	:rtype: bool
	"""

	for Char in text.lower():
		if Char in _CYRYLLIC_CHARACTERS: return True
	
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
