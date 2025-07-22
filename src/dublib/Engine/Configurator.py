from ..Methods.Filesystem import ReadJSON, ReadYAML, WriteJSON, WriteYAML
from ..Methods.Data import Copy

from pathlib import Path
from os import PathLike
from typing import Any

from pydantic import BaseModel

class Config:
	"""Модуль параметров."""

	#==========================================================================================#
	# >>>>> СТАТИЧЕСКИЕ АТРИБУТЫ <<<<< #
	#==========================================================================================#

	__INSTANCE: "Config | None" = None

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
	# >>>>> СПЕЦИАЛЬНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __new__(cls: "Config", *args, **kwargs) -> "Config":
		"""
		Инициализирует новый объект или возвращает уже существующий (паттерн Singleton).

		:param cls: Текущий экземпляр объекта.
		:type cls: Config
		:return: Экземпляр объекта.
		:rtype: Config
		"""

		if not cls.__INSTANCE: cls.__INSTANCE = super().__new__(cls)

		return cls.__INSTANCE
	
	def __init__(self, path: PathLike):
		"""
		Модуль параметров.

		Может работать с файлами конфигураций JSON и YAML. Определение происходит по расширению файла, в противном случае предпочтение отдаётся JSON.

		:param path: Путь к файлу параметров. На данный момент поддерживается только JSON.
		:type path: PathLike
		"""

		self.__Path = Path(path)

		self.__Data: dict  = dict()
		self.__Model: BaseModel | None = None

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
		
		self.set(key, value)

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def get(self, key: str, copy: bool = True) -> Any:
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
	
	def load(self, validate: bool = True):
		"""
		Загружает параметры из файла JSON.

		:param validate: Если указана модель и включен этот параметр, будет проведена валидация прочитанного файла.
		:type validate: bool
		:raise pydantic.ValidationError: Выбрасывается при ошибке валидации.
		"""

		PosixPath = self.__Path.as_posix()

		match self.__Path.suffix:
			case ".yaml" | ".yml": self.__Data = ReadYAML(PosixPath)
			case _: self.__Data = ReadJSON(PosixPath)

		if self.__Model and validate: self.validate()

	def save(self):
		"""Записывает изменения параметров в файл."""

		PosixPath = self.__Path.as_posix()

		match self.__Path.suffix:
			case ".yaml" | ".yml": WriteYAML(PosixPath, self.__Data)
			case _: WriteJSON(PosixPath, self.__Data)

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