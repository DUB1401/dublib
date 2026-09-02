from enum import Enum

from . import types

class ValidableTypes(Enum):
	"""Перечисление типов валидаторов."""

	All = types.All
	Alpha = types.Alpha
	Base64 = types.Base64
	Bool = types.Bool
	Datetime = types.Datetime
	Domain = types.Domain
	Email = types.Email
	Float = types.Float
	Integer = types.Integer
	IPv4 = types.IPv4
	IPv6 = types.IPv6
	Number = types.Number
	Path = types.Path
	UnsignedInteger = types.UnsignedInteger
	URL = types.URL
	ValidPath = types.ValidPath