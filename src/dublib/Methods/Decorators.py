from ..CLI.TextStyler import FastStyler

from typing import Callable
import warnings

def deprecated(message: str | None = None) -> Callable:
	"""
	Декоратор: помечает функцию как устаревшую.

	:param message: Сопровождающее сообщение.
	:type message: str | None
	"""

	def decorator(function: Callable) -> Callable:

		def new_function(*args, **kwargs) -> Callable:
			Message = f" {message}" or ""
			Function = FastStyler(function.__name__).decorate.bold
			warnings.warn(f"{Function} is deprecated.{Message}", DeprecationWarning, stacklevel = 2)

			return function(*args, **kwargs)
		return new_function
	return decorator