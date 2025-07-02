from .Codes import *

from dataclasses import dataclass

@dataclass(frozen = True)
class Drops:
	"""Набор специальных управляющих последовательностей ANSI."""

	RESET = f"\033[{DropsCodes.RESET.value}m"

	DEFAULT_COLOR = f"\033[{DropsCodes.DEFAULT_COLOR.value}m"
	DEFAULT_BACKGROUND = f"\033[{DropsCodes.DEFAULT_BACKGROUND.value}m"

	DISABLE_BOLD = f"\033[{DropsCodes.DISABLE_BOLD.value}m"
	DISABLE_ITALIC = f"\033[{DropsCodes.DISABLE_ITALIC.value}m"
	DISABLE_UNDERLINED = f"\033[{DropsCodes.DISABLE_UNDERLINED.value}m"
	DISABLE_BLINCKED = f"\033[{DropsCodes.DISABLE_BLINCKED.value}m"
	DISABLE_THROUGHLINED = f"\033[{DropsCodes.DISABLE_THROUGHLINED.value}m"
	DISABLE_UPPERLINED = f"\033[{DropsCodes.DISABLE_UPPERLINED.value}m"

@dataclass(frozen = True)
class Colors:
	"""Набор управляющих последовательностей цветов ANSI."""

	Black = f"\033[{ColorsCodes.Black.value}m"
	Red = f"\033[{ColorsCodes.Red.value}m"
	Green = f"\033[{ColorsCodes.Green.value}m"
	Yellow = f"\033[{ColorsCodes.Yellow.value}m"
	Blue = f"\033[{ColorsCodes.Blue.value}m"
	Magenta = f"\033[{ColorsCodes.Magenta.value}m"
	Cyan = f"\033[{ColorsCodes.Cyan.value}m"
	White = f"\033[{ColorsCodes.White.value}m"
	Gray = f"\033[{ColorsCodes.Gray.value}m"
	BrightRed = f"\033[{ColorsCodes.BrightRed.value}m"
	BrightGreen = f"\033[{ColorsCodes.BrightGreen.value}m"
	BrightYellow = f"\033[{ColorsCodes.BrightYellow.value}m"
	BrightBlue = f"\033[{ColorsCodes.BrightBlue.value}m"
	BrightMagenta = f"\033[{ColorsCodes.BrightMagenta.value}m"
	BrightCyan = f"\033[{ColorsCodes.BrightCyan.value}m"
	BrightWhite = f"\033[{ColorsCodes.BrightWhite.value}m"

@dataclass(frozen = True)
class BackgroundColors:
	"""Набор управляющих последовательностей цветов фона ANSI."""

	Black = f"\033[{BackgroundsColorsCodes.Black.value}m"
	Red = f"\033[{BackgroundsColorsCodes.Red.value}m"
	Green = f"\033[{BackgroundsColorsCodes.Green.value}m"
	Yellow = f"\033[{BackgroundsColorsCodes.Yellow.value}m"
	Blue = f"\033[{BackgroundsColorsCodes.Blue.value}m"
	Magenta = f"\033[{BackgroundsColorsCodes.Magenta.value}m"
	Cyan = f"\033[{BackgroundsColorsCodes.Cyan.value}m"
	White = f"\033[{BackgroundsColorsCodes.White.value}m"
	Gray = f"\033[{BackgroundsColorsCodes.Gray.value}m"
	BrightRed = f"\033[{BackgroundsColorsCodes.BrightRed.value}m"
	BrightGreen = f"\033[{BackgroundsColorsCodes.BrightGreen.value}m"
	BrightYellow = f"\033[{BackgroundsColorsCodes.BrightYellow.value}m"
	BrightBlue = f"\033[{BackgroundsColorsCodes.BrightBlue.value}m"
	BrightMagenta = f"\033[{BackgroundsColorsCodes.BrightMagenta.value}m"
	BrightCyan = f"\033[{BackgroundsColorsCodes.BrightCyan.value}m"
	BrightWhite = f"\033[{BackgroundsColorsCodes.BrightWhite.value}m"

@dataclass(frozen = True)
class Decorations:
	"""Набор управляющих последовательностей декораций ANSI."""

	Bold = f"\033[{DecorationsCodes.Bold.value}m"
	Italic = f"\033[{DecorationsCodes.Italic.value}m"
	Underlined = f"\033[{DecorationsCodes.Underlined.value}m"
	Blincked = f"\033[{DecorationsCodes.Blincked.value}m"
	Throughline = f"\033[{DecorationsCodes.Throughline.value}m"
	DoubleUnderlined = f"\033[{DecorationsCodes.DoubleUnderlined.value}m"
	Upperlined = f"\033[{DecorationsCodes.Upperlined.value}m"