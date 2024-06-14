# dublib
**dublib** – это библиотека, поставляющая компоненты, требующиеся в проектах [@DUB1401](https://github.com/DUB1401), написанных на Python.

Данный набор модулей распространяется по Rolling-модели. Это значит, что разработчик не заботится об обратной совместимости с прошлыми релизами, потому рекомендуется привязывать ваш проект строго к определённой версии библиотеки.

Все компоненты поставляют лишь базовую документацию, необходимую для общего понимания принципов работы. Библиотека является самодокументируемой.

# Поставляемые компоненты
Библиотека включает следующие модули:
* [CLI](https://github.com/DUB1401/dublib/blob/main/docs/CLI.md)
* [Methods](https://github.com/DUB1401/dublib/blob/main/docs/Methods.md)
* [Polyglot](https://github.com/DUB1401/dublib/blob/main/docs/Polyglot.md)
* [TelebotUtils](https://github.com/DUB1401/dublib/blob/main/docs/Terminalyzer.md)
* [Terminalyzer](https://github.com/DUB1401/dublib/blob/main/docs/Terminalyzer.md)
* [WebRequestor](https://github.com/DUB1401/dublib/blob/main/docs/WebRequestor.md)

# Установка
Библиотека поддерживает установку из двух типов репозиториев:
* **PyPI** – стабильные выпуски (с возможностью выбора конкретной версии);
* **GitHub** – канал разработки со всеми последними изменениями и исправлениями.

_**Примечание:**_ Для установки библиотеки из репозитория GitHub на вашем устройстве должна присутствовать система контроля версий Git.
```
# Установка из PyPi.
pip install dublib

# Установка конкретной версии из PyPi.
pip install dublib=={version}

# Установка из GitHub.
pip install git+https://github.com/DUB1401/dublib
```

_Copyright © DUB1401. 2023-2024._