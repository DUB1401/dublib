from os import PathLike

import yaml

from . import atomic_write

def read(path: PathLike[str] | str) -> dict:
	"""
	Считывает файл YAML и десириализует его в словарь.

	:param path: Путь к файлу.
	:type path: PathLike[str] | str
	:return: Словарное представление данных YAML.
	:rtype: dict
	:raises FileNotFoundError: Выбрасывается при отсутствии файла.
	"""

	with open(path, "r") as FileReader:
		return yaml.safe_load(FileReader)

def write(path: PathLike[str] | str, data: dict, atomic: bool = False):
	"""
	Записывает файл YAML.

	:param path: Путь к файлу.
	:type path: PathLike[str] | str
	:param data: Словарь для сериализации в YAML.
	:type data: dict
	:param atomic: Переключает использование атомарной записи.
	:type atomic: bool
	"""

	FileContent: bytes = yaml.dump(data, allow_unicode = True, sort_keys = False).encode()

	if atomic:
		atomic_write(path, FileContent)
	else:
		with open(path, "wb") as FileWrite: FileWrite.write(FileContent)
