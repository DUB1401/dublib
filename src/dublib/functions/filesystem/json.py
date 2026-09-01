import json
from os import PathLike

import orjson

from . import atomic_write

def read(path: PathLike[str] | str) -> dict:
	"""
	Считывает файл JSON и десериализует его в словарь.

	:param path: Путь к файлу.
	:type path: PathLike[str] | str
	:return: Словарное представление данных JSON.
	:rtype: dict
	:raises json.JSONDecodeError: Выбрасывается при невозможности десериализовать файл.
	:raises FileNotFoundError: Выбрасывается при отсутствии файла.
	"""

	with open(path, "rb") as FileReader:
		return orjson.loads(FileReader.read())

def write(path: PathLike[str] | str, data: dict, pretty: bool = True, atomic: bool = False):
	"""
	Записывает отформатированный файл JSON.

	:param path: Путь к файлу.
	:type path: PathLike[str] | str
	:param data: Словарь для сериализации в JSON.
	:type data: dict
	:param pretty: Включает режим форматирования с использованием символов новых строк и табуляции.
	:type pretty: bool
	:param atomic: Переключает использование атомарной записи.
	:type atomic: bool
	:raise TypeError: Выбрасывается при невозможности сериализации данных в JSON.
	"""

	Content: bytes | None = None

	if pretty:
		Content = json.dumps(data, ensure_ascii = False, indent = "\t", separators = (",", ": ")).encode()
	else:
		Content = orjson.dumps(data)

	if atomic:
		atomic_write(path, Content)
	else:
		with open(path, "wb") as FileWriter: FileWriter.write(Content)
