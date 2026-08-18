import subprocess
import sys

def CheckPythonMinimalVersion(major: int, minor: int, raise_exception: bool = True) -> bool:
	"""
	Проверяет, соответствует ли используемая версия Python минимальной требуемой.

	:param major: Идентификатор Major-версии Python.
	:type major: int
	:param minor: Идентификатор Minor-версии Python.
	:type minor: int
	:param raise_exception: Указывает, как поступать при несоответствии версии: выбрасывать исключение или возвращать значение.
	:type raise_exception: bool
	:raises RuntimeError: Неподдерживаемая версия Python.
	"""

	if sys.version_info < (major, minor): 
		if raise_exception:
			raise RuntimeError(f"Python {major}.{minor} or newer is required.")
		else:
			return False

	return True

def Clear(clear_history: bool = True):
	"""
	Очищает терминал.

	:param clear_history: Указывает, нужно ли удалить также и буфер обратной прокрутки терминала.
	:type clear_history: bool
	"""

	Operation: str = "\033[H\033[2J"
	if clear_history: Operation += "\033[3J"
	sys.stdout.write(Operation)
	sys.stdout.flush()

def Shutdown():
	"""Выключает устройство."""
	
	if sys.platform == "linux":
		subprocess.run(("sudo", "shutdown", "now"))
		
	elif sys.platform == "win32":
		subprocess.run(("shutdown", "/s", "/t", "0"))