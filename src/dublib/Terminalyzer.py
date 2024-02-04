from .Exceptions import InvalidArgumentsTypes, IdenticalIndicators, NotEnoughArguments, TooManyArguments, \
    MutuallyExclusivePositions, MutuallyExclusiveFlags, MutuallyExclusiveKeys
from .Methods import ReadJSON
from urllib.parse import urlparse

import enum
import sys
import os


# ==========================================================================================#
# >>>>> ВСПОМОГАТЕЛЬНЫЕ ТИПЫ ДАННЫХ <<<<< #
# ==========================================================================================#

class ArgumentsTypes(enum.Enum):
    """Перечисление типов аргументов."""

    All = "all"
    Number = "number"
    ValidPath = "validpath"
    Text = "text"
    URL = "url"


class Command:
    """Контейнер описания команды."""

    # ==========================================================================================#
    # >>>>> СВОЙСТВА ТОЛЬКО ДЛЯ ЧТЕНИЯ <<<<< #
    # ==========================================================================================#

    @property
    def arguments(self) -> list:
        """Список аргументов."""

        return self.__Arguments

    @property
    def description(self) -> str:
        """Описание команды."""

        return self.__Description

    @property
    def flags_indicator(self) -> str:
        """Индикатор флагов."""

        return self.__FlagIndicator

    @property
    def flags_positions(self) -> list:
        """Список позиций флагов."""

        return self.__FlagsPositions

    @property
    def keys_indicator(self) -> str:
        """Индикатор ключей."""

        return self.__KeyIndicator

    @property
    def keys_positions(self) -> list:
        """Список позиций ключей."""

        return self.__KeysPositions

    @property
    def max_parameters(self) -> int:
        """Максимальное количество параметров."""

        return self.__MaxArgc

    @property
    def min_parameters(self) -> int:
        """Минимальное количество параметров."""

        return self.__MinArgc

    @property
    def name(self) -> str:
        """Название команды."""

        return self.__Name

    # ==========================================================================================#
    # >>>>> МЕТОДЫ <<<<< #
    # ==========================================================================================#

    def __CalculateMaxParameters(self):
        """Подсчитывает максимальное количество параметров."""

        # Обнуление максимального количества параметров.
        self.__MaxArgc = 0

        # Для каждой позиции флага.
        for FlagsPostionIngex in range(0, len(self.__FlagsPositions)):

            # Если позиция флага не лежит на слое, посчитать её.
            if self.__FlagsPositions[FlagsPostionIngex]["layout-index"] is None:
                self.__MaxArgc += 1

        # Для каждой позиции ключа.
        for KeysPostionIngex in range(0, len(self.__KeysPositions)):

            # Если позиция ключа не лежит на слое, посчитать её за 2 параметра (ключ-значение).
            if self.__KeysPositions[KeysPostionIngex]["layout-index"] is None:
                self.__MaxArgc += 2

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
        """Подсчитывает минимальное количество параметров."""

        # Обнуление минимального количества параметров.
        self.__MinArgc = 0

        # Для каждой позиции флага.
        for FlagsPostionIngex in range(0, len(self.__FlagsPositions)):

            # Если позиция флага не лежит на слое и является важной, посчитать её.
            if self.__FlagsPositions[FlagsPostionIngex]["layout-index"] is None and \
                    self.__FlagsPositions[FlagsPostionIngex]["important"] is True:
                self.__MinArgc += 1

        # Для каждой позиции ключа.
        for KeysPostionIngex in range(0, len(self.__KeysPositions)):

            # Если позиция ключа не лежит на слое и является важной, посчитать её за 2 параметра (ключ-значение).
            if self.__KeysPositions[KeysPostionIngex]["layout-index"] is None and \
                    self.__KeysPositions[KeysPostionIngex]["important"] is True:
                self.__MinArgc += 2

        # Для каждого аргумента.
        for Argument in self.__Arguments:

            # Если аргумент не лежит на слое и является важным, посчитать его.
            if Argument["layout-index"] is None and Argument["important"]:
                self.__MinArgc += 1

        # Для каждого слоя.
        for LayoutIndex in self.__Layouts.keys():

            # Если слой является важным и содержит ключи.
            if self.__Layouts[LayoutIndex]["important"] and self.__Layouts[LayoutIndex]["keys"] > 0:
                # Посчитать слой за 2 параметра.
                self.__MinArgc += 1

            else:
                # Посчитать слой за 1 параметр.
                self.__MaxArgc += 1

    def __InitializeLayout(self, layout_index: int):
        """Инициализирует описательную структуру слоя.

        layout_index – индекс слоя.
        """

        # Преобразование индекса слоя в строку.
        layout_index = str(layout_index)
        # Если слой с таким индексом не описан, создать для него структуру.
        if layout_index not in self.__Layouts.keys():
            self.__Layouts[layout_index] = {"arguments": 0, "flags": 0, "keys": 0, "important": False}

    def __SetLayoutAsImportant(self, layout_index: int):
        """Делает все параметры слоя важными.

        layout_index – индекс слоя.
        """

        # Установка важности слоя.
        self.__Layouts[str(layout_index)]["important"] = True

        # Для каждой позиции флага.
        for FlagPositionIndex in range(len(self.__FlagsPositions)):

            # Если позиция флага лежит на важном слое, сделать ей важной.
            if self.__FlagsPositions[FlagPositionIndex]["layout-index"] == layout_index:
                self.__FlagsPositions[FlagPositionIndex]["important"] = True

        # Для каждой позиции ключа.
        for KeyPositionIndex in range(len(self.__KeysPositions)):

            # Если позиция ключа лежит на важном слое, сделать её важной.
            if self.__KeysPositions[KeyPositionIndex]["layout-index"] == layout_index:
                self.__KeysPositions[KeyPositionIndex]["important"] = True

        # Для каждого аргумента.
        for ArgumentIndex in range(len(self.__Arguments)):

            # Если аргумент лежит на важном слое, сделать его важным.
            if self.__Arguments[ArgumentIndex]["layout-index"] == layout_index:
                self.__Arguments[ArgumentIndex]["important"] = True

    def __init__(self, name: str, description: str | None = None):
        """Контейнер описания команды.

        name – название команды.
        """

        # ---> Генерация динамических свойств.
        # ==========================================================================================#
        # Список флагов.
        self.__FlagsPositions = []
        # Список ключей.
        self.__KeysPositions = []
        # Индикатор ключа.
        self.__KeyIndicator = "--"
        # Индикатор флага.
        self.__FlagIndicator = "-"
        # Список аргументов.
        self.__Arguments = []
        # Название команды.
        self.__Name = name
        # Максимальное количество аргументов.
        self.__MaxArgc = 0
        # Минимальное количество аргументов.
        self.__MinArgc = 0
        # Словарь, предоставляющий список слоёв и количество параметров на них.
        self.__Layouts = {}
        # Описание команды.
        self.__Description = description

    def add_argument(self,
                     type: ArgumentsTypes = ArgumentsTypes.All,
                     important: bool = False,
                     layout_index: int | None = None):
        """Добавляет аргумент к команде.

        type – тип аргумента;
        important – является ли аргумент обязательным;
        layout_index – индекс слоя, на который помещается аргумент.
        """

        # Запись аргумента в описание команды.
        self.__Arguments.append({"type": type, "important": important, "layout-index": layout_index})

        # Если задан важный слой.
        if layout_index is not None:
            # Инициализация слоя.
            self.__InitializeLayout(layout_index)
            # Инкремент количества аргументов на слое.
            self.__Layouts[str(layout_index)]["arguments"] += 1
            # Если аргумент важный, сделать слой важным.
            if important: self.__SetLayoutAsImportant(layout_index)

        # Вычисление максимального и минимального количества аргументов.
        self.__CalculateMaxParameters()
        self.__CalculateMinParameters()

    def add_flag_position(self, flags: list[str], important: bool = False, layout_index: int | None = None):
        """Добавляет позицию флага к команде.

        flags – список названий флагов;
        important – является ли флаг обязательным;
        layout_index – индекс слоя, на который помещается флаг.
        """

        # Запись позиции ключа в описание команды.
        self.__FlagsPositions.append({"names": flags, "important": important, "layout-index": layout_index})

        # Если задан важный слой.
        if layout_index is not None:
            # Инициализация слоя.
            self.__InitializeLayout(layout_index)
            # Инкремент количества флагов на слое.
            self.__Layouts[str(layout_index)]["flags"] += 1
            # Если позиция важная, сделать слой важным.
            if important:
                self.__SetLayoutAsImportant(layout_index)

        # Вычисление максимального и минимального количества аргументов.
        self.__CalculateMaxParameters()
        self.__CalculateMinParameters()

    def add_key_position(self,
                         keys: list[str],
                         types: list[ArgumentsTypes] | ArgumentsTypes,
                         important: bool = False,
                         layout_index: int | None = None):
        """Добавляет позицию ключа к команде.

        keys – список названий ключей;
        types – список типов значений для конкретных ключей или один тип для всех значений;
        important – является ли ключ обязательным;
        layout_index – индекс слоя, на который помещается ключ.
        """

        # Если для всех значений установлен один тип аргумента.
        if isinstance(types, ArgumentsTypes):
            # Буфер заполнения.
            bufer = list()
            # На каждый ключ продублировать тип значения.
            for Type in keys:  # TODO: я не понял что ты тут хотел?????
                bufer.append(types)
            # Замена аргумента буфером.
            types = bufer

        # Запись позиции ключа в описание команды.
        self.__KeysPositions.append(
            {"names": keys, "types": types, "important": important, "layout-index": layout_index})

        # Если задан важный слой.
        if layout_index is not None:
            # Инициализация слоя.
            self.__InitializeLayout(layout_index)
            # Инкремент количества ключей на слое.
            self.__Layouts[str(layout_index)]["keys"] += 1
            # Если позиция важная, сделать слой важным.
            if important:
                self.__SetLayoutAsImportant(layout_index)

        # Вычисление максимального и минимального количества аргументов.
        self.__CalculateMaxParameters()
        self.__CalculateMinParameters()

    def get_layout_arguments_count(self, layout_index: int) -> int:
        """Возвращает количество аргументов на слое.

        layout_index – индекс слоя для поиска аргументов.
        """

        # Количество аргументов на слое.
        layout_arguments_count = 0

        # Для каждого аргумента.
        for Argument in self.__Arguments:

            # Если аргумент лежит на слое, посчитать его.
            if Argument["layout-index"] == layout_index:
                layout_arguments_count += 1

        return layout_arguments_count

    def get_layout_flags(self, layout_index: int, add_indicator: bool = False) -> list[str]:
        """Возвращает список всех возможных флагов на слое.

        layout_index – индекс слоя для поиска флагов;
        add_indicator – указывает, нужно ли добавить индикаторы к названиям флагов.
        """

        # Список флагов на слое.
        layout_flags = []

        # Для каждой позиции флага.
        for FlagPosition in self.__FlagsPositions:

            # Если флаг лежит на слое.
            if FlagPosition["layout-index"] == layout_index:

                # Если не нужно добавлять индикаторы.
                if not add_indicator:
                    # Запись флагов текущей позиции.
                    layout_flags += FlagPosition["names"]

                else:

                    # Для каждого названия флага на позиции.
                    for FlagName in FlagPosition["names"]:
                        # Запись флага с индикатором.
                        layout_flags.append(self.__FlagIndicator + FlagName)

        return layout_flags

    def get_layout_keys(self, layout_index: int, add_indicator: bool = False) -> list[str]:
        """Возвращает список всех возможных ключей на слое.

        layout_index – индекс слоя для поиска ключей;
        add_indicator – указывает, нужно ли добавить индикаторы к названиям ключей.
        """

        # Список ключей на слое.
        layout_keys = []

        # Для каждой позиции ключа.
        for KeyPosition in self.__KeysPositions:

            # Если ключ лежит на слое.
            if KeyPosition["layout-index"] == layout_index:

                # Если не нужно добавлять индикаторы.
                if not add_indicator:
                    # Запись ключей текущей позиции.
                    layout_keys += KeyPosition["names"]

                else:

                    # Для каждого названия ключа на позиции.
                    for KeyName in KeyPosition["names"]:
                        # Запись ключа с индикатором.
                        layout_keys.append(self.__KeyIndicator + KeyName)

        return layout_keys

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

    def __init__(self,
                 name: str,
                 flags: list[str] = None,
                 keys: list[str] = None,
                 values: list[str] = None,
                 arguments: list[str] = None):
        """
        Контейнер хранения данных обработанной команды.
            name – название команды;
            flags – список активированных флагов;
            keys – список активированных ключей;
            values – словарь значений активированных ключей;
            Arguments – список аргументов.
        """

        # ---> Генерация динамических свойств.
        # ==========================================================================================#
        # Значение аргумента.
        if flags is None:
            flags = []
        if keys is None:
            keys = []
        if arguments is None:
            arguments = []
        if values is None:
            values = {}
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
    """JSON-конфигурация команд."""

    # ==========================================================================================#
    # >>>>> СВОЙСТВА ТОЛЬКО ДЛЯ ЧТЕНИЯ <<<<< #
    # ==========================================================================================#

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

    # ==========================================================================================#
    # >>>>> МЕТОДЫ <<<<< #
    # ==========================================================================================#

    def __ProcessTypes(self, types: list[str] | str) -> list[str] | str:
        """
        Конвертирует текстовое представление типов в классовое.
            types – список названий типов или конкретное название.
        """

        # Типы аргументов.
        types = list()

        # Если передан список типов.
        if isinstance(types, list):
            # Запись всех типов.
            types = types

        else:
            # Дополнение списка типом.
            types.append(types)

        # Для каждого типа.
        for Index in range(0, len(types)):
            # Замещение строкового типа аргумента классовым.
            types[Index] = self.arguments_types[types[Index]]

        # Если передан один тип, вернуть строку, а не список.
        if len(types) == 1:
            types = types[0]

        return types

    def __init__(self, path: str | None = None):
        """JSON-конфигурация команд."""

        # ---> Генерация динамических свойств.
        # ==========================================================================================#
        # Конфигурация.
        self.__Config = None

        # Если указан путь к файлу, прочитать его.
        if path is not None:
            self.read(path)

    def build_commands(self) -> list[Command]:
        """Строит список описаний команд из конфигурации."""

        # Список описательных структур команд.
        commands_list = []

        # Для каждой команды.
        for CommandName in self.__Config["commands"].keys():
            # Буфер обрабатываемой команды.
            bufer = self.__Config["commands"][CommandName]
            # Структура команды.
            command_description = Command(CommandName)

            # Если указано описание команды, игнорировать его.
            if "description" in bufer.keys():
                command_description.set_description(bufer["description"])

            # Если указан индикатор флагов, записать его.
            if "flags-indicator" in bufer.keys():
                command_description.set_flags_indicator(bufer["flags-indicator"])

            # Если указан индикатор ключей, записать его.
            if "keys-indicator" in bufer.keys():
                command_description.set_keys_indicator(bufer["keys-indicator"])

            # Если для команды указаны позиции флагов.
            if "flags" in bufer.keys():

                # Для каждого флага.
                for FlagPosition in bufer["flags"]:
                    # Состояние: является ли позиция важной.
                    is_important = False
                    # Индекс слоя.
                    layout_index = None
                    # Если определено состояние важности, записать его.
                    if "important" in FlagPosition.keys():
                        is_important = FlagPosition["important"]
                    # Если определён индекс слоя, записать его.
                    if "layout_index" in FlagPosition.keys():
                        layout_index = FlagPosition["layout_index"]
                    # Формирование позиции флага.
                    command_description.add_flag_position(FlagPosition["names"], is_important, layout_index)

            # Если для команды указаны позиции ключей.
            if "keys" in bufer.keys():

                # Для каждого ключа.
                for KeyPosition in bufer["keys"]:
                    # Типы значений.
                    types = ArgumentsTypes.All
                    # Состояние: является ли позиция важной.
                    is_important = False
                    # Индекс слоя.
                    layout_index = None
                    # Если указаны специфические типы, преобразовать их строковые представления в классовые.
                    if "types" in KeyPosition.keys():
                        types = self.__ProcessTypes(KeyPosition["types"])
                    # Если определено состояние важности, записать его.
                    if "important" in KeyPosition.keys():
                        is_important = KeyPosition["important"]
                    # Если определён индекс слоя, записать его.
                    if "layout_index" in KeyPosition.keys():
                        layout_index = KeyPosition["layout_index"]
                    # Формирование позиции ключа.
                    command_description.add_key_position(KeyPosition["names"], types, is_important, layout_index)

            # Если для команды указаны аргументы.
            if "arguments" in bufer.keys():

                # Для каждого аргумента.
                for Argument in bufer["arguments"]:
                    # Типы значений.
                    types = ArgumentsTypes.All
                    # Состояние: является ли позиция важной.
                    is_important = False
                    # Индекс слоя.
                    layout_index = None
                    # Если указаны специфические типы, преобразовать их строковые представления в классовые.
                    if "type" in Argument.keys():
                        types = self.__ProcessTypes(Argument["type"])
                    # Если определено состояние важности, записать его.
                    if "important" in Argument.keys():
                        is_important = Argument["important"]
                    # Если определён индекс слоя, записать его.
                    if "layout_index" in Argument.keys():
                        layout_index = Argument["layout_index"]
                    # Формирование аргумента.
                    command_description.add_argument(types, is_important, layout_index)

            # Запись команды в список.
            commands_list.append(command_description)

        return commands_list

    def read(self, path: str):
        """Читает конфигурацию из JSON файла.

        path – путь к файлу.
        """

        self.__Config = ReadJSON(path)


# ==========================================================================================#
# >>>>> ОСНОВНОЙ КЛАСС <<<<< #
# ==========================================================================================#

class Terminalyzer:
    """Обработчик консольных аргументов."""

    def __CheckArgc(self, command: Command):
        """Проверяет соответвтсие количества аргументов.

        command – описательная структура команды.
        """

        # Если аргументов слишком много, выбросить исключение.
        if len(self.__Argv) - 1 > command.max_parameters:
            raise TooManyArguments(" ".join(self.__Argv))
        # Если аргументов слишком мало, выбросить исключение.
        if len(self.__Argv) - 1 < command.min_parameters:
            raise NotEnoughArguments(" ".join(self.__Argv))

    def __CheckArguments(self, command: Command) -> list[str | None]:
        """Возвращает значения аргументов.

        command – описательная структура команды.
        """

        # Значения аргументов.
        values = []
        # Список возможных аргументов.
        arguments_description = command.arguments
        # Список параметров без команды.
        parameters_list = self.__Argv[1:]
        # Список незадействованных параметров.
        free_parameters = []

        # Для каждого параметра.
        for PositionIndex in range(0, len(parameters_list)):

            # Если позиция не лежит на слое.
            if self.__LayoutsStatuses[PositionIndex] is None:

                # Если позиция не была задействована.
                if not self.__PositionsStatuses[PositionIndex]:
                    # Записать параметр как свободный.
                    free_parameters.append(parameters_list[PositionIndex])

            else:

                # Если позиция не была задействована.
                if not self.__PositionsStatuses[PositionIndex]:
                    # Записать параметр как свободный.
                    free_parameters.append(parameters_list[PositionIndex])

                else:
                    # Списки названий флагов и ключей.
                    flags_names = command.get_layout_flags(self.__LayoutsStatuses[PositionIndex], True)
                    keys_names = command.get_layout_keys(self.__LayoutsStatuses[PositionIndex], True)
                    # Если параметр является флагом или ключём того же слоя, записать пустое значение.
                    if parameters_list[PositionIndex] in flags_names or parameters_list[PositionIndex] in keys_names:
                        free_parameters.append(None)

        # Если количество свободных параметров (игнорируя None) превышает максимальное, выбросить исключение.
        if len([x for x in free_parameters if x is not None]) > len(arguments_description):
            raise TooManyArguments(" ".join(self.__Argv))

        # Для каждого свободного параметра.
        for Index in range(0, len(free_parameters)):

            # Если параметр не исключён.
            if free_parameters[Index] is not None:

                # Если параметр соответствует типу.
                if self.__CheckArgumentsTypes(free_parameters[Index], arguments_description[Index]["type"]):
                    # Сохранение параметра в качестве аргумента.
                    values.append(free_parameters[Index])

                else:
                    # Выброс исключения.
                    raise InvalidArgumentsTypes(free_parameters[Index], command.arguments["type"])

            else:
                # Сохранение пустого значения аргумента.
                values.append(None)

        return values

    def __CheckArgumentsTypes(self, value: str, type_name: ArgumentsTypes = ArgumentsTypes.All) -> bool:
        """Проверяет значение аргумента.

        value – значение аргумента;
        type_name – тип аргумента.
        """

        # Если требуется проверить специфический тип аргумента.
        if type_name != ArgumentsTypes.All:

            # Если аргумент должен являться числом.
            if type_name == ArgumentsTypes.Number:

                # Если вся строка, без учёта отрицательного знака, не является числом, выбросить исключение.
                if not value.lstrip('-').isdigit():
                    raise InvalidArgumentsTypes(value, "Number")

            # Если аргумент должен являться валидным путём к файлу или директории.
            if type_name == ArgumentsTypes.ValidPath:

                # Если строка не является валидным путём к файлу или директории, выбросить исключение.
                if not os.path.exists(value):
                    raise InvalidArgumentsTypes(value, "ValidPath")

            # Если аргумент должен являться набором букв.
            if type_name == ArgumentsTypes.Text:

                # Если строка содержит небуквенные символы, выбросить исключение.
                if not value.isalpha():
                    raise InvalidArgumentsTypes(value, "Text")

            # Если аргумент должен являться URL.
            if type_name == ArgumentsTypes.URL:

                # Если строка не является URL, выбросить исключение.
                if not bool(urlparse(value).scheme):
                    raise InvalidArgumentsTypes(value, "URL")

        return True

    def __CheckCommand(self, command: Command) -> CommandData | None:
        """
        Выполняет проверку соответствия конкретной команде.
            command – описательная структура команды.
        """

        # Если название команды соответствует.
        if self.__CheckName(command):

            # Если данные команды не кэшированы.
            if self.__CommandData is None:
                # Заполнение статусов позиций параметров.
                self.__PositionsStatuses = [False] * (len(self.__Argv) - 1)
                # Заполнение статусов слоёв параметров.
                self.__LayoutsStatuses = [None] * (len(self.__Argv) - 1)
                # Проверка соответствия количества параметров.
                self.__CheckArgc(command)
                # Получение названия команды.
                name = command.name
                # Проверка активированных флагов.
                flags = self.__CheckFlags(command)
                # Проверка активированных ключей.
                check_keys = self.__CheckKeys(command)
                # Получение аргументов.
                arguments = self.__CheckArguments(command)
                # Данные проверки команды.
                self.__CommandData = CommandData(name, flags, list(check_keys.keys()), check_keys, arguments)

        return self.__CommandData

    def __CheckFlags(self, command: Command) -> list[str]:
        """
        Возвращает список активных флагов.
            command – описательная структура команды.
        """

        # Список позиций флагов.
        flags_positions = command.flags_positions
        # Индикатор флага.
        flag_indicator = command.flags_indicator
        # Список активных флагов.
        flags = []

        # Для каждой позиции флага.
        for PositionIndex in range(0, len(flags_positions)):
            # Состояние: активирован ли флаг на позиции.
            is_position_activated = False

            # Для каждого названия флага на позиции.
            for FlagName in flags_positions[PositionIndex]["names"]:

                # Если индикатор с названием флага присутствует в параметрах.
                if flag_indicator + FlagName in self.__Argv:
                    # Установка активного статуса позиции параметра команды.
                    self.__PositionsStatuses[self.__Argv.index(flag_indicator + FlagName) - 1] = True

                    # Если взаимоисключающий флаг на данной позиции не был активирован.
                    if not is_position_activated:
                        # Установка активного статуса для флага.
                        flags.append(FlagName)
                        # Блокировка позиции.
                        is_position_activated = True

                        # Если для флага задан слой.
                        if flags_positions[PositionIndex]["layout-index"] is not None:
                            # Индекс слоя текущей позиции.
                            layout_index = flags_positions[PositionIndex]["layout-index"]

                            # Если индекс слоя текущей позиции флага не активен.
                            if layout_index not in self.__LayoutsStatuses:
                                # Активация слоя.
                                self.__LayoutsStatuses[self.__Argv.index(flag_indicator + FlagName) - 1] = layout_index

                            else:
                                # Выброс исключения.
                                raise MutuallyExclusivePositions(" ".join(self.__Argv))

                    else:
                        # Выброс исключения.
                        raise MutuallyExclusiveFlags(" ".join(self.__Argv))

        return flags

    def __CheckKeys(self, command: Command) -> dict | list[int]:
        """Возвращает словарь активных ключей и их содержимое.

        command – описательная структура команды.
        """

        # Список позиций ключей.
        keys_positions = command.keys_positions
        # Индикатор ключа.
        key_indicator = command.keys_indicator
        # Словарь статусов ключей.
        keys = {}

        # Для каждой позиции ключа.
        for PositionIndex in range(0, len(keys_positions)):
            # Состояние: активирован ли ключ для позиции.
            is_position_activated = False

            # Для каждого названия ключа на позиции.
            for KeyIndex in range(0, len(keys_positions[PositionIndex]["names"])):
                # Название ключа.
                key_name = keys_positions[PositionIndex]["names"][KeyIndex]

                # Если индикатор с названием ключа присутствует в параметрах.
                if key_indicator + key_name in self.__Argv:
                    # Установка активного статуса позициям параметров команды.
                    self.__PositionsStatuses[self.__Argv.index(key_indicator + key_name) - 1] = True
                    self.__PositionsStatuses[self.__Argv.index(key_indicator + key_name)] = True

                    # Если взаимоисключающий ключ на данной позиции не был активирован.
                    if not is_position_activated:
                        # Установка значения для ключа.
                        keys[key_name] = self.__Argv[self.__Argv.index(key_indicator + key_name) + 1]
                        # Блокировка позиции.
                        is_position_activated = True
                        # Проверка типа значения ключа.
                        self.__CheckArgumentsTypes(keys[key_name], keys_positions[PositionIndex]["types"][KeyIndex])

                        # Если для ключа задан слой.
                        if keys_positions[PositionIndex]["layout-index"] is not None:
                            # Индекс слоя текущей позиции.
                            LayoutIndex = keys_positions[PositionIndex]["layout-index"]

                            # Если индекс слоя текущей позиции ключа не активен.
                            if LayoutIndex not in self.__LayoutsStatuses:
                                # Активация слоя.
                                self.__LayoutsStatuses[self.__Argv.index(key_indicator + key_name) - 1] = LayoutIndex

                            else:
                                # Выброс исключения.
                                raise MutuallyExclusivePositions(" ".join(self.__Argv))

                    else:
                        # Выброс исключения.
                        raise MutuallyExclusiveKeys(" ".join(self.__Argv))

        return keys

    def __CheckName(self, command: Command) -> bool:
        """Проверяет соответствие названия команды.

        command – описательная структура команды.
        """

        # Состояние: определена ли команда.
        is_determined = False

        # Если переданы параметры и имя команды определено, переключить статус проверки.
        if len(self.__Argv) > 0 and command.name == self.__Argv[0]:
            is_determined = True

        return is_determined

    def __CreateBaseHelp(self, commands: list[Command]) -> str | None:
        # Буфер базовой помощи.
        base_help = ""
        # Модификатор выравнивания.
        modificator = 0

        # Если используется автовыравнивание.
        if self.__Ljust == 0:
            # Список названий команд.
            commandsNames = []
            # Для каждой команды записать имя.
            for CurrentCommand in commands: commandsNames.append(CurrentCommand.name)
            # Вычисление длиннейшей строки.
            modificator = len(max(commandsNames, key=len))

        # Если задано конкретное значение выравнивания.
        elif self.__Ljust is not None:
            # Установка конкретного значения.
            modificator = self.__Ljust

        # Для каждой команды.
        for CurrentCommand in commands:
            # Добавление имени.
            base_help += CurrentCommand.name.ljust(modificator)
            # Добавление описания.
            if CurrentCommand.description is not None:
                base_help += " " + CurrentCommand.description
            # Завершение строки.
            base_help += "\n"

        # Обнуление пустой помощи.
        if base_help == "": base_help = None

        return base_help

    def __init__(self, source: list[str] = None):
        """Обработчик консольных аргументов.

        source – список из названия команды и её параметров
        """

        # ---> Генерация динамических свойств.
        # ==========================================================================================#
        # Список задействованных позиций.
        if source is None:
            source = sys.argv[1:]
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
        if isinstance(commands, Command):
            # Преобразование команды в список.
            commands = [commands]

        # Если тип обрабатываемого значения – описание команды.
        elif isinstance(commands, Config):
            # Преобразование конфигурации в список команд.
            commands = commands.build_commands()

        # Проверка каждой команды из списка.
        for CurrentCommand in commands:
            self.__CheckCommand(CurrentCommand)

        # Если включена обработка помощи
        if self.__EnableHelp and self.__CommandData.name == "help":
            # Буфер вывода.
            out = None
            # Если нет аргументов, создать базовую помощь.
            if len(self.__CommandData.arguments) == 0:
                out = self.__CreateBaseHelp(commands)
            # Отправка помощи в вывод.
            self.__OutMethod(out)

        return self.__CommandData

    def enable_help(self, out_method: any = print, ljust: int | None = 0):
        """Включает обработку дополнительной команды вывода помощи.

        out_method – указывает функцию, в которую будет перенаправлен вывод помощи;
        ljust – задаёт длину названия команд для выравнивания методом добавления пробелов (0 включает автоматическое выравнивание по самой длинной команде).
        """

        # Установка параметров.
        self.__EnableHelp = True
        self.__OutMethod = out_method
        self.__Ljust = ljust

    def set_source(self, source: list[str]):
        """Задаёт обрабатываемый источник. Первым элементом списка обязательно должно являться название команды.

        source – список из названия команды и её параметров
        """

        self.__Argv = source
