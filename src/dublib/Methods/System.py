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

	# Состояние: корректна ли версия.
	IsVersionCorrect = True
	
	# Если версия Python старше минимальной требуемой.
	if sys.version_info < (major, minor): 
		
		# Если указано выбросить исключение.
		if raise_exception == True:
			# Выброс исключения.
			raise RuntimeError(f"Python {major}.{minor} or newer is required.")

		else: 
			# Переключение статуса проверки.
			IsVersionCorrect = False

	return IsVersionCorrect

def Clear():
	"""Очищает консоль."""

	os.system("cls" if os.name == "nt" else "clear")

def Shutdown():
	"""Выключает устройство."""

	# Если устройство работает под управлением ОС семейства Linux.
	if sys.platform in ["linux", "linux2"]: os.system("sudo shutdown now")
	# Если устройство работает под управлением ОС семейства Windows.
	if sys.platform == "win32": os.system("shutdown /s")