# ExecutionStatus
**ExecutionStatus** – это подмодуль для организации общения между методами и функциями по принципу возвращаемого значения. Он представляет собой удобную структуру данных, которая может содержать целочисленный код, значение, последовательность сообщений и дополнительные данные типа ключ-значение. 

Статус также поддерживыает слияние через метод `merge()`, что позволяет создавать конвейеры общения.

## Пример
```Python
from dublib.Engine.Bus import ExecutionStatus

# Функция для деления двух значений.
def some_function(first_value: int, second_value: int) -> ExecutionStatus:
	# Результат выполнения.
	Status = ExecutionStatus()

	try:
		# Деление.
		Result = first_value / second_value
		# Составление отчёта о выполнении.
		Status.value = Result

	except ZeroDivisionError:
		# Формирование отчёта об ошибке с описанием в виде названия исключения.
		Status.push_error(ZeroDivisionError.__name__)

	return Status

# Выполнение деления.
Result = some_function(10, 0)
# Если значение в статусе проходит проверку на истинность, вывести результат.
if Result: print(Result.value)
# Иначе вывести все сообщения.
else: Result.print_messages()

```