# TextStyler
**TextStyler** – это подмодуль для вывода стилизованного текста в консоль с возможностью автосброса стилей и отключения перехода на новую строку. Он использует только ANSI-коды для обеспечения полной совместимости.

## Пример использования
```Python
from dublib.CLI.TextStyler import TextStyler

# Импорт стилей напрямую.
from dublib.CLI.TextStyler.Styles import Colors, Decorations
# Импорт контейнера стилей (полезно при занятых именах вышеперечисленных классов).
from dublib.CLI.TextStyler import Styles

# Вывод текста с декорациями.
TextStyler("This is a decorated text.", decorations = [Decorations.Underlined, Decorations.Italic]).print()

# Вывод стилизованного текста через стандартный метод.
Text = TextStyler("This is a styled text.", decorations = Styles.Decorations.Bold, text_color = Styles.Colors.Purple).text
print(Text)

# Использование быстрого форматирования.
print(TextStyler("This is a fast green text.").colorize.green)
print(TextStyler("This is a fast throughlined text.").decorate.throughline)
print(TextStyler("This is a fast backgrounded text.").background.blue)
```

## Скриншот (до версии 0.14.0)
![Screenshot](/docs/Images/StyledPrinter.png)