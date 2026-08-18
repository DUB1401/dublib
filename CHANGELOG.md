# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
#### cli
- Добавлен модуль `progress_indicator` для индикации прогресса в терминале на основе протокола **OSC 9;4**.
- В модуле `templates.bus` добавлен шаблон вывода для отладочного сообщения.
#### web_requestor
- Добавлена поддержка запросов `DELETE`.

### Changed
- Модули переименованы в соответствии с [PEP 8](https://peps.python.org/pep-0008).
#### engine.bus
- Удалены все методы генерации текстовых представлений и вывода в консоль.
#### web_requestor
- В классе `WebConfig` метод `generate_user_agent()` теперь может принимать строку, а не только последовательности строк.
- Управление всеми заголовками вынесено в свойство `headers`.
- Оптимизированы попытки парсинга JSON внутри `WebResponse` через библиотеку [orjson](https://github.com/ijl/orjson).

### Removed
#### filesystem
- Удалена функция `ListDir()`.

### Fixed
#### web_requestor
- Конфигурация `WebConfig` не отдавала заголовки **Client Hints**.
- Запросы типа **POST** через [requests](https://github.com/psf/requests) ошибочно выполнялись как **GET**.

## [0.29.0] - 2026-08-05

### Added
#### Functions.Data
- Добавлена функция `InsertDictionaryAfterKey()` для вставки одного словаря внутрь другого после определённого ключа.
#### Functions.System
- Функция `Clear()` теперь может сохранять буфер прокрутки сессии терминала через соответствующий параметр.
#### WebRequestor
- Для `WebConfig` добавлен метод `set_header()`, а метод `add_header()` теперь запрещает переопределение заголовка. Также реализовано соответствующее исключение `HeaderRedefining`.
- В `WebResponse` реализовано хранилище заголовков ответа.
- Добавлен метод для разрешения запросов **Client Hints**, а также режим их автоматическоро разрешения при выполнении запросов.

### Changed
- Модуль `Methods` переименован в `Functions`.
#### Functions.System
- Функция `Clear()` теперь использует ANSI-коды вместо вызова системных утилит.
#### WebRequestor
- Заголовки внутри `WebConfig` теперь всегда хранятся в нижнем регистре.
- Метод `remove_header()` теперь может быть настроен для игнорирования попытки удаления несуществующего заголовка.
- Для генерации заголовка _User-Agent_ и **Client Hints** применена библиотека [ua-generator](https://github.com/iamdual/ua-generator).
- Код 404 удалён из считаемых результатом успешного выполнения запроса.

### Fixed
#### Validators
- Невозможно импортировать исключения модуля `Validators`.
#### WebRequestor
- Установка целочисленных значений в заголовок запроса приводила к сбою.

### Security
- Заменены устаревшие вызовы `os.system()` на `subprocess.run()`.

## [0.28.5] - 2026-07-22

### Added
- Для `Methods.System` и `Methods.Decorators` теперь поставляется документация.

### Changed
- Модуль `Validators` вынесен в корень и более не привязан к `CLI`.