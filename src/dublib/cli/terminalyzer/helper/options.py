from dataclasses import dataclass

@dataclass(frozen = True)
class HelperOptions:
	"""Опции генератора справки по командам."""

	sort: bool = True
	stylize: bool = True
	parse_html: bool = True
	typing: bool = True

	indent: str = "\u0020" * 2
	position_marker: str = "•\u0020"
	base_marker: str = "‣\u0020"

