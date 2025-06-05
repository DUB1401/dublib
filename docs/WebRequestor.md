# WebRequestor
**WebRequestor** – это менеджер запросов, поддерживающий библиотеки [curl_cffi](https://github.com/yifeikong/curl_cffi), [httpx](https://github.com/encode/httpx) и [requests](https://github.com/psf/requests), а также ротацию прокси.

## Пример
```Python
from dublib.WebRequestor import Protocols, Proxy, WebConfig, WebLibs, WebRequestor

import logging

# Настройка вывода логов модуля в консоль.
logging.getLogger("dublib.WebRequestor").addHandler(logging.StreamHandler())

# Создание конфигурации.
Config = WebConfig()
# Выбор библиотеки (по умолчанию используется requests).
Config.select_lib(WebLibs.curl_cffi)
# Генерация User-Agent для ПК.
Config.generate_user_agent(platforms = ["desktop"])
# Установка количества повторов при неудачном запросе.
Config.set_retries_count(2)
# Установка TLS отпечатка Google Chrome 124.
Config.curl_cffi.select_fingerprint("chrome124")

# Инициализация менеджера запросов.
Requestor = WebRequestor(Config)
# Установка прокси.
Requestor.add_proxy(Proxy().parse("https://{login}:{password}@{ip}:{port}"))

# Выполнение GET-запроса.
Response = Requestor.get("https://site.com/")

# Если запрос успешен.
if Response.status_code == 200:
	# Вывод ответа.
	print(Response.text)

# Выполнение POST-запроса.
Response = Requestor.post("https://api.site.com/", data = "Lorem ipsum.")

# Если запрос успешен.
if Response.status_code == 200:
	# Вывод ответа, десериализованного в словарь из JSON.
	print(Response.json)
```