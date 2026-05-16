from dublib.Exceptions.Engine import Bus as BusExceptions
from dublib.Engine.Bus import ExecutionResult

def test_check_data():
	Result = ExecutionResult()
	Result[123] = 456
	Result["123"] = "456"

	assert Result.check_data("123") == True
	assert Result.check_data(123) == True
	assert Result.check_data(456) == False

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
	assert IsExceptionRaised == True

	IsExceptionRaised = None
	ResultOne.rules.require_value_initialization.disable()
	try: 
		ResultOne.value
		IsExceptionRaised = False
	except BusExceptions.ValueNotInintialized: IsExceptionRaised = True
	assert IsExceptionRaised == False

	# Слияние значений.
	assert ResultOne.is_value_setted == False
	ResultOne.value = 123
	assert ResultOne.is_value_setted == True
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
	assert ResultOne.messages.has_errors == False
	ResultOne.messages.push_error("Error")
	assert ResultOne.messages.has_errors == True

	assert ResultTwo.messages.has_warnings == False
	ResultTwo.messages.push_warning("Warning")
	assert ResultTwo.messages.has_warnings == True

	ResultOne += ResultTwo
	assert ResultOne.messages.has_warnings == True
	assert ResultOne.messages.count == 2

def test_delete_value():
	Result = ExecutionResult()
	assert Result.is_value_setted == False
	Result.value = 123
	assert Result.is_value_setted == True
	Result.value = None
	assert Result.is_value_setted == True
	Result.delete_value()
	assert Result.is_value_setted == False
	assert bool(Result) == False

def test_set_code():
	Result = ExecutionResult()
	assert Result.code == None
	Result.code = 123
	assert Result.code == 123

def test_set_value():
	Result = ExecutionResult()
	Result.value = 123
	assert Result.value == 123
	Result.value = None
	assert Result.is_value_setted == True