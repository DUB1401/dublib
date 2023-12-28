# WebRequestor
**WebRequestor** – это модуль для запроса HTML кода веб-страниц, поддерживающий библиотеки [requests](https://github.com/psf/requests) и [Selenium](https://github.com/SeleniumHQ/selenium).

## Классы
* `Browsers` – перечисление поддерживаемых браузеров:
	* **Chrome** – Google Chrome.
* `RequestsConfig` – конфигурация для использования библиотеки [requests](https://github.com/psf/requests).
* `SeleniumConfig` – конфигурация для использования библиотеки [Selenium](https://github.com/SeleniumHQ/selenium).
* `WebResponse` – имплементация requests-подобного ответа для Selenium.

## Пример
```Python
from Source.WebRequestor import WebRequestor

# Запросчик HTML кода веб-страниц (с включеным ведением логов).
Requestor = WebRequestor(Logging = True)

# Создание конфигурации для выбора одной из библиотек: requests или Selenium.
Config = RequestsConfig()
Config = SeleniumConfig(Browsers.Chrome)

# Инициализация запросчика через выбранную библиотеку.
Requestor.initialize(Config)
# Запрос HTML кода веб-страницы.
Response = Requestor.get("https://site.com/")

# Если запрос успешен.
if Response.status_code == 200:
	# Вывод HTML кода.
	print(Response.text)
```