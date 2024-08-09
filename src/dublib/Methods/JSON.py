import json

#==========================================================================================#
# >>>>> ФУНКЦИИ УПРОЩЁННОЙ РАБОТЫ С JSON <<<<< #
#==========================================================================================#

def ReadJSON(path: str) -> dict:
	"""
	Считывает файл JSON и конвертирует его в словарь.
		path – путь к файлу.
	"""

	JSON = dict()
	with open(path, encoding = "utf-8") as FileReader: JSON = json.load(FileReader)

	return JSON

def WriteJSON(path: str, dictionary: dict):
	"""
	Записывает стандартизированный JSON файл. Для отступов используются символы табуляции.
		path – путь к файлу;\n
		dictionary – словарь, конвертируемый в формат JSON.
	"""

	with open(path, "w", encoding = "utf-8") as FileWriter: json.dump(dictionary, FileWriter, ensure_ascii = False, indent = "\t", separators = (",", ": "))