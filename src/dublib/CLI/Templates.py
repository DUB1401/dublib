from . import readline

#==========================================================================================#
# >>>>> ШАБЛОНЫ ВВОДА-ВЫВОДА <<<<< #
#==========================================================================================#

def Confirmation(text: str, question: str | None = None, yes: str | None = None, no: str | None = None) -> bool:
	"""
	Запрашивает подтверждение пользователя.
		text – описание вопроса;\n
		question – строка, обозначающая сам вопрос в используемом языке;\n
		yes – строка, обозначающая согласие при вводе в консоль;\n
		no – строка, обозначающая отсутствие согласия при вводе в консоль.
	"""

	Response = None
	if not question: question = "Confirm?"
	if not yes: yes = "Y"
	if not no: no = "N"

	while True:
		InputLine = input(f"{text}\n{question} [{yes}/{no}]: ").strip().lower()
		if InputLine == yes.lower(): Response = True
		if InputLine == no.lower(): Response = False
		if Response != None: break

	return Response