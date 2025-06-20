# Документация
В данном проекте используется автоматически генерируемая на основе [Sphinx](https://github.com/sphinx-doc/sphinx) документация, сборка которой должна производиться локально на целевом устройстве.

## Инструкции для Linux
```Bash
# Требуется версия Python 3.11 или новее.
python -V
# Клонирование репозитория.
git clone https://github.com/DUB1401/dublib
cd dublib
# Создание виртуальной среды.
python3 -m venv .venv
# Активация вирутальной среды.
source .venv/bin/activate
# Установка зависимостей.
pip install .[all]
# Генерация документации (вместо docs/build можно указать любой каталог).
sphinx-build -b html docs docs/build
# Открытие главного файла документации в браузере.
xdg-open docs/build/index.html
```