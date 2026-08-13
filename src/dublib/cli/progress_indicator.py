import math
import sys
from typing import Literal, Self

class ProgressIndicator:
	"""Терминальный индикатор прогресса на основе протокола **OSC 9;4**."""

	#==========================================================================================#
	# >>>>> СТАТИЧЕСКИЕ АТРИБУТЫ <<<<< #
	#==========================================================================================#

	__INSTANCE: "ProgressIndicator | None" = None

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def progress(self) -> int:
		"""Процент прогресса выполнения."""

		return self.__Progress

	@property
	def state(self) -> Literal[0, 1, 2, 3, 4]:
		"""Состояние: 0 – не выполняется, 1 – прогресс, 2 – ошибка, 3 – неопределённое состояние, 4 – предупреждение."""

		return self.__State

	#==========================================================================================#
	# >>>>> ПРИВАТНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __Write(self):
		"""Отправляет управляющую последовательность прогресса в терминал."""

		sys.stdout.write(f"\x1b]9;4;{self.__State};{self.__Progress}\x1b\\")
		sys.stdout.flush()

	#==========================================================================================#
	# >>>>> СПЕЦИАЛЬНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __new__(cls: "type[Self]", *args, **kwargs) -> "ProgressIndicator":
		"""
		Инициализирует новый объект или возвращает уже существующий.

		:param cls: Текущий экземпляр объекта.
		:type cls: type[Self]
		:return: Экземпляр объекта.
		:rtype: ProgressIndicator
		"""

		if not cls.__INSTANCE:
			Instance = super().__new__(cls)
			Instance.__IS_INITIALIZED = False
			cls.__INSTANCE = Instance

		return cls.__INSTANCE
	
	def __init__(self):
		"""Терминальный индикатор прогресса на основе протокола **OSC 9;4**."""

		if self.__IS_INITIALIZED: return

		self.__State: Literal[0, 1, 2, 3, 4] = 0
		self.__Progress: int = 0

		self.__IS_INITIALIZED: bool = True

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def end(self):
		"""Завершает индикацию прогресса."""

		self.__State = 0
		self.__Progress = 0
		self.__Write()

	def error(self):
		"""Переводит индикатор в состояние ошибки."""

		self.__State = 2
		self.__Write()

	def indeterminate(self):
		"""Переводит индикатор в неопределённое состояние."""

		self.__State = 3
		self.__Write()

	def pause(self):
		"""Переводит индикатор в состояние паузы/предупреждения."""

		self.__State = 4
		self.__Write()

	def set_progress(self, progress: int | float):
		"""
		Задаёт прогресс выполнения.

		:param progress: Прогресс выполнения от 0 до 100. При передаче типа `float` производится округление по математическим правилам.
		:type progress: int | float
		:param state: Код состояния от 1 до 4: 1 – прогресс, 2 – ошибка, 3 – неопределённое состояние, 4 – предупреждение.
		:type state: Literal[1, 2, 3, 4]
		:raises ValueError: Выход за диапазон значений прогресса.
		"""

		Progress: int = int(math.floor(progress + 0.5))

		if Progress < 0 or Progress > 100:
			raise ValueError(f"Progress value must be between 0 and 100, given {Progress}.")

		self.__State = 1
		self.__Progress = Progress
		self.__Write()

		