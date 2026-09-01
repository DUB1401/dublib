from os import PathLike
from typing import Literal, Sequence, overload

from . import atomic_write

@overload
def read(path: PathLike[str] | str, split: Literal[True], strip_level: Literal[0, 1, 2] = 0) -> list[str]: ...
@overload
def read(path: PathLike[str] | str, split: Literal[False] = False, strip_level: Literal[0, 1, 2] = 0) -> str: ...

def read(path: PathLike[str] | str, split: bool = False, strip_level: Literal[0, 1, 2] = 0) -> str | list[str]:
	"""
	Считывает текстовый файл.

	:param path: Путь к файлу.
	:type path: PathLike[str] | str
	:param split: Если активировано, файл будет разбит на набор строк по символу новой строки.
	:type split: bool
	:param strip: Уровень очистки от пробельных символов. 0 – отключён, 1 – применить `strip()` к каждой строке, 2 – дополнительно убрать пустые строки (если включён параметр **split**s).
	:type strip: Literal[0, 1, 2]
	:return: Содержимое текстового файла в виде строки или набора строк.
	:rtype: str | tuple[str]
	:raises FileNotFoundError: Выбрасывается при отсутствии файла.
	"""

	Text: str | None = None

	with open(path, encoding = "utf-8") as FileReader:
		Text = FileReader.read()

	TextLines: list[str] = Text.split("\n")

	if strip_level:
		for Index in range(len(TextLines)):
			Buffer: str = TextLines[Index].strip()

			if strip_level == 1: TextLines[Index] = Buffer
			elif Buffer: TextLines[Index] = Buffer
			

	return TextLines if split else "\n".join(TextLines)

def write(path: PathLike[str] | str , text: str | Sequence[str], atomic: bool = False):
	"""
	Записывает текстовый файл.

	:param path: Путь к файлу.
	:type path: PathLike[str] | str
	:param text: Строка или последовательность строк, которые должны быть объединены через символ новой строки.
	:type text: str | Sequence[str]
	:param atomic: Переключает использование атомарной записи.
	:type atomic: bool
	"""

	if type(text) is not str:
		text = "\n".join(text)

	TextBytes: bytes = text.encode()

	if atomic:
		atomic_write(path, TextBytes)
	else:
		with open(path, "wb") as FileWrite: FileWrite.write(TextBytes)
