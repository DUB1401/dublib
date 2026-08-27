# Configurator
**Configurator** – это модуль для хранения конфигураций, реализованный в паттерне *Singleton*, что позволяет ему быть инициализированным однократно для конкретного файла параметров. Контейнер поддерживает отслеживание изменений в файле и автоматическую перезагрузку, а валидация структуры производится методом создания модели в виде замороженного класса данных [pydantic](https://github.com/pydantic/pydantic).

## Как использовать
```Python
from time import sleep

from dublib.engine.configurator import Config, ConfigTemplate, dataclass

@dataclass(frozen = True)
class ConfigModel(ConfigTemplate):
	token: str

# При повторной инициализации с данным именем файла вернёт тот же экземпляр.
config = Config("test.json", ConfigModel) 

print(config.data.token) # Выведет токен.
config.watch() 
# Имитация деятельности программы, во время которой токен можно изменить.
sleep(10)
print(config.data.token) # Выведет изменённый токен.
```

## Асинхронность
Класс `Config` вместе с отслеживанием может быть использован в асинхронном режиме.
```Python
import asyncio
from time import sleep

from dublib.engine.configurator import Config, ConfigTemplate, dataclass

@dataclass(frozen = True)
class ConfigModel(ConfigTemplate):
	token: str

config = Config("test.json", ConfigModel)

async def main():
	print(config.data.token) # Выведет токен.
	asyncio.create_task(config.watch_async())
	# Имитация деятельности программы, во время которой токен можно изменить.
	await asyncio.sleep(5)
	print(config.data.token) # Выведет изменённый токен.

asyncio.run(main())
```
