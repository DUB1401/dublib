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

def NormalizePath(path: str, use_unix_separator: bool | None = None, is_directory: bool | None = None):
	"""
	Нормализует путь к файлу по заданным параметрам. По умолчанию определяет автоматически.
		path – путь к файлу или каталогу;
		use_unix_separator – указывает, следует ли использовать Unix-разделитель или стиль Windows;
		is_directory – указывает, что в конце пути обязан находиться разделитель.
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

	# Если включено автоматическое определение директории.
	if is_directory == None:
		# Проверка: ведёт ли путь к каталогу.
		is_directory = os.path.isdir(path)
	
	# Используемый разделитель.
	UsedSeparator = "/" if use_unix_separator else "\\"
	# Если путь помечен как ведущий к каталогу и не заканчивается разделителем, добавить разделитель.
	if is_directory and not path.endswith(UsedSeparator): path += UsedSeparator

	return path

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
