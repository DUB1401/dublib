progress_indicator
==================
.. automodule:: dublib.cli.progress_indicator
	:members:
	
Описание
--------
Модуль ``progress_indicator`` позволяет сообщать терминалу о прогрессе выполнения задачи через протокол **OSC 9;4**. Используемый объект реализован по паттерну _Singleton_, что не позволяет его пересоздавать и гарантирует уникальность управляющей системы при использовании текущего модуля.

Пример
------
.. code-block:: python

	from time import sleep

	from dublib.cli.progress_indicator import ProgressIndicator

	Indicator = ProgressIndicator()

	for Index in range(100):
		# Вывод в терминал управляющей последовательности.
		Indicator.set_progress(Index)
		# Симуляция ошибки во время выполнения.
		if Index == 55: Indicator.error()

		sleep(0.1)

	