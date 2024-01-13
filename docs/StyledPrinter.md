# StyledPrinter
**StyledPrinter** – это модуль для вывода цветного и стилизованного текста в терминал с возможностью автосброса стилей и отключения перехода на новую строку.

## Классы
* `Styles` – содержит два контейнера: для декораций и стилей.
* `StylesGroup` – предоставляет возможность комбинировать стили для их однократной инициализации и повторного использования. При интерпретации в `str()` предоставляет строковый маркер стилей.

## Функции
* `StyledPrinter(text: str, styles: StylesGroup | None = None, decorations: list[Styles.Decoration] = list(), text_color: Styles.Color | None = None, background_color: Styles.Color | None = None, autoreset: bool = True, end: bool = True)` – выводит в терминал стилизованный текст с возможностью автоматического сброса стилей и отключения перехода на новую строку.
* `TextStyler(text: str, styles: StylesGroup | None = None, decorations: list[Styles.Decoration] = list(), text_color: Styles.Color | None = None, background_color: Styles.Color | None = None, autoreset: bool = True) -> str` – возвращает стилизованный текст.

> [!WARNING]  
> Не используйте одновременно группу стилей и отдельные стили, так как это приводит к ошибке переопределения.

## Пример
```Python
from dublib.StyledPrinter import *

# Вывод цветного текста.
StyledPrinter("Colored Text", text_color = Styles.Color.Red)

# Вывод цветного текста на фоне.
StyledPrinter("Colored Text on Background", text_color = Styles.Color.Red, background_color = Styles.Color.White)

# Вывод стилизованного цветного текста на фоне.
StyledPrinter("Colored Text", decorations = [Styles.Decoration.Italic], text_color = Styles.Color.Purple, background_color = Styles.Color.Yellow)

# Вывод стилизованного цветного текста на фоне c отключением сброса стилей к стандартным.
StyledPrinter("Colored Text", decorations = [Styles.Decoration.Italic], text_color = Styles.Color.Purple, background_color = Styles.Color.Yellow, autoreset = True)

# Вывод стилизованного цветного текста на фоне с отключением сброса стилей к стандартным и перехода на новую строку.
StyledPrinter("Colored Text", decorations = [Styles.Decoration.Italic], text_color = Styles.Color.Purple, background_color = Styles.Color.Yellow, autoreset = True, end = False)

# Создание группы стилей.
GroupOfStyles = StylesGroup(decorations = [Styles.Decoration.Italic], text_color = Styles.Color.Purple, background_color = Styles.Color.Yellow)

# Вывод стилизованного цветного текста на фоне (при помощи группы стилей) с отключением сброса стилей к стандартным и перехода на новую строку.
StyledPrinter("Colored Text", GroupOfStyles, autoreset = True, end = False)

# Создание стилизованного текста (при помощи группы стилей) для использования в стандартном методе вывода.
StyledText = TextStyler("Colored Text", GroupOfStyles)

# Вывод стилизованного текста стандартным методом.
print(StyledText)
```

## Скриншот
![Screenshot](Images/StyledPrinter.png)