import enum

#==========================================================================================#
# >>>>> ПЕРЕЧИСЛЕНИЯ ДЕКОРАЦИЙ И ЦВЕТОВ <<<<< #
#==========================================================================================#

class Colors(enum.Enum):
	"""Перечисление цветов."""

	Black = "0"
	Red = "1"
	Green = "2"
	Yellow = "3"
	Blue = "4"
	Purple = "5"
	Cyan = "6"
	White = "7"

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