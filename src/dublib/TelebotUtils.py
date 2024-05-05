from .Methods import ReadJSON, WriteJSON
from .Exceptions.TelebotUtils import *

from telebot.types import User

import os

#==========================================================================================#
# >>>>> УПРАВЛЕНИЕ ПОЛЬЗОВАТЕЛЯМИ <<<<< #
#==========================================================================================#

class UserData:
	"""Объектное представление данных пользователя."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА ТОЛЬКО ДЛЯ ЧТЕНИЯ <<<<< #
	#==========================================================================================#

	@property
	def id(self) -> int:
		"""ID пользователя."""

		return self.__ID

	@property
	def is_premium(self) -> bool:
		"""Состояние: есть ли Premium-подписка у пользователя."""

		return self.__Data["premium"]

	@property
	def language(self) -> str:
		"""Код используемого клиентом языка по стандарту ISO 639-1."""

		return self.__Data["language"]

	@property
	def permissions(self) -> list:
		"""Список прав доступа пользователя."""

		return self.__Data["permissions"]

	@property
	def username(self) -> str:
		"""Ник пользователя."""

		return self.__Data["username"]

	#==========================================================================================#
	# >>>>> ПРИВАТНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __SaveData(self):
		"""Записывает данные в локальный файл."""

		# Запись локального файла.
		WriteJSON(self.__StorageDirectory + f"/{self.__ID}.json", self.__Data)

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, storage_dir: str, user_id: int, data: dict | None = None):
		"""
		Объектное представление данных пользователя.
			storage_dir – путь к директории хранения данных;
			user_id – ID пользователя;
			data – словарь с описанием данных пользователя для инициализации (если не передан, данные будут загружены из файла).
		"""

		#---> Генерация динамических свойств.
		#==========================================================================================#
		# ID пользователя.
		self.__ID = user_id
		# Директория хранилища.
		self.__StorageDirectory = storage_dir.replace("\\", "/").rstrip("/")
		# Словарное представление данных пользователя.
		self.__Data = {
			"username": None,
			"language": None,
			"is_premium": None,
			"permissions": [],
			"data": {}
		}

		# Если переданы данные в виде словаря.
		if type(data) == dict:
			# Копирование данных.
			self.__Data = data

		# Если переданы данные в виде объекта.
		elif type(data) == User:
			# Обновление данных.
			self.update(data)

		# Если существует локальный файл.
		elif os.path.exists(self.__StorageDirectory + f"/{user_id}.json"):
			# Чтение файла.
			self.__Data = ReadJSON(self.__StorageDirectory + f"/{user_id}.json")

		# Создание файла.
		else:
			# Сохранение данных.
			WriteJSON(self.__StorageDirectory + f"/{user_id}.json", self.__Data)

	def add_permissions(self, permissions: list[str] | str):
		"""
		Задаёт разрешения.
			permissions – разрешения.
		"""

		# Если указано одно разрешение, преобразовать в список.
		if type(permissions) == str: permissions = [permissions]
		# Состояние: изменялся ли список разрешений.
		IsChanged = False

		# Для каждого разрешения.
		for Permission in permissions:

			# Если разрешение не определено.
			if Permission not in self.__Data["permissions"]:
				# Добавление разрешения.
				self.__Data["permissions"].append(Permission)
				# Переключение состояния.
				IsChanged = True

		# Если список разрешений изменён, отсортировать его.
		if IsChanged: self.__Data["permissions"] = sorted(self.__Data["permissions"])
		# Сохранение данных.
		self.__SaveData()

	def create_property(self, key: str, value: any):
		"""
		Создаёт свойство пользователя и задаёт ему значение, если такового ещё не существует.
			key – ключ свойства;
			value – значение.
		"""
		
		# Если свойства не существует.
		if key not in self.__Data["data"].keys():
			# Создание свойства.
			self.__Data["data"][key] = value
			# Сохранение данных.
			self.__SaveData()

	def get_property(self, key: str) -> any:
		"""
		Возвращает значение свойства пользователя.
			key – ключ свойства.
		"""

		return self.__Data["data"][key]

	def has_permissions(self, permissions: list[str] | str) -> bool:
		"""
		Проверяет, имеет ли пользователь все перечисленные разрешения.
			permissions – разрешения.
		"""

		# Если указано одно разрешение, преобразовать в список.
		if type(permissions) == str: permissions = [permissions]
		# Состояние: имеет ли пользователь все указанные разрешения.
		IsOwned = True

		# Для каждого разрешения.
		for Permission in permissions:

			# Если разрешение не определено, переключить состояние.
			if Permission not in self.__Data["permissions"]: IsOwned = False

		return IsOwned

	def remove(self):
		"""Удаляет локальный файл пользователя."""

		# Удаление локального файла.
		os.remove(self.__StorageDirectory + f"/{self.__ID}.json")

	def remove_permissions(self, permissions: list[str] | str):
		"""
		Удаляет разрешения.
			permissions – разрешения.
		"""

		# Если указано одно разрешение, преобразовать в список.
		if type(permissions) == str: permissions = [permissions]

		# Для каждого разрешения.
		for Permission in permissions:

			# Если разрешение определено.
			if Permission in self.__Data["permissions"]:
				# Удаление разрешения.
				self.__Data["permissions"].remove(Permission)

		# Сохранение данных.
		self.__SaveData()

	def remove_property(self, key: str):
		"""
		Удаляет свойство пользователя.
			key – ключ свойства.
		"""

		# Если свойство существует.
		if key in self.__Data["data"].keys():
			# Удаление свойства.
			del self.__Data["data"][key]
			# Сохранение данных.
			self.__SaveData()

	def set_property(self, key: str, value: any):
		"""
		Обновляет значение существующего свойства пользователя.
			key – ключ свойства;
			value – значение.
		"""
		
		# Если свойство существует.
		if key in self.__Data["data"].keys():
			# Обновление данных.
			self.__Data["data"][key] = value
			# Сохранение данных.
			self.__SaveData()

	def update(self, user: User):
		"""
		Обновляет данные пользователя из параметров, содержащихся в сообщении.
			user – объект представления пользователя.
		"""

		# Если ID соответствует.
		if user.id == self.__ID:
			# Обновление данных.
			self.__Data["is_premium"] = bool(user.is_premium)
			self.__Data["language"] = user.language_code
			self.__Data["username"] = user.username
			# Сохранение файла.
			self.__SaveData()

		else: raise UpdateByOtherUser()

class UsersManager:
	"""Менеджер пользователей."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА ТОЛЬКО ДЛЯ ЧТЕНИЯ <<<<< #
	#==========================================================================================#

	@property
	def admins(self) -> list[UserData]:
		"""Список пользователей с правами администратора."""

		# Список администраторов.
		Admins = list()

		# Для каждого пользователя.
		for UserID in self.__Users.keys():
			# Добавление пользователя в список.
			if self.__Users[UserID].is_admin: Admins.append(self.__Users[UserID])

		return Admins

	@property
	def premium_users(self) -> list[UserData]:
		"""Список пользователей с Premium подпиской."""

		# Список подписчиков.
		PremiumUsers = list()

		# Для каждого пользователя.
		for UserID in self.__Users:
			# Добавление пользователя в список.
			if self.__Users[UserID].is_premium: PremiumUsers.append(self.__Users[UserID])

		return PremiumUsers

	@property
	def users(self) -> list[UserData]:
		"""Список пользователей."""

		# Список пользователей.
		Users = list()
		# Для каждого пользователя записать значение в список.
		for UserID in self.__Users.keys(): Users.append(self.__Users[UserID])

		return Users

	#==========================================================================================#
	# >>>>> МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __LoadUsers(self):
		"""Загружает данные пользователей."""

		# Получение списка файлов в директории пользователей.
		Files = os.listdir(self.__StorageDirectory)
		# Фильтрация только файлов формата JSON.
		Files = list(filter(lambda List: List.endswith(".json"), Files))

		# Для каждого файла.
		for File in Files:
			# Чтение файла.
			Buffer = ReadJSON(self.__StorageDirectory + f"/{File}")
			# ID пользователя.
			UserID = int(File.replace(".json", ""))
			# Запись пользовательских данных.
			self.__Users[UserID] = UserData(self.__StorageDirectory, UserID, Buffer)

	def __init__(self, dir: str):
		"""
		Менеджер пользователей.
			dir – путь к директории хранения данных.
		"""

		#---> Генерация динамических свойств.
		#==========================================================================================#
		# Словарь пользователей.
		self.__Users = dict()
		# Директория хранилища.
		self.__StorageDirectory = dir.replace("\\", "/").rstrip("/")

		# Если директория пользователей не существует, создать её.
		if not os.path.exists(self.__StorageDirectory): os.makedirs(self.__StorageDirectory)
		# Загрузка данных пользователей.
		self.__LoadUsers()

	def auth(self, user: User) -> UserData:
		"""
		Выполняет идентификацию и обновление данных существующего пользователя или создаёт локальный файл для нового.
			user – структура описания пользователя Telegram.
		"""
		
		# Текущий пользователь.
		CurrentUser = None

		# Если пользователь ещё не существует.
		if user.id not in self.__Users.keys():
			# Создание нового пользователя.
			self.__Users[user.id] = UserData(self.__StorageDirectory, user.id, user)

		# Обновление данных пользователя.
		self.__Users[user.id].update(user)
		# Установка текущего пользователя.
		CurrentUser = self.__Users[user.id]

		return CurrentUser

	def get_user(self, user_id: int | str) -> UserData:
		"""
		Возвращает объект данных пользователя.
			user_id – ID пользователя.
		"""
		
		return self.__Users[int(user_id)]

	def get_users(self, include_permissions: list[str] | str | None = None, exclude_permissions: list[str] | str | None = None) -> list[UserData]:
		"""
		Возвращает список пользователей, подходящих под переданные фильтры. По умолчанию возвращает список всех пользователей.
			include_permissions – разрешения, которыми должен обладать пользователь;
			exclude_permissions – разрешения, которых у пользователя быть не должно.
		"""

		# Копирование списка пользователей.
		Users = self.users

		# Если переданы включения разрешений для фильтрации.
		if include_permissions:
			# Буфер фильтрации.
			Buffer = list()

			# Для каждого пользователя.
			for User in Users: 
				# Если пользователь имеет все указанные разрешения, записать его.
				if User.has_permissions(include_permissions): Buffer.append(User)

			# Перезапись списка пользователей буфером.
			Users = Buffer

		# Если переданы исключения разрешений для фильтрации.
		if exclude_permissions:
			# Буфер фильтрации.
			Buffer = list()

			# Для каждого пользователя.
			for User in Users: 
				# Если пользователь не имеет все указанные разрешения, записать его.
				if not User.has_permissions(exclude_permissions): Buffer.append(User)

			# Перезапись списка пользователей буфером.
			Users = Buffer

		return Users

	def remove_user(self, user_id: int | str):
		"""
		Удаляет пользователя из системы.
			user_id – ID пользователя.
		"""

		# Приведение ID пользователя к целочисленному.
		user_id = int(user_id)
		# Удаление локального файла.
		self.__Users[user_id].remove()
		# Удаление объекта.
		del self.__Users[user_id]