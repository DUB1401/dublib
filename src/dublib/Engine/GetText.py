from ..Methods.Data import ToIterable

from typing import Iterable

import gettext
import os

class GetText:
	"""Абстракция управления GNU gettext."""

	#==========================================================================================#
	# >>>>> СТАТИЧЕСКИЕ АТРИБУТЫ <<<<< #
	#==========================================================================================#

	METHOD = gettext.gettext
	DOMAIN = None
	LANGUAGES = None
	PATH = None

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def initialize(domain: str, languages: Iterable[str] | str, path: str | None = None):
		"""
		Инициализирует подключение к файлам для обработки GNU gettext.

		:param domain: Домен перевода.
		:type domain: str
		:param languages: Набор требуемых языков.
		:type languages: Iterable[str] | str
		:param path: Путь к каталогу с PO файлами. По умолчанию _Locales_.
		:type path: str | None
		:raises FileNotFoundError: Не найден кастомный каталог с локализацией.
		"""

		if path and not os.path.exists(path): raise FileNotFoundError(path)

		GetText.DOMAIN = domain
		GetText.LANGUAGES = ToIterable(languages)
		GetText.PATH = path or "Locales"

		try: GetText.METHOD = gettext.translation(GetText.DOMAIN, GetText.PATH, languages = GetText.LANGUAGES).gettext
		except FileNotFoundError: pass

	def gettext(message: str, languages: list[str] | str = None) -> str:
		"""
		Возвращает локализованную строку в контексте заданного языка.
			message – оригинальная строка.
		"""
		
		if languages:
			if type(languages) == str: languages = [languages]

			try: return gettext.translation(GetText.DOMAIN, GetText.PATH, languages = languages).gettext(message)
			except FileNotFoundError: return GetText.gettext(message)

		else: return GetText.METHOD(message)
	
_ = GetText.gettext