import shutil
import os

#==========================================================================================#
# >>>>> ФУНКЦИИ РАБОТЫ С ФАЙЛАМИ И ДИРЕКТОРИЯМИ <<<<< #
#==========================================================================================#

def MakeRootDirectories(directories: list[str]):
	"""
	Создаёт каталоги в текущей корневой директории скрипта.
		directories – список названий каталогов.
	"""
	
	# Для каждого названия каталога.
	for Name in directories:
		# Если каталог не существует, то создать его.
		if os.path.exists(Name) == False: os.makedirs(Name)

def RemoveDirectoryContent(path: str):
	"""
	Удаляет всё содержимое каталога.
		path – путь к каталогу.
	"""

	# Список содержимого в папке.
	FolderContent = os.listdir(path)

	# Для каждого элемента.
	for Item in FolderContent:

		# Если элемент является каталогом.
		if os.path.isdir(path + "/" + Item):
			# Удаление каталога.
			shutil.rmtree(path + "/" + Item)

		else:
			# Удаление файла.
			os.remove(path + "/" + Item)
