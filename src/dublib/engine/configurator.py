import asyncio
from os import PathLike
from pathlib import Path
from threading import Thread
from typing import Self

from pydantic import TypeAdapter
from pydantic.dataclasses import dataclass
from watchfiles import awatch, watch

from ..functions.filesystem import json, yaml

#==========================================================================================#
# >>>>> ВСПОМОГАТЕЛЬНЫЕ СТРУКТУРЫ ДАННЫХ <<<<< #
#==========================================================================================#

@dataclass
class ConfigTemplate:
	"""Модель конфигурации."""

	pass

#==========================================================================================#
# >>>>> ОСНОВНОЙ КЛАСС <<<<< #
#==========================================================================================#

class Config[T: ConfigTemplate]:
	"""Контейнер конфигурации."""

	__WatchingThread: Thread | None

	#==========================================================================================#
	# >>>>> СТАТИЧЕСКИЕ АТРИБУТЫ <<<<< #
	#==========================================================================================#

	__INSTANCES: "dict[str, Config]" = {}

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def data(self) -> T:
		"""Параметры конфигурации."""

		return self.__Data

	@property
	def path(self) -> Path:
		"""Путь к файлу конфигурации."""

		return self.__ConfigFile

	#==========================================================================================#
	# >>>>> ПРИВАТНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __Watch(self):
		"""Метод отслеживания изменений в файле конфигурации."""

		for _ in watch(self.__ConfigFile):
			if not self.__IsWatching: break
			self.load()

		self.__WatchingThread = None

	#==========================================================================================#
	# >>>>> СПЕЦИАЛЬНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __new__(cls: "type[Self]", *args, **kwargs) -> "Config":
		"""
		Инициализирует новый объект или возвращает уже существующий (поддерживает множественные конфигурации).

		:param cls: Текущий экземпляр объекта.
		:type cls: type[Self]
		:return: Экземпляр объекта.
		:rtype: Config
		"""

		if args[0] not in cls.__INSTANCES:
			Instance = super().__new__(cls)
			Instance._IS_INITIALIZED = False
			ConfigPath = Path(args[0])
			cls.__INSTANCES[ConfigPath.as_posix()] = Instance

		return cls.__INSTANCES[args[0]]
	
	def __init__(self, path: PathLike[str] | str, model: type[T]):
		"""
		Контейнер конфигурации.

		Может работать с файлами JSON и YAML. Определение происходит по расширению файла, в противном случае предпочтение отдаётся JSON.

		:param path: Путь к файлу параметров. На данный момент поддерживается только JSON.
		:type path: PathLike[str] | str
		:param model: Модель для валидации конфигурации, унаследованная от `ConfigTemplate`.
		:type model: type[ConfigTemplate]
		"""

		if self._IS_INITIALIZED: return

		self.__ConfigFile: Path = Path(path)
		self.__Model: type[T] = model

		self.__Data: T = self.load()
		
		self.__IsWatching: bool = False
		self.__WatchingThread: Thread | None = None

		self._IS_INITIALIZED: bool = True

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def load(self) -> T:
		"""
		Считывает файл конфигурации.

		:return: Данные конфигурации.
		:rtype: ConfigTemplate
		"""

		Data: dict | None = None

		match self.__ConfigFile.suffix:
			case ".yaml" | ".yml": Data = yaml.read(self.path)
			case _: Data = json.read(self.path)

		self.__Data = TypeAdapter(self.__Model).validate_python(Data)

		return self.__Data

	def save(self):
		"""Сохраняет файл конфигурации."""

		Data = TypeAdapter(self.__Model).dump_python(self.__Data)

		match self.__ConfigFile.suffix:
			case ".yaml" | ".yml": yaml.write(self.path, Data)
			case _: json.write(self.path, Data)

	def stop_watching(self):
		"""
		Останавливает отслеживание изменений в файле.

		При отключении синхронизации демон остаётся функционировать до следующего изменения файла, но загрузку изменений пропустит. Это связано с отсутствием в **Python** механизмов прерывания потоков.
		"""

		self.__IsWatching = False

	def unload(self):
		"""Выгружает контейнер из памяти."""

		del self.__INSTANCES[self.path.as_posix()]

	def watch(self):
		"""Включает отслеживание изменений в файле конфигурации и автоматическую перезагрузку последнего."""

		self.__IsWatching = True

		if not self.__WatchingThread:
			self.__WatchingThread = Thread(target = self.__Watch, daemon = True)
			self.__WatchingThread.start()

	async def watch_async(self):
		"""Включает асинхронное отслеживание изменений в файле конфигурации и автоматическую перезагрузку последнего."""

		self.__IsWatching = True
		
		async for _ in awatch(self.__ConfigFile):
			if not self.__IsWatching: break
			await asyncio.to_thread(self.load)