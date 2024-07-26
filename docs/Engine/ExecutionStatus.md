# ExecutionStatus
**ExecutionStatus** – это подмодуль для организации общения между методами и функциями по принципу возвращаемого значения. Отчёты о предупреждении и ошибках наследуются от отчёта о выполнении, потому имеют одинаковую структуру и отличаются лишь типом, который может быть использован при выводе через `CLI.Templates`.

### Классы
* `StatussesTypes` – содержит типы отчётов.
* `ExecutionStatus` – отчёт о выполнении;
* `ExecutionWarning` – отчёт о предупреждении выполнения;
* `ExecutionError` – отчёт об ошибке;
* `ExecutionCritical` – отчёт о критической ошибке.

## Пример
```Python
from dublib.CLI.Templates import PrintExecutionStatus
from dublib.Engine.ExecutionStatus import *

# Функция для деления двух значений.
def some_function(first_value: int, second_value: int) -> ExecutionStatus:
	# Результат выполнения.
	Status = None

	try:
		# Деление.
		Result = first_value / second_value
		# Составление отчёта о выполнении.
		Status = ExecutionStatus(0, value = Result)

	except ZeroDivisionError:
		# Формирование отчёта об ошибке с описанием в виде названия исключения.
		Status = ExecutionError(-1, ZeroDivisionError.__name__)

	return Status

# Выполнение деления.
Result = some_function(10, 0)
# Если выполнение успешно, вывести результат, иначе вывести отчёт об ошибке.
if Result.code == 0: print(Result.value)
else: PrintExecutionStatus(Result)

```