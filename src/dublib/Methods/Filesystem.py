from .Data import ToIterable

from typing import Iterable
from pathlib import Path
from os import PathLike
import shutil
import json
import os

import orjson

#==========================================================================================#
# >>>>> ФУНКЦИИ РАБОТЫ С ФАЙЛАМИ И ДИРЕКТОРИЯМИ <<<<< #
#==========================================================================================#

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

def WriteJSON(path: PathLike, data: dict, pretty: bool = True):
	"""
	Записывает отформатированный файл JSON.

	:param path: Путь к файлу.
	:type path: PathLike
	:param data: Словарь для сериализации в JSON.
	:type data: dict
	:param pretty: Включает режим форматирования с использованием символов новых строк и табуляции.
	:type pretty: bool
	:raise TypeError: Выбрасывается при невозможности сериализации данных в JSON.
	"""

	if pretty:
		Content: str = json.dumps(data, ensure_ascii = False, indent = "\t", separators = (",", ": "))
		with open(path, "w") as FileWriter: FileWriter.write(Content)

	else:
		Content: bytes = orjson.dumps(data)
		with open(path, "wb") as FileWriter: FileWriter.write(Content)

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
	if split: Text = Text.split(split)

	if strip:
		if type(Text) == str: Text = Text.strip()
		else: Text = tuple(Value.strip() for Value in Text)

	return Text

def WriteTextFile(path: PathLike, text: str | Iterable[str]):
	"""
	Записывает текстовый файл.

	:param path: Путь к файлу.
	:type path: PathLike
	:param text: Строка или последовательность строк, которые должны быть объединены через символ новой строки.
	:type text: str | Iterable[str]
	"""

	if type(text) != str: text = "\n".join(text)
	with open(path, "w", encoding = "utf-8") as FileWrite: FileWrite.write(text)