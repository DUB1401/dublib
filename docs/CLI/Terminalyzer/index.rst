Terminalyzer
============
.. automodule:: dublib.CLI.Terminalyzer
	:members:
.. toctree::
	Command
	Helper

Описание
--------
Модуль ``Terminalyzer`` предназначен для расширенного, типизированного и защищённого анализа текстовых команд в стиле **Shell**.

Доступны три типа параметров:
	* **Аргумент** – значение, поддерживающее приведение к определённому типу.
	* **Флаг** – логический переключатель, который может иметь псевдонимы.
	* **Ключ** – идентификатор того, что следующий параметр является значением определённого типа (именованный аргумент, поддерживающий логические проверки присутствия). Также может иметь псевдонимы.

Пример
------
.. code-block:: python

	from dublib.CLI.Terminalyzer import Terminalyzer, Command, ValidableTypes

	Commands = list()

	# Создание описания команды.
	Com = Command("open", "Open some file.")
	# Создание обязательной позиции с аргументом типа существующего пути.
	ComPos = Com.create_position("TARGET", "Target to open", important = True)
	ComPos.set_argument(ValidableTypes.ValidPath, "Path to file.")
	# Добавление альтернативы аргументу, флага и ключа.
	ComPos.add_flag("-l", aliases = ("--last",), description = "Open last file.")
	ComPos.add_key("-p", aliases = ("--path",), description = "Specify path.")

	Commands.append(Com)

	# Инициализация анализатора. По умолчанию ввод берётся из sys.argv.
	Analyzer = Terminalyzer()
	# Включение команды help, выводящей детализированную помощь.
	Analyzer.helper.enable()
	# Поиск и парсинг команды.
	CommandData = Analyzer.check_commands(Commands)

	if CommandData and Command.name == "open":
		# Проверка активации флага по псевдониму.
		if CommandData.check_flag("--last"):
			pass

		# Проверка активации ключа по имени.
		elif CommandData.check_key("-p"):
			# Получение пути к файлу через значение ключа.
			CommandData.get_key_value("--path")

		else:
			# Получение пути к файлу через слот позиции.
			CommandData.get_position_parameter("TARGET").value
			# Получение пути к файлу через индекс аргумента.
			CommandData.arguments[0].value