from dublib.Exceptions.Terminalyzer import *
from urllib.parse import urlparse

import enum
import sys
import os

#==========================================================================================#
# >>>>> ВСПОМОГАТЕЛЬНЫЕ ТИПЫ ДАННЫХ <<<<< #
#==========================================================================================#

class ArgumentType(enum.Enum):
	"""
	Перечисление типов аргументов.
	"""

	All = "@all"
	Number = "@number"
	ValidPath = "@validpath"
	Text = "@text"
	URL = "@url"
	
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
	
	def __init__(self, name: str):
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

	def add_argument(self, type: ArgumentType = ArgumentType.All, important: bool = False, layout_index: int | None = None):
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

	def add_key_position(self, keys: list[str], types: list[ArgumentType] | ArgumentType, important: bool = False, layout_index: int | None = None):
		"""
		Добавляет позицию ключа к команде.
			keys – список названий ключей;
			types – список типов значений для конкретных ключей или один тип для всех значений;
			important – является ли ключ обязательным;
			layout_index – индекс слоя, на который помещается ключ.
		"""
		
		# Если для всех значений установлен один тип аргумента.
		if type(types) == ArgumentType:
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
		self.Arguments = arguments
		# Словарь значений ключей.
		self.Values = values
		# Список активированных флагов.
		self.Flags = flags
		# Список активированных ключей.
		self.Keys = keys
		# Название команды.
		self.Name = name

	def __str__(self):
		return str({
			"name": self.Name, 
			"flags": self.Flags, 
			"keys": self.Keys, 
			"values": self.Values, 
			"arguments": self.Arguments
		})

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
		if len(self.__Argv) - 1 > CommandDescription.getMaxArgc(): raise TooManyArguments(" ".join(self.__Argv))
		# Если аргументов слишком мало, выбросить исключение.
		if len(self.__Argv) - 1 < CommandDescription.getMinArgc(): raise NotEnoughArguments(" ".join(self.__Argv))
	
	def __CheckArguments(self, command: Command) -> list[str | None]:
		"""
		Возвращает значения аргументов.
			command – описательная структура команды.
		"""
		
		# Значения аргументов.
		Values = list()
		# Список возможных аргументов.
		ArgumentsDescription = CommandDescription.arguments
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
					FlagsNames = CommandDescription.getLayoutFlags(self.__LayoutsStatuses[PositionIndex], True)
					KeysNames = CommandDescription.getLayoutKeys(self.__LayoutsStatuses[PositionIndex], True)
					# Если параметр является флагом или ключём того же слоя, записать пустое значение.
					if ParametersList[PositionIndex] in FlagsNames or ParametersList[PositionIndex] in KeysNames: FreeParameters.append(None)		

		# Если количество свободных параметров (игнорируя None) превышает максимальное, выбросить исключение.
		if len([x for x in FreeParameters if x != None]) > len(ArgumentsDescription): raise TooManyArguments(" ".join(self.__Argv))

		# Для каждого свободного параметра.
		for Index in range(0, len(FreeParameters)):
			
			# Если параметр не исключён.
			if FreeParameters[Index] != None:

				# Если параметр соответствует типу.
				if self.__CheckArgumentType(FreeParameters[Index], ArgumentsDescription[Index]["type"]) == True:
					# Сохранение параметра в качестве аргумента.
					Values.append(FreeParameters[Index])

				else:
					# Выброс исключения.
					raise InvalidArgumentType(FreeParameters[Index], CommandDescription.getArguments()["type"])
				
			else:
				# Сохранение пустого значения аргумента.
				Values.append(None)

		return Values
	
	def __CheckArgumentType(self, value: str, type_name: ArgumentType = ArgumentType.All) -> bool:
		"""
		Проверяет значение аргумента.
			value – значение аргумента;
			type_name – тип аргумента.
		"""
		
		# Если требуется проверить специфический тип аргумента.
		if type_name != ArgumentType.All:
			
			# Если аргумент должен являться числом.
			if type_name == ArgumentType.Number:

				# Если вся строка, без учёта отрицательного знака, не является числом, выбросить исключение.
				if value.lstrip('-').isdigit() == False: raise InvalidArgumentType(value, "Number")
				
			# Если аргумент должен являться валидным путём к файлу или директории.
			if type_name == ArgumentType.ValidPath:

				# Если строка не является валидным путём к файлу или директории, выбросить исключение.
				if os.path.exists(value) == False: raise InvalidArgumentType(value, "ValidPath")

			# Если аргумент должен являться набором букв.
			if type_name == ArgumentType.Text:

				# Если строка содержит небуквенные символы, выбросить исключение.
				if value.isalpha() == False: raise InvalidArgumentType(value, "Text")

			# Если аргумент должен являться URL.
			if type_name == ArgumentType.URL:

				# Если строка не является URL, выбросить исключение.
				if bool(urlparse(value).scheme) == False: raise InvalidArgumentType(value, "URL")

		return True

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
						self.__CheckArgumentType(Keys[KeyName], KeysPositions[PositionIndex]["types"][KeyIndex])
						
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

	def __init__(self):
		"""
		Обработчик консольных аргументов.
		"""

		#---> Генерация динамических свойств.
		#==========================================================================================#
		# Список задействованных позиций.
		self.__PositionsStatuses = list()
		# Список задействованных слоёв.
		self.__LayoutsStatuses = list()
		# Переданные параметры.
		self.__Argv = sys.argv[1:]
		# Кэшированные данные команды.
		self.__CommandData = None
		
	def check_command(self, command: Command) -> CommandData | None:
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
				Name = command.getName()
				# Проверка активированных флагов.
				Flags = self.__CheckFlags(command)
				# Проверка активированных ключей.
				Keys = self.__CheckKeys(command)
				# Получение аргументов.
				Arguments = self.__CheckArguments(command)
				# Данные проверки команды.
				self.__CommandData = CommandData(Name, Flags, list(Keys.keys()), Keys, Arguments)

		return self.__CommandData

	def check_commands(self, commands: list[Command]) -> CommandData | None:
		"""
		Выполняет проверку соответствия списку команд.
			commands – описательная структура команды.
		"""

		# Проверить каждую команду из списка.
		for CurrentCommand in commands: self.check_command(CurrentCommand)

		return self.__CommandData