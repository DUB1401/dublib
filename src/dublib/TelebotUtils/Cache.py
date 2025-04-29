from ..Methods.Filesystem import NormalizePath, ReadJSON, WriteJSON

from dataclasses import dataclass
import os

from telebot import TeleBot, types

#==========================================================================================#
# >>>>> ВСПОМОГАТЕЛЬНЫЕ СТРУКТУРЫ ДАННЫХ <<<<< #
#==========================================================================================#

@dataclass(frozen = True)
class Cache:
	"""Данные кэша."""

	file_id: int
	message_id: int

class CachedFile:
	"""Данные кэшированного файла."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#
	
	@property
	def chat_id(self) -> int:
		"""Идентификатор чата с файлом."""

		return self._ChatID
	
	@property
	def data(self) -> dict:
		"""Словарь дополнительных данных."""

		return self._Data

	@property
	def file_id(self) -> str:
		"""Идентификатор файла на сервере Telegram."""

		return self._FileID

	@property
	def identificator(self) -> str:
		"""Идентификатор файла или путь к нему."""

		return self._Identificator

	@property
	def message_id(self) -> int | None:
		"""Идентификатор сообщения с файлом."""

		return self._MessageID
	
	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, identificator: str, chat_id: int, file_id: str, message_id: int | None = None, data: dict | None = None):
		"""
		Данные кэшированного файла.
			identificator – путь к файлу или его виртуальный идентификатор;\n
			chat_id – идентификатор чата с файлом;\n
			file_id – идентификатор файла на сервере Telegram;\n
			message_id – идентификатор сообщения с файлом.
		"""

		#---> Генерация динамических свойств.
		#==========================================================================================#
		self._Identificator = identificator
		self._ChatID = chat_id
		self._FileID = file_id
		self._MessageID = message_id
		self._Data = data or dict()

	def __str__(self) -> str:
		"""Преобразует данные в строку."""

		return str(self.to_dict())
	
	def to_dict(self) -> dict:
		"""Генерирует словарь данных кэшированного файла."""

		return {"identificator": self._Identificator, "chat_id": self._ChatID, "file_id": self._FileID, "message_id": self._MessageID, "data": self._Data}

class RealCachedFile(CachedFile):

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def path(self) -> str:
		"""Путь к файлу или его виртуальный идентификатор."""

		return self._Identificator
	
	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def to_dict(self) -> dict:
		"""Генерирует словарь данных кэшированного файла."""

		return {"path": self._Identificator, "chat_id": self._ChatID, "file_id": self._FileID, "message_id": self._MessageID, "data": self._Data}
	
#==========================================================================================#
# >>>>> ОСНОВНОЙ КЛАСС <<<<< #
#==========================================================================================#

class TeleCache:
	"""Менеджер кэша загружаемых в Telegram файлов."""

	#==========================================================================================#
	# >>>>> ПРИВАТНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __Read(self):
		"""Считывает данные или инициализирует новое хранилище."""

		try: JSON = ReadJSON(self.__StoragePath)
		except FileNotFoundError: return

		for Cache in JSON["real"]:
			Path = Cache["path"]
			self.__RealData[Path] = RealCachedFile(Path, Cache["chat_id"], Cache["file_id"], Cache["message_id"])

		for Cache in JSON["virtual"]:
			ID = Cache["identificator"]
			self.__VirtualData[ID] = CachedFile(ID, Cache["chat_id"], Cache["file_id"], Cache["message_id"])

	def __UploadFile(self, path: str, type: types.InputMedia | None = None) -> Cache:
		"""
		Кэширует файл.
			path – путь к файлу;\n
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

		return Cache(FileID, Message.id)

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, storage_path: str | None = None):
		"""
		Менеджер кэша загружаемых в Telegram файлов.
			storage_path – путь к файлу базы данных.
		"""

		#---> Генерация динамических свойств.
		#==========================================================================================#
		self.__StoragePath = storage_path or ".telecache.json"

		self.__Bot = None
		self.__ChatID = None

		self.__RealData: dict[str, RealCachedFile] = dict()
		self.__VirtualData: dict[str, CachedFile] = dict()

		self.__Read()

	def drop(self):
		"""Удаляет данные всех кэшированных файлов."""

		self.__RealData = dict()
		self.__VirtualData = dict()
		self.save()

	def save(self):
		"""Сохраняет данные кэша."""

		Buffer = {
			"real": [Cache.to_dict() for Cache in self.__RealData.values()],
			"virtual": [Cache.to_dict() for Cache in self.__VirtualData.values()]
		}

		WriteJSON(self.__StoragePath, Buffer)

	def set_options(self, bot: TeleBot | str, chat_id: int):
		"""
		Задаёт бота и идентификатор чата для кэширования.
			bot – бот Telegram или его токен;\n
			chat_id – идентификатор чата, в который будут загружаться кэшируемые файлы.
		"""

		if type(bot) == str: self.__Bot = TeleBot(bot)
		else: self.__Bot = bot
		self.__ChatID = chat_id

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ РАБОТЫ С РЕАЛЬНЫМИ ФАЙЛАМИ <<<<< #
	#==========================================================================================#

	def cache_real_file(self, path: str, type: types.InputMedia | None = None, data: dict | None = None) -> RealCachedFile:
		"""
		Кэширует реальный файл.
			path – путь к файлу;\n
			type – тип файла при автозагрузке (по умолчанию документ);\n
			data – словарь дополнительных данных.
		"""

		path = NormalizePath(path)
		if not type: type = types.InputMediaDocument

		if path not in self.__RealData.keys():
			Cache = self.__UploadFile(path, type)
			self.register_real_file(path, self.__ChatID, Cache.file_id, Cache.message_id, data)

		return self.__RealData[path]

	def clear_real_cache(self):
		"""Удаляет данные кэшированных файлов, пути к которым более не являются валидными."""

		for Path in list(self.__RealData.keys()):
			if not os.path.exists(Path): del self.__RealData[Path]

		self.save()

	def drop_real_cache(self):
		"""Удаляет данные всех реальных кэшированных файлов."""

		self.__RealData = dict()
		self.save()

	def get_real_cached_file(self, path: str, autoupload_type: types.InputMedia | None = None) -> RealCachedFile:
		"""
		Возвращает данные реального кэшированного файла.
			path – путь к файлу;\n
			autoupload_type – если файл отсутствует в кэше и указан тип, то он будет автоматически кэширован в соответствии с ним.
		"""

		path = NormalizePath(path)
		if autoupload_type: self.cache_real_file(path, autoupload_type)

		return self.__RealData[path]
	
	def register_real_file(self, path: str, chat_id: int, file_id: str, message_id: int | None = None, data: dict | None = None) -> RealCachedFile:
		"""
		Регистрирует кэш реального файла.
			path – путь к файлу;\n
			chat_id – идентификатор чата с файлом;\n
			file_id – идентификатор файла на сервере Telegram;\n
			message_id – идентификатор сообщения с файлом;\n
			data – словарь дополнительных данных.
		"""
		
		File = RealCachedFile(path, chat_id, file_id, message_id, data)	
		self.__RealData[path] = File
		self.save()
		
		return File

	def remove_real_cache(self, path: str):
		"""
		Удаляет данные реального кэшированного файла.
			path – путь к файлу.
		"""

		path = NormalizePath(path)
		del self.__RealData[path]
		self.save()

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ РАБОТЫ С ВИРТУАЛЬНЫМИ ФАЙЛАМИ <<<<< #
	#==========================================================================================#

	def cache_virtual_file(self, path: str, identificator: str, type: types.InputMedia | None = None, data: dict | None = None) -> RealCachedFile:
		"""
		Кэширует реальный файл.
			path – путь к файлу;\n
			identificator – виртуальный идентификатор файла;\n
			type – тип файла при автозагрузке (по умолчанию документ);\n
			data – словарь дополнительных данных.
		"""

		path = NormalizePath(path)
		if not type: type = types.InputMediaDocument

		if path not in self.__VirtualData.keys():
			Cache = self.__UploadFile(path, type)
			self.register_virtual_file(identificator, self.__ChatID, Cache.file_id, Cache.message_id, data)

		return self.__VirtualData[identificator]

	def drop_virtual_cache(self):
		"""Удаляет данные всех виртуальных кэшированных файлов."""

		self.__VirtualData = dict()
		self.save()

	def get_virtual_cached_file(self, identificator: str) -> CachedFile:
		"""
		Возвращает данные виртуального кэшированного файла.
			identificator – виртуальный идентификатор файла.
		"""

		return self.__VirtualData[identificator]
	
	def register_virtual_file(self, identificator: str, chat_id: int, file_id: str, message_id: int | None = None, data: dict | None = None) -> CachedFile:
		"""
		Регистрирует кэш виртуального файла.
			identificator – виртуальный идентификатор файла;\n
			chat_id – идентификатор чата с файлом;\n
			file_id – идентификатор файла на сервере Telegram;\n
			message_id – идентификатор сообщения с файлом;\n
			data – словарь дополнительных данных.
		"""
		
		File = CachedFile(identificator, chat_id, file_id, message_id, data)	
		self.__VirtualData[identificator] = File
		self.save()
		
		return File

	def remove_virtual_cache(self, identificator: str):
		"""
		Удаляет данные виртуального кэшированного файла.
			identificator – виртуальный идентификатор файла.
		"""

		del self.__VirtualData[identificator]
		self.save()