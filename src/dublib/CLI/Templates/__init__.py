from .. import readline

#==========================================================================================#
# >>>>> ШАБЛОНЫ ВВОДА-ВЫВОДА <<<<< #
#==========================================================================================#

def Confirmation(text: str, question: str | None = None, yes: str | None = None, no: str | None = None) -> bool:
	"""
	Запрашивает подтверждение пользователя.

	:param text: Текст вопроса.
	:type text: str
	:param question: Строка, представляющая сам вопрос. По умолчанию `Confirm?`.
	:type question: str | None
	:param yes: Строка, обозначающая согласие при вводе в консоль. По умолчанию `Y`.
	:type yes: str | None
	:param no: Строка, обозначающая отсутствие согласия при вводе в консоль. По умолчанию `N`.
	:type no: str | None
	:return: Состояние согласия пользователя.
	:rtype: bool
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