import json

#==========================================================================================#
# >>>>> ФУНКЦИИ УПРОЩЁННОЙ РАБОТЫ С JSON <<<<< #
#==========================================================================================#

def ReadJSON(path: str) -> dict:
	"""
	Читает файл JSON и конвертирует его в словарь.
		path – путь к файлу.
	"""

	# Словарь для преобразования.
	JSON = dict()
	# Открытие и чтение файла JSON.
	with open(path, encoding = "utf-8") as FileRead: JSON = json.load(FileRead)

	return JSON

def WriteJSON(path: str, dictionary: dict):
	"""
	Записывает стандартизированный JSON файл. Для отступов используются символы табуляции.
		path – путь к файлу;
		dictionary – словарь, конвертируемый в формат JSON.
	"""

	# Запись словаря в JSON файл.
	with open(path, "w", encoding = "utf-8") as FileWrite: json.dump(dictionary, FileWrite, ensure_ascii = False, indent = "\t", separators = (",", ": "))