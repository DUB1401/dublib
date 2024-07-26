#==========================================================================================#
# >>>>> ФУНКЦИИ ПРОВЕРКИ ДАННЫХ <<<<< #
#==========================================================================================#

def CheckForCyrillic(text: str) -> bool:
	"""
	Проверяет, имеются ли кирилические символы в строке.
		text – проверяемая строка.
	"""

	# Русский алфавит в нижнем регистре.
	Alphabet = set("абвгдеёжзийклмнопрстуфхцчшщъыьэюя")
	# Состояние: содержит ли строка кирилические символы.
	IsTextContainsCyrillicCharacters = not Alphabet.isdisjoint(text.lower())

	return IsTextContainsCyrillicCharacters

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

#==========================================================================================#
# >>>>> ФУНКЦИИ ОБРАБОТКИ ДАННЫХ <<<<< #
#==========================================================================================#

def ChunkList(value: list, length: int) -> list[list]:
	"""
	Разделяет список на фрагменты фиксированной длинны.
		value – обрабатываемое значение;\n
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

def MergeDictionaries(base_dictionary: dict, mergeable_dictionary: dict, overwrite: bool = False) -> dict:
	"""
	Объединяет словари.
		base_dictionary – словарь, в который идёт копирование;\n
		mergeable_dictionary – словарь, из котрого идёт копирование;\n
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
		string – строка, из которой удаляются повторы;\n
		Substring – удаляемая подстрока.
	"""

	# Пока в строке находятся повторы указанного символа, удалять их.
	while substring + substring in string: string = string.replace(substring + substring, substring)

	return string

def ReplaceDictionaryKey(dictionary: dict, old_key: any, new_key: any) -> dict:
	"""
	Заменяет ключ в словаре, сохраняя исходный порядок элементов.
		dictionary – обрабатываемый словарь;\n
		old_key – старое название ключа;\n
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