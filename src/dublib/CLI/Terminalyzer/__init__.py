from .Command.Parser import _CommandParser, _ParsedCommandData
from .Command.Definition import Command
from .Enums import ParametersTypes
from .Helper import _Helper

from ...Methods.Data import ToIterable
from ... import Exceptions

from typing import Iterable
import sys

#==========================================================================================#
# >>>>> ОСНОВНОЙ КЛАСС <<<<< #
#==========================================================================================#

class Terminalyzer:
	"""Обработчик консольных параметров."""

	@property
	def helper(self) -> _Helper:
		"""Настройки модуля помощи."""

		return self.__Helper

	#==========================================================================================#
	# >>>>> ПРИВАТНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __CheckCommandsUniqueness(self, commands: list[Command]):
		"""
		Проверяет уникальность переданных для проверки команд.

		:param commands: Список команд.
		:type commands: list[Command]
		:raises Exceptions.CLI.Terminalyzer.MultipleCommandDefinition: Множественное определение команды.
		"""

		CommandsNames = [CurrentCommand.name for CurrentCommand in commands]
		for Name in CommandsNames:
			if CommandsNames.count(Name) > 1: raise Exceptions.CLI.Terminalyzer.MultipleCommandDefinition(Name)

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, input: Iterable[str] | None = None):
		"""
		Обработчик консольных параметров.

		:param input: Последовательность параметров команды, первым из которых является названия. По умолчанию берётся из *sys.argv* скрипта.
		:type input: Iterable[str] | None
		"""

		self.set_input(input)
		
		self.__Helper = _Helper(self)

	def check_commands(self, commands: list[Command] | Command) -> _ParsedCommandData | None:
		"""
		Проверяет каждое из переданных описаний команд на соответствие текущей. 

		:param commands: Описательные структуры команд или их JSON-конфигурация.
		:type commands: list[Command] | Command
		:return: При успешной проверке парсит данные команды и возвращает их.
		:rtype: ParsedCommandData | None
		:raises MultipleCommandDefinition: Несколько определений для одной команды.
		"""
		
		if not self.__CommandName: return

		commands: list[Command] = ToIterable(commands, list)
		if self.__Helper.is_enabled: commands.append(self.__Helper.command)
		CommandData: _ParsedCommandData = None
 
		self.__CheckCommandsUniqueness(commands)

		for CurrentCommand in commands:
			if CurrentCommand.name == self.__CommandName:
				CommandData = _CommandParser(CurrentCommand, self.__Parameters).parse()
				break

		if self.__Helper.is_enabled and CommandData and CommandData.name == "help":
			if CommandData.arguments: self.__Helper.generate_help_command(commands, CommandData.arguments[0], CommandData.check_flag("t"))
			else: self.__Helper.generate_help_list(commands)
		
		return CommandData

	def set_input(self, input: Iterable[str]):
		"""
		Задаёт последовательность параметров, из которых будут парситься данные команды.

		:param parameters: Последовательность параметров команды, первым из которых является названия. По умолчанию берётся из *sys.argv* скрипта.
		:type parameters: Iterable[str]
		"""

		self.__Input = input or sys.argv[1:]

		self.__CommandName = None
		self.__Parameters = tuple()

		if self.__Input: self.__CommandName = self.__Input[0]
		if len(self.__Input) > 1: self.__Parameters = self.__Input[1:]