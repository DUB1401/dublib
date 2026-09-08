from dataclasses import dataclass

@dataclass
class HelperOptions:
	"""Опции генератора справки по командам."""

	sort: bool = True
	stylize: bool = True
	parse_html: bool = True
	typing: bool = False

	indent: str = "\u0020" * 2
	position_marker: str = "•\u0020"
	base_marker: str = "‣\u0020"
