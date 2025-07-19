from ..Methods.Filesystem import NormalizePath, ReadJSON, WriteJSON

from dataclasses import dataclass
from os import PathLike
import enum
import os

from telebot import TeleBot, types

#==========================================================================================#
# >>>>> ВСПОМОГАТЕЛЬНЫЕ СТРУКТУРЫ ДАННЫХ <<<<< #
#==========================================================================================#

class FileTypes(enum.Enum):
	"""Перечисление представлений файлов."""

	Animation = types.InputMediaAnimation
	Audio = types.InputMediaAudio
	Document = types.InputMediaDocument
	Photo = types.InputMediaPhoto
	Video = types.InputMediaVideo
	Null = None

@dataclass(frozen = True)
class Cache:
	"""Данные кэша."""

	file_id: int
	message_id: int
	type: types.InputFile

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
	def message_id(self) -> int | None:
		"""Идентификатор сообщения с файлом."""

		return self._MessageID
	
	@property
	def type(self) -> types.InputMedia | None:
		"""Тип представления файла в Telegram."""

		return self._Type
	
	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, identificator: PathLike | str, chat_id: int, file_id: str, message_id: int | None = None, data: dict | None = None, type: types.InputMedia | None = None):
		"""
		Данные кэшированного файла.

		:param identificator: Путь к файлу или его вирутальный идентификатор.
		:type identificator: PathLike | str
		:param chat_id: ID чата с файлом.
		:type chat_id: int
		:param file_id: ID файла 
		:type file_id: str
		:param message_id: ID сообщения с файлом.
		:type message_id: int | None
		:param data: Словарь дополнительных данных о файле.
		:type data: dict | None
		:param type: Тип представления файла в Telegram.
		:type type: types.InputMedia | None
		"""

		self._Identificator = identificator
		self._ChatID = chat_id
		self._FileID = file_id
		self._MessageID = message_id
		self._Data = data or dict()
		self._Type = type

class VirtualCachedFile(CachedFile):

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def identificator(self) -> str:
		"""Идентификатор файла."""

		return self._Identificator
	
	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def to_dict(self) -> dict:
		"""
		Возвращает словарное представление объекта.

		:return: Словарное представление объекта.
		:rtype: dict
		"""

		Data = {"identificator": self._Identificator, "chat_id": self._ChatID, "file_id": self._FileID, "message_id": self._MessageID}
		if self._Data: Data["data"] = self._Data.copy()
		if self._Type: Data["type"] = FileTypes(self._Type).name.lower()

		return Data

class RealCachedFile(CachedFile):

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def path(self) -> PathLike:
		"""Путь к файлу или его виртуальный идентификатор."""

		return self._Identificator
	
	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def to_dict(self) -> dict:
		"""
		Возвращает словарное представление объекта.

		:return: Словарное представление объекта.
		:rtype: dict
		"""

		Data = {"path": self._Identificator, "chat_id": self._ChatID, "file_id": self._FileID, "message_id": self._MessageID}
		if self._Data: Data["data"] = self._Data.copy()
		if self._Type: Data["type"] = FileTypes(self._Type).name.lower()

		return Data
	
#==========================================================================================#
# >>>>> ОСНОВНОЙ КЛАСС <<<<< #
#==========================================================================================#

class TeleCache:
	"""Менеджер кэша загружаемых в Telegram файлов."""

	#==========================================================================================#
	# >>>>> ПРИВАТНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __Read(self):
		"""Считывает данные кэша."""

		if not os.path.exists(self.__StoragePath): return
		JSON = ReadJSON(self.__StoragePath)

		Determinations = {
			"real": {
				"key": "path",
				"object": RealCachedFile,
				"storage": self.__RealData
			},
			"virtual": {
				"key": "identificator",
				"object": VirtualCachedFile,
				"storage": self.__VirtualData
			}
		}

		for CacheType in Determinations.keys():

			for Cache in JSON[CacheType]:
				Cache: dict[str, str | int]

				MainKey = Determinations[CacheType]["key"]
				Object = Determinations[CacheType]["object"]
				Storage = Determinations[CacheType]["storage"]

				Identificator = Cache[MainKey]

				for Key in ("data", "type"):
					if Key not in Cache.keys(): Cache[Key] = None

				if Cache["type"]:
					Cache["type"] = Cache["type"].title()
					Cache["type"] = FileTypes[Cache["type"]].value

				Storage[Identificator] = Object(Identificator, Cache["chat_id"], Cache["file_id"], Cache["message_id"], Cache["data"], Cache["type"])

	def __UploadFile(self, path: PathLike, type: types.InputMedia | None = None) -> Cache:
		"""
		Кэширует файл.

		:param path: Путь к файлу.
		:type path: PathLike
		:param type: Тип вложения (по умолчанию `types.InputMediaDocument`).
		:type type: types.InputMedia | None
		:raises RuntimeError: Выбрасывается при отсутствии привязки менеджера к боту Telegram.
		:return: Данные кэша.
		:rtype: Cache
		"""
		
		if not self.__Bot: raise RuntimeError("TeleBot not initialized.")
		if not type: type = types.InputMediaDocument

		path = NormalizePath(path)
		Message: types.Message = None
		FileID: str = None
		
		match type:

			case types.InputMediaAnimation:
				Message = self.__Bot.send_animation(chat_id = self.__ChatID, animation = types.InputFile(path))
				if Message.animation: FileID = Message.animation.file_id
				# Некоторые анимации отображаются верно, но распознаются как документы.
				else: FileID = Message.document.file_id

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

		return Cache(FileID, Message.id, type)

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, storage_path: PathLike | None = None):
		"""
		Менеджер кэша загружаемых в Telegram файлов.

		:param storage_path: Путь к файлу JSON для хранения данных. По умолчанию `.telecache.json`.
		:type storage_path: PathLike | None
		"""

		self.__StoragePath = storage_path or ".telecache.json"

		self.__Bot = None
		self.__ChatID = None

		self.__RealData: dict[str, RealCachedFile] = dict()
		self.__VirtualData: dict[str, VirtualCachedFile] = dict()

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

	def set_bot(self, bot: TeleBot | str):
		"""
		Задаёт используемого для выгрузки бота Telegram.

		:param bot: Токен бота Telegram или объект бота.
		:type bot: TeleBot | str
		"""

		if type(bot) == str: self.__Bot = TeleBot(bot)
		else: self.__Bot = bot

	def set_chat_id(self, chat_id: int):
		"""
		Задаёт используемого для выгрузки бота Telegram.

		:param chat_id: ID чата для отправки сообщений с файлами.
		:type chat_id: int
		"""

		self.__ChatID = chat_id

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ РАБОТЫ С РЕАЛЬНЫМИ ФАЙЛАМИ <<<<< #
	#==========================================================================================#

	def cache_real_file(self, path: PathLike, type: types.InputMedia | None = None, data: dict | None = None) -> RealCachedFile:
		"""
		Кэширует реальный файл.

		:param path: Путь к файлу.
		:type path: PathLike
		:param type: Тип вложения (по умолчанию `types.InputMediaDocument`).
		:type type: types.InputMedia | None
		:param data: Словарь дополнительных данных.
		:type data: dict | None
		:return: Данные кэша реального файла.
		:rtype: RealCachedFile
		"""

		path = NormalizePath(path)
		if not type: type = types.InputMediaDocument

		if path not in self.__RealData.keys():
			Cache = self.__UploadFile(path, type)
			self.register_real_file(path, self.__ChatID, Cache.file_id, Cache.message_id, data, Cache.type)

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

	def get_real_cached_file(self, path: PathLike, autoupload_type: types.InputMedia | None = None) -> RealCachedFile:
		"""
		Возвращает данные кэша реального файла.

		:param path: Путь к файлу.
		:type path: PathLike
		:param autoupload_type: Если файл отсутствует в кэше, а тип указан, то он автоматически будет выгружен на сервера Telegram.
		:type autoupload_type: types.InputMedia | None
		:raises FileNotFoundError: Выбрасывается при отсутствии файла.
		:return: Данные кэша реального файла.
		:rtype: RealCachedFile
		"""

		path = NormalizePath(path)
		if not os.path.exists(path): raise FileNotFoundError(path)
		if autoupload_type: self.cache_real_file(path, autoupload_type)

		return self.__RealData[path]
	
	def has_real_cache(self, path: PathLike) -> bool:
		"""
		Проверяет наличие реального файла в кэше.

		:param path: Путь к файлу.
		:type path: PathLike
		:return: Возвращает `True`, если указанный файл найден в кэше.
		:rtype: bool
		"""

		path = NormalizePath(path)

		return path in self.__RealData.keys()

	def register_real_file(self, path: PathLike, chat_id: int, file_id: str, message_id: int | None = None, data: dict | None = None, type: types.InputMedia | None = None) -> RealCachedFile:
		"""
		Регистрирует в хранилище данные кэша реального файла.

		:param path: Путь к файлу.
		:type path: PathLike
		:param chat_id: ID чата.
		:type chat_id: int
		:param file_id: ID файла.
		:type file_id: str
		:param message_id: ID сообщения с файлом.
		:type message_id: int | None
		:param data: Словарь дополнительных данных.
		:type data: dict | None
		:param type: Тип представления файла.
		:type type: types.InputMedia | None
		:return: Данные кэша реального файла.
		:rtype: RealCachedFile
		"""
		
		File = RealCachedFile(path, chat_id, file_id, message_id, data, type)	
		self.__RealData[path] = File
		self.save()
		
		return File

	def remove_real_cache(self, path: PathLike):
		"""
		Удаляет из хранилища данные кэша реального файла.

		:param path: Путь к файлу.
		:type path: PathLike
		:raise KeyError: Выбрасывается при отсутствии кэша файла по указанному пути.
		"""

		path = NormalizePath(path)
		del self.__RealData[path]
		self.save()

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ РАБОТЫ С ВИРТУАЛЬНЫМИ ФАЙЛАМИ <<<<< #
	#==========================================================================================#

	def cache_virtual_file(self, path: PathLike, identificator: str, type: types.InputMedia | None = None, data: dict | None = None) -> VirtualCachedFile:
		"""
		Кэширует виртуальный файл.

		:param path: Путь к файлу.
		:type path: PathLike
		:param identificator: Идентификатор файла.
		:type identificator: str
		:param type: Тип вложения (по умолчанию `types.InputMediaDocument`).
		:type type: types.InputMedia | None
		:param data: Словарь дополнительных данных.
		:type data: dict | None
		:return: Данные кэша виртуального файла.
		:rtype: VirtualCachedFile
		"""

		path = NormalizePath(path)
		if not type: type = types.InputMediaDocument

		if path not in self.__VirtualData.keys():
			Cache = self.__UploadFile(path, type)
			self.register_virtual_file(identificator, self.__ChatID, Cache.file_id, Cache.message_id, data, Cache.type)

		return self.__VirtualData[identificator]

	def drop_virtual_cache(self):
		"""Удаляет данные всех виртуальных кэшированных файлов."""

		self.__VirtualData = dict()
		self.save()

	def get_virtual_cached_file(self, identificator: str) -> VirtualCachedFile:
		"""
		Возвращает данные кэша виртуального файла.

		:param identificator: Идентификатор файла.
		:type identificator: str
		:raise KeyError: Выбрасывается при отсутствии кэша файла с указанным идентификатором.
		:return: Данные кэша виртуального файла.
		:rtype: VirtualCachedFile
		"""

		return self.__VirtualData[identificator]
	
	def has_virtual_cache(self, identificator: str) -> bool:
		"""
		Проверяет наличие виртуального файла в кэше.

		:param identificator: Идентификатор файла.
		:type identificator: str
		:return: Возвращает `True`, если указанный файл найден в кэше.
		:rtype: bool
		"""

		return identificator in self.__VirtualData.keys()
	
	def register_virtual_file(self, identificator: str, chat_id: int, file_id: str, message_id: int | None = None, data: dict | None = None, type: types.InputMedia | None = None) -> VirtualCachedFile:
		"""
		Регистрирует в хранилище данные кэша виртуального файла.

		:param identificator: Идентификатор файла.
		:type identificator: str
		:param chat_id: ID чата.
		:type chat_id: int
		:param file_id: ID файла.
		:type file_id: str
		:param message_id: ID сообщения с файлом.
		:type message_id: int | None
		:param data: Словарь дополнительных данных.
		:type data: dict | None
		:param type: Тип представления файла.
		:type type: types.InputMedia | None
		:return: Данные кэша виртуального файла.
		:rtype: VirtualCachedFile
		"""
		
		File = VirtualCachedFile(identificator, chat_id, file_id, message_id, data, type)	
		self.__VirtualData[identificator] = File
		self.save()
		
		return File

	def remove_virtual_cache(self, identificator: str):
		"""
		Удаляет из хранилища данные кэша виртуального файла.

		:param identificator: Идентификатор файла.
		:type identificator: str
		:raise KeyError: Выбрасывается при отсутствии кэша файла с указанным идентификатором.
		"""

		del self.__VirtualData[identificator]
		self.save()