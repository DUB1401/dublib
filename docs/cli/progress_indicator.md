# Progress Indicator
It is a module that allows to inform the terminal about the progress of task execution via the [OSC 9;4](https://docs.otty.sh/vt/osc/osc-9-4) protocol. Indicator system designed with the *Singleton* pattern, which prevents it from being recreated and guarantees the uniqueness of the control system.

## How to use
```Python
from time import sleep

from dublib.cli.progress_indicator import ProgressIndicator

indicator = ProgressIndicator()

for index in range(100):
	# Send control sequence in terminal.
	indicator.set_progress(index)
	# Simulating an error during runtime.
	if index == 55: indicator.error()

	sleep(0.1)

indicator.end()
```

```{eval-rst}
.. automodule:: dublib.cli.progress_indicator
	:members:
```
