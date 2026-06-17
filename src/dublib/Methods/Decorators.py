from ..CLI.TextStyler import FastStyler

import functools
import warnings

def deprecated(message: str | None = None):
	"""
	Декоратор: помечает функцию как устаревшую.

	:param message: Сопровождающее сообщение.
	:type message: str | None
	"""

	def decorator(function):

		@functools.wraps(function)
		def Wrapper(*args, **kwargs):
			Message = f" {message}" or ""
			Function = FastStyler(function.__name__).decorate.bold
			warnings.warn(f"{Function} is deprecated.{Message}", DeprecationWarning, stacklevel = 2)

			return function(*args, **kwargs)
		
		return Wrapper
	
	return decorator

def run_before_method(method_name: str):
	"""
	Декоратор: запускает публичный или защищённый метод, не принимающий аргументов, перед выполнением метода экземпляра класса. Запущенный метод имеет доступ к экземпляру.

	:param method_name: Имя метода.
	:type method_name: str
	"""

	if method_name.startswith("__"):
		raise ValueError("Only public and protected methods supported in @run_befor_method decorator.")
	
	def decorator(function):

		@functools.wraps(function)
		def Wrapper(*args, **kwargs):
			if args:
				Object = args[0]
				Method = getattr(Object, method_name, None)
				if Method and callable(Method):
					Method()

			return function(*args, **kwargs)
		
		return Wrapper
	
	return decorator