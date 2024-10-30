# Cache
**Cache** – это подмодуль, помогающий удобно хранить медиафайлы на серверах Telegram для быстрого повторного использования.

## Пример
```Python
from dublib.TelebotUtils.Cache import TeleCache
from telebot import types

# Токен бота Telegram.
BOT_TOKEN = ""
# ID чата для хранения медиафайлов. Нельзя указывать других ботов и чаты, к которым у бота нет доступа.
CHAT_ID = 0

# Инициализация менеджера кэша.
Cacher = TeleCache()
# Установка данных для выгрузки медиафайлов.
Cacher.set_options(BOT_TOKEN, CHAT_ID)

# Ручная выгрузка файла на сервер Telegram.
Cacher.upload_file("test.jpg", types.InputMediaPhoto)
# Получение структуры данных кэшированного файла.
File = Cacher.get_cached_file("test.jpg")
# Получение ID кэшированного файла.
FileID = Cacher["test.jpg"]

# Самостоятельная регистрация файла, загруженного сторонними методами.
# Пример использования виртуального идентификатора вместо пути к реальному файлу.
Cacher.register_file("youtube/123/480p", 0, "file123")
```