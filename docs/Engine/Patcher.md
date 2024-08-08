# Patcher
**Patcher** – это подмодуль, использующийся для многоразовой модификации файлов исходного кода и конфигураций.

## Пример
### Файл до изменений
```Python
# Здесь должен быть шебанг.
PATH = None
```

### Патч
```Python
from dublib.Engine.Patcher import Patch

# Чтение файла.
File = Patch("file.py")
# Замена первой строки на некорректный шебанг.
File.replace_line(1, "!/usr/bin/env python3")
# Комментирование первой строки.
File.comment(1, space = False)
# Замена по регулярному выражению.
File.replace_by_regex("PATH = .+", "PATH = \"Settings.json\"")
# Сохранение изменённого файла.
File.save()
```

### Файл после изменений
```Python
#!/usr/bin/env python3"
PATH = "Settings.json"
```