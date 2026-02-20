from .Data import ToIterable

from typing import Iterable
from pathlib import Path
from os import PathLike
import tempfile
import random
import shutil
import json
import os

import orjson
import yaml

#==========================================================================================#
# >>>>> ФУНКЦИИ РАБОТЫ С ФАЙЛАМИ И ДИРЕКТОРИЯМИ <<<<< #
#==========================================================================================#

def AtomicWrite(path: PathLike, data: bytes):
	"""
	Атомарно производит запись файла в бинарном представлении, используя создание временного файла и операцию `os.replace()`.

	:param path: Путь к записываемому файлу.
	:type path: PathLike
	:param data: Набор байтов для записи.
	:type data: bytes
	"""

	PathObject = Path(path)
	TempPath = None

	with tempfile.NamedTemporaryFile("wb", delete = False, dir = PathObject.parent) as TempWriter:
		TempWriter.write(data)
		TempPath = Path(TempWriter.name)

	os.replace(TempPath, path)

def GetRandomFile(directory: PathLike) -> PathLike | None:
	"""
	Выбирает случайный файл из каталога.

	:param directory: Путь к каталогу.
	:type directory: PathLike
	:raise FileNotFoundError: Выбрасывается, если каталог не существует.
	:return: Путь к случайному файлу в каталоге по стандарту POSIX или `None`, если каталог пустой.
	:rtype: PathLike
	"""

	directory = NormalizePath(directory)
	Files = ListDir(directory)
	if not Files: return

	return f"{directory}/" + random.choice(Files)

def ListDir(path: PathLike | None = None) -> list[str]:
	"""
	Основана на `os.scandir()`, более быстром и подробном варианте `os.listdir()`.

	:param path: Путь для сканирования. Если передать `None`, будет возвращёт список элементов в текущем каталоге.
	:type path: PathLike | None
	:return: Список названий каталогов и имён файлов по указанному пути
	:rtype: list[str]
	"""

	return [Entry.name for Entry in os.scandir(path)]

def MakeRootDirectories(directories: Iterable[str] | str):
	"""
	Создаёт наборы каталогов в текущей корневой директории скрипта.

	:param directories: Последовательность названий директорий или название конкретной директории.
	:type directories: Iterable[str]
	"""

	directories = ToIterable(directories)
	
	for Name in directories:
		if not os.path.exists(Name): os.makedirs(Name)

def NormalizePath(path: PathLike, strip: bool = True) -> PathLike:
	"""
	Приводит путь к POSIX-стандарту.

	:param path: Обрабатываемый путь.
	:type path: PathLike
	:param strip: Указывает, следует ли удалить наклонную черту из конца пути при наличии.
	:type strip: bool
	:return: Путь в POSIX-стандарте.
	:rtype: PathLike
	"""
	
	path: str = Path(path).as_posix()
	if strip: path = path.rstrip("/")

	return path

def RemoveDirectoryContent(path: PathLike):
	"""
	Удлаляет содержимое каталога.

	:param path: Путь к каталогу.
	:type path: PathLike
	"""

	FolderContent = ListDir(path)

	for Item in FolderContent:
		ItemPath = f"{path}/{Item}"

		if os.path.isdir(ItemPath): shutil.rmtree(ItemPath)
		else: os.remove(ItemPath)

#==========================================================================================#
# >>>>> ФУНКЦИИ РАБОТЫ С JSON <<<<< #
#==========================================================================================#

def ReadJSON(path: PathLike) -> dict:
	"""
	Считывает файл JSON и десириализует его в словарь.

	:param path: Путь к файлу.
	:type path: PathLike
	:return: Словарное представление данных JSON.
	:rtype: dict
	:raises json.JSONDecodeError: Выбрасывается при невозможности десериализовать файл.
	:raises FileNotFoundError: Выбрасывается при отсутствии файла.
	"""

	with open(path, "rb") as FileReader: return orjson.loads(FileReader.read())

def WriteJSON(path: PathLike, data: dict, pretty: bool = True, atomic: bool = False):
	"""
	Записывает отформатированный файл JSON.

	:param path: Путь к файлу.
	:type path: PathLike
	:param data: Словарь для сериализации в JSON.
	:type data: dict
	:param pretty: Включает режим форматирования с использованием символов новых строк и табуляции.
	:type pretty: bool
	:param atomic: Переключает использование атомарной записи.
	:type atomic: bool
	:raise TypeError: Выбрасывается при невозможности сериализации данных в JSON.
	"""

	Content = None

	if pretty: Content: str = json.dumps(data, ensure_ascii = False, indent = "\t", separators = (",", ": ")).encode()
	else: Content: bytes = orjson.dumps(data)

	if atomic:
		AtomicWrite(path, Content)
	else:
		with open(path, "wb") as FileWriter: FileWriter.write(Content)

#==========================================================================================#
# >>>>> ФУНКЦИИ РАБОТЫ С YAML <<<<< #
#==========================================================================================#

def ReadYAML(path: PathLike) -> dict:
	"""
	Считывает файл YAML и десириализует его в словарь.

	:param path: Путь к файлу.
	:type path: PathLike
	:return: Словарное представление данных YAML.
	:rtype: dict
	:raises FileNotFoundError: Выбрасывается при отсутствии файла.
	"""

	with open(path, "r") as FileReader: return yaml.safe_load(FileReader)

def WriteYAML(path: PathLike, data: dict, atomic: bool = False):
	"""
	Записывает файл YAML.

	:param path: Путь к файлу.
	:type path: PathLike
	:param data: Словарь для сериализации в YAML.
	:type data: dict
	:param atomic: Переключает использование атомарной записи.
	:type atomic: bool
	"""

	data: str = yaml.dump(data, allow_unicode = True, sort_keys = False)

	if atomic:
		AtomicWrite(path, data.encode())
	else:
		with open(path, "w", encoding = "utf-8") as FileWrite: FileWrite.write(data)

#==========================================================================================#
# >>>>> ФУНКЦИИ РАБОТЫ С ТЕКСТОВЫМИ ФАЙЛАМИ <<<<< #
#==========================================================================================#

def ReadTextFile(path: PathLike, split: bool = False, strip: bool = False) -> str | tuple[str]:
	"""
	Считывает текстовый файл.

	:param path: Путь к файлу.
	:type path: PathLike
	:param split: Если активировано, файл будет разбит на набор строк по символу новой строки.
	:type split: bool
	:param strip: Если активировано, к каждой возвращаемой строке будет применён метод `strip()`.
	:type strip: bool
	:return: Содержимое текстового файла в виде строки или набора строк.
	:rtype: str | tuple[str]
	:raises FileNotFoundError: Выбрасывается при отсутствии файла.
	"""

	Text = None
	with open(path, encoding = "utf-8") as FileReader: Text = FileReader.read()
	if split: Text = Text.split("\n")

	if strip:
		if type(Text) == str: Text = Text.strip()
		else: Text = tuple(Value.strip() for Value in Text)

	return Text

def WriteTextFile(path: PathLike, text: str | Iterable[str], atomic: bool = False):
	"""
	Записывает текстовый файл.

	:param path: Путь к файлу.
	:type path: PathLike
	:param text: Строка или последовательность строк, которые должны быть объединены через символ новой строки.
	:type text: str | Iterable[str]
	:param atomic: Переключает использование атомарной записи.
	:type atomic: bool
	"""

	if type(text) != str: text = "\n".join(text)

	if atomic:
		AtomicWrite(path, text.encode())
	else:
		with open(path, "w", encoding = "utf-8") as FileWrite: FileWrite.write(text)
