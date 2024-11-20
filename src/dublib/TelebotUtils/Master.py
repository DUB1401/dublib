from .Users import UserData

from telebot import apihelper, REPLY_MARKUP_TYPES, TeleBot, types
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
	
	def send_message(
			self,
			chat_id: int | str,
			text: str,
			parse_mode: str | None = None,
			entities: types.List[types.MessageEntity] | None = None,
			disable_web_page_preview: bool | None = None,
			disable_notification: bool | None = None,
			protect_content: bool | None = None,
			reply_to_message_id: int | None = None,
			allow_sending_without_reply: bool | None = None,
			reply_markup: REPLY_MARKUP_TYPES | None = None,
			timeout: int | None = None,
			message_thread_id: int | None = None,
			reply_parameters: types.ReplyParameters | None = None,
			link_preview_options: types.LinkPreviewOptions | None = None,
			business_connection_id: str | None = None,
			message_effect_id: str | None = None,
		) -> types.Message:
		"""Отправляет сообщение. Автоматически выдерживает интервал при ошибке слишком частых запросов."""

		Message = None

		while not Message:
			try:
				Message = self.__Bot.send_message(
					chat_id,
					text,
					parse_mode,
					entities,
					disable_web_page_preview,
					disable_notification,
					protect_content,
					reply_to_message_id,
					allow_sending_without_reply,
					reply_markup,
					timeout,
					message_thread_id,
					reply_parameters,
					link_preview_options,
					business_connection_id,
					message_effect_id
				)

			except apihelper.ApiTelegramException as ExceptionData:

				if "Error code: 429. Description: Too Many Requests" in str(ExceptionData):
					Seconds = float(str(ExceptionData).split(" ")[-1])
					sleep(Seconds)

				else: raise ExceptionData

		return Message