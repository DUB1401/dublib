from dublib.functions import data

def test_deep_copy():
	Dictionary = {"test": [1]}
	Copy = data.deep_copy(Dictionary)
	assert Copy is not Dictionary
	assert Copy["test"] is not Dictionary["test"]

def test_stringify_float():
	assert data.stringify_float(1.056) == "1.06"
	assert data.stringify_float(1.054) == "1.05"
	assert data.stringify_float(1.0) == "1"
	assert data.stringify_float(0.00) == "0"

def test_string_to_bool():
	assert data.string_to_bool("0") is False
	assert data.string_to_bool("fAlsE") is False
	assert data.string_to_bool("1") is True
	assert data.string_to_bool("") is False


def test_to_sequence():
	assert data.to_sequence("test") == ("test",)
	assert data.to_sequence(["test"]) == ("test",)
	assert data.to_sequence("test", target_type = list) == ["test"]

def test_zerotify():
	assert data.zerotify(0) is None
	assert data.zerotify("") is None
	assert data.zerotify(-1) == -1
	assert data.zerotify("1") == "1"