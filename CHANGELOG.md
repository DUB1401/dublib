# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
#### Methods.Data
- Добавлена функция `InsertDictionaryAfterKey()` для вставки одного словаря внутрь другого после определённого ключа.
#### Methods.System
- Функция `Clear()` теперь может сохранять буфер прокрутки сессии терминала через соответствующий параметр.
#### WebRequestor
- Для `WebConfig` добавлен метод `set_header()`, а метод `add_header()` теперь запрещает переопределение заголовка. Также реализовано соответствующее исключение `HeaderRedefining`.
- В `WebResponse` реализовано хранилище заголовков ответа.
- Добавлен метод для разрешения запросов **Client Hints**, а также режим их автоматическоро разрешения при выполнении запросов.

### Changed
#### Methods.System
- Функция `Clear()` теперь использует ANSI-коды вместо вызова системных утилит.
#### WebRequestor
- Заголовки внутри `WebConfig` теперь всегда хранятся в нижнем регистре.
- Метод `remove_header()` теперь может быть настроен для игнорирования попытки удаления несуществующего заголовка.
- Для генерации заголовка _User-Agent_ и **Client Hints** применена библиотека [ua-generator](https://github.com/iamdual/ua-generator).

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