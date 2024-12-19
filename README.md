# dublib
**dublib** – это библиотека Python, поставляющая полезные компоненты общего назначения.

Данный набор модулей распространяется по Rolling-модели. Это значит, что разработчик не заботится об обратной совместимости с прошлыми релизами, потому рекомендуется привязывать ваш проект строго к определённой версии библиотеки!

Все компоненты поставляют лишь базовую документацию, необходимую для общего понимания принципов работы.

# Поставляемые компоненты
Библиотека включает следующие модули:
* [CLI](https://github.com/DUB1401/dublib/blob/main/docs/CLI/README.md)
* [Engine](https://github.com/DUB1401/dublib/blob/main/docs/Engine/README.md)
* [Methods](https://github.com/DUB1401/dublib/blob/main/docs/Methods/README.md)
* [Polyglot](https://github.com/DUB1401/dublib/blob/main/docs/Polyglot.md)
* [TelebotUtils](https://github.com/DUB1401/dublib/blob/main/docs/TelebotUtils/README.md)
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

_Copyright © DUB1401. 2023-2025._