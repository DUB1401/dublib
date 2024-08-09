import sys
import os

#==========================================================================================#
# >>>>> ФУНКЦИИ РАБОТЫ С СИСТЕМОЙ <<<<< #
#==========================================================================================#

def CheckPythonMinimalVersion(major: int, minor: int, raise_exception: bool = True) -> bool:
	"""
	Проверяет, соответствует ли используемая версия Python минимальной требуемой.
		major – идентификатор Major-версии Python;\n
		minor – идентификатор Minor-версии Python;\n
		raise_exception – указывает, как поступать при несоответствии версии: выбрасывать исключение или возвращать значение.
	"""

	IsVersionCorrect = True
	
	if sys.version_info < (major, minor): 
		
		if raise_exception == True:
			raise RuntimeError(f"Python {major}.{minor} or newer is required.")

		else: 
			IsVersionCorrect = False

	return IsVersionCorrect

def Clear():
	"""Очищает консоль."""

	os.system("cls" if os.name == "nt" else "clear")

def Shutdown():
	"""Выключает устройство."""

	if sys.platform in ["linux", "linux2"]: os.system("sudo shutdown now")
	if sys.platform == "win32": os.system("shutdown /s")