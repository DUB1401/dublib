import os
import random
import shutil
import tempfile
from os import PathLike
from pathlib import Path
from typing import Sequence

from ..data import ToSequence

def atomic_write(path: PathLike[str] | str, data: bytes):
	"""
	Атомарно производит запись файла в бинарном представлении, используя создание временного файла со сбросом кэша записи и операцию `os.replace()`.

	:param path: Путь к записываемому файлу.
	:type path: PathLike[str] | str
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

def get_random_file(directory: PathLike[str] | str) -> Path | None:
	"""
	Выбирает случайный файл из директории.

	:param directory: Путь к директории.
	:type directory: PathLike[str] | str
	:return: Путь к случайному файлу в директории или `None`, если таковая пуста.
	:rtype: Path
	:raises FileNotFoundError: Директория не существует.
	"""

	DirectoryPath = Path(directory)
	Files = os.listdir(DirectoryPath)
	if not Files: return None
	FilePath = DirectoryPath / random.choice(Files)

	return FilePath

def make_cwd_directories(directories: str | Sequence[str]):
	"""
	Создаёт наборы каталогов в текущей корневой директории скрипта.

	:param directories: Последовательность названий директорий или название конкретной директории.
	:type directories: str | Sequence[str]
	"""

	for Name in ToSequence(directories):
		os.makedirs(Name, exist_ok = True)

def clear_directory(directory: PathLike[str] | str):
	"""
	Удлаляет содержимое директории.

	:param directory: Путь к директории.
	:type directory: PathLike[str] | str
	"""

	DirectoryPath = Path(directory)
	shutil.rmtree(DirectoryPath)
	DirectoryPath.mkdir()
