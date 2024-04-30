# TelebotUtils
**TelebotUtils** – это коллекция инструментов для упрощения проектирования ботов Telegram при помощи библиотеки [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI).

На данный момент включает в себя классы для межсессионного хранения базовых данных пользователя в файлах JSON и управления уровнем доступа.

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
	User = UsersManagerObject.auth(Message)

	# Если пользователь имеет права администратора.
	if User.has_permissions("admin"):
		# Получение тестовых данных из межсессионного хранилища.
		Data = User.get_property("test")
		# Вывод в консоль: тестовое сообщение.
		print("Is admin!")


	else:
		# Выдача пользователю прав администратора.
		User.add_permissions(["admin"])
		# Помещение тестовых данных в межсессионное хранилище.
		User.set_property("test", "Is a data!")
```
