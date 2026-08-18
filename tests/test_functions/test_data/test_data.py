from dublib.functions import data

def test_Copy():
	Dictionary = {"test": [1]}
	Copy = data.Copy(Dictionary)
	assert Copy is not Dictionary
	assert Copy["test"] is not Dictionary["test"]

def test_StringifyFloat():
	assert data.StringifyFloat(1.056) == "1.06"
	assert data.StringifyFloat(1.054) == "1.05"
	assert data.StringifyFloat(1.0) == "1"
	assert data.StringifyFloat(0.00) == "0"

def test_StringToBool():
	assert data.StringToBool("0") is False
	assert data.StringToBool("fAlsE") is False
	assert data.StringToBool("1") is True
	assert data.StringToBool("") is False


def test_ToSequence():
	assert data.ToSequence("test") == ("test",)
	assert data.ToSequence(["test"]) == ("test",)
	assert data.ToSequence("test", target_type = list) == ["test"]

def test_Zerotify():
	assert data.Zerotify(0) is None
	assert data.Zerotify("") is None
	assert data.Zerotify(-1) == -1
	assert data.Zerotify("1") == "1"