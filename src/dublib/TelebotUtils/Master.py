from .Users import UserData

from telebot import apihelper, TeleBot, types
from typing import Callable
from time import sleep

class TeleMaster:
	"""Набор дополнительного функционала для бота Telegram."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def bot(self) -> TeleBot:
		"""Бот Telegram."""

		return self.__Bot

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, bot: str | TeleBot):
		"""
		Набор дополнительного функционала для бота Telegram.
			bot – бот Telegram или его токен.
		"""

		if type(bot) == str: bot = TeleBot(bot)

		#---> Генерация динамических свойств.
		#==========================================================================================#
		self.__Bot = bot

	def check_user_subscriptions(self, user: UserData, chats: int | list[int]) -> bool:
		"""
		Проверяет, состоит ли пользователь в указанных чатах.
			user – проверяемый пользователь;\n
			chats – список ID чатов.
		"""

		if type(chats) == int: chats = [chats]

		IsSubscripted = False
		Subscriptions = 0
			
		for ChatID in chats:
			
			try:
				Response = self.__Bot.get_chat_member(ChatID, user.id)
				if Response.status in ["administrator", "creator", "member", "restricted"]: Subscriptions += 1
				
			except: pass
		
		if Subscriptions == len(chats): IsSubscripted = True
		self.__Bot.send_message()
		
		return IsSubscripted
	
	#==========================================================================================#
	# >>>>> ДЕКОРАТОРЫ <<<<< #
	#==========================================================================================#

	def ignore_frecuency_errors(function: Callable) -> Callable:
		"""Игнорирует ошибки частоты запросов, автоматически выжидая необходимый интервал."""

		def new_function(*args, **kwargs) -> types.Message:
			Message = None

			while not Message:
				
				try: 
					Message = function(*args, **kwargs)

				except apihelper.ApiTelegramException as ExceptionData:

					if "Error code: 429. Description: Too Many Requests" in str(ExceptionData):
						Seconds = float(str(ExceptionData).split(" ")[-1])
						sleep(Seconds)

					else: raise ExceptionData

			return Message