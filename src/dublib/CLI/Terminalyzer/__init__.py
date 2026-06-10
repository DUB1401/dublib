from .Command.Parser import _CommandParser, ParsedCommandData
from .Command.Definition import Command
from .Validators import ValidableValuesTypes
from .Helper import Helper

from ...Core import LOGS_HANDLER
from ... import Exceptions

from typing import Iterable
import logging
import sys

#==========================================================================================#
# >>>>> ИНИЦИАЛИЗАЦИЯ СИСТЕМЫ ЛОГГИРОВАНИЯ <<<<< #
#==========================================================================================#

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(LOGS_HANDLER)
LOGGER.setLevel(logging.INFO)

#==========================================================================================#
# >>>>> ОСНОВНОЙ КЛАСС <<<<< #
#==========================================================================================#

class Terminalyzer:
	"""Обработчик консольных параметров."""

	@property
	def helper(self) -> Helper:
		"""Настройки модуля помощи."""

		return self.__Helper

	#==========================================================================================#
	# >>>>> ПРИВАТНЫЕ МЕТОДЫ ВАЛИДАЦИИ <<<<< #
	#==========================================================================================#

	def __CheckSinglePositionalParametersDescriptionMissing(self, command: Command):
		"""
		Проверяет параметры позиций команд на предмет дублирования описаний в случае установки лишь одного параметра для позиции. Результат выводит в формате предупреждений.

		:param command: Определение команды.
		:type command: Command
		"""

		for CurrentPosition in command.positions:
			if CurrentPosition.description and len(CurrentPosition.parameters) == 1 and CurrentPosition.parameters[0].description:
				LOGGER.warning(f"Command: \"{command.name}\". Parametr description suppressed by position description on \"{CurrentPosition.name}\".")

	def __CheckCommandForEmptyPositions(self, command: Command):
		"""
		Проверяет команду на наличие пустых позиций.

		:param command: Определение команды.
		:type command: Command
		:raises Exceptions.CLI.Terminalyzer.EmptyPosition: Для позиции не описан ни один параметр.
		"""

		for CurrentPosition in command.positions:
			if not CurrentPosition.parameters: raise Exceptions.CLI.Terminalyzer.EmptyPosition(command.name, CurrentPosition.name)

		return command

	def __CheckCommandsUniqueness(self, commands: list[Command]):
		"""
		Проверяет уникальность переданных для проверки команд.

		:param commands: Список команд.
		:type commands: list[Command]
		:raises Exceptions.CLI.Terminalyzer.MultipleCommandDefinition: Множественное определение команды.
		"""

		CommandsNames = tuple(CurrentCommand.name for CurrentCommand in commands)
		for Name in CommandsNames:
			if CommandsNames.count(Name) > 1: raise Exceptions.CLI.Terminalyzer.MultipleCommandDefinition(Name)

	def __ValidateCommandsDefinitions(self, commands: list[Command]):
		"""
		Проводит валидацию определений команд.

		:param command: Список определений команд.
		:type command: list[Command]
		:raises Exceptions.CLI.Terminalyzer.EmptyPosition: Для позиции не описан ни один параметр.
		:raises Exceptions.CLI.Terminalyzer.MultipleCommandDefinition: Множественное определение команды.
		"""

		self.__CheckCommandsUniqueness(commands)

		for CurrentCommand in commands:
			self.__CheckSinglePositionalParametersDescriptionMissing(CurrentCommand)
			self.__CheckCommandForEmptyPositions(CurrentCommand)

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
		
		self.__Helper = Helper()

	def check_commands(self, commands: list[Command]) -> ParsedCommandData | None:
		"""
		Проверяет текущую команду на соответствие одному из переданных описаний.

		:param commands: Список описаний команд.
		:type commands: list[Command]
		:return: При успешной проверке парсит данные команды и возвращает их.
		:rtype: ParsedCommandData | None
		:raises Exceptions.CLI.Terminalyzer.EmptyPosition: Для позиции не описан ни один параметр.
		:raises Exceptions.CLI.Terminalyzer.MultipleCommandDefinition: Множественное определение команды.
		"""
		
		if not self.__CommandName: return

		self.__ValidateCommandsDefinitions(commands)
		if self.__Helper.is_enabled: commands.append(self.__Helper.command)
		CommandData: ParsedCommandData = None
 
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