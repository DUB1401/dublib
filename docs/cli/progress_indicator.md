# Progress Indicator

**Progress Indicator** – это модуль, позволяющий сообщать терминалу о прогрессе выполнения задачи через протокол [OSC 9;4](https://docs.otty.sh/vt/osc/osc-9-4). Используемый объект реализован по паттерну _Singleton_, что не позволяет его пересоздавать для одного и того же файла и гарантирует уникальность управляющей системы.

## Пример
```Python
from time import sleep

from dublib.cli.progress_indicator import ProgressIndicator

Indicator = ProgressIndicator()

for Index in range(100):
	# Вывод в терминал управляющей последовательности.
	Indicator.set_progress(Index)
	# Симуляция ошибки во время выполнения.
	if Index == 55: Indicator.error()

	sleep(0.1)

Indicator.end()
```

## Компоненты
```{eval-rst}
.. automodule:: dublib.cli.progress_indicator
	:members:
```