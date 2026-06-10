Validators
==========
.. automodule:: dublib.CLI.Terminalyzer.Validators
	:members:

Для создания собственного валидатора необходимо унаследовать класс от ``BaseValidator``, указать целевой тип данных в квадратных скобках при наследовании, а также переопределить два статических метода: ``validate()`` и ``convert()``.

Любой валидатор наследует также метод ``parse()``, автоматически валидирующий и приводящий значение к нужному типу, а в случае ошибки выбрасывающий исключение типа ``ValidationError``.

Создание
--------

.. code-block:: python

	from dublib.CLI.Terminalyzer.Validators import BaseValidator

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

Использование
-------------

После создания кастомного валидатора его можно использовать в ``Terminalyzer`` как указатель ожидаемого типа параметра.

.. code-block:: python

	from dublib.CLI.Terminalyzer import Terminalyzer, Command, ValidableValuesTypes

	from enum import Enum

	class CustomValidableValuesTypes(ValidableValuesTypes):
		ExampleBool = CustomValidator_ExampleBool

	Commands = list()

	Com = Command("example")
	Com.base.add_argument(CustomValidableValuesTypes.ExampleBool)
	Commands.append(Com)

	# Дальнейшая обработка через Terminalyzer...

	
