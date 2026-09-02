# Validators
Данный модуль содержит набор валидаторов строк для их проверки и преобразования в иные типы данных.

## Использование
```Python
from dublib.validators import types

types.UnsignedInteger.validate("123") # True
types.UnsignedInteger.validate("-123") # False

types.UnsignedInteger.convert("123") # 123
types.UnsignedInteger.convert("test") # Неопределённое поведение, нет валидации.

types.UnsignedInteger.parse("123") # 123
types.UnsignedInteger.parse("test") # ValidationError
```

## Создание валидатора
Для создания собственного валидатора необходимо унаследовать класс от `BaseValidator` и указать целевой тип данных в квадратных скобках при наследовании, а также переопределить два статических метода: `validate()` и `convert()`.

В качестве имени кастомного валидатора рекомендуется использовать краткое описание валидируемого типа, например для электронной почты **Email**.

Любой валидатор наследует также метод `parse()`, автоматически валидирующий и приводящий значение к нужному типу, а в случае ошибки выбрасывающий исключение типа `ValidationError`.

```Python
# types.py
from dublib.validators.base import BaseValidator

class Zero(BaseValidator[int]):

	@staticmethod
	def convert(value: str) -> int:

		return int(value)
	
	@staticmethod
	def validate(value: str) -> bool:

		return value == "0"
```

После создания собственного валидатора его можно использовать в `Terminalyzer`.

```Python
# main.py
from dublib.cli.terminalyzer import Terminalyzer, Command, ValidableTypes

from . import types

class CustomValidableTypes(ValidableTypes):
	Zero = types.Zero

Commands = []

Com = Command("example")
Com.base.add_argument(CustomValidableTypes.Zero)
Commands.append(Com)
```

## Предоставленные валидаторы
```{eval-rst}
.. automodule:: dublib.validators.types
	:members:
```