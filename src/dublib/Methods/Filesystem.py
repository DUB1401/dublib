from .Data import ToSequence

from typing import overload, Literal, Sequence
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
	Атомарно производит запись файла в бинарном представлении, используя создание временного файла со сбросом кэша записи и операцию `os.replace()`.

	:param path: Путь к записываемому файлу.
	:type path: PathLike
	:param data: Набор байтов для записи.
	:type data: bytes
	"""

	PathObject = Path(path)
	TempPath = None

	with tempfile.NamedTemporaryFile("wb", delete = False, dir = PathObject.parent) as TempWriter:
		TempWriter.write(data)
		TempWriter.flush()
		os.fsync(TempWriter.fileno())
		TempPath = Path(TempWriter.name)

	os.replace(TempPath, path)

def GetRandomFile(directory: PathLike) -> Path | None:
	"""
	Выбирает случайный файл из директории.

	:param directory: Путь к директории.
	:type directory: PathLike
	:return: Путь к случайному файлу в директории или `None`, если таковая пуста.
	:rtype: Path
	:raises FileNotFoundError: Директория не существует.
	"""

	DirectoryPath = Path(directory)
	Files = ListDir(directory)
	if not Files: return None
	FilePath = DirectoryPath / random.choice(Files)

	return FilePath

def ListDir(directory: PathLike | None = None) -> list[str]:
	"""
	Основана на `os.scandir()`, более быстром и подробном варианте `os.listdir()`.

	:param directory: Путь для сканирования. Если передать `None`, будет возвращёт список элементов в текущей директории.
	:type directory: PathLike | None
	:return: Список названий каталогов и имён файлов по указанному пути
	:rtype: list[str]
	"""

	TargetPath = Path(directory) if directory else Path(".")

	return [Entry.name for Entry in os.scandir(TargetPath)]

def MakeRootDirectories(directories: Sequence[str] | str):
	"""
	Создаёт наборы каталогов в текущей корневой директории скрипта.

	:param directories: Последовательность названий директорий или название конкретной директории.
	:type directories: Sequence[str]
	"""

	for Name in ToSequence(directories): os.makedirs(Name, exist_ok = True)

def RemoveDirectoryContent(directory: PathLike):
	"""
	Удлаляет содержимое директории.

	:param directory: Путь к директории.
	:type directory: PathLike
	"""

	DirectoryPath = Path(directory)
	shutil.rmtree(DirectoryPath)
	DirectoryPath.mkdir()

#==========================================================================================#
# >>>>> ФУНКЦИИ РАБОТЫ С JSON <<<<< #
#==========================================================================================#

def ReadJSON(path: PathLike) -> dict:
	"""
	Считывает файл JSON и десериализует его в словарь.

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

	Content: bytes | None = None

	if pretty: Content = json.dumps(data, ensure_ascii = False, indent = "\t", separators = (",", ": ")).encode()
	else: Content = orjson.dumps(data)

	if atomic: AtomicWrite(path, Content)
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

	FileContent: bytes = yaml.dump(data, allow_unicode = True, sort_keys = False).encode()

	if atomic: AtomicWrite(path, FileContent)
	else:
		with open(path, "wb") as FileWrite: FileWrite.write(FileContent)

#==========================================================================================#
# >>>>> ФУНКЦИИ РАБОТЫ С ТЕКСТОВЫМИ ФАЙЛАМИ <<<<< #
#==========================================================================================#

@overload
def ReadTextFile(path: PathLike, split: Literal[True], strip: bool = False) -> tuple[str, ...]: ...
@overload
def ReadTextFile(path: PathLike, split: Literal[False] = False, strip: bool = False) -> str: ...

def ReadTextFile(path: PathLike, split: bool = False, strip: bool = False) -> str | tuple[str, ...]:
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

	Text: str | None = None
	with open(path, encoding = "utf-8") as FileReader: Text = FileReader.read()
	TextLines: list[str] = Text.split("\n")

	if strip:
		for Index in range(len(TextLines)): TextLines[Index] = TextLines[Index].strip()

	return tuple(TextLines) if split else "\n".join(TextLines)

def WriteTextFile(path: PathLike, text: str | Sequence[str], atomic: bool = False):
	"""
	Записывает текстовый файл.

	:param path: Путь к файлу.
	:type path: PathLike
	:param text: Строка или последовательность строк, которые должны быть объединены через символ новой строки.
	:type text: str | Sequence[str]
	:param atomic: Переключает использование атомарной записи.
	:type atomic: bool
	"""

	if type(text) != str: text = "\n".join(text)
	TextBytes: bytes = text.encode()

	if atomic: AtomicWrite(path, TextBytes)
	else:
		with open(path, "wb") as FileWrite: FileWrite.write(TextBytes)
