from dublib.engine.bus import ExecutionResult
from dublib.exceptions.engine import bus as BusExceptions

def test_check_data():
	Result = ExecutionResult()
	Result[123] = 456
	Result["123"] = "456"

	assert Result.check_data("123") is True
	assert Result.check_data(123) is True
	assert Result.check_data(456) is False

def test_merge():
	
	# Слияние целочисленных кодов.
	ResultOne = ExecutionResult()
	ResultTwo = ExecutionResult()
	ResultOne.code = 1
	ResultTwo.code = None
	ResultOne += ResultTwo
	assert ResultOne.code == 1

	ResultOne.code = None
	ResultTwo.code = 2
	ResultOne += ResultTwo
	assert ResultOne.code == 2

	# Проверка инициализации значений.
	IsExceptionRaised = None

	try: 
		ResultOne.value
		IsExceptionRaised = False
	except BusExceptions.ValueNotInintialized: IsExceptionRaised = True
	assert IsExceptionRaised is True

	IsExceptionRaised = None
	ResultOne.rules.require_value_initialization.disable()
	try: 
		ResultOne.value
		IsExceptionRaised = False
	except BusExceptions.ValueNotInintialized: IsExceptionRaised = True
	assert IsExceptionRaised is False

	# Слияние значений.
	assert ResultOne.is_value_setted is False
	ResultOne.value = 123
	assert ResultOne.is_value_setted is True
	assert ResultOne.value == 123

	# Слияние дополнительных данных.
	ResultOne = ExecutionResult()
	ResultTwo = ExecutionResult()
	ResultOne[123] = 456
	ResultTwo[123] = 789
	ResultOne.merge(ResultTwo)
	assert ResultOne[123] == 789

	ResultOne[123] = 456
	ResultOne.merge(ResultTwo, overwrite = False)
	assert ResultOne[123] == 456

	# Слияние сообщений.
	assert ResultOne.messages.has_errors is False
	ResultOne.messages.push_error("Error")
	assert ResultOne.messages.has_errors is True

	assert ResultTwo.messages.has_warnings is False
	ResultTwo.messages.push_warning("Warning")
	assert ResultTwo.messages.has_warnings is True

	ResultOne += ResultTwo
	assert ResultOne.messages.has_warnings is True
	assert ResultOne.messages.count == 2

def test_delete_value():
	Result = ExecutionResult()
	assert Result.is_value_setted is False
	Result.value = 123
	assert Result.is_value_setted is True
	Result.value = None
	assert Result.is_value_setted is True
	Result.delete_value()
	assert Result.is_value_setted is False
	assert bool(Result) is False

def test_set_code():
	Result = ExecutionResult()
	assert Result.code is None
	Result.code = 123
	assert Result.code == 123

def test_set_value():
	Result = ExecutionResult()
	Result.value = 123
	assert Result.value == 123
	Result.value = None
	assert Result.is_value_setted is True