# Polyglot
**Polyglot** – это средство базовой работы с некоторыми языками разметки текста.

На данный момент поддерживаются: HTML, Markdown.

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
