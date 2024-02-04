import shutil
import json
import sys
import os
import re


# ==========================================================================================#
# >>>>> ФУНКЦИИ РАБОТЫ С СИСТЕМОЙ <<<<< #
# ==========================================================================================#

def CheckPythonMinimalVersion(major: int, minor: int, raise_exception: bool = True) -> bool:
    """Проверяет, соответствует ли используемая версия Python минимальной требуемой.

    major – идентификатор Major-версии Python;
    minor – идентификатор Minor-версии Python;
    raise_exception – указывает, как поступать при несоответствии версии: выбрасывать исключение или возвращать значение.
    """

    # Состояние: корректна ли версия.
    is_version_correct = True

    # Если версия Python старше минимальной требуемой.
    if sys.version_info < (major, minor):
        # Если указано выбросить исключение.
        if raise_exception:
            # Выброс исключения.
            raise RuntimeError(f"Python {major}.{minor} or newer is required.")
        # Переключение статуса проверки.
        is_version_correct = False

    return is_version_correct


def Cls():
    """Очищает консоль."""

    os.system("cls" if os.name == "nt" else "clear")


def MakeRootDirectories(directories: list[str]):
    """Создаёт каталоги в текущей корневой директории скрипта.

    directories – список названий каталогов.
    """

    # Для каждого названия каталога.
    for Name in directories:
        # Если каталог не существует, то создать его.
        if not os.path.exists(Name):
            os.makedirs(Name)


def RemoveFolderContent(path: str):
    """Удаляет всё содержимое каталога.

    path – путь к каталогу.
    """

    # Список содержимого в папке.
    folder_content = os.listdir(path)

    # Для каждого элемента.
    for Item in folder_content:

        # Если элемент является каталогом.
        if os.path.isdir(path + "/" + Item):
            # Удаление каталога.
            shutil.rmtree(path + "/" + Item)

        else:
            # Удаление файла.
            os.remove(path + "/" + Item)


def Shutdown():
    """Выключает устройство."""

    # Если устройство работает под управлением ОС семейства Linux.
    if sys.platform in ["linux", "linux2"]:
        os.system("sudo shutdown now")
    # Если устройство работает под управлением ОС семейства Windows.
    if sys.platform == "win32":
        os.system("shutdown /s")


# ==========================================================================================#
# >>>>> ФУНКЦИИ ОБРАБОТКИ ТИПОВ ДАННЫХ <<<<< #
# ==========================================================================================#

def CheckForCyrillicPresence(text: str) -> bool:
    """Проверяет, имеются ли кирилические символы в строке.

    text – проверяемая строка.
    """

    # Русский алфавит в нижнем регистре.
    alphabet = set("абвгдеёжзийклмнопрстуфхцчшщъыьэюя")
    # Состояние: содержит ли строка кирилические символы.
    is_text_contains_cyrillic_characters = not alphabet.isdisjoint(text.lower())

    return is_text_contains_cyrillic_characters


def MergeDictionaries(base_dictionary: dict, mergeable_dictionary: dict, overwrite: bool = False) -> dict:
    """Объединяет словари.

    base_dictionary – словарь, в который идёт копирование;
    mergeable_dictionary – словарь, из котрого идёт копирование;
    overwrite – указывает, нужно ли перезаписывать значения конфликтующих ключей базового словаря.
    """

    # Для каждого ключа.
    for Key in mergeable_dictionary.keys():

        # Если перезапись отключена и ключ отсутствует в базовом словаре.
        if not overwrite and Key not in base_dictionary.keys():
            # Копирование в базовый словарь ключа и его значения из объединяемого.
            base_dictionary[Key] = mergeable_dictionary[Key]

        # Если перезапись включена.
        elif overwrite:
            # Копирование в базовый словарь ключа и его значения из объединяемого.
            base_dictionary[Key] = mergeable_dictionary[Key]

    return base_dictionary


def RemoveRecurringSubstrings(string: str, substring: str) -> str:
    """Удаляет из строки подряд идущие повторяющиеся подстроки.

    string – строка, из которой удаляются повторы;
    Substring – удаляемая подстрока.
    """

    # Пока в строке находятся повторы указанного символа, удалять их.
    while substring + substring in string:
        string = string.replace(substring + substring, substring)

    return string


def ReplaceDictionaryKey(dictionary: dict, old_key: any, new_key: any) -> dict:
    """Заменяет ключ в словаре, сохраняя исходный порядок элементов.

    dictionary – обрабатываемый словарь;
    old_key – старое название ключа;
    new_key – новое название ключа.
    """

    # Результат выполнения.
    result = dict()
    # Если ключ не найден, выбросить исключение.
    if old_key not in dictionary.keys():
        raise KeyError(str(old_key))

    # Для каждого ключа.
    for Key in dictionary.keys():

        # Если текущий ключ совпадает с искомым.
        if Key == old_key:
            # Замена ключа новым.
            result[new_key] = dictionary[old_key]

        else:
            # Копирование старой пары ключ-значение.
            result[Key] = dictionary[Key]

    return result


def ReplaceRegexSubstring(origin: str, regex: str, substring: str) -> str:
    """Заменяет все вхождения регулярного выражения в строке на подстроку.

    origin – обрабатываемая строка;
    regex – регулярное выражение для поиска подстрок;
    substring – вставляемая подстрока.
    """

    # Список совпадений.
    while re.findall(regex, origin):
        # Буфер.
        regex_substring = re.findall(regex, origin)
        # Поиск всех совпадений.
        regex_substring = regex_substring[0] if len(regex_substring) > 0 else None
        # Удаление подстроки.
        if regex_substring is not None:
            origin = origin.replace(regex_substring, substring)

    return origin


# ==========================================================================================#
# >>>>> ФУНКЦИИ РАБОТЫ С JSON <<<<< #
# ==========================================================================================#

def ReadJSON(path: str) -> dict:
    """Читает файл JSON и конвертирует его в словарь.
    path – путь к файлу.
    """

    # Открытие и чтение файла JSON.
    with open(path, encoding="utf-8") as FileRead:
        js = json.load(FileRead)

    return js


def WriteJSON(path: str, dictionary: dict, indent: str = None):
    """Записывает стандартизированный JSON файл. Для отступов используются символы табуляции.

    path – путь к файлу;
    dictionary – словарь, конвертируемый в формат JSON.
    """

    # Запись словаря в JSON файл.
    if indent is None:
        indent = "\t"
    with open(path, "w", encoding="utf-8") as FileWrite:
        json.dump(dictionary, FileWrite, ensure_ascii=False, indent=indent, separators=(",", ": "))
