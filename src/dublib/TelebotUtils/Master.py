from ..Methods.Data import ToIterable
from .Users import UserData

from typing import Callable, Iterable
from time import sleep
import logging

from telebot import apihelper, TeleBot, types

#==========================================================================================#
# >>>>> ИНИЦИАЛИЗАЦИЯ СИСТЕМЫ ЛОГГИРОВАНИЯ <<<<< #
#==========================================================================================#

# Инициализация модуля ведения логов.
Logger = logging.getLogger(__name__)
Logger.addHandler(logging.StreamHandler().setFormatter(logging.Formatter("[%(name)s] %(levelname)s: %(message)s")))
Logger.setLevel(logging.INFO)

#==========================================================================================#
# >>>>> ДОПОЛНИТЕЛЬНЫЕ КОНФИГУРАЦИИ БИБЛИОТЕК ЗАПРОСОВ <<<<< #
#==========================================================================================#

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
		
		:param bot: Бот Telegram. Вместо объекта бота можно передать токен, на основе которого будет инициализирован новый объект.
		:type bot: str | TeleBot
		"""

		if type(bot) == str: bot = TeleBot(bot)

		#---> Генерация динамических свойств.
		#==========================================================================================#
		self.__Bot = bot

	def check_user_subscriptions(self, user: UserData, chats: int | Iterable[int]) -> bool | None:
		"""
		Проверяет, состоит ли пользователь в указанных чатах. Бот должен состоять во всех проверяемых чатах.
			user – проверяемый пользователь;\n
			chats – список ID чатов.
		"""

		chats = ToIterable(chats)

		IsSubscripted = False
		Subscriptions = 0
			
		for ChatID in chats:
			
			try:
				Response = self.__Bot.get_chat_member(ChatID, user.id)
				if Response.status in ("administrator", "creator", "member", "restricted"): Subscriptions += 1
				
			except Exception as ExceptionData:
				if str(ExceptionData).endswith("chat not found"): Logger.error(f"Chat {ChatID} not found. May be bot not a member.")
		
		if Subscriptions == len(chats): IsSubscripted = True
		
		return IsSubscripted
	
	def safely_delete_messages(self, chat_id: int, messages: int | Iterable[int], complex: bool = False) -> Exception | None:
		"""
		Безопасно удаляет сообщения без выброса исключений.

		:param chat_id: ID чата.
		:type chat_id: int
		:param messages: Последовательность ID сообщений или ID конкретного сообщения.
		:type messages: int | Iterable[int]
		:param complex: При включении сообщения будут удалены одним запросом. По умолчанию `False`.
		:type complex: bool, optional
		:return: Выброшенное во время работы исключение в случае наличия такового.
		:rtype: Exception | None
		"""

		messages: tuple[int] = ToIterable(messages)
		ExceptionObject: Exception | None = None

		if complex:
			try: self.__Bot.delete_messages(chat_id, messages)
			except Exception as ExceptionData: ExceptionObject = ExceptionData

		else:
			for MessageID in messages:
				try: self.__Bot.delete_message(chat_id, MessageID)
				except Exception as ExceptionData: ExceptionObject = ExceptionData

		return ExceptionObject

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