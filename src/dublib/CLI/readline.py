"""Обёртка для кросс-платформенной имплементации GNU readline."""

import sys

try: import readline
except ImportError:

	if sys.platform == "win32":
		try: import pyreadline3 as readline
		except ImportError: pass