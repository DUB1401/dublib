from enum import Enum

class ParametersTypes(Enum):
	"""Перечисление типов значений параметров."""

	All = "All"
	Alpha = "Alpha"
	Base64 = "Base64"
	Bool = "Bool"
	Datetime = "Datetime"
	Email = "Email"
	Float = "Float"
	Integer = "Integer"
	IPv4 = "IPv4"
	IPv6 = "IPv6"
	Number = "Number"
	UnsignedInteger = "UnsignedInteger"
	URL = "URL"
	ValidPath = "ValidPath"