from ..Methods.Filesystem import NormalizePath
from ..Methods.JSON import ReadJSON, WriteJSON

from telebot import TeleBot, types

import enum
import os

#==========================================================================================#
# >>>>> ВСПОМОГАТЕЛЬНЫЕ СТРУКТУРЫ ДАННЫХ <<<<< #
#==========================================================================================#

class CachedFile:
	"""Данные кэшированного файла."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#
	
	@property
	def chat_id(self) -> int:
		"""Идентификатор чата с файлом."""

		return self.__ChatID
	
	@property
	def id(self) -> str:
		"""Идентификатор файла на сервере Telegram."""

		return self.__FileID

	@property
	def message_id(self) -> int | None:
		"""Идентификатор сообщения с файлом."""

		return self.__MessageID

	@property
	def path(self) -> str:
		"""Путь к файлу или его виртуальный идентификатор."""

		return self.__Path
	
	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, path: str, chat_id: int, file_id: str, message_id: int | None = None):
		"""
		Данные кэшированного файла.
			path – путь к файлу или его виртуальный идентификатор;\n
			chat_id – идентификатор чата с файлом;\n
			file_id – идентификатор файла на сервере Telegram;\n
			message_id – идентификатор сообщения с файлом.
		"""

		#---> Генерация динамических свойств.
		#==========================================================================================#
		self.__Path = path
		self.__ChatID = chat_id
		self.__FileID = file_id
		self.__MessageID = message_id

	def __str__(self) -> str:
		"""Преобразует данные в строку."""

		return str(self.to_dict())

	def to_dict(self) -> dict:
		"""Генерирует словарь данных кэшированного файла."""

		return {"path": self.__Path, "chat_id": self.__ChatID, "file_id": self.__FileID, "message_id": self.__MessageID}

class StorageTypes(enum.Enum):
	"""Типы локальных хранилищ данных кэша."""

	SQLite = "sqlite3"
	JSON = "json"

#==========================================================================================#
# >>>>> ОСНОВНОЙ КЛАСС <<<<< #
#==========================================================================================#

class TeleCache:
	"""Менеджер кэша загружаемых в Telegram файлов."""

	#==========================================================================================#
	# >>>>> ПРИВАТНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __GetStoragePath(self, storage: str | None) -> str:
		"""
		Возвращает валидный путь к базе данных.
			storage – установленный путь.
		"""

		if not storage:
			Filetype = "db" if self.__Type == StorageTypes.SQLite else "json"
			storage = f"TeleCache.{Filetype}"

		else:
			storage = NormalizePath(storage)

		return storage

	def __Read(self) -> dict:
		"""Инициализирует базу данных."""

		CacheData = dict()

		if self.__Type == StorageTypes.JSON:

			try:
				JSON = ReadJSON(self.__Storage)

				for Cache in JSON["cache"]:
					Path = Cache["path"]
					CacheData[Path] = CachedFile(Path, Cache["chat_id"], Cache["file_id"], Cache["message_id"])

			except FileNotFoundError: pass

		elif self.__Type == StorageTypes.SQLite: pass

		return CacheData	

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, storage: str | None = None, type: StorageTypes = StorageTypes.JSON):
		"""
		Менеджер кэша загружаемых в Telegram файлов.
			storage – путь к файлу базы данных;\n
			type – тип базы данных.
		"""

		if type == StorageTypes.SQLite: raise Exception("SQLite cache not supported yet.")

		#---> Генерация динамических свойств.
		#==========================================================================================#
		self.__Type = type
		self.__Storage = self.__GetStoragePath(storage)

		self.__Bot = None
		self.__ChatID = None

		self.__Data = self.__Read()

	def __getitem__(self, path: str) -> str:
		"""
		Возвращает ID кэшированного файла.
			path – путь к файлу.
		"""

		return self.get_cached_file(path, upload = False, autosave = False).id
	
	def clear(self, autosave: bool = True):
		"""
		Удаляет данные кэшированных файлов, пути к которым более не являются валидными. Не рекомендуется к вызову при использовании виртуальных идентификаторов!
			autosave – включает автосохранение базы данных.
		"""

		for Path in list(self.__Data.keys()):
			if not os.path.exists(Path): del self.__Data[Path]

		if autosave: self.save()

	def drop(self, autosave: bool = True):
		"""
		Удаляет данные всех кэшированных файлов.
			autosave – включает автосохранение базы данных.
		"""

		self.__Data = {"cache": []}
		if autosave: self.save()

	def get_cached_file(self, path: str, upload: bool = True, type: types.InputMedia | None = None, autosave: bool = True) -> CachedFile:
		"""
		Возвращает данные кэшированного файла. Если кэш не обнаружен, выполняет автоматическое кэширование.
			path – путь к файлу или его виртуальный идентификатор;\n
			upload – указывает, нужно ли кэшировать новый файл;\n
			type – тип файла при автозагрузке (по умолчанию документ);\n
			autosave – включает автосохранение базы данных.
		"""

		path = NormalizePath(path)
		if not type: type = types.InputMediaDocument
		if path not in self.__Data.keys() and upload: self.__Data[path] = self.upload_file(path, type, autosave = False)
		if autosave: self.save()

		return self.__Data[path]

	def register_file(self, path: str, chat_id: int, file_id: str, message_id: int | None = None, autosave: bool = True):
		"""
		Регистрирует существующий кэшированный файл в базе данных.
			path – путь к файлу или его виртуальный идентификатор;\n
			chat_id – идентификатор чата с файлом;\n
			file_id – идентификатор файла на сервере Telegram;\n
			message_id – идентификатор сообщения с файлом;\n
			autosave – включает автосохранение базы данных.
		"""
		
		File = CachedFile(path, chat_id, file_id, message_id)	
		self.__Data[path] = File
		if autosave: self.save()
		
		return File

	def remove_cache(self, path: str, autosave: bool = True):
		"""
		Удаляет данные кэшированного файла.
			path – путь к файлу или его виртуальный идентификатор;\n
			autosave – включает автосохранение базы данных.
		"""

		path = NormalizePath(path)
		del self.__Data[path]
		if autosave: self.save()

	def save(self):
		"""Сохраняет данные кэша."""

		if self.__Type == StorageTypes.JSON:
			Buffer = {
				"cache": []
			}
			for Cache in self.__Data.values(): Buffer["cache"].append(Cache.to_dict())
			WriteJSON(self.__Storage, Buffer)

		elif self.__Type == StorageTypes.SQLite: pass

	def set_options(self, bot: TeleBot | str, chat_id: int):
		"""
		Задаёт бота и идентификатор чата для кэширования.
			bot – бот Telegram или его токен;\n
			chat_id – идентификатор чата, в который будут загружаться кэшируемые файлы.
		"""

		if type(bot) == str: self.__Bot = TeleBot(bot)
		else: self.__Bot = bot
		self.__ChatID = chat_id

	def upload_file(self, path: str, type: types.InputMedia | None = None, autosave: bool = True) -> CachedFile:
		"""
		Кэширует файл.
			path – путь к файлу или его виртуальный идентификатор;\n
			type – тип файла (по умолчанию документ);\n
			autosave – включает автосохранение базы данных.
		"""
		
		if not self.__Bot: raise Exception("TeleBot not initialized.")
		if not type: type = types.InputMediaDocument

		path = NormalizePath(path)
		Message: types.Message = None
		FileID: str = None
		
		match type:

			case types.InputMediaAnimation:
				Message = self.__Bot.send_animation(chat_id = self.__ChatID, animation = types.InputFile(path))
				FileID = Message.animation.file_id

			case types.InputMediaAudio:
				Message = self.__Bot.send_audio(chat_id = self.__ChatID, audio = types.InputFile(path))
				FileID = Message.audio.file_id

			case types.InputMediaDocument:
				Message = self.__Bot.send_document(chat_id = self.__ChatID, document = types.InputFile(path))
				FileID = Message.document.file_id
			
			case types.InputMediaPhoto:
				Message = self.__Bot.send_photo(chat_id = self.__ChatID, photo = types.InputFile(path))
				FileID = Message.photo[-1].file_id

			case types.InputMediaVideo:
				Message = self.__Bot.send_video(chat_id = self.__ChatID, video = types.InputFile(path))
				FileID = Message.video.file_id

		self.register_file(path, self.__ChatID, FileID, Message.id, autosave = False)
		if autosave: self.save()
		
		return self.get_cached_file(path, upload = False, autosave = False)