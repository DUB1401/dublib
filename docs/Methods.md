# Methods
**Methods** – это модуль, содержащий коллекцию полезных функций.

## Функции
* `CheckForCyrillicPresence(Text: str) -> bool` – проверяет, имеются ли кирилические символы в строке.
* `Cls()` – очищает консоль (кросплатформенная функция).
* `MergeDictionaries(FirstDictionary: dict, SecondDictionary: dict) -> dict` – объединяет словари без перезаписи значений уже существующих ключей.
* `ReadJSON(Path: str) -> dict` – считывает JSON файл в словарь.
* `RemoveFolderContent(Path: str)` – удаляет все папки и файлы внутри директории.
* `RemoveHTML(TextHTML: str) -> str` – удаляет теги HTML из строки, а также преобразует спецсимволы HTML в Unicode.
* `RemoveRecurringSubstrings(String: str, Substring: str) -> str` – удаляет из строки подряд идущие повторяющиеся подстроки.
* `RemoveRegexSubstring(String: str, Regex: str) -> str` – удаляет из строки все вхождения подстрок, совпадающие с регулярным выражением.
* `RenameDictionaryKey(Dictionary: dict, OldKey: str, NewKey: str) -> dict` – переименовывает ключ в словаре, сохраняя исходный порядок.
* `Shutdown()` – выключает питание устройства (кроссплатформенная функция).
* `WriteJSON(Path: str, Dictionary: dict)` – сохраняет стилизованный JSON файл. Для отступов используются символы табуляции, новая строка проставляется после запятых, а после двоеточий добавляется пробел.