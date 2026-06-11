from .Codes import Drops as _DropsCodes, Colors as _ColorsCodes, BackgroundsColors as _BackgroundsColorsCodes, Decorations as _DecorationsCodes

from dataclasses import dataclass

@dataclass(frozen = True)
class Drops:
	"""Набор специальных управляющих последовательностей ANSI."""

	RESET: str = f"\033[{_DropsCodes.RESET.value}m"

	DEFAULT_COLOR: str = f"\033[{_DropsCodes.DEFAULT_COLOR.value}m"
	DEFAULT_BACKGROUND: str = f"\033[{_DropsCodes.DEFAULT_BACKGROUND.value}m"

	DISABLE_BOLD: str = f"\033[{_DropsCodes.DISABLE_BOLD.value}m"
	DISABLE_ITALIC: str = f"\033[{_DropsCodes.DISABLE_ITALIC.value}m"
	DISABLE_UNDERLINED: str = f"\033[{_DropsCodes.DISABLE_UNDERLINED.value}m"
	DISABLE_BLINCKED: str = f"\033[{_DropsCodes.DISABLE_BLINCKED.value}m"
	DISABLE_THROUGHLINED: str = f"\033[{_DropsCodes.DISABLE_THROUGHLINED.value}m"
	DISABLE_UPPERLINED: str = f"\033[{_DropsCodes.DISABLE_UPPERLINED.value}m"

@dataclass(frozen = True)
class Colors:
	"""Набор управляющих последовательностей цветов ANSI."""

	Black: str = f"\033[{_ColorsCodes.Black.value}m"
	Red: str = f"\033[{_ColorsCodes.Red.value}m"
	Green: str = f"\033[{_ColorsCodes.Green.value}m"
	Yellow: str = f"\033[{_ColorsCodes.Yellow.value}m"
	Blue: str = f"\033[{_ColorsCodes.Blue.value}m"
	Magenta: str = f"\033[{_ColorsCodes.Magenta.value}m"
	Cyan: str = f"\033[{_ColorsCodes.Cyan.value}m"
	White: str = f"\033[{_ColorsCodes.White.value}m"
	Gray: str = f"\033[{_ColorsCodes.Gray.value}m"
	BrightRed: str = f"\033[{_ColorsCodes.BrightRed.value}m"
	BrightGreen: str = f"\033[{_ColorsCodes.BrightGreen.value}m"
	BrightYellow: str = f"\033[{_ColorsCodes.BrightYellow.value}m"
	BrightBlue: str = f"\033[{_ColorsCodes.BrightBlue.value}m"
	BrightMagenta: str = f"\033[{_ColorsCodes.BrightMagenta.value}m"
	BrightCyan: str = f"\033[{_ColorsCodes.BrightCyan.value}m"
	BrightWhite: str = f"\033[{_ColorsCodes.BrightWhite.value}m"

@dataclass(frozen = True)
class BackgroundColors:
	"""Набор управляющих последовательностей цветов фона ANSI."""

	Black: str = f"\033[{_BackgroundsColorsCodes.Black.value}m"
	Red: str = f"\033[{_BackgroundsColorsCodes.Red.value}m"
	Green: str = f"\033[{_BackgroundsColorsCodes.Green.value}m"
	Yellow: str = f"\033[{_BackgroundsColorsCodes.Yellow.value}m"
	Blue: str = f"\033[{_BackgroundsColorsCodes.Blue.value}m"
	Magenta: str = f"\033[{_BackgroundsColorsCodes.Magenta.value}m"
	Cyan: str = f"\033[{_BackgroundsColorsCodes.Cyan.value}m"
	White: str = f"\033[{_BackgroundsColorsCodes.White.value}m"
	Gray: str = f"\033[{_BackgroundsColorsCodes.Gray.value}m"
	BrightRed: str = f"\033[{_BackgroundsColorsCodes.BrightRed.value}m"
	BrightGreen: str = f"\033[{_BackgroundsColorsCodes.BrightGreen.value}m"
	BrightYellow: str = f"\033[{_BackgroundsColorsCodes.BrightYellow.value}m"
	BrightBlue: str = f"\033[{_BackgroundsColorsCodes.BrightBlue.value}m"
	BrightMagenta: str = f"\033[{_BackgroundsColorsCodes.BrightMagenta.value}m"
	BrightCyan: str = f"\033[{_BackgroundsColorsCodes.BrightCyan.value}m"
	BrightWhite: str = f"\033[{_BackgroundsColorsCodes.BrightWhite.value}m"

@dataclass(frozen = True)
class Decorations:
	"""Набор управляющих последовательностей декораций ANSI."""

	Bold: str = f"\033[{_DecorationsCodes.Bold.value}m"
	Italic: str = f"\033[{_DecorationsCodes.Italic.value}m"
	Underlined: str = f"\033[{_DecorationsCodes.Underlined.value}m"
	Blincked: str = f"\033[{_DecorationsCodes.Blincked.value}m"
	Throughline: str = f"\033[{_DecorationsCodes.Throughline.value}m"
	DoubleUnderlined: str = f"\033[{_DecorationsCodes.DoubleUnderlined.value}m"
	Upperlined: str = f"\033[{_DecorationsCodes.Upperlined.value}m"