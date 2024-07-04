# WebRequestor
**WebRequestor** – это менеджер запросов, поддерживающий библиотеки [curl_cffi](https://github.com/yifeikong/curl_cffi), [httpx](https://github.com/encode/httpx) и [requests](https://github.com/psf/requests), а также ротацию прокси.

## Пример
```Python
from dublib.WebRequestor import Protocols, WebConfig, WebLibs, WebRequestor

# Инициализация менеджера запросов.
Requestor = WebRequestor()
# Создание конфигурации (по умолчанию используется requests).
Config = WebConfig()
# Выбор библиотеки.
Config.select_lib(WebLibs.curl_cffi)
# Генерация User-Agent для ПК.
Config.generate_user_agent("pc")
# Установка базового количества повторов при неудачном запросе.
Config.set_tries_count(3)
# Установка TLS отпечатка Google Chrome 124.
Config.curl_cffi.select_fingerprint("chrome124")
# Установка прокси.
Requestor.add_proxy(
	Protocols.HTTPS,
	host = "1.2.3.4",
	port = 8080,
	login = "login",
	password = "password"
)

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
	# Вывод ответа, спаршенного в словарь из JSON.
	print(Response.json)
```