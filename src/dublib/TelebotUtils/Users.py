from ..Methods.Filesystem import ListDir, NormalizePath, ReadJSON, WriteJSON
from ..Exceptions.TelebotUtils import *

from telebot.types import User
from typing import Any

import os

#==========================================================================================#
# >>>>> УПРАВЛЕНИЕ ПОЛЬЗОВАТЕЛЯМИ <<<<< #
#==========================================================================================#

class UserData:
	"""Объектное представление данных пользователя."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

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
		self.__SaveData()

	def __ReadData(self) -> dict:
		"""Считывает данные из файла пользователя и дополняет отсутствующие поля."""

		Data = ReadJSON(self.__Path)

		for Key in self.__Data.keys():
			if Key not in Data.keys(): Data[Key] = self.__Data[Key]

		return Data

	def __RemoveFlags(self, flags: list[str] | str, key: str):
		"""
		Убирает флаги по указанному ключу словаря данных пользователя.
			flags – набор флагов;\n
			key – ключ для помещения флагов.
		"""

		if type(flags) == str: flags = (flags,)

		for Flag in flags:
			if Flag in self.__Data[key]: self.__Data[key].remove(Flag)

		self.__SaveData()

	def __SaveData(self):
		"""Записывает данные в локальный файл."""

		WriteJSON(self.__Path, self.__Data)

	def __SetProperty(self, property_type: str, key: str, value: Any):
		"""
		Задаёт свойство пользователя.
			property_type – ключ раздела хранения свойства;\n
			key – ключ свойства;\n
			value – значение.
		"""

		self.__Data[property_type][key] = value
		self.__SaveData()

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, storage_dir: str, user_id: int, data: dict | None = None):
		"""
		Объектное представление данных пользователя.
			storage_dir – путь к директории хранения данных;\n
			user_id – ID пользователя;\n
			data – словарь с описанием данных пользователя для инициализации (если не передан, данные будут загружены из файла).
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
			"flags": [],
			"data": {},
			"temp": {}
		}

		self.__Objects = dict()
		self.__Path = self.__StorageDirectory + f"/{user_id}.json"

		if type(data) == dict: self.__Data = data
		elif type(data) == User: self.update(data)
		elif os.path.exists(self.__Path): self.__Data = self.__ReadData()
		else: self.__SaveData()

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
		self.__SaveData()		

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
	
	def has_property(self, key: str) -> bool:
		"""
		Проверяет, имеет ли пользователь свойство с таким ключом.
			key – ключ свойства.
		"""

		IsExists = False
		if key in self.__Data["data"].keys() or key in self.__Data["temp"].keys(): IsExists = True

		return IsExists

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

		self.__SaveData()

	def set_chat_forbidden(self, status: bool):
		"""
		Задаёт ожидаемый от пользователя тип данных.
			status – состояние.
		"""

		self.__Data["is_chat_forbidden"] = status
		self.__SaveData()

	def set_expected_type(self, type_name: str | None):
		"""
		Задаёт ожидаемый от пользователя тип данных.
			type_name – название типа.
		"""

		self.__Data["expected_type"] = type_name
		self.__SaveData()

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
		Обновляет данные пользователя из параметров, содержащихся в сообщении.
			user – объект представления пользователя;\n
			is_chat_forbidden – указывает, заблокировал ли пользователь бота.
		"""

		if user.id == self.__ID:
			if is_chat_forbidden != None: self.__Data["is_chat_forbidden"] = is_chat_forbidden
			self.__Data["is_premium"] = bool(user.is_premium)
			self.__Data["language"] = user.language_code
			self.__Data["username"] = user.username
			self.__SaveData()

		else: raise IncorrectUserToUpdate()

class UsersManager:
	"""Менеджер пользователей."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def premium_users(self) -> list[UserData]:
		"""Список пользователей с Premium подпиской."""

		PremiumUsers = list()

		for UserID in self.__Users:
			if self.__Users[UserID].is_premium: PremiumUsers.append(self.__Users[UserID])

		return PremiumUsers

	@property
	def users(self) -> list[UserData]:
		"""Список пользователей."""

		Users = list()
		for UserID in self.__Users.keys(): Users.append(self.__Users[UserID])

		return Users

	#==========================================================================================#
	# >>>>> ПРИВАТНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __LoadUsers(self):
		"""Загружает данные пользователей."""

		Files = ListDir(self.__StorageDirectory)
		Files = list(filter(lambda List: List.endswith(".json"), Files))

		for File in Files:
			Buffer = ReadJSON(self.__StorageDirectory + f"/{File}")
			UserID = int(File.replace(".json", ""))
			self.__Users[UserID] = UserData(self.__StorageDirectory, UserID, Buffer)

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

	def auth(self, user: User) -> UserData:
		"""
		Выполняет идентификацию и обновление данных существующего пользователя или создаёт локальный файл для нового.
			user – структура описания пользователя Telegram.
		"""
		
		if type(user) != User: raise ValueError("User object expected, not " + str(type(user)) + ".")
		CurrentUser = None
		if user.id not in self.__Users.keys():self.__Users[user.id] = UserData(self.__StorageDirectory, user.id, user)
		self.__Users[user.id].update(user)
		CurrentUser = self.__Users[user.id]
		if CurrentUser.is_chat_forbidden: CurrentUser.set_chat_forbidden(False)

		return CurrentUser

	def delete_user(self, user_id: int | str):
		"""
		Удаляет пользователя из системы.
			user_id – ID пользователя.
		"""

		user_id = int(user_id)
		self.__Users[user_id].delete()
		del self.__Users[user_id]

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
	
	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ МАССОВОГО РЕДАКТИРОВАНИЯ ПОЛЬЗОВАТЕЛЕЙ <<<<< #
	#==========================================================================================#

	def clear_temp_properties(self):
		"""Очищает временные свойства всех пользователей."""

		for User in self.__Users.values(): User.clear_temp_properties()

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

	def set_temp_property(self, key: str, value: Any):
		"""
		Задаёт значение временного свойства для всех пользователей.
			key – ключ свойства;\n
			value – значение.
		"""

		for User in self.__Users.values(): User.set_temp_property(key, value)