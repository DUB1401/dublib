from ..CLI.TextStyler import TextStyler

from typing import Callable
import warnings

def deprecated(message: str | None = None) -> Callable:
    """
    Помечает функцию как устаревшую.
        message – сопровождающее сообщение.
    """

    def decorator(function: Callable) -> Callable:

        def new_function(*args, **kwargs) -> Callable:
            Message = f" {message}" or ""
            Function = TextStyler(function.__name__).decorate.bold
            warnings.warn(f"{Function} is deprecated.{Message}", DeprecationWarning, stacklevel = 2)

            return function(*args, **kwargs)
        return new_function
    return decorator