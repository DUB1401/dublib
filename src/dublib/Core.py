from .CLI.TextStyler import FastStyler, GetStyledTextFromHTML

import logging

class ColorFormatter(logging.Formatter):
	"""Форматировщик вывода в консоль с поддержкой цветов."""

	def format(self, record: logging.LogRecord) -> str:
		"""
		Форматирует записи с поддержкой цветной палитры.

		:param record: Запись лога.
		:type record: LogRecord
		:return: Текст сообщения.
		:rtype: str
		"""
		
		Message = super().format(record)

		match record.levelno: 
			case logging.WARNING: Message = FastStyler(Message).colorize.yellow
			case logging.ERROR: Message = FastStyler(Message).colorize.red

		return Message

LOGS_HANDLER = logging.StreamHandler()
LOGS_HANDLER.setFormatter(ColorFormatter(GetStyledTextFromHTML("<b>[%(name)s]</b> %(levelname)s: %(message)s")))