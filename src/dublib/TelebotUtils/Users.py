from ..Methods.Filesystem import ListDir, NormalizePath, ReadJSON, WriteJSON
from ..Methods.Data import Copy, ToIterable
from ..Exceptions.TelebotUtils import *

from typing import Any, Iterable, Literal
from datetime import datetime, timedelta
from os import PathLike
import os

import dateparser
import telebot

#==========================================================================================#
# >>>>> УПРАВЛЕНИЕ ПОЛЬЗОВАТЕЛЯМИ <<<<< #
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
	def path(self) -> PathLike:
		"""Путь к файлу пользователя."""

		return self.__Path

	@property
	def permissions(self) -> tuple[str]:
		"""Список прав пользователя."""

		return tuple(self.__Data["permissions"])

	@property
	def username(self) -> str:
		"""Ник пользователя."""

		return self.__Data["username"]

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

		if not os.path.exists(self.__Path): self.save()
		else: self.refresh()

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
		
		if key not in self.__Objects.keys() or force: self.__Objects[key] = object

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
		"""Считывает данные из файла пользователя и дополняет отсутствующие поля."""

		Data = ReadJSON(self.__Path)

		for Key in self.__Data.keys():
			if Key not in Data.keys(): Data[Key] = self.__Data[Key]

		if Data["last_activity"]: Data["last_activity"] = dateparser.parse(Data["last_activity"]).replace(tzinfo = None)
		else: self.update_acitivity()
		
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

	def save(self):
		"""Записывает данные пользователя в локальный файл."""

		Data = self.__Data.copy()
		Data["last_activity"] = str(Data["last_activity"])
		WriteJSON(self.__Path, Data)

	def set_chat_forbidden(self, status: bool):
		"""
		Задаёт состояние: может ли бот контактировать с пользователем.

		:param status: Состояние.
		:type status: bool
		"""

		self.__Data["is_chat_forbidden"] = status
		self.save()

	def set_expected_type(self, type_name: str | None):
		"""
		Задаёт название ожидаемого типа данных.

		:param type_name: Название ожидаемого от пользователя типа данных.
		:type type_name: str | None
		"""

		self.__Data["expected_type"] = type_name
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

	def update(self, user: telebot.types.User, is_chat_forbidden: bool | None = None):
		"""
		Обновляет данные пользователя (язык, наличие подписки, ник) из его структуры Telegram.
			user – объект представления пользователя;\n
			is_chat_forbidden – указывает, заблокировал ли пользователь бота.

		:param user: Структура данных пользователя Telegram.
		:type user: telebot.types.User
		:param is_chat_forbidden: Состояние: может ли бот контактировать с пользователем. Если указать `None`, обновление состояния не произойдёт.
		:type is_chat_forbidden: bool | None
		:raises IncorrectUserToUpdate: Выбрасывается при передаче несоответствующей по ID структуры.
		"""

		if user.id == self.__ID:
			if is_chat_forbidden != None: self.__Data["is_chat_forbidden"] = is_chat_forbidden
			self.__Data["is_premium"] = bool(user.is_premium)
			self.__Data["language"] = user.language_code
			self.__Data["username"] = user.username
			self.save()

		else: raise IncorrectUserToUpdate()

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
	def active_users(self) -> tuple[UserData]:
		"""Последовательность активных за последние 24 часа пользователей."""

		return self.get_active_users()

	@property
	def premium_users(self) -> tuple[UserData]:
		"""Последовательность пользователей с Premium-подпиской."""

		PremiumUsers = list()

		for UserID in self.__Users:
			if self.__Users[UserID].is_premium: PremiumUsers.append(self.__Users[UserID])

		return tuple(PremiumUsers)

	@property
	def storage_directory(self) -> PathLike:
		"""Путь к каталогу файлов пользователей."""

		return self.__StorageDirectory

	@property
	def users(self) -> tuple[UserData]:
		"""Последовательность всех пользователей."""

		return tuple(self.__Users.values())

	#==========================================================================================#
	# >>>>> ПРИВАТНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __LoadUsers(self):
		"""Загружает данные пользователей."""

		Files = ListDir(self.__StorageDirectory)
		Files = list(filter(lambda List: List.endswith(".json"), Files))

		for File in Files:
			UserID = int(File.replace(".json", ""))
			self.__Users[UserID] = UserData(self, UserID)

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, storage_directory: PathLike):
		"""
		Менеджер пользователей.

		:param storage_directory: Путь к каталог файлов пользователей. Директория создаётся автоматически.
		:type storage_directory: PathLike
		"""

		self.__StorageDirectory = NormalizePath(storage_directory)

		self.__Users: dict[int, UserData] = dict()

		if not os.path.exists(self.__StorageDirectory): os.makedirs(self.__StorageDirectory)
		self.__LoadUsers()

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
		:raises ValueError: Выбрасывается при передаче неверного типа структуры данных пользователя.
		:return: Данные пользователя.
		:rtype: UserData
		"""
		
		if type(user) != telebot.types.User: raise ValueError(f"telebot.types.User object expected, not {type(user)}.")

		if user.id not in self.__Users.keys():self.__Users[user.id] = UserData(self, user.id)
		self.__Users[user.id].update(user)
		CurrentUser = self.__Users[user.id]
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
		
		return self.__Users[user_id]

	def get_users(
			self,
			last_activity: int | None = None,
			premium: bool | None = None,
			include_permissions: Iterable[str] | str | None = None,
			exclude_permissions: Iterable[str] | str | None = None
		) -> tuple[UserData]:
		"""
		Возвращает последовательность пользователей, удовлетворяющих переданным фильтрам. При передаче `None` фильтр игнорируется.

		:param last_activity: Количество часов для проверки активности.
		:type last_activity: int | None
		:param premium: Состояние Premium-подписки пользователя.
		:type premium: bool | None
		:param include_permissions: Набор прав или право, которое должно иметься.
		:type include_permissions: Iterable[str] | str | None
		:param exclude_permissions: Набор прав или право, которого быть не должно.
		:type exclude_permissions: Iterable[str] | str | None
		:return: Последовательность данных пользователей.
		:rtype: tuple[UserData]
		"""

		Users = self.users
		if last_activity: Users = self.get_active_users(last_activity)

		if premium != None:
			Buffer = list()

			for User in Users: 
				if User.is_premium == premium: Buffer.append(User)

			Users = Buffer

		if include_permissions:
			Buffer = list()

			for User in Users: 
				if User.has_permissions(include_permissions): Buffer.append(User)

			Users = Buffer

		if exclude_permissions:
			Buffer = list()

			for User in Users: 
				if not User.has_permissions(exclude_permissions): Buffer.append(User)

			Users = Buffer

		return tuple(Users)
	
	def is_user_exists(self, user_id: int) -> bool:
		"""
		Проверяет, зарегестрирован ли пользователь в системе.

		:param user_id: ID пользователя.
		:type user_id: int
		:return: Возвращает `True`, если данные пользователя обнаружены.
		:rtype: bool
		"""

		return user_id in self.__Users.keys()

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