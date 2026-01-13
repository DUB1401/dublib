from ..Methods.Filesystem import ReadJSON, ReadYAML, WriteJSON, WriteYAML
from ..Methods.Data import Copy

from typing import Any, Callable
from threading import Thread
from pathlib import Path
from os import PathLike

from pydantic import BaseModel
from watchfiles import watch

class Config:
	"""Контейнер конфигурации."""

	#==========================================================================================#
	# >>>>> СТАТИЧЕСКИЕ АТРИБУТЫ <<<<< #
	#==========================================================================================#

	__INSTANCES: "dict[PathLike, Config]" = dict()

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def data(self) -> dict:
		"""Глубокая копия словаря параметров."""

		return Copy(self.__Data)

	@property
	def path(self) -> PathLike:
		"""Путь к файлу параметров."""

		return self.__Path.as_posix()
	
	#==========================================================================================#
	# >>>>> ПРИВАТНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __GetValue(self, key: str, copy: bool = True) -> Any:
		"""
		Возвращает значение параметра.

		:param key: Ключ параметра.
		:type key: str
		:param copy: Указывает, нужно ли вернуть копию для изменяемых типов (`dict`, `list`). Не рекомендуется отключать без острой необходимости прямой манипуляции объектами.
		:type copy: bool
		:raise KeyError: Выбрасывается при отсутствии параметра с указанным ключом.
		:return: Значение параметра.
		:rtype: Any
		"""

		Value = self.__Data[key]
		if copy and type(Value) in (dict, list): Value = Copy(Value)

		return Value

	def __SyncProcessor(self):
		"""Метод отслеживания изменений в файле конфигурации."""

		for _ in watch(self.__Path):
			if not self.__IsSync: break
			if self.__OnChangesCallback: self.__OnChangesCallback()
			self.load()

		self.__SyncThread = None

	#==========================================================================================#
	# >>>>> СПЕЦИАЛЬНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __new__(cls: "Config", *args, **kwargs) -> "Config":
		"""
		Инициализирует новый объект или возвращает уже существующий (поддерживает множественные конфигурации).

		:param cls: Текущий экземпляр объекта.
		:type cls: Config
		:return: Экземпляр объекта.
		:rtype: Config
		"""

		if args[0] not in cls.__INSTANCES:
			Instance = super().__new__(cls)
			Instance._IS_INITIALIZED = False
			cls.__INSTANCES[args[0]] = Instance

		return cls.__INSTANCES[args[0]]
	
	def __init__(self, path: PathLike):
		"""
		Контейнер конфигурации.

		Может работать с файлами JSON и YAML. Определение происходит по расширению файла, в противном случае предпочтение отдаётся JSON.

		:param path: Путь к файлу параметров. На данный момент поддерживается только JSON.
		:type path: PathLike
		"""

		if self._IS_INITIALIZED: return

		self.__Path = Path(path)

		self.__Data: dict  = dict()
		self.__Model: BaseModel | None = None

		self.__IsSync = True
		self.__SyncThread = None
		self.__OnChangesCallback = None

		self._IS_INITIALIZED = True

	def __getitem__(self, key: str) -> Any:
		"""
		Возвращает значение параметра. Для изменяемых типов (`dict`, `list`) возвращает копию.

		:param key: Ключ параметра.
		:type key: str
		:raise KeyError: Выбрасывается при отсутствии параметра с указанным ключом.
		:return: Значение параметра.
		:rtype: Any
		"""
		
		return self.get(key)
	
	def __setitem__(self, key: str, value: Any):
		"""
		Задаёт значение параметра. Если файл параметров не загружался, будет создан новый.

		:param key: Ключ параметра.
		:type key: str
		:param value: Значение параметра.
		:type value: Any
		"""
		
		self.__GetValue(key, value)

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def disable_sync(self):
		"""
		Отключает отслеживание изменений в файле конфигурации.

		Демон остаётся функционировать до следующего изменения файла, но загрузку изменений и вызов Callback-функции пропустит. Это связано с отсутствием в Python механизмов прерывания потоков.
		"""

		self.__IsSync = False

	def enable_sync(self, callback: Callable | None = None):
		"""
		Включает отслеживание изменений в файле конфигурации.

		При отключении синхронизации демон остаётся функционировать до следующего изменения файла, но загрузку изменений пропустит. Это связано с отсутствием в Python механизмов прерывания потоков.

		:param callback: Функция, вызываемая при обнаружении изменений в файле конфигурации.
		:type callback: Callable | None
		"""

		self.__IsSync = True
		self.__OnChangesCallback = callback

		if self.__IsSync and not self.__SyncThread:
			self.__SyncThread = Thread(target = self.__SyncProcessor, daemon = True)
			self.__SyncThread.start()

	def get(self, key: str, copy: bool = True, default: Any = None) -> Any:
		"""
		Возвращает значение параметра.

		:param key: Ключ параметра.
		:type key: str
		:param copy: Указывает, нужно ли вернуть копию для изменяемых типов (`dict`, `list`). Не рекомендуется отключать без острой необходимости прямой манипуляции объектами.
		:type copy: bool
		:param default: Значение по умолчанию.
		:type default: Any
		:return: Значение параметра.
		:rtype: Any
		"""

		try: return self.__GetValue(key, copy)
		except KeyError: return default
	
	def load(self, validate: bool = True):
		"""
		Загружает параметры из файла JSON.

		:param validate: Если указана модель и включен этот параметр, будет проведена валидация прочитанного файла.
		:type validate: bool
		:raise pydantic.ValidationError: Выбрасывается при ошибке валидации.
		"""

		match self.__Path.suffix:
			case ".yaml" | ".yml": self.__Data = ReadYAML(self.path)
			case _: self.__Data = ReadJSON(self.path)

		if self.__Model and validate: self.validate()

	def save(self):
		"""Записывает изменения параметров в файл."""

		match self.__Path.suffix:
			case ".yaml" | ".yml": WriteYAML(self.path, self.__Data)
			case _: WriteJSON(self.path, self.__Data)

	def set(self, key: str, value: Any):
		"""
		Задаёт значение параметра. Если файл параметров не загружался, будет создан новый.

		:param key: Ключ параметра.
		:type key: str
		:param value: Значение параметра.
		:type value: Any
		"""

		self.__Data[key] = value
		self.save()

	def set_data(self, data: dict, validate: bool = True):
		"""
		Задаёт словарь параметров.

		:param data: Словарь параметров.
		:type data: dict
		:param validate: Если указана модель и включен этот параметр, будет проведена валидация данных.
		:type validate: bool
		:raise pydantic.ValidationError: Выбрасывается при ошибке валидации.
		"""

		self.__Data = data
		if self.__Model and validate: self.validate()

	def set_model(self, model: BaseModel | None):
		"""
		Задаёт модель валидации **pydantic**.

		:param model: Модель для валидации.
		:type model: BaseModel | None
		"""

		self.__Model = model

	def unload(self):
		"""Выгружает контейнер из памяти."""

		del self.__INSTANCES[self.path]

	def validate(self, model: BaseModel | None = None):
		"""
		Проводит валидацию параметров согласно модели **pydantic**.

		:param model: Модель для валидации.
		:type model: BaseModel | None
		:raise pydantic.ValidationError: Выбрасывается при ошибке валидации.
		:raise TypeError: Выбрасывается при отсутствии модели для валидации.
		"""

		Model = model or self.__Model
		if not Model: raise TypeError("Missing model for validation.")
		Model(**self.__Data)