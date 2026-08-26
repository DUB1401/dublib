from os import PathLike
from pathlib import Path
from typing import Self

from pydantic import TypeAdapter
from pydantic.dataclasses import dataclass

from ..functions.filesystem import ReadJSON, ReadYAML, WriteJSON, WriteYAML

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
	
	def __init__(self, path: str | PathLike[str], model: type[T]):
		"""
		Контейнер конфигурации.

		Может работать с файлами JSON и YAML. Определение происходит по расширению файла, в противном случае предпочтение отдаётся JSON.

		:param path: Путь к файлу параметров. На данный момент поддерживается только JSON.
		:type path: str | PathLike[str]
		:param model: Модель для валидации конфигурации, унаследованная от `ConfigTemplate`.
		:type model: type[ConfigTemplate]
		"""

		if self._IS_INITIALIZED: return

		self.__ConfigFile: Path = Path(path)
		self.__Model: type[T] = model
		self.__Data: T = self.load()

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
			case ".yaml" | ".yml": Data = ReadYAML(self.path)
			case _: Data = ReadJSON(self.path)

		self.__Data = TypeAdapter(self.__Model).validate_python(Data)

		return self.__Data

	def save(self):
		"""Сохраняет файл конфигурации."""

		Data = TypeAdapter(self.__Model).dump_python(self.__Data)

		match self.__ConfigFile.suffix:
			case ".yaml" | ".yml": WriteYAML(self.path, Data)
			case _: WriteJSON(self.path, Data)

	def unload(self):
		"""Выгружает контейнер из памяти."""

		del self.__INSTANCES[self.path.as_posix()]
