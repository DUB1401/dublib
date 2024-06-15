# Polyglot
**Polyglot** – это средство базовой работы с языками разметки текста. Поддерживаются: HTML, Markdown.

Принцип работы включаемых подмодулей таков: вызов методов приводит к изменению свойства внутри класса, но ничего не возвращает. Для получения данных необходимо либо интерпретировать класс в `str()`, либо обратиться к свойству.

## Пример
```Python
from dublib.Polyglot import HTML, Markdown

# Получение сырого текста без следов HTML.
HTML("Lorem <b>ipsum</b>.").plain_text
# >> Lorem ipsum.

# Замена тегов.
PolyHTML = HTML("Lorem <b>ipsum</b>.").replace_tag("b", "i")
PolyHTML.text
# >> Lorem <i>ipsum</i>.

# Экранирование спецсимволов Markdown.
PolyMarkdown = Markdwon("Lorem ipsum.").escape()
Text = PolyMarkdown.text
# >> Lorem ipsum\.

# Все обработчики поддерживают приведение к строковому типу.
PolyHTML = HTML("Lorem <b>ipsum</b>.")
str(PolyHTML)
# >> Lorem <b>ipsum</b>.
```
