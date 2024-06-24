# TelebotUtils
**TelebotUtils** – это коллекция инструментов для упрощения проектирования ботов Telegram при помощи библиотеки [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI). Включает в себя средства для межсессионного хранения базовых данных пользователя в файлах JSON, управления уровнем доступа, а также ожидания от пользователя определённых значений.

Для использования нужно установить дополнительные зависимости: `pip install dublib[telebot]`.

## Пример
```Python
from dublib.TelebotUtils import UsersManager, UserData
from telebot import types

# Инициализация менеджера с указанием каталога для хранения JSON файлов.
Manager = UsersManager("Data/Users")

# Обработка команды: start.
@Bot.message_handler(commands = ["start"])
def Start(Message: types.Message):
	# Авторизация пользователя.
	User = Manager.auth(Message.from_user)
	# Отправка сообщения: введите пароль.
	Bot.send_message(Message.chat.id, "Отправьте мне пароль.")
	# Установка ожидаемого значения.
	User.set_expected_type("password")

# Обработка ввода пароля.
@Bot.message_handler(content_types = ["text"])
def Password(Message: types.Message):
	# Авторизация пользователя.
	User = Manager.auth(Message.from_user)

	# Если от пользователя ожидается пароль и он его ввёл пароль.
	if User.expected_type == "password" and Message.text == "1234":
		# Выдача пользователю прав администратора.
		User.add_permissions("admin")

# Обработка команды: start_work.
@Bot.message_handler(commands = ["start_work"])
def StartWork(Message: types.Message):
	# Авторизация пользователя.
	User = Manager.auth(Message.from_user)

	# Если пользователь имеет права администратора.
	if User.has_permissions("admin"):
		# Установка свойства пользователя.
		User.set_property("property", True)
		# Установка временного свойства пользователя.
		User.set_temp_property("temp_property", True)
		# Вывод в консоль: тестовое сообщение.
		print("Work started!")

# Обработка команды: end_work.
@Bot.message_handler(commands = ["end_work"])
def EndWork(Message: types.Message):
	# Авторизация пользователя.
	User = Manager.auth(Message.from_user)

	# Если пользователь имеет права администратора.
	if User.has_permissions("admin"):
		# Получение свойств пользователя.
		Property = User.get_property("property")
		TempProperty = User.get_temp_property("temp_property")
		# Удаление временных свойств.
		User.clear_temp_properties()
		# Вывод в консоль: тестовое сообщение.
		print(f"Property: {Property}\nTemp property: {TempProperty}")
```
