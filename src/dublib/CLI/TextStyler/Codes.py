import enum

class Drops(enum.Enum):
	"""Перечисление сбрасывающих кодов ANSI."""

	RESET = 0

	DEFAULT_COLOR = 39
	DEFAULT_BACKGROUND = 49

	DISABLE_BOLD = 22
	DISABLE_ITALIC = 23
	DISABLE_UNDERLINED = 24
	DISABLE_BLINCKED = 25
	DISABLE_THROUGHLINED = 29
	DISABLE_UPPERLINED = 29

class Colors(enum.Enum):
	"""Перечисление кодов цветов ANSI."""

	Black = 30
	Red = 31
	Green = 32
	Yellow = 33
	Blue = 34
	Magenta = 35
	Cyan = 36
	White = 37
	Gray = 90
	BrightRed = 91
	BrightGreen = 92
	BrightYellow = 93
	BrightBlue = 94
	BrightMagenta = 95
	BrightCyan = 96
	BrightWhite = 97

class BackgroundsColors(enum.Enum):
	"""Перечисление кодов цветов фона ANSI."""

	Black = 40
	Red = 41
	Green = 42
	Yellow = 43
	Blue = 44
	Magenta = 45
	Cyan = 46
	White = 47
	Gray = 100
	BrightRed = 101
	BrightGreen = 102
	BrightYellow = 103
	BrightBlue = 104
	BrightMagenta = 105
	BrightCyan = 106
	BrightWhite = 107

class Decorations(enum.Enum):
	"""Перечисление кодов декораций ANSI."""

	Bold = 1
	Italic = 3
	Underlined = 4
	Blincked = 5
	Throughline = 9
	DoubleUnderlined = 21
	Upperlined = 53