import enum

#==========================================================================================#
# >>>>> ПЕРЕЧИСЛЕНИЯ ДЕКОРАЦИЙ И ЦВЕТОВ <<<<< #
#==========================================================================================#

class Colors(enum.Enum):
	"""Перечисление цветов."""

	Black = "30"
	Red = "31"
	Green = "32"
	Yellow = "33"
	Blue = "34"
	Magenta = "35"
	Cyan = "36"
	White = "37"
	Gray = "90"
	BrightRed = "91"
	BrightGreen = "92"
	BrightYellow = "93"
	BrightBlue = "94"
	BrightMagenta = "95"
	BrightCyan = "96"
	BrightWhite = "97"

class Decorations(enum.Enum):
	"""Перечисление декораций."""

	Bold = "1"
	Faded = "2"
	Italic = "3"
	Underlined = "4"
	Flashing = "5"
	Throughline = "9"
	DoubleUnderlined = "21"
	Framed = "51"
	Surrounded = "52"
	Upperlined = "53"