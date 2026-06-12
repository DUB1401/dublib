from functools import wraps
from time import sleep

from telebot import apihelper, types

def ignore_frecuency_errors(function):
	"""
	Декоратор. Игнорирует ошибки частоты запросов, автоматически выжидая необходимый интервал.

	:param function: Функция или метод из библиотеки **pyTelegramBotAPI**.
	"""

	@wraps(function)
	def Wrapper(*args, **kwargs):
		Value = None
			
		try: Value = function(*args, **kwargs)
		except apihelper.ApiTelegramException as ExceptionData:

			if "Error code: 429. Description: Too Many Requests" in str(ExceptionData):
				Seconds = float(str(ExceptionData).split(" ")[-1])
				sleep(Seconds)

			else: raise ExceptionData

		else: return Value
	
	return Wrapper