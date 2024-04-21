import shutil
import html
import json
import sys
import os
import re

#==========================================================================================#
# >>>>> ФУНКЦИИ РАБОТЫ С СИСТЕМОЙ <<<<< #
#==========================================================================================#

def CheckPythonMinimalVersion(major: int, minor: int, raise_exception: bool = True) -> bool:
	"""
	Проверяет, соответствует ли используемая версия Python минимальной требуемой.
		major – идентификатор Major-версии Python;
		minor – идентификатор Minor-версии Python;
		raise_exception – указывает, как поступать при несоответствии версии: выбрасывать исключение или возвращать значение.
	"""

	# Состояние: корректна ли версия.
	IsVersionCorrect = True
	
	# Если версия Python старше минимальной требуемой.
	if sys.version_info < (major, minor): 
		
		# Если указано выбросить исключение.
		if raise_exception == True:
			# Выброс исключения.
			raise RuntimeError(f"Python {major}.{minor} or newer is required.")

		else: 
			# Переключение статуса проверки.
			IsVersionCorrect = False

	return IsVersionCorrect

def Cls():
	"""Очищает консоль."""

	os.system("cls" if os.name == "nt" else "clear")

def MakeRootDirectories(directories: list[str]):
	"""
	Создаёт каталоги в текущей корневой директории скрипта.
		directories – список названий каталогов.
	"""
	
	# Для каждого названия каталога.
	for Name in directories:
		# Если каталог не существует, то создать его.
		if os.path.exists(Name) == False: os.makedirs(Name)

def RemoveFolderContent(path: str):
	"""
	Удаляет всё содержимое каталога.
		path – путь к каталогу.
	"""

	# Список содержимого в папке.
	FolderContent = os.listdir(path)

	# Для каждого элемента.
	for Item in FolderContent:

		# Если элемент является каталогом.
		if os.path.isdir(path + "/" + Item):
			# Удаление каталога.
			shutil.rmtree(path + "/" + Item)

		else:
			# Удаление файла.
			os.remove(path + "/" + Item)

def Shutdown():
	"""Выключает устройство."""

	# Если устройство работает под управлением ОС семейства Linux.
	if sys.platform in ["linux", "linux2"]: os.system("sudo shutdown now")
	# Если устройство работает под управлением ОС семейства Windows.
	if sys.platform == "win32": os.system("shutdown /s")

#==========================================================================================#
# >>>>> ФУНКЦИИ ОБРАБОТКИ ТИПОВ ДАННЫХ <<<<< #
#==========================================================================================#

def CheckForCyrillicPresence(text: str) -> bool:
	"""
	Проверяет, имеются ли кирилические символы в строке.
		text – проверяемая строка.
	"""

	# Русский алфавит в нижнем регистре.
	Alphabet = set("абвгдеёжзийклмнопрстуфхцчшщъыьэюя")
	# Состояние: содержит ли строка кирилические символы.
	IsTextContainsCyrillicCharacters = not Alphabet.isdisjoint(text.lower())

	return IsTextContainsCyrillicCharacters

def ChunkList(value: list, length: int) -> list[list]:
	"""
	Разделяет список на фрагменты фиксированной длинны.
		value – обрабатываемое значение;
		length – длина фрагментов.
	"""

	# Список списков.
	Result = list()
	# Индекс обрезки.
	CutIndex = 1
	# Буфер обрезки.
	Buffer = list()

	# Для каждого элемента.
	for Index in range(len(value)):

		# Если индекс обрезки совпадает с длиной.
		if CutIndex == length:
			# Запись и обнуление буфера.
			Result.append(Buffer)
			Buffer = list()

		else:
			# Запись элемента в буфер.
			Buffer.append(value[Index])

		# Инкремент индекса обрезки.
		CutIndex += 1

	# Если в буфере что-то осталось, записать отдельной строкой.
	if len(Buffer) > 0: Result.append(Buffer)

	return Result

def IsNotAlpha(text: str) -> bool:
	"""
	Проверяет, состоит ли строка целиком из небуквенных символов.
	"""

	# Результат проверки.
	Result = True

	# Для каждого символа в строке.
	for Character in text:

		# Если символ является буквой.
		if Character.isalpha():
			# Изменение результата.
			Result = False
			# Прерывание цикла.
			break

	return Result

def MergeDictionaries(base_dictionary: dict, mergeable_dictionary: dict, overwrite: bool = False) -> dict:
	"""
	Объединяет словари.
		base_dictionary – словарь, в который идёт копирование;
		mergeable_dictionary – словарь, из котрого идёт копирование;
		overwrite – указывает, нужно ли перезаписывать значения конфликтующих ключей базового словаря.
	"""

	# Для каждого ключа.
	for Key in mergeable_dictionary.keys():

		# Если перезапись отключена и ключ отсутствует в базовом словаре.
		if overwrite == False and Key not in base_dictionary.keys():
			# Копирование в базовый словарь ключа и его значения из объединяемого.
			base_dictionary[Key] = mergeable_dictionary[Key]

		# Если перезапись включена.
		elif overwrite == True:
			# Копирование в базовый словарь ключа и его значения из объединяемого.
			base_dictionary[Key] = mergeable_dictionary[Key]

	return base_dictionary

def RemoveRecurringSubstrings(string: str, substring: str) -> str:
	"""
	Удаляет из строки подряд идущие повторяющиеся подстроки.
		string – строка, из которой удаляются повторы;
		Substring – удаляемая подстрока.
	"""

	# Пока в строке находятся повторы указанного символа, удалять их.
	while substring + substring in string: string = string.replace(substring + substring, substring)

	return string

def ReplaceDictionaryKey(dictionary: dict, old_key: any, new_key: any) -> dict:
	"""
	Заменяет ключ в словаре, сохраняя исходный порядок элементов.
		dictionary – обрабатываемый словарь;
		old_key – старое название ключа;
		new_key – новое название ключа.
	"""
	
	# Результат выполнения.
	Result = dict()
	# Если ключ не найден, выбросить исключение.
	if old_key not in dictionary.keys(): raise KeyError(str(old_key))

	# Для каждого ключа.
	for Key in dictionary.keys():

		# Если текущий ключ совпадает с искомым.
		if Key == old_key:
			# Замена ключа новым.
			Result[new_key] = dictionary[old_key]

		else:
			# Копирование старой пары ключ-значение.
			Result[Key] = dictionary[Key]

	return Result

def StripAlpha(text: str) -> str:
	"""
	Удаляет из строки начальные и конечные небуквенные символы.
		text – обрабатываемая строка.
	"""

	try:
		# Пока по краям строки есть небуквенные символы, удалять их по одному.
		while not text[0].isalpha(): text.pop(0)
		while not text[-1].isalpha(): text.pop()

	except:
		# Очистка строки.
		text = ""

def Zerotify(value: any) -> any:
	"""
	Преобразует значения, логически интерпретируемые в False, в тип None.
		value – обрабатываемое значение.
	"""

	# Если значение логически интерпретируется в False, обнулить его.
	if bool(value) == False: value = None

	return value

#==========================================================================================#
# >>>>> ФУНКЦИИ РАБОТЫ С JSON <<<<< #
#==========================================================================================#

def ReadJSON(path: str) -> dict:
	"""
	Читает файл JSON и конвертирует его в словарь.
		path – путь к файлу.
	"""

	# Словарь для преобразования.
	JSON = dict()
	# Открытие и чтение файла JSON.
	with open(path, encoding = "utf-8") as FileRead: JSON = json.load(FileRead)

	return JSON

def WriteJSON(path: str, dictionary: dict):
	"""
	Записывает стандартизированный JSON файл. Для отступов используются символы табуляции.
		path – путь к файлу;
		dictionary – словарь, конвертируемый в формат JSON.
	"""

	# Запись словаря в JSON файл.
	with open(path, "w", encoding = "utf-8") as FileWrite: json.dump(dictionary, FileWrite, ensure_ascii = False, indent = '\t', separators = (",", ": "))