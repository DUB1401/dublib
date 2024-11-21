from .JSON import ReadJSON, WriteJSON

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
	
	for Name in directories:
		if os.path.exists(Name) == False: os.makedirs(Name)

def NormalizePath(path: str, unix_separator: bool | None = None, separator_at_end: bool = False):
	"""
	Нормализует путь к файлу по заданным параметрам, которые по умолчанию определяет автоматически.
		path – путь к файлу или каталогу;\n
		use_unix_separator – указывает, следует ли использовать Unix-разделитель или стиль Windows;\n
		separator_at_end – указывает, что в конце пути обязан находиться разделитель.
	"""

	if unix_separator == None:
		if sys.platform == "win32": unix_separator = False
		else: unix_separator = True

	if unix_separator and "\\" in path: path = path.replace("\\", "/")
	elif not unix_separator and "/" in path: path = path.replace("/", "\\")

	UsedSeparator = "/" if unix_separator else "\\"

	if separator_at_end and not path.endswith(UsedSeparator): path += UsedSeparator
	elif not separator_at_end and path.endswith(UsedSeparator): path = path.rstrip(UsedSeparator)

	return path

def ReadTextFile(path: str, split: str | None = None) -> str | list[str]:
	"""
	Считывает содержимое текстового файла.
		path – путь к файлу;\n
		split – указывает, по вхождению какой подстроки следует разбить содержимое файла.
	"""

	Text = None
	with open(path, encoding = "utf-8") as FileReader: Text = FileReader.read()
	if split: Text = Text.split(split)

	return Text

def RemoveDirectoryContent(path: str):
	"""
	Удаляет всё содержимое каталога.
		path – путь к каталогу.
	"""

	FolderContent = os.listdir(path)

	for Item in FolderContent:

		if os.path.isdir(path + "/" + Item):
			shutil.rmtree(path + "/" + Item)

		else:
			os.remove(path + "/" + Item)

def WriteTextFile(path: str, text: str | list[str], join: str | None = None):
	"""
	Записывает текстовый файл.
		path – путь к файлу;\n
		text – текст для записи;\n
		join – если в качестве текста передан список строк, можно указать специальную строку, через которую будут объеденены все остальные.
	"""

	if not join: join = ""
	if type(text) == list: text = join.join(text)
	with open(path, "w", encoding = "utf-8") as FileWrite: FileWrite.write(text)