from ..Methods.Filesystem import ListDir, NormalizePath, ReadJSON, WriteJSON
from ..Exceptions.TelebotUtils import *

from datetime import datetime, timedelta
from typing import Any
import os

from telebot.types import User
import dateparser

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
	def is_chat_forbidden(self) -> bool | None:
		"""Состояние: запретил ли пользователь бота."""
		
		if "is_chat_forbidden" in self.__Data.keys(): return self.__Data["is_chat_forbidden"]

		return None

	@property
	def is_premium(self) -> bool:
		"""Состояние: есть ли Premium-подписка у пользователя."""

		return self.__Data["is_premium"]

	@property
	def language(self) -> str:
		"""Код используемого клиентом языка по стандарту ISO 639-1."""

		return self.__Data["language"]

	@property
	def permissions(self) -> tuple[str]:
		"""Список прав доступа пользователя."""

		return tuple(self.__Data["permissions"])

	@property
	def username(self) -> str:
		"""Ник пользователя."""

		return self.__Data["username"]

	#==========================================================================================#
	# >>>>> ПРИВАТНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __AddFlags(self, flags: list[str] | str, key: str):
		"""
		Добавляет флаги по указанному ключу словаря данных пользователя.
			flags – набор флагов;\n
			key – ключ для помещения флагов.
		"""

		if type(flags) == str: flags = (flags,)
		IsChanged = False

		for Flag in flags:

			if Flag not in self.__Data[key]:
				self.__Data[key].append(Flag)
				IsChanged = True

		if IsChanged: self.__Data[key] = sorted(self.__Data[key])
		self.save()

	def __RemoveFlags(self, flags: list[str] | str, key: str):
		"""
		Убирает флаги по указанному ключу словаря данных пользователя.
			flags – набор флагов;\n
			key – ключ для помещения флагов.
		"""

		if type(flags) == str: flags = (flags,)

		for Flag in flags:
			if Flag in self.__Data[key]: self.__Data[key].remove(Flag)

		self.save()

	def __SetProperty(self, property_type: str, key: str, value: Any):
		"""
		Задаёт свойство пользователя.
			property_type – ключ раздела хранения свойства;\n
			key – ключ свойства;\n
			value – значение.
		"""

		self.__Data[property_type][key] = value
		self.save()

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, storage_dir: str, user_id: int, data: dict | None = None):
		"""
		Объектное представление данных пользователя.
			storage_dir – путь к директории хранения данных;\n
			user_id – ID пользователя.
		"""

		#---> Генерация динамических атрибутов.
		#==========================================================================================#
		self.__StorageDirectory = storage_dir.replace("\\", "/").rstrip("/")
		self.__ID = user_id
		self.__Data = {
			"username": None,
			"language": None,
			"is_chat_forbidden": None,
			"is_premium": None,
			"expected_type": None,
			"permissions": [],
			"last_activity": None,
			"flags": [],
			"data": {},
			"temp": {}
		}

		self.__Objects = dict()
		self.__Path = self.__StorageDirectory + f"/{user_id}.json"

		if not os.path.exists(self.__Path): self.save()
		else: self.refresh()

	def add_flags(self, flags: list[str] | str):
		"""
		Устанавливает флаги для пользователя.
			flags – флаги.
		"""

		self.__AddFlags(flags, "flags")

	def add_permissions(self, permissions: list[str] | str):
		"""
		Задаёт разрешения.
			permissions – разрешения.
		"""

		self.__AddFlags(permissions, "permissions")

	def check_flags(self, flags: list[str] | str) -> bool:
		"""
		Возвращает статус активации флагов.
			flags – флаги.
		"""

		if type(flags) == str: flags = (flags,)

		for Flag in flags:
			if Flag not in self.__Data["flags"]: return False

		return True

	def clear_temp_properties(self):
		"""Очищает временные свойства пользователя."""

		self.__Data["temp"] = dict()
		self.save()		

	def delete(self):
		"""Удаляет локальный файл пользователя."""

		os.remove(self.__StorageDirectory + f"/{self.__ID}.json")

	def get_object(self, key: str) -> Any:
		"""
		Возвращает объект Python из свойств пользователя.
			key – ключ объекта.
		"""

		return self.__Objects[key]

	def get_property(self, key: str) -> Any:
		"""
		Возвращает значение свойства пользователя, в том числе временного.
			key – ключ свойства.
		"""

		if key in self.__Data["data"].keys(): return self.__Data["data"][key]
		if key in self.__Data["temp"].keys(): return self.__Data["temp"][key]

		raise KeyError(key)
	
	def get_property_type(self, key: str) -> Any:
		"""
		Возвращает значение типа свойства пользователя, в том числе временного.
			key – ключ свойства.
		"""

		if key in self.__Data["data"].keys(): return type(self.__Data["data"][key])
		if key in self.__Data["temp"].keys(): return type(self.__Data["temp"][key])

		raise KeyError(key)

	def has_permissions(self, permissions: list[str] | str) -> bool:
		"""
		Проверяет, имеет ли пользователь все перечисленные разрешения.
			permissions – разрешения.
		"""

		if type(permissions) == str: permissions = [permissions]
		IsOwned = True

		for Permission in permissions:

			if Permission not in self.__Data["permissions"]: IsOwned = False

		return IsOwned
	
	def has_object(self, key: str) -> bool:
		"""
		Проверяет, прикреплён ли к пользователю объект с таким ключом.
			key – ключ объекта.
		"""

		return key in self.__Objects.keys()

	def has_property(self, key: str) -> bool:
		"""
		Проверяет, имеет ли пользователь свойство с таким ключом.
			key – ключ свойства.
		"""

		IsExists = False
		if key in self.__Data["data"].keys() or key in self.__Data["temp"].keys(): IsExists = True

		return IsExists

	def refresh(self):
		"""Считывает данные из файла пользователя и дополняет отсутствующие поля."""

		Data = ReadJSON(self.__Path)

		for Key in self.__Data.keys():
			if Key not in Data.keys(): Data[Key] = self.__Data[Key]

		if Data["last_activity"]: Data["last_activity"] = dateparser.parse(Data["last_activity"])

		self.__Data = Data

	def remove_object(self, key: str):
		"""
		Удаляет привязанный к пользователю объект.
			key – ключ объекта.
		"""

		del self.__Objects[key]

	def remove_flags(self, flags: list[str] | str):
		"""
		Удаляет флаги.
			flags – флаги.
		"""

		self.__RemoveFlags(flags, "flags")

	def remove_permissions(self, permissions: list[str] | str):
		"""
		Удаляет разрешения.
			permissions – разрешения.
		"""

		self.__RemoveFlags(permissions, "permissions")

	def remove_property(self, key: str):
		"""
		Удаляет свойство пользователя.
			key – ключ свойства.
		"""

		if key in self.__Data["data"].keys(): del self.__Data["data"][key]
		elif key in self.__Data["temp"].keys(): del self.__Data["temp"][key]
		else: KeyError(key)

		self.save()

	def save(self):
		"""Записывает данные пользователя в локальный файл."""

		Data = self.__Data.copy()
		Data["last_activity"] = str(Data["last_activity"])
		WriteJSON(self.__Path, Data)

	def set_chat_forbidden(self, status: bool):
		"""
		Задаёт ожидаемый от пользователя тип данных.
			status – состояние.
		"""

		self.__Data["is_chat_forbidden"] = status
		self.save()

	def set_expected_type(self, type_name: str | None):
		"""
		Задаёт ожидаемый от пользователя тип данных.
			type_name – название типа.
		"""

		self.__Data["expected_type"] = type_name
		self.save()

	def set_object(self, key: str, object: Any):
		"""
		Сохраняет объект Python в оперативной памяти и привязывает его к текущему пользователю наподобие свойства.
			key – ключ объекта;\n
			object – объект.
		"""
		
		if key not in self.__Objects.keys(): self.__Objects[key] = object

	def set_property(self, key: str, value: Any, force: bool = True):
		"""
		Задаёт значение свойства пользователя.
			key – ключ свойства;\n
			value – значение;\n
			force – указывает, необходимо ли перезаписывать значение уже существующего ключа.
		"""
		
		if key not in self.__Data["data"].keys(): self.__SetProperty("data", key, value)
		elif key in self.__Data["data"].keys() and force: self.__SetProperty("data", key, value)

	def set_temp_property(self, key: str, value: Any):
		"""
		Задаёт значение временного свойства пользователя.
			key – ключ свойства;\n
			value – значение.
		"""
		
		self.__SetProperty("temp", key, value)

	def update(self, user: User, is_chat_forbidden: bool | None = None):
		"""
		Обновляет данные пользователя (язык, Premium подписка, ник, запрещён ли чат) из его структуры.
			user – объект представления пользователя;\n
			is_chat_forbidden – указывает, заблокировал ли пользователь бота.
		"""

		if user.id == self.__ID:
			if is_chat_forbidden != None: self.__Data["is_chat_forbidden"] = is_chat_forbidden
			self.__Data["is_premium"] = bool(user.is_premium)
			self.__Data["language"] = user.language_code
			self.__Data["username"] = user.username
			self.save()

		else: raise IncorrectUserToUpdate()

	def update_acitivity(self) -> datetime:
		"""Обновляет дату последней активности пользователя."""

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
		"""Список пользователей с Premium подпиской."""

		PremiumUsers = list()

		for UserID in self.__Users:
			if self.__Users[UserID].is_premium: PremiumUsers.append(self.__Users[UserID])

		return tuple(PremiumUsers)

	@property
	def users(self) -> tuple[UserData]:
		"""Список пользователей."""

		Users = list()
		for UserID in self.__Users.keys(): Users.append(self.__Users[UserID])

		return tuple(Users)

	#==========================================================================================#
	# >>>>> ПРИВАТНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __LoadUsers(self):
		"""Загружает данные пользователей."""

		Files = ListDir(self.__StorageDirectory)
		Files = list(filter(lambda List: List.endswith(".json"), Files))

		for File in Files:
			UserID = int(File.replace(".json", ""))
			self.__Users[UserID] = UserData(self.__StorageDirectory, UserID)

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, directory: str):
		"""
		Менеджер пользователей.
			dir – путь к директории хранения данных.
		"""

		#---> Генерация динамических атрибутов.
		#==========================================================================================#
		self.__Users: dict[int, UserData] = dict()
		self.__StorageDirectory = NormalizePath(directory)

		if not os.path.exists(self.__StorageDirectory): os.makedirs(self.__StorageDirectory)
		self.__LoadUsers()

		#---> Генерация динамических атрибутов.
		#==========================================================================================#
		self.__Users: dict[int, UserData] = dict()
		self.__StorageDirectory = NormalizePath(directory)

		if not os.path.exists(self.__StorageDirectory): os.makedirs(self.__StorageDirectory)
		self.__LoadUsers()

	def __getitem__(self, user_id: int) -> UserData:
		"""
		Возвращает объект данных пользователя.
			user_id – ID пользователя.
		"""

		return self.get_user(user_id)

	def auth(self, user: User, update_activity: bool = True) -> UserData:
		"""
		Выполняет идентификацию и обновление данных существующего пользователя или создаёт локальный файл для нового.
			user – структура описания пользователя Telegram;\n
			update_activity – указывает, нужно ли обновлять активность пользователя.
		"""
		
		if type(user) != User: raise ValueError("User object expected, not " + str(type(user)) + ".")
		CurrentUser = None
		if user.id not in self.__Users.keys():self.__Users[user.id] = UserData(self.__StorageDirectory, user.id, user)
		self.__Users[user.id].update(user)
		CurrentUser = self.__Users[user.id]
		if CurrentUser.is_chat_forbidden: CurrentUser.set_chat_forbidden(False)
		if update_activity: CurrentUser.update_acitivity()

		return CurrentUser

	def delete_user(self, user_id: int | str):
		"""
		Удаляет пользователя из системы.
			user_id – ID пользователя.
		"""

		user_id = int(user_id)
		self.__Users[user_id].delete()
		del self.__Users[user_id]

	def get_active_users(self, hours: int = 24) -> tuple[UserData]:
		"""
		Возвращает последовательность пользователей, для которых обнавлялась активность за последние N часов.
			hours – количество часов.
		"""

		Now = datetime.now()
		Delta = timedelta(hours = hours)
		Users = [UserObject for UserObject in self.__Users.values() if UserObject.last_activity and Now - UserObject.last_activity <= Delta]

		return tuple(Users)

	def get_user(self, user_id: int | str) -> UserData:
		"""
		Возвращает объект данных пользователя.
			user_id – ID пользователя.
		"""
		
		return self.__Users[int(user_id)]

	def get_users(self, include_permissions: list[str] | str | None = None, exclude_permissions: list[str] | str | None = None) -> list[UserData]:
		"""
		Возвращает список пользователей, подходящих под переданные фильтры. По умолчанию возвращает список всех пользователей.
			include_permissions – разрешения, которыми должен обладать пользователь;\n
			exclude_permissions – разрешения, которых у пользователя быть не должно.
		"""

		Users = self.users

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

		return Users
	
	def is_user_exists(self, user_id: int) -> bool:
		"""
		Проверяет наличие пользователя с переданным идентификатором в базе данных.
			user_id – ID пользователя.
		"""

		return user_id in self.__Users.keys()

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ МАССОВОГО РЕДАКТИРОВАНИЯ ПОЛЬЗОВАТЕЛЕЙ <<<<< #
	#==========================================================================================#

	def add_flags(self, flags: list[str] | str):
		"""
		Добавляет флаги для всех пользователей.
			flags – флаги.
		"""

		for User in self.__Users.values(): User.add_flags(flags)

	def clear_temp_properties(self):
		"""Очищает временные свойства всех пользователей."""

		for User in self.__Users.values(): User.clear_temp_properties()

	def remove_flags(self, flags: list[str] | str):
		"""
		Удаляет флаги у всех пользователей.
			flags – флаги.
		"""

		for User in self.__Users.values(): User.remove_flags(flags)

	def remove_permissions(self, permissions: list[str] | str):
		"""
		Удаляет разрешения у всех пользователей.
			permissions – разрешения.
		"""

		for User in self.__Users.values(): User.remove_permissions(permissions)

	def remove_property(self, key: str):
		"""
		Удаляет свойство для всех пользователей.
			key – ключ свойства.
		"""

		for User in self.__Users.values(): User.set_property(key)

	def set_property(self, key: str, value: Any, force: bool = True):
		"""
		Задаёт значение свойства для всех пользователей.
			key – ключ свойства;\n
			value – значение;\n
			force – указывает, необходимо ли перезаписывать значение уже существующего ключа.
		"""

		for User in self.__Users.values(): User.set_property(key, value, force)