import readline

#==========================================================================================#
# >>>>> ШАБЛОНЫ ВВОДА-ВЫВОДА <<<<< #
#==========================================================================================#

def Confirmation(text: str, question: str | None = None, yes: str | None = None, no: str | None = None) -> bool:
	"""
	Запрашивает подтверждение.
		text – описание вопроса;
		question – строка, обозначающая сам вопрос в используемом языке;
		yes – строка, обозначающая согласие при вводе в консоль;
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