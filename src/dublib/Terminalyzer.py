from dublib.Exceptions.Terminalyzer import *
from dublib.Methods import ReadJSON
from urllib.parse import urlparse

import enum
import sys
import os

#==========================================================================================#
# >>>>> ВСПОМОГАТЕЛЬНЫЕ ТИПЫ ДАННЫХ <<<<< #
#==========================================================================================#

class ArgumentsTypes(enum.Enum):
	"""
	Перечисление типов аргументов.
	"""

	All = "all"
	Number = "number"
	ValidPath = "validpath"
	Text = "text"
	URL = "url"
	
class Command:
	"""
	Контейнер описания команды.
	"""

	#==========================================================================================#
	# >>>>> СВОЙСТВА ТОЛЬКО ДЛЯ ЧТЕНИЯ <<<<< #
	#==========================================================================================#

	@property
	def arguments(self) -> list:
		"""
		Список аргументов.
		"""

		return self.__Arguments
	
	@property
	def description(self) -> str:
		"""
		Описание команды.
		"""

		return self.__Description

	@property
	def flags_indicator(self) -> str:
		"""
		Индикатор флагов.
		"""

		return self.__FlagIndicator

	@property
	def flags_positions(self) -> list:
		"""
		Список позиций флагов.
		"""

		return self.__FlagsPositions
	
	@property
	def keys_indicator(self) -> str:
		"""
		Индикатор ключей.
		"""

		return self.__KeyIndicator
	
	@property
	def keys_positions(self) -> list:
		"""
		Список позиций ключей.
		"""

		return self.__KeysPositions
	
	@property
	def max_parameters(self) -> int:
		"""
		Максимальное количество параметров.
		"""

		return self.__MaxArgc

	@property
	def min_parameters(self) -> int:
		"""
		Минимальное количество параметров.
		"""

		return self.__MinArgc
 
	@property
	def name(self) -> str:
		"""
		Название команды.
		"""

		return self.__Name

	#==========================================================================================#
	# >>>>> МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __CalculateMaxParameters(self):
		"""
		Подсчитывает максимальное количество параметров.
		"""

		# Обнуление максимального количества параметров.
		self.__MaxArgc = 0

		# Для каждой позиции флага.
		for FlagsPostionIngex in range(0, len(self.__FlagsPositions)):

			# Если позиция флага не лежит на слое, посчитать её.
			if self.__FlagsPositions[FlagsPostionIngex]["layout-index"] == None: self.__MaxArgc += 1
				
		# Для каждой позиции ключа.
		for KeysPostionIngex in range(0, len(self.__KeysPositions)):

			# Если позиция ключа не лежит на слое, посчитать её за 2 параметра (ключ-значение).
			if self.__KeysPositions[KeysPostionIngex]["layout-index"] == None: self.__MaxArgc += 2

		# Подсчёт количества аргументов.
		self.__MaxArgc += len(self.__Arguments)

		# Для каждого слоя.
		for LayoutIndex in self.__Layouts.keys():
			
			# Если на слое лежит ключ.
			if self.__Layouts[LayoutIndex]["keys"] > 0:
				# Посчитать слой за 2 параметра.
				self.__MaxArgc += 2

			else:
				# Посчитать слой за 1 параметр.
				self.__MaxArgc += 1

	def __CalculateMinParameters(self):
		"""
		Подсчитывает минимальное количество параметров.
		"""

		# Обнуление минимального количества параметров.
		self.__MinArgc = 0
		
		# Для каждой позиции флага.
		for FlagsPostionIngex in range(0, len(self.__FlagsPositions)):
			
			# Если позиция флага не лежит на слое и является важной, посчитать её.
			if self.__FlagsPositions[FlagsPostionIngex]["layout-index"] == None and self.__FlagsPositions[FlagsPostionIngex]["important"] == True: self.__MinArgc += 1
		
		# Для каждой позиции ключа.
		for KeysPostionIngex in range(0, len(self.__KeysPositions)):
			
			# Если позиция ключа не лежит на слое и является важной, посчитать её за 2 параметра (ключ-значение).
			if self.__KeysPositions[KeysPostionIngex]["layout-index"] == None and self.__KeysPositions[KeysPostionIngex]["important"] == True: self.__MinArgc += 2
		
		# Для каждого аргумента.
		for Argument in self.__Arguments:

			# Если аргумент не лежит на слое и является важным, посчитать его.
			if Argument["layout-index"] == None and Argument["important"] == True: self.__MinArgc += 1
		
		# Для каждого слоя.
		for LayoutIndex in self.__Layouts.keys():
			
			# Если слой является важным и содержит ключи.
			if self.__Layouts[LayoutIndex]["important"] == True and self.__Layouts[LayoutIndex]["keys"] > 0:
				# Посчитать слой за 2 параметра.
				self.__MinArgc += 1
			
			else:
				# Посчитать слой за 1 параметр.
				self.__MaxArgc += 1
		
	def __InitializeLayout(self, layout_index: int):
		"""
		Инициализирует описательную структуру слоя.
			layout_index – индекс слоя.
		"""
		
		# Преобразование индекса слоя в строку.
		layout_index = str(layout_index)
		# Если слой с таким индексом не описан, создать для него структуру.
		if layout_index not in self.__Layouts.keys(): self.__Layouts[layout_index] = {"arguments": 0, "flags": 0, "keys": 0, "important": False}
				
	def __SetLayoutAsImportant(self, layout_index: int):
		"""
		Делает все параметры слоя важными.
			layout_index – индекс слоя.
		"""
		
		# Установка важности слоя.
		self.__Layouts[str(layout_index)]["important"] = True
		
		# Для каждой позиции флага.
		for FlagPositionIndex in range(len(self.__FlagsPositions)):

			# Если позиция флага лежит на важном слое, сделать ей важной.
			if self.__FlagsPositions[FlagPositionIndex]["layout-index"] == layout_index: self.__FlagsPositions[FlagPositionIndex]["important"] = True
				
		# Для каждой позиции ключа.
		for KeyPositionIndex in range(len(self.__KeysPositions)):

			# Если позиция ключа лежит на важном слое, сделать её важной.
			if self.__KeysPositions[KeyPositionIndex]["layout-index"] == layout_index: self.__KeysPositions[KeyPositionIndex]["important"] = True
				
		# Для каждого аргумента.
		for ArgumentIndex in range(len(self.__Arguments)):

			# Если аргумент лежит на важном слое, сделать его важным.
			if self.__Arguments[ArgumentIndex]["layout-index"] == layout_index: self.__Arguments[ArgumentIndex]["important"] = True
	
	def __init__(self, name: str, description: str | None = None):
		"""
		Контейнер описания команды.
			name – название команды.
		"""

		#---> Генерация динамических свойств.
		#==========================================================================================#
		# Список флагов.
		self.__FlagsPositions = list()
		# Список ключей.
		self.__KeysPositions = list()
		# Индикатор ключа.
		self.__KeyIndicator = "--"
		# Индикатор флага.
		self.__FlagIndicator = "-"
		# Список аргументов.
		self.__Arguments = list()
		# Название команды.
		self.__Name = name
		# Максимальное количество аргументов.
		self.__MaxArgc = 0
		# Минимальное количество аргументов.
		self.__MinArgc = 0
		# Словарь, предоставляющий список слоёв и количество параметров на них.
		self.__Layouts = dict()
		# Описание команды.
		self.__Description = description

	def add_argument(self, type: ArgumentsTypes = ArgumentsTypes.All, important: bool = False, layout_index: int | None = None):
		"""
		Добавляет аргумент к команде.
			type – тип аргумента;
			important – является ли аргумент обязательным;
			layout_index – индекс слоя, на который помещается аргумент.
		"""
		
		# Запись аргумента в описание команды.
		self.__Arguments.append({"type": type, "important": important, "layout-index": layout_index})

		# Если задан важный слой.
		if layout_index != None:
			# Инициализация слоя.
			self.__InitializeLayout(layout_index)
			# Инкремент количества аргументов на слое.
			self.__Layouts[str(layout_index)]["arguments"] += 1
			# Если аргумент важный, сделать слой важным.
			if important == True: self.__SetLayoutAsImportant(layout_index)	
				
		# Вычисление максимального и минимального количества аргументов.
		self.__CalculateMaxParameters()
		self.__CalculateMinParameters()

	def add_flag_position(self, flags: list[str], important: bool = False, layout_index: int | None = None):
		"""
		Добавляет позицию флага к команде.
			flags – список названий флагов;
			important – является ли флаг обязательным;
			layout_index – индекс слоя, на который помещается флаг.
		"""
		
		# Запись позиции ключа в описание команды.
		self.__FlagsPositions.append({"names": flags, "important": important, "layout-index": layout_index})
		
		# Если задан важный слой.
		if layout_index != None:
			# Инициализация слоя.
			self.__InitializeLayout(layout_index)
			# Инкремент количества флагов на слое.
			self.__Layouts[str(layout_index)]["flags"] += 1
			# Если позиция важная, сделать слой важным.
			if important == True: self.__SetLayoutAsImportant(layout_index)	

		# Вычисление максимального и минимального количества аргументов. 
		self.__CalculateMaxParameters()
		self.__CalculateMinParameters()

	def add_key_position(self, keys: list[str], types: list[ArgumentsTypes] | ArgumentsTypes, important: bool = False, layout_index: int | None = None):
		"""
		Добавляет позицию ключа к команде.
			keys – список названий ключей;
			types – список типов значений для конкретных ключей или один тип для всех значений;
			important – является ли ключ обязательным;
			layout_index – индекс слоя, на который помещается ключ.
		"""
		
		# Если для всех значений установлен один тип аргумента.
		if type(types) == ArgumentsTypes:
			# Буфер заполнения.
			Bufer = list()
			# На каждый ключ продублировать тип значения.
			for Type in keys: Bufer.append(types)
			# Замена аргумента буфером.
			types = Bufer 

		# Запись позиции ключа в описание команды.
		self.__KeysPositions.append({"names": keys, "types": types, "important": important, "layout-index": layout_index})

		# Если задан важный слой.
		if layout_index != None:
			# Инициализация слоя.
			self.__InitializeLayout(layout_index)
			# Инкремент количества ключей на слое.
			self.__Layouts[str(layout_index)]["keys"] += 1
			# Если позиция важная, сделать слой важным.
			if important == True: self.__SetLayoutAsImportant(layout_index)	

		# Вычисление максимального и минимального количества аргументов. 
		self.__CalculateMaxParameters()
		self.__CalculateMinParameters()

	def get_layout_arguments_count(self, layout_index: int) -> int:
		"""
		Возвращает количество аргументов на слое.
			layout_index – индекс слоя для поиска аргументов.
		"""
		
		# Количество аргументов на слое.
		LayoutArgumentsCount = 0

		# Для каждого аргумента.
		for Argument in self.__Arguments:

			# Если аргумент лежит на слое, посчитать его.
			if Argument["layout-index"] == layout_index: LayoutArgumentsCount += 1
				
		return LayoutArgumentsCount
	
	def get_layout_flags(self, layout_index: int, add_indicator: bool = False) -> list[str]:
		"""
		Возвращает список всех возможных флагов на слое.
			layout_index – индекс слоя для поиска флагов;
			add_indicator – указывает, нужно ли добавить индикаторы к названиям флагов.
		"""
		
		# Список флагов на слое.
		LayoutFlags = list()
		
		# Для каждой позиции флага.
		for FlagPosition in self.__FlagsPositions:
			
			# Если флаг лежит на слое.
			if FlagPosition["layout-index"] == layout_index:
				
				# Если не нужно добавлять индикаторы.
				if add_indicator == False:
					# Запись флагов текущей позиции.
					LayoutFlags += FlagPosition["names"]
					
				else:
					
					# Для каждого названия флага на позиции.
					for FlagName in FlagPosition["names"]:
						# Запись флага с индикатором.
						LayoutFlags.append(self.__FlagIndicator + FlagName)
		
		return LayoutFlags
	
	def get_layout_keys(self, layout_index: int, add_indicator: bool = False) -> list[str]:
		"""
		Возвращает список всех возможных ключей на слое.
			layout_index – индекс слоя для поиска ключей;
			add_indicator – указывает, нужно ли добавить индикаторы к названиям ключей.
		"""
		
		# Список ключей на слое.
		LayoutKeys = list()
		
		# Для каждой позиции ключа.
		for KeyPosition in self.__KeysPositions:
			
			# Если ключ лежит на слое.
			if KeyPosition["layout-index"] == layout_index:
				
				# Если не нужно добавлять индикаторы.
				if add_indicator == False:
					# Запись ключей текущей позиции.
					LayoutFlags += KeyPosition["names"]
					
				else:

					# Для каждого названия ключа на позиции.
					for KeyName in KeyPosition["names"]:
						# Запись ключа с индикатором.
						LayoutKeys.append(self.__KeyIndicator + KeyName)
		
		return LayoutKeys
	
	def set_description(self, description: str):
		"""
		Задаёт описание команды.
			description – описание команды.
		"""

		self.__Description = description

	def set_flags_indicator(self, indicator: str):
		"""
		Задаёт индикатор флагов.
			indicator – индикатор флагов.
		"""

		# Если новый индикатор флага не повторяет индикатор ключа.
		if indicator != self.__KeyIndicator:
			# Установка нового индикатора.
			self.__FlagIndicator = indicator

		else:
			# Выброс исключения.
			raise IdenticalIndicators()

	def set_keys_indicator(self, indicator: str):
		"""
		Задаёт индикатор ключей.
			indicator – индикатор ключей.
		"""

		# Если новый индикатор ключа не повторяет индикатор флага.
		if indicator != self.__FlagIndicator:
			# Установка нового индикатора.
			self.__KeyIndicator = indicator

		else:
			# Выброс исключения.
			raise IdenticalIndicators()

class CommandData:
	"""
	Контейнер хранения данных обработанной команды.
	"""

	def __init__(self, name: str, flags: list[str] = list(), keys: list[str] = list(), values: dict[str, str] = dict(), arguments: list[str] = list()):
		"""
		Контейнер хранения данных обработанной команды.
			name – название команды;
			flags – список активированных флагов;
			keys – список активированных ключей;
			values – словарь значений активированных ключей;
			Arguments – список аргументов.
		"""

		#---> Генерация динамических свойств.
		#==========================================================================================#
		# Значение аргумента.
		self.arguments = arguments
		# Словарь значений ключей.
		self.values = values
		# Список активированных флагов.
		self.flags = flags
		# Список активированных ключей.
		self.keys = keys
		# Название команды.
		self.name = name

	def __str__(self):
		return str({
			"name": self.name, 
			"flags": self.flags, 
			"keys": self.keys, 
			"values": self.values, 
			"arguments": self.arguments
		})

class Config:
	"""
	JSON-конфигурация команд.
	"""

	#==========================================================================================#
	# >>>>> СВОЙСТВА ТОЛЬКО ДЛЯ ЧТЕНИЯ <<<<< #
	#==========================================================================================#

	@property
	def arguments_types(self) -> dict:
		"""
		Словарь строковых и классовых представлений типов аргументов.
		"""

		return {
			"all": ArgumentsTypes.All,
			"number": ArgumentsTypes.Number,
			"validpath": ArgumentsTypes.ValidPath,
			"text": ArgumentsTypes.Text,
			"url": ArgumentsTypes.URL,
		}

	#==========================================================================================#
	# >>>>> МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __ProcessTypes(self, types: list[str] | str) -> list[str] | str:
		"""
		Конвертирует текстовое представление типов в классовое.
			types – список названий типов или конкретное название.
		"""

		# Типы аргументов.
		Types = list()

		# Если передан список типов.
		if type(types) == list:
			# Запись всех типов.
			Types = types

		else:
			# Дополнение списка типом.
			Types.append(types)

		# Для каждого типа.
		for Index in range(0, len(Types)):
			# Замещение строкового типа аргумента классовым.
			Types[Index] = self.arguments_types[Types[Index]]

		# Если передан один тип, вернуть строку, а не список.
		if len(Types) == 1: Types = Types[0]

		return Types

	def __init__(self, path: str | None = None):
		"""
		JSON-конфигурация команд.
		"""

		#---> Генерация динамических свойств.
		#==========================================================================================#
		# Конфигурация.
		self.__Config = None

		# Если указан путь к файлу, прочитать его.
		if path != None: self.read(path)

	def build_commands(self) -> list[Command]:
		"""
		Строит список описаний команд из конфигурации.
		"""

		# Список описательных структур команд.
		CommandsList = list()

		# Для каждой команды.
		for CommandName in self.__Config["commands"].keys():
			# Буфер обрабатываемой команды.
			Bufer = self.__Config["commands"][CommandName]
			# Структура команды.
			CommandDescription = Command(CommandName)

			# Если указано описание команды, игнорировать его.
			if "description" in Bufer.keys(): CommandDescription.set_description(Bufer["description"])

			# Если указан индикатор флагов, записать его.
			if "flags-indicator" in Bufer.keys(): CommandDescription.set_flags_indicator(Bufer["flags-indicator"])

			# Если указан индикатор ключей, записать его.
			if "keys-indicator" in Bufer.keys(): CommandDescription.set_keys_indicator(Bufer["keys-indicator"])

			# Если для команды указаны позиции флагов.
			if "flags" in Bufer.keys():
				
				# Для каждого флага.
				for FlagPosition in Bufer["flags"]:
					# Состояние: является ли позиция важной.
					IsImportant = False
					# Индекс слоя.
					LayoutIndex = None
					# Если определено состояние важности, записать его.
					if "important" in FlagPosition.keys(): IsImportant = FlagPosition["important"]
					# Если определён индекс слоя, записать его.
					if "layout_index" in FlagPosition.keys(): LayoutIndex = FlagPosition["layout_index"]
					# Формирование позиции флага.
					CommandDescription.add_flag_position(FlagPosition["names"], IsImportant, LayoutIndex)
			
			# Если для команды указаны позиции ключей.
			if "keys" in Bufer.keys():
				
				# Для каждого ключа.
				for KeyPosition in Bufer["keys"]:
					# Типы значений.
					Types = ArgumentsTypes.All
					# Состояние: является ли позиция важной.
					IsImportant = False
					# Индекс слоя.
					LayoutIndex = None
					# Если указаны специфические типы, преобразовать их строковые представления в классовые.
					if "types" in KeyPosition.keys(): Types = self.__ProcessTypes(KeyPosition["types"])
					# Если определено состояние важности, записать его.
					if "important" in KeyPosition.keys(): IsImportant = KeyPosition["important"]
					# Если определён индекс слоя, записать его.
					if "layout_index" in KeyPosition.keys(): LayoutIndex = KeyPosition["layout_index"]
					# Формирование позиции ключа.
					CommandDescription.add_key_position(KeyPosition["names"], Types, IsImportant, LayoutIndex)

			# Если для команды указаны аргументы.
			if "arguments" in Bufer.keys():
				
				# Для каждого аргумента.
				for Argument in Bufer["arguments"]:
					# Типы значений.
					Types = ArgumentsTypes.All
					# Состояние: является ли позиция важной.
					IsImportant = False
					# Индекс слоя.
					LayoutIndex = None
					# Если указаны специфические типы, преобразовать их строковые представления в классовые.
					if "type" in Argument.keys(): Types = self.__ProcessTypes(Argument["type"])
					# Если определено состояние важности, записать его.
					if "important" in Argument.keys(): IsImportant = Argument["important"]
					# Если определён индекс слоя, записать его.
					if "layout_index" in Argument.keys(): LayoutIndex = Argument["layout_index"]
					# Формирование аргумента.
					CommandDescription.add_argument(Types, IsImportant, LayoutIndex)

			# Запись команды в список.
			CommandsList.append(CommandDescription)

		return CommandsList

	def read(self, path: str):
		"""
		Читает конфигурацию из JSON файла.
			path – путь к файлу.
		"""

		self.__Config = ReadJSON(path)

#==========================================================================================#
# >>>>> ОСНОВНОЙ КЛАСС <<<<< #
#==========================================================================================#

class Terminalyzer:
	"""
	Обработчик консольных аргументов.
	"""

	def __CheckArgc(self, command: Command):
		"""
		Проверяет соответвтсие количества аргументов.
			command – описательная структура команды.
		"""

		# Если аргументов слишком много, выбросить исключение.
		if len(self.__Argv) - 1 > command.max_parameters: raise TooManyArguments(" ".join(self.__Argv))
		# Если аргументов слишком мало, выбросить исключение.
		if len(self.__Argv) - 1 < command.min_parameters: raise NotEnoughArguments(" ".join(self.__Argv))
	
	def __CheckArguments(self, command: Command) -> list[str | None]:
		"""
		Возвращает значения аргументов.
			command – описательная структура команды.
		"""
		
		# Значения аргументов.
		Values = list()
		# Список возможных аргументов.
		ArgumentsDescription = command.arguments
		# Список параметров без команды.
		ParametersList = self.__Argv[1:]
		# Список незадействованных параметров.
		FreeParameters = list()

		# Для каждого параметра.
		for PositionIndex in range(0, len(ParametersList)):
			
			# Если позиция не лежит на слое.
			if self.__LayoutsStatuses[PositionIndex] == None:
				
				# Если позиция не была задействована.
				if self.__PositionsStatuses[PositionIndex] == False:
					# Записать параметр как свободный.
					FreeParameters.append(ParametersList[PositionIndex])
			
			else:
				
				# Если позиция не была задействована.
				if self.__PositionsStatuses[PositionIndex] == False:
					# Записать параметр как свободный.
					FreeParameters.append(ParametersList[PositionIndex])
						
				else:
					# Списки названий флагов и ключей.
					FlagsNames = command.get_layout_flags(self.__LayoutsStatuses[PositionIndex], True)
					KeysNames = command.get_layout_keys(self.__LayoutsStatuses[PositionIndex], True)
					# Если параметр является флагом или ключём того же слоя, записать пустое значение.
					if ParametersList[PositionIndex] in FlagsNames or ParametersList[PositionIndex] in KeysNames: FreeParameters.append(None)		

		# Если количество свободных параметров (игнорируя None) превышает максимальное, выбросить исключение.
		if len([x for x in FreeParameters if x != None]) > len(ArgumentsDescription): raise TooManyArguments(" ".join(self.__Argv))

		# Для каждого свободного параметра.
		for Index in range(0, len(FreeParameters)):
			
			# Если параметр не исключён.
			if FreeParameters[Index] != None:

				# Если параметр соответствует типу.
				if self.__CheckArgumentsTypes(FreeParameters[Index], ArgumentsDescription[Index]["type"]) == True:
					# Сохранение параметра в качестве аргумента.
					Values.append(FreeParameters[Index])

				else:
					# Выброс исключения.
					raise InvalidArgumentsTypes(FreeParameters[Index], command.arguments["type"])
				
			else:
				# Сохранение пустого значения аргумента.
				Values.append(None)

		return Values
	
	def __CheckArgumentsTypes(self, value: str, type_name: ArgumentsTypes = ArgumentsTypes.All) -> bool:
		"""
		Проверяет значение аргумента.
			value – значение аргумента;
			type_name – тип аргумента.
		"""
		
		# Если требуется проверить специфический тип аргумента.
		if type_name != ArgumentsTypes.All:
			
			# Если аргумент должен являться числом.
			if type_name == ArgumentsTypes.Number:

				# Если вся строка, без учёта отрицательного знака, не является числом, выбросить исключение.
				if value.lstrip('-').isdigit() == False: raise InvalidArgumentsTypes(value, "Number")
				
			# Если аргумент должен являться валидным путём к файлу или директории.
			if type_name == ArgumentsTypes.ValidPath:

				# Если строка не является валидным путём к файлу или директории, выбросить исключение.
				if os.path.exists(value) == False: raise InvalidArgumentsTypes(value, "ValidPath")

			# Если аргумент должен являться набором букв.
			if type_name == ArgumentsTypes.Text:

				# Если строка содержит небуквенные символы, выбросить исключение.
				if value.isalpha() == False: raise InvalidArgumentsTypes(value, "Text")

			# Если аргумент должен являться URL.
			if type_name == ArgumentsTypes.URL:

				# Если строка не является URL, выбросить исключение.
				if bool(urlparse(value).scheme) == False: raise InvalidArgumentsTypes(value, "URL")

		return True

	def __CheckCommand(self, command: Command) -> CommandData | None:
		"""
		Выполняет проверку соответствия конкретной команде.
			command – описательная структура команды.
		"""

		# Если название команды соответствует.
		if self.__CheckName(command) == True:

			# Если данные команды не кэшированы.
			if self.__CommandData == None:
				# Заполнение статусов позиций параметров.
				self.__PositionsStatuses = [False] * (len(self.__Argv) - 1)
				# Заполнение статусов слоёв параметров.
				self.__LayoutsStatuses = [None] * (len(self.__Argv) - 1)
				# Проверка соответствия количества параметров.
				self.__CheckArgc(command)
				# Получение названия команды.
				Name = command.name
				# Проверка активированных флагов.
				Flags = self.__CheckFlags(command)
				# Проверка активированных ключей.
				Keys = self.__CheckKeys(command)
				# Получение аргументов.
				Arguments = self.__CheckArguments(command)
				# Данные проверки команды.
				self.__CommandData = CommandData(Name, Flags, list(Keys.keys()), Keys, Arguments)

		return self.__CommandData

	def __CheckFlags(self, command: Command) -> list[str]:
		"""
		Возвращает список активных флагов.
			command – описательная структура команды.
		"""

		# Список позиций флагов.
		FlagsPositions = command.flags_positions
		# Индикатор флага.
		FlagIndicator = command.flags_indicator
		# Список активных флагов.
		Flags = list()

		# Для каждой позиции флага.
		for PositionIndex in range(0, len(FlagsPositions)):
			# Состояние: активирован ли флаг на позиции.
			IsPositionActivated = False

			# Для каждого названия флага на позиции.
			for FlagName in FlagsPositions[PositionIndex]["names"]:

				# Если индикатор с названием флага присутствует в параметрах.
				if FlagIndicator + FlagName in self.__Argv:
					# Установка активного статуса позиции параметра команды.
					self.__PositionsStatuses[self.__Argv.index(FlagIndicator + FlagName) - 1] = True
					
					# Если взаимоисключающий флаг на данной позиции не был активирован.
					if IsPositionActivated == False:
						# Установка активного статуса для флага.
						Flags.append(FlagName)
						# Блокировка позиции.
						IsPositionActivated = True
						
						# Если для флага задан слой.
						if FlagsPositions[PositionIndex]["layout-index"] != None:
							# Индекс слоя текущей позиции.
							LayoutIndex = FlagsPositions[PositionIndex]["layout-index"]
							
							# Если индекс слоя текущей позиции флага не активен.
							if LayoutIndex not in self.__LayoutsStatuses:
								# Активация слоя.
								self.__LayoutsStatuses[self.__Argv.index(FlagIndicator + FlagName) - 1] = LayoutIndex
								
							else:
								# Выброс исключения.
								raise MutuallyExclusivePositions(" ".join(self.__Argv))

					else:
						# Выброс исключения.
						raise MutuallyExclusiveFlags(" ".join(self.__Argv))

		return Flags

	def __CheckKeys(self, command: Command) -> dict | list[int]:
		"""
		Возвращает словарь активных ключей и их содержимое.
			command – описательная структура команды.
		"""

		# Список позиций ключей.
		KeysPositions = command.keys_positions
		# Индикатор ключа.
		KeyIndicator = command.keys_indicator
		# Словарь статусов ключей.
		Keys = dict()
		
		# Для каждой позиции ключа.
		for PositionIndex in range(0, len(KeysPositions)):
			# Состояние: активирован ли ключ для позиции.
			IsPositionActivated = False

			# Для каждого названия ключа на позиции.
			for KeyIndex in range(0, len(KeysPositions[PositionIndex]["names"])):
				# Название ключа.
				KeyName = KeysPositions[PositionIndex]["names"][KeyIndex]

				# Если индикатор с названием ключа присутствует в параметрах.
				if KeyIndicator + KeyName in self.__Argv:
					# Установка активного статуса позициям параметров команды.
					self.__PositionsStatuses[self.__Argv.index(KeyIndicator + KeyName) - 1] = True
					self.__PositionsStatuses[self.__Argv.index(KeyIndicator + KeyName)] = True

					# Если взаимоисключающий ключ на данной позиции не был активирован.
					if IsPositionActivated == False:
						# Установка значения для ключа.
						Keys[KeyName] = self.__Argv[self.__Argv.index(KeyIndicator + KeyName) + 1]
						# Блокировка позиции.
						IsPositionActivated = True
						# Проверка типа значения ключа.
						self.__CheckArgumentsTypes(Keys[KeyName], KeysPositions[PositionIndex]["types"][KeyIndex])
						
						# Если для ключа задан слой.
						if KeysPositions[PositionIndex]["layout-index"] != None:
							# Индекс слоя текущей позиции.
							LayoutIndex = KeysPositions[PositionIndex]["layout-index"]
							
							# Если индекс слоя текущей позиции ключа не активен.
							if LayoutIndex not in self.__LayoutsStatuses:
								# Активация слоя.
								self.__LayoutsStatuses[self.__Argv.index(KeyIndicator + KeyName) - 1] = LayoutIndex
								
							else:
								# Выброс исключения.
								raise MutuallyExclusivePositions(" ".join(self.__Argv))

					else:
						# Выброс исключения.
						raise MutuallyExclusiveKeys(" ".join(self.__Argv))

		return Keys
			
	def __CheckName(self, command: Command) -> bool:
		"""
		Проверяет соответствие названия команды.
			command – описательная структура команды.
		"""
		
		# Состояние: определена ли команда.
		IsDetermined = False

		# Если переданы параметры и имя команды определено, переключить статус проверки.
		if len(self.__Argv) > 0 and command.name == self.__Argv[0]: IsDetermined = True

		return IsDetermined

	def __CreateBaseHelp(self, commands: list[Command]) -> str | None:
		# Буфер базовой помощи.
		BaseHelp = ""
		# Модификатор выравнивания.
		Modificator = 0

		# Если используется автовыравнивание.
		if self.__Ljust == 0:
			# Список названий команд.
			CommandsNames = list()
			# Для каждой команды записать имя.
			for CurrentCommand in commands: CommandsNames.append(CurrentCommand.name)
			# Вычисление длиннейшей строки.
			Modificator = len(max(CommandsNames, key = len))

		# Если задано конкретное значение выравнивания.
		elif self.__Ljust != None:
			# Установка конкретного значения.
			Modificator = self.__Ljust

		# Для каждой команды.
		for CurrentCommand in commands:
			# Добавление имени.
			BaseHelp += CurrentCommand.name.ljust(Modificator)
			# Добавление описания.
			if CurrentCommand.description != None: BaseHelp += " " + CurrentCommand.description
			# Завершение строки.
			BaseHelp += "\n"

		# Обнуление пустой помощи.
		if BaseHelp == "": BaseHelp = None

		return BaseHelp

	def __init__(self, source: list[str] = sys.argv[1:]):
		"""
		Обработчик консольных аргументов.
			source – список из названия команды и её параметров
		"""

		#---> Генерация динамических свойств.
		#==========================================================================================#
		# Список задействованных позиций.
		self.__PositionsStatuses = list()
		# Список задействованных слоёв.
		self.__LayoutsStatuses = list()
		# Кэшированные данные команды.
		self.__CommandData = None
		# Состояние: используется ли помощь.
		self.__EnableHelp = False
		# Метод вывода данных помощи.
		self.__OutMethod = None
		# Переданные параметры.
		self.__Argv = source
		# Модификатор выравнивания базовой помощи.
		self.__Ljust = None

	def check_commands(self, commands: list[Command] | Command | Config) -> CommandData | None:
		"""
		Выполняет проверку соответствия списку команд.
			commands – список описательных структур команд.
		"""

		# Если тип обрабатываемого значения – описание команды.
		if type(commands) == Command:
			# Преобразование команды в список.
			commands = [commands]

		# Если тип обрабатываемого значения – описание команды.
		elif type(commands) == Config:
			# Преобразование конфигурации в список команд.
			commands = commands.build_commands()

		# Проверка каждой команды из списка.
		for CurrentCommand in commands: self.__CheckCommand(CurrentCommand)

		# Если включена обработка помощи 
		if self.__EnableHelp == True and self.__CommandData.name == "help":
			# Буфер вывода.
			Out = None
			# Если нет аргументов, создать базовую помощь.
			if len(self.__CommandData.arguments) == 0: Out = self.__CreateBaseHelp(commands)
			# Отправка помощи в вывод.
			self.__OutMethod(Out)

		return self.__CommandData

	def enable_help(self, out_method: any = print, ljust: int | None = 0):
		"""
		Включает обработку дополнительной команды вывода помощи.
			out_method – указывает функцию, в которую будет перенаправлен вывод помощи;
			ljust – задаёт длину названия команд для выравнивания методом добавления пробелов (0 включает автоматическое выравнивание по самой длинной команде).
		"""

		# Установка параметров.
		self.__EnableHelp = True
		self.__OutMethod = out_method
		self.__Ljust = ljust

	def set_source(self, source: list[str]):
		"""
		Задаёт обрабатываемый источник. Первым элементом списка обязательно должно являться название команды.
			source – список из названия команды и её параметров
		"""

		self.__Argv = source