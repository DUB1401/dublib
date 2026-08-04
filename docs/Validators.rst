Validators
==========

Данный модуль содержит набор валидаторов строк для их проверки и преобразования в иные типы данных.

Использование
-------------

.. code-block:: python

	from dublib.Validators import Validator_UnsignedInteger

	Validator_UnsignedInteger.validate("123") # True
	Validator_UnsignedInteger.validate("-123") # False

	Validator_UnsignedInteger.convert("123") # 123
	Validator_UnsignedInteger.convert("-123") # ValidationError

Создание валидатора
-------------------

Для создания собственного валидатора необходимо унаследовать класс от ``BaseValidator`` и указать целевой тип данных в квадратных скобках при наследовании, а также переопределить два статических метода: ``validate()`` и ``convert()``.

В качестве имени кастомного валидатора рекомендуется использовать ``CustomValidator_{TYPE}``, что позволяет извлекать тип при генерации исключений.

Любой валидатор наследует также метод ``parse()``, автоматически валидирующий и приводящий значение к нужному типу, а в случае ошибки выбрасывающий исключение типа ``ValidationError``.

.. code-block:: python

	from dublib.Validators import BaseValidator

	class CustomValidator_ExampleBool(BaseValidator[bool]):

		@staticmethod
		def convert(value: str) -> bool:
			value = value.lower()
			if value in ("true",): return True

			return False
		
		@staticmethod
		def validate(value: str) -> bool:
			Buffer = value.lower()

			return Buffer in ("true", "false")

	# После создания собственного валидатора его можно использовать в Terminalyzer.

	from dublib.CLI.Terminalyzer import Terminalyzer, Command, ValidableTypes

	from enum import Enum

	class CustomValidableTypes(ValidableTypes):
		ExampleBool = CustomValidator_ExampleBool

	Commands = []

	Com = Command("example")
	Com.base.add_argument(CustomValidableTypes.ExampleBool)
	Commands.append(Com)

Предоставленные типы
--------------------

.. automodule:: dublib.Validators
	:members:
