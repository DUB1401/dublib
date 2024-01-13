# Polyglot
**Polyglot** – это средство базовой работы с некоторыми языками разметки текста.

На данный момент поддерживаются: HTML, Markdown.

## Пример
```Python
from dublib.Polyglot import HTML, Markdown

# Получение сырого текста без следов HTML.
HTML("Some <b>html</b>.").plain_text

# Экранирование спецсимволов Markdown.
MarkdownObject = Markdwon("Some Markdown.").escape()
Text = MarkdownObject.text

# Все обработчики поддерживают приведение к строковому типу.
HTMLObject = HTML("Some <b>html</b>.")
str(HTMLObject)

MarkdownObject = Markdwon("Some Markdown.")
str(MarkdownObject)
```
