from .Users import UserData

from telebot import TeleBot

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
		
		return IsSubscripted