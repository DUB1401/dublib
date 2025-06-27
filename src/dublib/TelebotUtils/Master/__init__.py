from .Decorators import ignore_frecuency_errors
from ...Methods.Data import ToIterable
from ..Users import UserData

from typing import Iterable
import logging

from urllib3.exceptions import ReadTimeoutError
from requests.exceptions import ReadTimeout
from telebot import TeleBot

#==========================================================================================#
# >>>>> ИНИЦИАЛИЗАЦИЯ СИСТЕМЫ ЛОГГИРОВАНИЯ <<<<< #
#==========================================================================================#

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

		self.__Bot = TeleBot(bot) if type(bot) == str else bot

	def check_user_subscriptions(self, user: UserData, chats: int | Iterable[int], max_tries: int = 3) -> bool:
		"""
		Проверяет, состоит ли пользователь в указанных чатах. Бот должен иметь доступ ко всем проверяемым чатам.
		
		Также содержит в себе механизм повторов при превышении времени ожидания ответа от сервера.

		:param user: Данные проверяемого пользователя.
		:type user: UserData
		:param chats: ID чата или набор ID чатов, для которых производится проверка.
		:type chats: int | Iterable[int]
		:param max_tries: Количество попыток запросов. Повторные запросы отправляются только в случае превышения времени ожидания ответа. Не может быть меньше 1.
		:type max_tries: int
		:return: Возвращает `True`, если пользователь состоит во всех указанных чатах.
		:raise ValueError: Выбрасывается, если количество попыток запросов меньше 1.
		:raise urllib3.exceptions.ReadTimeoutError: Выбрасывается в случае превышения времени ожидания ответа от сервера.
		:raise requests.exceptions.ReadTimeout: Выбрасывается в случае превышения времени ожидания ответа от сервера.
		:rtype: bool
		"""

		chats = ToIterable(chats)
		if max_tries < 1: raise ValueError("Max tries can't be less than 1.")

		IsSubscripted = False
		Subscriptions = 0
			
		for ChatID in chats:
			Try = 1

			while Try <= max_tries:
				Try += 1

				try:
					Response = self.__Bot.get_chat_member(ChatID, user.id)
					if Response.status in ("administrator", "creator", "member", "restricted"): Subscriptions += 1
					
				except (ReadTimeoutError, ReadTimeout) as ExceptionData:
					if Try == max_tries: raise ExceptionData

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
		:type complex: bool
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