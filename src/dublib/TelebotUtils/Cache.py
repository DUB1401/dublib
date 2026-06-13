from ..Exceptions.TelebotUtils import ChatNotSpecified, UnableCacheFile
from ..Methods.Filesystem import ReadJSON, WriteJSON

from dataclasses import dataclass
from typing import Any, cast
from pathlib import Path
from os import PathLike
import functools
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

	file_id: str
	message_id: int
	file_type: type[types.InputMedia]

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
	def file_type(self) -> type[types.InputMedia] | None:
		"""Тип представления файла в Telegram."""

		return self._Type
	
	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, identificator: PathLike | str, chat_id: int, file_id: str, message_id: int | None = None, data: dict | None = None, file_type: type[types.InputMedia] | None = None):
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
		:param file_type: Тип представления файла в Telegram.
		:type file_type: type[types.InputMedia] | None
		"""

		self._Identificator = identificator
		self._ChatID = chat_id
		self._FileID = file_id
		self._MessageID = message_id
		self._Data: dict[str, Any] = data or dict()
		self._Type = file_type

class VirtualCachedFile(CachedFile):

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def identificator(self) -> str:
		"""Идентификатор файла."""

		return cast(str, self._Identificator)
	
	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def to_dict(self) -> dict:
		"""
		Возвращает словарное представление объекта.

		:return: Словарное представление объекта.
		:rtype: dict
		"""

		Data: dict = {
			"identificator": self._Identificator,
			"chat_id": self._ChatID,
			"file_id": self._FileID,
			"message_id": self._MessageID
		}
		if self._Data: Data["data"] = self._Data.copy()
		if self._Type: Data["type"] = FileTypes(self._Type).name.lower()

		return Data

class RealCachedFile(CachedFile):

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def path(self) -> Path:
		"""Путь к файлу или его виртуальный идентификатор."""

		return Path(self._Identificator)
	
	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def to_dict(self) -> dict:
		"""
		Возвращает словарное представление объекта.

		:return: Словарное представление объекта.
		:rtype: dict
		"""

		Data: dict = {
			"path": self._Identificator,
			"chat_id": self._ChatID,
			"file_id": self._FileID,
			"message_id": self._MessageID
		}
		Data["data"] = self._Data.copy()
		if self._Type: Data["type"] = FileTypes(self._Type).name.lower()

		return Data
	
#==========================================================================================#
# >>>>> ОСНОВНОЙ КЛАСС <<<<< #
#==========================================================================================#

class TeleCache:
	"""Менеджер кэша загружаемых в Telegram файлов."""

	#==========================================================================================#
	# >>>>> ДЕКОРАТОРЫ <<<<< #
	#==========================================================================================#

	@staticmethod
	def require_initialization(function):
		"""
		Декоратор. Проверяет, инициализирован ли менеджер кэша.

		:param function: Метод объекта.
		:raises ChatNotSpecified: Не указан чат для выгрузки.
		:raises UnableCacheFile: Не удалось кэшировать файл.
		"""

		@functools.wraps(function)
		def Wrapper(self: "TeleCache", *args, **kwargs):
			if not self.__ChatID: raise ChatNotSpecified()
			if not self.__Bot: raise RuntimeError("TeleBot not initialized.")
			return function(self, *args, **kwargs)
		
		return Wrapper

	#==========================================================================================#
	# >>>>> ПРИВАТНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __Read(self):
		"""Считывает данные кэша."""

		if not os.path.exists(self.__StoragePath): return
		JSON = ReadJSON(self.__StoragePath)

		Determinations: dict[str, dict] = {
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
				MainKey: str = Determinations[CacheType]["key"]
				Object: type[RealCachedFile | VirtualCachedFile] = Determinations[CacheType]["object"]
				Storage: dict = Determinations[CacheType]["storage"]

				Identificator = Cache[MainKey]

				for Key in ("data", "type"):
					if Key not in Cache.keys(): Cache[Key] = None

				if Cache["type"]:
					CachedFileType: str = Cache["type"]
					Cache["type"] = FileTypes[CachedFileType.title()].value

				Storage[Identificator] = Object(Identificator, Cache["chat_id"], Cache["file_id"], Cache["message_id"], Cache["data"], Cache["type"])

	@require_initialization
	def __UploadFile(self, path: PathLike, type: type[types.InputMedia] | None = None) -> Cache:
		"""
		Кэширует файл.

		:param path: Путь к файлу.
		:type path: PathLike
		:param type: Тип вложения (по умолчанию `types.InputMediaDocument`).
		:type type: type[types.InputMedia] | None
		:raises RuntimeError: Выбрасывается при отсутствии привязки менеджера к боту Telegram.
		:raises TypeError: Выбрасывается при попытке использования полноценного видео (например со звуковой дорожкой) в качестве анимации.
		:return: Данные кэша.
		:rtype: Cache
		"""
		
		if not type: type = types.InputMediaDocument
		ChatID = cast(int, self.__ChatID)
		Bot = cast(TeleBot, self.__Bot)
		FilePath = Path(path)

		Message: types.Message | None = None
		FileID: str | None = None
		
		match type:

			case types.InputMediaAnimation:
				Message = Bot.send_animation(chat_id = ChatID, animation = types.InputFile(FilePath))
				if Message.animation: FileID = Message.animation.file_id
				# Некоторые анимации отображаются верно, но распознаются как документы.
				elif Message.document: FileID = Message.document.file_id
				# Выброс исключения при попытке использования полноценного видео в качестве анимации.
				elif Message.video: raise TypeError("Use InputMediaVideo for this file.")

			case types.InputMediaAudio:
				Message = Bot.send_audio(chat_id = ChatID, audio = types.InputFile(FilePath))
				if Message.audio: FileID = Message.audio.file_id

			case types.InputMediaDocument:
				Message = Bot.send_document(chat_id = ChatID, document = types.InputFile(FilePath))
				if Message.document: FileID = Message.document.file_id
			
			case types.InputMediaPhoto:
				Message = Bot.send_photo(chat_id = ChatID, photo = types.InputFile(FilePath))
				if Message.photo: FileID = Message.photo[-1].file_id

			case types.InputMediaVideo:
				Message = Bot.send_video(chat_id = ChatID, video = types.InputFile(FilePath))
				if Message.video: FileID = Message.video.file_id

		if not FileID or not Message: raise UnableCacheFile(FilePath)

		return Cache(FileID, Message.id, type)

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, bot: TeleBot, cache_file_path: PathLike | None = None,):
		"""
		Менеджер кэша загружаемых в Telegram файлов.

		:param bot: Бот Telegram.
		:type bot: TeleBot
		:param storage_path: Путь к файлу JSON для хранения данных. По умолчанию `.telecache.json`.
		:type storage_path: PathLike | None
		:raises IsADirectoryError: По переданному пути к файлу кэша находится директория.
		"""

		self.__StoragePath = Path(cache_file_path) if cache_file_path else Path(".telecache.json")
		if self.__StoragePath.is_dir(): raise IsADirectoryError(self.__StoragePath)

		self.__Bot: TeleBot = bot
		self.__ChatID: int | None = None

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

		if type(bot) is TeleBot: self.__Bot = bot 
		else: 
			bot = cast(str, bot)
			self.__Bot = TeleBot(bot)

	def set_chat_id(self, chat_id: int, check_chat_access: bool = True):
		"""
		Задаёт ID чата, в который будут выгружаться файлы.

		:param chat_id: ID чата, в который будут выгружаться файлы.
		:type chat_id: int
		:raises RuntimeError: Затребована проверка доступа к чату до инициализации бота.
		:raises ApiTelegramException: Доступ к чату отсутствует.
		"""

		if check_chat_access:
			if not self.__Bot: raise RuntimeError("TeleBot not initialized. Chat access check impossible.")
			self.__Bot.get_chat(chat_id)

		self.__ChatID = chat_id

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ РАБОТЫ С РЕАЛЬНЫМИ ФАЙЛАМИ <<<<< #
	#==========================================================================================#

	@require_initialization
	def cache_real_file(self, path: PathLike, type: type[types.InputMedia] | None = None, data: dict | None = None) -> RealCachedFile:
		"""
		Кэширует реальный файл.

		:param path: Путь к файлу.
		:type path: PathLike
		:param type: Тип вложения (по умолчанию `types.InputMediaDocument`).
		:type type: type[types.InputMedia] | None
		:param data: Словарь дополнительных данных.
		:type data: dict | None
		:return: Данные кэша реального файла.
		:rtype: RealCachedFile
		"""

		if not type: type = types.InputMediaDocument

		if path not in self.__RealData.keys():
			Cache = self.__UploadFile(path, type)
			self.register_real_file(path, cast(int, self.__ChatID), Cache.file_id, Cache.message_id, data, Cache.file_type)

		return self.__RealData[str(path)]

	def clear_real_cache(self):
		"""Удаляет данные кэшированных файлов, пути к которым более не являются валидными."""

		for FilePath in list(self.__RealData.keys()):
			if not os.path.exists(FilePath): del self.__RealData[FilePath]

		self.save()

	def drop_real_cache(self):
		"""Удаляет данные всех реальных кэшированных файлов."""

		self.__RealData = dict()
		self.save()

	def get_real_cached_file(self, path: PathLike, autoupload_type: type[types.InputMedia] | None = None) -> RealCachedFile:
		"""
		Возвращает данные кэша реального файла.

		:param path: Путь к файлу.
		:type path: PathLike
		:param autoupload_type: Если файл отсутствует в кэше, а тип указан, то он автоматически будет выгружен на сервера Telegram.
		:type autoupload_type: type[types.InputMedia] | None
		:raises FileNotFoundError: Выбрасывается при отсутствии файла.
		:return: Данные кэша реального файла.
		:rtype: RealCachedFile
		"""

		if not os.path.exists(path): raise FileNotFoundError(path)
		if autoupload_type: self.cache_real_file(path, autoupload_type)

		return self.__RealData[str(path)]
	
	def has_real_cache(self, path: PathLike) -> bool:
		"""
		Проверяет наличие реального файла в кэше.

		:param path: Путь к файлу.
		:type path: PathLike
		:return: Возвращает `True`, если указанный файл найден в кэше.
		:rtype: bool
		"""

		return path in self.__RealData.keys()

	def register_real_file(self, path: PathLike, chat_id: int, file_id: str, message_id: int | None = None, data: dict | None = None, type: type[types.InputMedia] | None = None) -> RealCachedFile:
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
		:type type: type[types.InputMedia] | None
		:return: Данные кэша реального файла.
		:rtype: RealCachedFile
		"""
		
		File = RealCachedFile(path, chat_id, file_id, message_id, data, type)	
		self.__RealData[str(path)] = File
		self.save()
		
		return File

	def remove_real_cache(self, path: PathLike):
		"""
		Удаляет из хранилища данные кэша реального файла.

		:param path: Путь к файлу.
		:type path: PathLike
		:raise KeyError: Выбрасывается при отсутствии кэша файла по указанному пути.
		"""

		del self.__RealData[str(path)]
		self.save()

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ РАБОТЫ С ВИРТУАЛЬНЫМИ ФАЙЛАМИ <<<<< #
	#==========================================================================================#

	def cache_virtual_file(self, path: PathLike, identificator: str, type: type[types.InputMedia] | None = None, data: dict | None = None) -> VirtualCachedFile:
		"""
		Кэширует виртуальный файл.

		:param path: Путь к файлу.
		:type path: PathLike
		:param identificator: Идентификатор файла.
		:type identificator: str
		:param type: Тип вложения (по умолчанию `types.InputMediaDocument`).
		:type type: type[types.InputMedia] | None
		:param data: Словарь дополнительных данных.
		:type data: dict | None
		:return: Данные кэша виртуального файла.
		:rtype: VirtualCachedFile
		"""

		self.__Bot = cast(TeleBot, self.__Bot)
		self.__ChatID = cast(int, self.__ChatID)

		if not type: type = types.InputMediaDocument

		if path not in self.__VirtualData.keys():
			Cache = self.__UploadFile(path, type)
			self.register_virtual_file(identificator, self.__ChatID, Cache.file_id, Cache.message_id, data, Cache.file_type)

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
	
	def register_virtual_file(self, identificator: str, chat_id: int, file_id: str, message_id: int | None = None, data: dict | None = None, type: type[types.InputMedia] | None = None) -> VirtualCachedFile:
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
		:type type: type[types.InputMedia] | None
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