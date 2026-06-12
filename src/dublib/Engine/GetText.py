from ..Methods.Data import ToSequence

from typing import Callable, Sequence

import gettext
import os

class GetText:
	"""Абстракция управления GNU gettext."""

	#==========================================================================================#
	# >>>>> СТАТИЧЕСКИЕ АТРИБУТЫ <<<<< #
	#==========================================================================================#

	_METHOD: Callable = gettext.gettext
	_DOMAIN: str
	_LANGUAGES: tuple[str]
	_PATH: str

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	@staticmethod
	def initialize(domain: str, languages: Sequence[str] | str, path: str | None = None):
		"""
		Инициализирует подключение к файлам для обработки GNU gettext.

		:param domain: Домен перевода.
		:type domain: str
		:param languages: Набор требуемых языков.
		:type languages: Sequence[str] | str
		:param path: Путь к каталогу с PO файлами. По умолчанию _Locales_.
		:type path: str | None
		:raises FileNotFoundError: Не найден кастомный каталог с локализацией.
		"""

		if path and not os.path.exists(path): raise FileNotFoundError(path)

		GetText._DOMAIN = domain
		GetText._LANGUAGES = ToSequence(languages)
		GetText._PATH = path or "Locales"

		try: GetText._METHOD = gettext.translation(GetText._DOMAIN, GetText._PATH, languages = GetText._LANGUAGES).gettext
		except FileNotFoundError: pass

	@staticmethod
	def gettext(message: str, languages: list[str] | str | None = None) -> str:
		"""
		Возвращает локализованную строку в контексте заданного языка.

		:param message: Оригинальная строка.
		:type message: str
		:param languages: Язык локализации.
		:type languages: list[str] | str | None, optional
		:return: _description_
		:rtype: str
		"""
		
		if languages:
			if type(languages) == str: languages = [languages]

			try: return gettext.translation(GetText._DOMAIN, GetText._PATH, languages = languages).gettext(message)
			except FileNotFoundError: return GetText.gettext(message)

		else: return GetText._METHOD(message)
	
_ = GetText.gettext