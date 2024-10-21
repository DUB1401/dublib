# Master
**Master** – это подмодуль, содержащий набор расширений и алгоритмов для стандартного функционала бота Telegram.

## Пример
```Python
from dublib.TelebotUtils import TeleMaster

# Токен бота Telegram.
BOT_TOKEN = ""

# Инициализация объекта.
MasterBot = TeleMaster(BOT_TOKEN)
# Получение стандартного объекта бота Telegram.
Bot = MasterBot.bot

# Обработка команды: start.
@Bot.message_handler(commands = ["start"])
def Command(Message: types.Message):
	# Авторизация пользователя.
	User = Users.auth(Message.from_user)
	# Проверка: состоит ли пользователь в указанном чате.
	IsSubscribed = MasterBot.check_user_subscriptions(User, -123456789)
	# Если пользователь не подписан, отправить ему сообщение.
	if not IsSubscribed: Bot.send_message(User.id, "Станьте участником чата -123456789!")
```