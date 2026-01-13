from ..Methods.Filesystem import ListDir, NormalizePath, ReadJSON, WriteJSON
from ..Methods.Data import Copy, ToIterable
from ..Exceptions.TelebotUtils import *
from ..Core import LOGS_HANDLER

from concurrent.futures import ThreadPoolExecutor
from typing import Any, Iterable, Literal
from datetime import datetime, timedelta
from threading import Thread
from os import PathLike
import logging
import hashlib
import enum
import os

from apscheduler.schedulers.background import BackgroundScheduler
from more_itertools import divide
import dateparser
import telebot
import orjson

#==========================================================================================#
# >>>>> ИНИЦИАЛИЗАЦИЯ СИСТЕМЫ ЛОГГИРОВАНИЯ <<<<< #
#==========================================================================================#

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(LOGS_HANDLER)
LOGGER.setLevel(logging.INFO)

#==========================================================================================#
# >>>>> ОСНОВНЫЕ КЛАССЫ <<<<< #
#==========================================================================================#

class UserData:
	"""Объектное представление данных пользователя."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def last_activity(self) -> datetime | None:
		"""Дата и время последней активности пользователя."""

		return self.__Data["last_activity"]

	@property
	def expected_type(self) -> str | None:
		"""Тип ожидаемого значения."""

		return self.__Data["expected_type"]

	@property
	def flags(self) -> tuple[str]:
		"""Набор активированных флагов."""

		return tuple(self.__Data["flags"])

	@property
	def id(self) -> int:
		"""ID пользователя."""

		return self.__ID

	@property
	def is_chat_forbidden(self) -> bool:
		"""Состояние: может ли бот контактировать с пользователем."""
		
		return self.__Data["is_chat_forbidden"]

	@property
	def is_premium(self) -> bool:
		"""Состояние: имеет ли пользователь Premium-подписку."""

		return self.__Data["is_premium"]

	@property
	def language(self) -> str:
		"""Код используемого клиентом языка по стандарту ISO 639-1."""

		return self.__Data["language"]

	@property
	def permissions(self) -> tuple[str]:
		"""Список прав пользователя."""

		return tuple(self.__Data["permissions"])

	@property
	def username(self) -> str:
		"""Ник пользователя."""

		return self.__Data["username"]

	#==========================================================================================#
	# >>>>> НЕСЕРИАЛИЗУЕМЫЕ СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def is_saving_suppressed(self) -> bool:
		"""Состояние: подавляется ли сохранение в локальный файл."""

		return self.__SuppressSaving

	@property
	def objects(self) -> dict[str, Any]:
		"""Словарь прикреплённых к пользователю объектов."""

		return self.__Objects

	@property
	def path(self) -> PathLike:
		"""Путь к файлу пользователя."""

		return self.__Path

	#==========================================================================================#
	# >>>>> ПРИВАТНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __AddFlags(self, flags: Iterable[str] | str, key: str):
		"""
		Реализовывает добавление флаговых переключателей в данные пользователя.

		:param flags: Набор флагов или конкретный флаг.
		:type flags: Iterable[str] | str
		:param key: Ключ, под который в структуру данных пользователя заносятся флаги.
		:type key: str
		"""

		flags = ToIterable(flags)
		IsChanged = False

		for Flag in flags:

			if Flag not in self.__Data[key]:
				self.__Data[key].append(Flag)
				IsChanged = True

		if IsChanged:
			self.__Data[key] = sorted(self.__Data[key])
			self.save()

	def __CalculateHash(self) -> str:
		"""
		Вычисляет MD5 хэш JSON строки пользователя.

		:return: MD5 хэш.
		:rtype: str
		"""

		Data = self.__ToSerializableDict()
		Bytes = orjson.dumps(Data)

		return hashlib.md5(Bytes).hexdigest()

	def __RemoveFlags(self, flags: Iterable[str] | str, key: str):
		"""
		Реализовывает удаление флаговых переключателей из данных пользователя.

		:param flags: Набор флагов или конкретный флаг.
		:type flags: Iterable[str] | str
		:param key: Ключ, по которому из структуры данных пользователя удаляются флаги.
		:type key: str
		"""

		if type(flags) == str: flags = (flags,)
		IsChanged = False

		for Flag in flags:

			if Flag in self.__Data[key]:
				self.__Data[key].remove(Flag)
				IsChanged = True

		if IsChanged: self.save()

	def __SetProperty(self, property_type: Literal["data", "temp"], key: str, value: Any):
		"""
		Задаёт свойство пользователя.

		:param property_type: Тип свойства.
		:type property_type: Literal["data", "temp"]
		:param key: Ключ, под который помещаются данные.
		:type key: str
		:param value: Сохраняемые данные. Для изменяемых типов создаётся глубокая копия.
		:type value: Any
		"""

		if type(value) in (dict, list): value = Copy(value)
		if key in self.__Data[property_type] and self.__Data[property_type][key] == value: return
		self.__Data[property_type][key] = value
		self.save()

	def __ToSerializableDict(self) -> dict:
		"""
		Приводит объект к сериализуемому словарю.
		:return: Сериализуемый словарь.
		:rtype: dict
		"""

		Data = self.__Data.copy()
		LastActivity: datetime = Data["last_activity"]
		if LastActivity:  Data["last_activity"] = LastActivity.strftime("%Y-%m-%d %H:%M")

		return Data

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, manager: "UsersManager", user_id: int):
		"""
		Данные пользователя.

		:param manager: Менеджер пользователей.
		:type manager: UsersManager
		:param user_id: ID пользователя.
		:type user_id: int
		"""

		self.__Manager = manager
		self.__ID = user_id
		self.__Data = {
			"username": None,
			"language": None,
			"is_chat_forbidden": False,
			"is_premium": None,
			"expected_type": None,
			"permissions": [],
			"last_activity": None,
			"flags": [],
			"data": {},
			"temp": {}
		}

		self.__Objects = dict()
		self.__Path = f"{self.__Manager.storage_directory}/{user_id}.json"
		self.__SuppressSaving = False
		self.__DeltaHash: str | None = None

		if not os.path.exists(self.__Path): self.save()
		else: self.refresh()

	def __repr__(self) -> str:
		"""
		Репрезентует объект в строковое представление.

		:return: Строковое представление.
		:rtype: str
		"""

		return self.__str__()

	def __str__(self) -> str:
		"""
		Преобразует объект в строковое представление.

		:return: Строковое представление.
		:rtype: str
		"""

		return f"User<{self.__ID}, {self.username}>"

	def add_flags(self, flags: Iterable[str] | str):
		"""
		Добавляет флаги пользователю.

		:param flags: Один или несколько флагов.
		:type flags: Iterable[str] | str
		"""

		self.__AddFlags(flags, "flags")

	def add_permissions(self, permissions: Iterable[str] | str):
		"""
		Добавляет права пользователю.

		:param permissions: Одно или несколько прав.
		:type permissions: Iterable[str] | str
		"""

		self.__AddFlags(permissions, "permissions")

	def attach_object(self, key: str, object: Any, force: bool = True):
		"""
		Прикрепляет объект к пользователю. При перезапуске объект будет удалён.

		:param key: Ключ объекта.
		:type key: str
		:param object: Прикрепляемый объект.
		:type object: Any
		:param force: Указывает, нужно ли перезаписывать уже существующий объект.
		:type force: bool
		"""
		
		if key not in self.__Objects or force: self.__Objects[key] = object

	def check_flags(self, flags: Iterable[str] | str) -> bool:
		"""
		Проверяет, активированы ли для пользователя указанные флаги.

		:param flags: Один или несколько флагов.
		:type flags: Iterable[str] | str
		:return: Возвращает `True`, если все флаги активированы.
		:rtype: bool
		"""

		flags = ToIterable(flags)

		for Flag in flags:
			if Flag not in self.__Data["flags"]: return False

		return True

	def clear_temp_properties(self):
		"""Очищает временные свойства пользователя."""

		self.__Data["temp"] = dict()
		self.save()		

	def get_object(self, key: str) -> Any:
		"""
		Возвращает объект, прикреплённый к пользователю.

		:param key: Ключ объекта.
		:type key: str
		:raise KeyError: Выбрасывается при отсутствии объекта с переданным ключом.
		:return: Прикреплённый объект.
		:rtype: Any
		"""

		return self.__Objects[key]

	def get_property(self, key: str, copy: bool = True) -> Any:
		"""
		Возвращает значение свойства пользователя. При наличии одинакового ключа в постоянных и временных свойствах, приоритет отдаётся временному.

		:param key: Ключ свойства.
		:type key: str
		:param copy: Указывает, нужно ли создавать копию ссылочных объектов для защиты данных. Не рекомендуется отключать, если свойство будет изменяться.
		:type copy: bool
		:raises KeyError: Выбрасывается при отсутствии свойства с переданным ключом.
		:return: Значение свойства.
		:rtype: Any
		"""

		Data = None

		if key in self.__Data["temp"].keys(): Data = self.__Data["temp"][key]
		else: Data = self.__Data["data"][key]

		# Для изменяемых объектов создание копии через сериализацию (быстрее глубокого копирования).
		if copy and type(Data) in (dict, list): Data = Copy(Data)

		return Data

	def has_permissions(self, permissions: Iterable[str] | str) -> bool:
		"""
		Проверяет, имеет ли пользователь все указанные права.

		:param permissions: Одно или несколько прав.
		:type permissions: Iterable[str] | str
		:return: Возвращает `True`, если пользователь имеет все указанные права.
		:rtype: bool
		"""

		permissions = ToIterable(permissions)

		for Permission in permissions:
			if Permission not in self.__Data["permissions"]: return False

		return True
	
	def has_object(self, key: str) -> bool:
		"""
		Проверяет, прикреплён ли к пользователю объект с переданным ключом.

		:param key: Ключ объекта.
		:type key: str
		:return: Возвращает `True`, если объект с таким ключом найден.
		:rtype: bool
		"""

		return key in self.__Objects.keys()

	def has_property(self, key: str) -> bool:
		"""
		Проверяет, имеется ли у пользователя свойство с указанным ключом.

		:param key: Ключ свойства.
		:type key: str
		:return: Возвращает `True`, если свойство с таким ключом найдено.
		:rtype: bool
		"""

		if key in self.__Data["data"].keys() or key in self.__Data["temp"].keys(): return True

		return False 

	def refresh(self):
		"""
		Считывает данные из файла пользователя и дополняет отсутствующие поля.

		:raise RefreshingBlocked: Выбрасывается при попытке чтения файла пользователя во время подавления сохранений.
		"""

		if self.__SuppressSaving: raise RefreshingBlocked()
		Data = ReadJSON(self.__Path)

		for Key in self.__Data.keys():
			if Key not in Data.keys(): Data[Key] = self.__Data[Key]

		if Data.get("last_activity"): Data["last_activity"] = dateparser.parse(Data["last_activity"]).replace(tzinfo = None)
		
		self.__Data = Data

	def remove_object(self, key: str):
		"""
		Удаляет прикреплённый объект.

		:param key: Ключ объекта.
		:type key: str
		:raise KeyError: Выбрасывается, если объект с указанным ключом не найден.
		"""

		del self.__Objects[key]

	def remove_flags(self, flags: Iterable[str] | str):
		"""
		Удаляет флаги.

		:param flags: Один или несколько флагов.
		:type flags: Iterable[str] | str
		"""

		self.__RemoveFlags(flags, "flags")

	def remove_permissions(self, permissions: Iterable[str] | str):
		"""
		Удаляет права.

		:param permissions: Одно или несколько прав.
		:type permissions: Iterable[str] | str
		"""

		self.__RemoveFlags(permissions, "permissions")

	def remove_property(self, key: str):
		"""
		Удаляет свойство пользователя. При поиске приоритет отдаётся постоянным свойствам, затем поиск осуществляется среди временных.

		:param key: Ключ свойства.
		:type key: str
		"""

		IsChanged = False

		if key in self.__Data["data"].keys():
			del self.__Data["data"][key]
			IsChanged = True

		elif key in self.__Data["temp"].keys():
			del self.__Data["temp"][key]
			IsChanged = True

		if IsChanged: self.save()

	def reset_expected_type(self):
		"""Сбрасывает ожидаемый тип к значению `None`."""

		self.__Data["expected_type"] = None
		self.save()

	def save(self, use_queue: bool = True):
		"""
		Записывает данные пользователя в локальный файл.

		Если значение с момента прошлого сохранения не изменено, сохранение будет пропущено.

		:param use_queue: Указывает, помещать ли задачу в очередь, если доступна, или выполнить сохранение немедленно.
		:type use_queue: bool
		"""

		
		if self.__SuppressSaving or self.__DeltaHash == self.__CalculateHash():
			LOGGER.debug(f"{self} data saving skipped.")
			return
		
		if self.__Manager.is_saving_queue_enabled and use_queue:
			self.__Manager.push_to_saving_queue(self)
			return

		WriteJSON(self.__Path, self.__ToSerializableDict(), pretty = self.__Manager.is_pretty_saving_enabled)
		self.__DeltaHash = self.__CalculateHash()

	def set_chat_forbidden(self, status: bool):
		"""
		Задаёт состояние: может ли бот контактировать с пользователем.

		:param status: Состояние.
		:type status: bool
		"""

		self.__Data["is_chat_forbidden"] = status
		self.save()

	def set_expected_type(self, expected_type: str | enum.Enum | None):
		"""
		Задаёт ожидаемый тип данных.

		:param expected_type: Ожидаемый от пользователя тип данных. При указании элемента перечисления берётся его значение.
		:type expected_type: str | Enum | None
		"""

		if isinstance(expected_type, enum.Enum): self.__Data["expected_type"] = expected_type.value
		else: self.__Data["expected_type"] = expected_type
		self.save()

	def set_property(self, key: str, value: Any, force: bool = True):
		"""
		Задаёт значение свойства пользователя.

		:param key: Ключ свойства.
		:type key: str
		:param value: Значение свойства.
		:type value: Any
		:param force: Указывает, нужно ли перезаписывать уже существующее свойство.
		:type force: bool
		"""
		
		if key not in self.__Data["data"].keys() or force: self.__SetProperty("data", key, value)

	def set_temp_property(self, key: str, value: Any, force: bool = True):
		"""
		Задаёт временное значение свойства пользователя.

		Временные значения могут служить для поэтапного ввода данных или непродолжительного хранения информации. Как правило их следует очищать методом `clear_temp_properties()`.

		:param key: Ключ свойства.
		:type key: str
		:param value: Значение свойства.
		:type value: Any
		:param force: Указывает, нужно ли перезаписывать уже существующее свойство.
		:type force: bool
		"""
		
		if key not in self.__Data["temp"].keys() or force: self.__SetProperty("temp", key, value)

	def suppress_saving(self, status: bool, save_on_disabling: bool = True):
		"""
		Подавляет сохранение в локальный файл.
		
		Следует использовать для оптимизации при множественных изменениях. Во время подавления недоступен вызов метода `refresh()`.

		:param status: Статус подавления.
		:type status: bool
		:param save_on_disabling: Указывает, следует ли выполнить обязательное сохранение после отключения подавления. Игнорируется при включении подавления.
		:type save_on_disabling: bool
		"""

		self.__SuppressSaving = status
		if not status and save_on_disabling: self.save()

	def update(self, user: telebot.types.User, is_chat_forbidden: bool | None = None):
		"""
		Обновляет данные пользователя (язык, наличие подписки, ник) из его структуры Telegram.

		:param user: Объект представления пользователя.
		:type user: telebot.types.User
		:param is_chat_forbidden: Указывает, заблокировал ли пользователь бота.
		:type is_chat_forbidden: bool | None
		:raises IncorrectUserToUpdate: Выбрасывается при передаче несоответствующей по ID структуры пользователя.
		"""

		if user.id != self.__ID: raise IncorrectUserToUpdate(self.__ID, user.id)

		if is_chat_forbidden != None: self.__Data["is_chat_forbidden"] = is_chat_forbidden
		self.__Data["is_premium"] = bool(user.is_premium)
		self.__Data["language"] = user.language_code
		self.__Data["username"] = user.username
		self.save()

	def update_acitivity(self) -> datetime:
		"""
		Обновляет дату и время последней активности пользователя.

		:return: Дата и время последней активности пользователя.
		:rtype: datetime
		"""

		self.__Data["last_activity"] = datetime.now()
		self.save()

class UsersManager:
	"""Менеджер пользователей."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def premium_users(self) -> tuple[UserData]:
		"""Последовательность пользователей с Premium-подпиской из числа хранящихся в памяти."""

		PremiumUsers = list()

		for UserID in self.__Users:
			if self.__Users[UserID].is_premium: PremiumUsers.append(self.__Users[UserID])

		return tuple(PremiumUsers)

	@property
	def storage_directory(self) -> PathLike:
		"""Путь к каталогу файлов пользователей."""

		return self.__StorageDirectory

	@property
	def unloaded_users_id(self) -> tuple[int]:
		"""Последовательность ID выгруженных из памяти пользователей."""

		return tuple(self.__UnloadedUsersID)

	@property
	def users(self) -> tuple[UserData]:
		"""Последовательность хранящихся в памяти пользователей."""

		return tuple(self.__Users.values())

	#==========================================================================================#
	# >>>>> ЛОГИЧЕСКИЕ ПЕРЕКЛЮЧАТЕЛИ <<<<< #
	#==========================================================================================#

	@property
	def is_pretty_saving_enabled(self) -> bool:
		"""Состояние: форматировать ли локальные файлы отступами."""

		return self.__IsPrettySaving
	
	@property
	def is_saving_queue_enabled(self) -> bool:
		"""Состояние: используется ли очередь сохранений."""

		return self.__IsSavingQueue

	#==========================================================================================#
	# >>>>> ПРИВАТНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __LoadUsers(self, users_id: Iterable[int]):
		"""
		Загружает данные пользователей для списка ID.

		:param users_id: Последовательность ID пользователей.
		:type users_id: Iterable[int]
		"""

		for UserID in users_id: self.__Users[UserID] = UserData(self, UserID)

	def __SavingQueueProcessor(self):
		"""Реализация очереди сохранений."""

		LOGGER.debug("Saving queue started. Tasks: " + str(len(self.__SavingQueue)) + ".")

		while self.__SavingQueue:
			UserID = self.__SavingQueue[0]
			User = self.get_user(UserID)
			User.save(use_queue = False)
			self.__SavingQueue.pop(0)

		self.__SavingQueueThread = None
		LOGGER.debug("Saving queue stopped.")

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, storage_directory: PathLike, threads: int = 1):
		"""
		Менеджер пользователей.

		:param storage_directory: Путь к каталог файлов пользователей. Директория создаётся автоматически.
		:type storage_directory: PathLike
		:param threads: Число потоков, использующихся для операций чтения при инициализации менеджера. По умолчанию 1.
		:type threads: int
		"""

		self.__StorageDirectory = NormalizePath(storage_directory)

		self.__Users: dict[int, UserData] = dict()

		self.__IsPrettySaving = True
		self.__IsSavingQueue = False

		self.__SavingQueue: list[int] = list()
		self.__SavingQueueThread = None

		self.__Scheduler: BackgroundScheduler | None = None
		self.__UnloaderTaskID: int | None = None
		self.__UnloadedUsersID: list[int] = list()

		if not os.path.exists(self.__StorageDirectory): os.makedirs(self.__StorageDirectory)
		self.reload_users(threads)

	def __getitem__(self, user_id: int) -> UserData:
		"""
		Возвращает данные пользователя.

		:param user_id: ID пользователя.
		:type user_id: int
		:raise KeyError: Выбрасывается при отсутствии данных для пользователя с указанным ID.
		:return: Данные пользователя.
		:rtype: UserData
		"""

		return self.get_user(user_id)

	def auth(self, user: telebot.types.User, update_activity: bool = True) -> UserData:
		"""
		Выполняет авторизацию пользователя в системе.

		:param user: Структуры данных пользователя Telegram.
		:type user: telebot.types.User
		:param update_activity: Указывает, нужно ли обновить дату и время последней активности пользователя.
		:type update_activity: bool
		:raises TypeError: Выбрасывается при передаче неверного типа структуры данных пользователя.
		:return: Данные пользователя.
		:rtype: UserData
		"""
		
		if type(user) != telebot.types.User: raise TypeError(f"telebot.types.User object expected, not {type(user)}.")

		if user.id not in self.__Users: self.__Users[user.id] = UserData(self, user.id)
		CurrentUser = self.__Users[user.id]
		CurrentUser.update(user)
		if CurrentUser.is_chat_forbidden: CurrentUser.set_chat_forbidden(False)
		if update_activity: CurrentUser.update_acitivity()

		return CurrentUser

	def delete_user(self, user_id: int):
		"""
		Удаляет данные пользователя.

		:param user_id: ID пользователя.
		:type user_id: int
		:raises KeyError: Выбрасывается при отсутствии пользователя с переданным ID.
		"""

		del self.__Users[user_id]
		os.remove(f"{self.__StorageDirectory}/{user_id}.json")

	def get_active_users(self, hours: int = 24) -> tuple[UserData]:
		"""
		Возвращает последовательность пользователей, для которых активных за последние N часов.

		:param hours: Количество часов для проверки активности. По умолчанию 24.
		:type hours: int
		:return: Последовательность данных пользователей.
		:rtype: tuple[UserData]
		"""

		Now = datetime.now()
		Delta = timedelta(hours = hours)
		Users = [UserObject for UserObject in self.__Users.values() if UserObject.last_activity and Now - UserObject.last_activity <= Delta]

		return tuple(Users)

	def get_user(self, user_id: int) -> UserData:
		"""
		Возвращает данные пользователя.

		:param user_id: ID пользователя.
		:type user_id: int
		:raise KeyError: Выбрасывается при отсутствии данных для пользователя с указанным ID.
		:return: Данные пользователя.
		:rtype: UserData
		"""

		if user_id not in self.__Users: 
			UserPath = f"{self.__StorageDirectory}/{user_id}.json"
			if not os.path.exists(UserPath): raise KeyError(f"User with ID {user_id} not exists.")
			self.__Users[user_id] = UserData(self, user_id)

		return self.__Users[user_id]
	
	def is_user_exists(self, user_id: int) -> bool:
		"""
		Проверяет, зарегестрирован ли пользователь в системе.

		:param user_id: ID пользователя.
		:type user_id: int
		:return: Возвращает `True`, если данные пользователя обнаружены.
		:rtype: bool
		"""

		return user_id in self.__Users or user_id in self.__UnloadedUsersID

	def push_to_saving_queue(self, user: UserData):
		"""
		Добавляет данные пользователя в очередь на сохранение.

		:param user: Данные пользователя.
		:type user: UserData
		:raise SavingQueueBlocked: Выбрасывается при отключённой очереди сохранений.
		"""

		if not self.__IsSavingQueue: raise SavingQueueBlocked()

		if user.id not in self.__SavingQueue:
			self.__SavingQueue.append(user.id)
			
			if not self.__SavingQueueThread or not self.__SavingQueueThread.is_alive():
				self.__SavingQueueThread = Thread(target = self.__SavingQueueProcessor, name = "Users manager saving queue.")
				self.__SavingQueueThread.start()

	def reload_users(self, threads: int = 1):
		"""
		Загружает данные пользователей из локальных файлов.
		
		Вызывается автоматически при инициализации менеджера. Повторный вызов без реализации механизмов защиты может привести к потере данных.

		:param threads: Число потоков, использующихся для операций чтения. По умолчанию 1.
		:type threads: int
		"""

		Files = ListDir(self.__StorageDirectory)
		Files = tuple(filter(lambda List: List.endswith(".json"), Files))
		UsersID = tuple(int(File[:-5]) for File in Files)
		Segments = tuple(tuple(Element) for Element in divide(threads, UsersID))
		self.__Users = dict()
		with ThreadPoolExecutor(max_workers = threads) as Executor: Executor.map(self.__LoadUsers, Segments)
		self.__UnloadedUsersID = list()

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ ВЫГРУЗКИ ПОЛЬЗОВАТЕЛЕЙ <<<<< #
	#==========================================================================================#

	def restore_unloaded_users(self):
		"""Заново загружает в память ранее выгруженные данные неактивных пользователей."""

		self.__LoadUsers(self.__UnloadedUsersID)
		self.__UnloadedUsersID = list()

	def start_unloader(self, interval: int, days: int):
		"""
		Запускает фоновую задачу по периодической выгрузке неактивных пользователей из памяти.

		:param interval: Интервал в часах для срабатывания выгрузки.
		:type interval: int
		:param days: Количество дней отсутствия активности.
		:type days: int
		"""

		if not self.__Scheduler:
			self.__Scheduler = BackgroundScheduler()
			self.__Scheduler.start()

		self.__UnloaderTaskID = self.__Scheduler.add_job(self.unload_users, args = (days,), trigger = "interval", hours = interval).id

	def stop_unloader(self):
		"""Останавливает фоновую задачу по периодической выгрузке неактивных пользователей из памяти."""

		if not self.__Scheduler: return 
		self.__Scheduler.remove_job(self.__UnloaderTaskID)
		self.__Scheduler = None

	def unload_users(self, days: int) -> tuple[int]:
		"""
		Выгружает из оперативной памяти данные пользователей, чья последняя активность выходит за указанное значение.

		:param days: Количество дней отсутствия активности. Минимум 1.
		:type days: int
		:return: Последовательность ID пользователей, для которых были выгружены данные.
		:rtype: tuple[int]
		:raise ValueError: Выбрасывается при неверной спецификации количества дней.
		"""

		if days < 1: raise ValueError("Days must be more than 1.")
		InactiveUsers = tuple(set(self.users) - set(self.get_active_users(hours = 24 * days)))

		for User in InactiveUsers:

			if User.objects:
				ObjectsCount = len(User.objects)
				LOGGER.debug(f"While unloading {User} unnatached {ObjectsCount} objects.")

			if User.is_saving_suppressed: LOGGER.warning(f"For unloaded {User} saving suppressed. Data may be loss.")

			User.save()
			del self.__Users[User.id]

		CurrentUnloadedUsersID = tuple(User.id for User in InactiveUsers)
		self.__UnloadedUsersID.extend(CurrentUnloadedUsersID)

		return CurrentUnloadedUsersID

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ НАСТРОЙКИ <<<<< #
	#==========================================================================================#

	def enable_pretty_saving(self, status: bool):
		"""
		Переключает форматирование локальных файлов с использованием отступов. Отключение может значительно ускорить операции записи.

		:param status: Состояние форматирования.
		:type status: bool
		"""

		self.__IsPrettySaving = status

	def enable_saving_queue(self, status: bool):
		"""
		Переключает использование очереди сохранений.

		:param status: Состояние использование очереди.
		:type status: bool
		"""

		self.__IsSavingQueue = status

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ МАССОВОГО РЕДАКТИРОВАНИЯ ПОЛЬЗОВАТЕЛЕЙ <<<<< #
	#==========================================================================================#

	def add_flags(self, flags: Iterable[str] | str):
		"""
		Добавляет флаги для всех пользователей.

		:param flags: Один или несколько флагов.
		:type flags: Iterable[str] | str
		"""

		for User in self.__Users.values(): User.add_flags(flags)

	def clear_temp_properties(self):
		"""Очищает временные свойства всех пользователей."""

		for User in self.__Users.values(): User.clear_temp_properties()

	def remove_flags(self, flags: Iterable[str] | str):
		"""
		Удаляет флаги у всех пользователей.

		:param flags: Один или несколько флагов.
		:type flags: Iterable[str] | str
		"""

		for User in self.__Users.values(): User.remove_flags(flags)

	def remove_permissions(self, permissions: list[str] | str):
		"""
		Удаляет права у всех пользователей.

		:param permissions: Одно или несколько прав.
		:type permissions: Iterable[str] | str
		"""

		for User in self.__Users.values(): User.remove_permissions(permissions)

	def remove_property(self, key: str):
		"""
		Удаляет свойство у всех пользователей.

		:param key: Ключ свойства.
		:type key: str
		"""

		for User in self.__Users.values(): User.remove_property(key)

	def set_property(self, key: str, value: Any, force: bool = True):
		"""
		Задаёт свойство для всех пользователей.

		:param key: Ключ свойства.
		:type key: str
		:param value: Значение свойства.
		:type value: Any
		:param force: Указывает, нужно ли перезаписывать уже существующее свойство.
		:type force: bool
		"""

		for User in self.__Users.values(): User.set_property(key, value, force)