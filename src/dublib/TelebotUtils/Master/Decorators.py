from typing import Callable
from time import sleep

from telebot import apihelper, types

def ignore_frecuency_errors(function: Callable) -> Callable:
	"""
	Декоратор. Игнорирует ошибки частоты запросов, автоматически выжидая необходимый интервал.

	:param function: Функция или метод из библиотеки **pyTelegramBotAPI**.
	:type function: Callable
	:return: Декорированная функция или метод.
	:rtype: Callable
	"""

	def new_function(*args, **kwargs) -> types.Message:
		Value = None
			
		try: Value = function(*args, **kwargs)
		except apihelper.ApiTelegramException as ExceptionData:

			if "Error code: 429. Description: Too Many Requests" in str(ExceptionData):
				Seconds = float(str(ExceptionData).split(" ")[-1])
				sleep(Seconds)

			else: raise ExceptionData

		else: return Value
	
	return new_function