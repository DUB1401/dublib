import shutil
import sys
import os

#==========================================================================================#
# >>>>> ФУНКЦИИ РАБОТЫ С ФАЙЛАМИ И ДИРЕКТОРИЯМИ <<<<< #
#==========================================================================================#

def MakeRootDirectories(directories: list[str]):
	"""
	Создаёт каталоги в текущей корневой директории скрипта.
		directories – список названий каталогов.
	"""
	
	# Для каждого названия каталога.
	for Name in directories:
		# Если каталог не существует, то создать его.
		if os.path.exists(Name) == False: os.makedirs(Name)

def NormalizePath(path: str, use_unix_separator: bool | None = None, separator_at_end: bool | None = None):
	"""
	Нормализует путь к файлу по заданным параметрам, которые по умолчанию определяет автоматически.
		path – путь к файлу или каталогу;\n
		use_unix_separator – указывает, следует ли использовать Unix-разделитель или стиль Windows;\n
		separator_at_end – указывает, что в конце пути обязан находиться разделитель (при автоматическом определении всегда добавляется к каталогам).
	"""

	# Если включено автоматическое определение разделителя.
	if use_unix_separator == None:
		# Определение стиля разделителя.
		if sys.platform == "win32": use_unix_separator = False
		else: use_unix_separator = True

	# Если используется Unix-разделитель, заменить все разделители на него.
	if use_unix_separator and "\\" in path: path = path.replace("\\", "/")
	# Если используется Windows-разделитель, заменить все разделители на него.
	elif not use_unix_separator and "/" in path: path = path.replace("/", "\\")

	# Если включено автоматическое определение разделителя в конце.
	if separator_at_end == None:
		# Проверка: ведёт ли путь к каталогу.
		separator_at_end = os.path.isdir(path)

	# Используемый разделитель.
	UsedSeparator = "/" if use_unix_separator else "\\"

	# Если в конце пути обязан быть разделитель, а его нет, то добавить.
	if separator_at_end and not path.endswith(UsedSeparator): path += UsedSeparator
	# Если в конце пути не должно быть разделителя, а он есть, то убрать.
	elif not separator_at_end and path.endswith(UsedSeparator): path = path.rstrip(UsedSeparator)

	return path

def ReadTextFile(path: str, split: str | None = None) -> str | list[str]:
	"""
	Считывает содержимое текстового файла.
		path – путь к файлу;\n
		split – указывает, по вхождению какой подстроки следует разбить содержимое файла.
	"""

	# Текст.
	Text = None
	# Открытие и чтение файла.
	with open(path, encoding = "utf-8") as FileReader: Text = FileReader.read()
	# Если указана подстрока для разбиения, разбить прочитанный текст.
	if split: Text = Text.split(split)

	return Text

def RemoveDirectoryContent(path: str):
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

def WriteTextFile(path: str, text: str | list[str], join: str | None = None):
	"""
	Записывает текстовый файл.
		path – путь к файлу;\n
		text – текст для записи;\n
		join – если в качестве текста передан список строк, можно указать специальную строку, через которую будут объеденены все остальные.
	"""

	# Если не передана строка для объединения, использовать пустую.
	if not join: join = ""
	# Если передан список строк, объединить их.
	if type(text) == list: text = join.join(text)
	# Запись файла.
	with open(path, "w", encoding = "utf-8") as FileWrite: FileWrite.write(text)