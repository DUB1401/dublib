from ..CLI.StyledPrinter import StyledPrinter, Styles
from ..Methods.System import Clear
from ..Engine.Bus import *

import readline

#==========================================================================================#
# >>>>> ШАБЛОНЫ ВВОДА-ВЫВОДА <<<<< #
#==========================================================================================#

def Confirmation(text: str, question: str | None = None, yes: str | None = None, no: str | None = None) -> bool:
	"""
	Запрашивает подтверждение пользователя.
		text – описание вопроса;\n
		question – строка, обозначающая сам вопрос в используемом языке;\n
		yes – строка, обозначающая согласие при вводе в консоль;\n
		yes – строка, обозначающая отсутствие согласия при вводе в консоль.
	"""

	# Ответ.
	Response = None
	# Если не заданы необязательные параметры, использовать стандартные.
	if not question: question = "Confirm?"
	if not yes: yes = "Y"
	if not no: no = "N"

	# Постоянно.
	while True:
		# Запрос подтверждения.
		InputLine = input(f"{text}\n{question} [{yes}/{no}]: ").strip().lower()
		# Проверка ответов.
		if InputLine == yes.lower(): Response = True
		if InputLine == no.lower(): Response = False
		# Если ответ дан, остановить цикл.
		if Response != None: break

	return Response

def PrintExecutionStatus(
		status: ExecutionStatus | ExecutionWarning | ExecutionError | ExecutionCritical,
		colorize: bool = True,
		format: str | None = None,
		printable_data_key: str = "print"
	):
	"""
	Выводит в консоль сообщение из отчёта о выполнении.
		status – статус выполнения;\n
		colorize – указывает, нужно ли окрасить вывод согласно типу отчёта;\n
		format – строка, определяющая формат вывода;\n
		printable_data_key – ключ для вывода значения из словаря дополнительных данных.
	Для форматирования используются следующие указатели позиций данных:
		%a – аргумент ошибки;\n
		%c – код выполнения;\n
		%d – значение из словаря дополнительных данных;\n
		%m – сообщение;\n
		%t – тип отчёта;\n
		%T – тип отчёта в верхнем регистре;\n
		%v – значение.
	"""

	# Если статус имеет нужный класс.
	if type(status) in [ExecutionStatus, ExecutionWarning, ExecutionError, ExecutionCritical] and status.message:
		# Получение литералов данных.
		Type = status.type.value.upper()
		FirstConnector = ": " if status.type.value and status.message else ""
		Message = status.message or ""
		SecondConnector = " – " if status.message and status.check_data(printable_data_key) else ""
		Value = str(status.data[printable_data_key]) if status.check_data(printable_data_key) else ""
		# Сообщение для вывода.
		Message = f"{Type}{FirstConnector}{Message}{SecondConnector}{Value}"
		# Определение цвета.
		TextColor = None

		# Если включено форматирование.
		if format:
			# Замещение указателей.
			Message = format.replace(r"%c", str(status.code))
			Message = Message.replace(r"%d", str(status.data))
			Message = Message.replace(r"%m", status.message)
			Message = Message.replace(r"%t", status.type.value)
			Message = Message.replace(r"%T", status.type.value.upper())
			Message = Message.replace(r"%v", str(status.value))
			
		# Если включена окраска.
		if colorize: 
			# Определение цвета.
			if status.type == StatussesTypes.Warning: TextColor = Styles.Colors.Yellow
			if status.type in [StatussesTypes.Error, StatussesTypes.Critical]: TextColor = Styles.Colors.Red

		# Вывод в консоль: отчёт.
		StyledPrinter(Message, text_color = TextColor)