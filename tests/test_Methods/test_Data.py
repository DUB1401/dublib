from dublib.Methods import Data

def test_Copy():
	Dictionary = {"test": [1]}
	Copy = Data.Copy(Dictionary)
	assert Copy is not Dictionary
	assert Copy["test"] is not Dictionary["test"]

def test_StringifyFloat():
	assert Data.StringifyFloat(1.056) == "1.06"
	assert Data.StringifyFloat(1.054) == "1.05"
	assert Data.StringifyFloat(1.0) == "1"
	assert Data.StringifyFloat(0.00) == "0"

def test_StringToBool():
	assert Data.StringToBool("0") == False
	assert Data.StringToBool("fAlsE") == False
	assert Data.StringToBool("1") == True
	assert Data.StringToBool("") == False


def test_ToIterable():
	assert Data.ToIterable("test") == ("test",)
	assert Data.ToIterable(["test"]) == ["test"]
	assert Data.ToIterable("test", iterable_type = list) == ["test"]

def test_Zerotify():
	assert Data.Zerotify(0) == None
	assert Data.Zerotify("") == None
	assert Data.Zerotify(-1) == -1
	assert Data.Zerotify("1") == "1"

def test_MultipleReplace():
	assert Data.MultipleReplace("123_456_789", ("456", "789"), "0") == "123_0_0"

def test_RemoveRecurringSubstrings():
	assert Data.RemoveRecurringSubstrings("12123412", "12") == "123412"

def test_StripAlpha():
	assert Data.StripAlpha("123qwe!") == "qwe"

def test_CheckForCyrillic():
	assert Data.CheckForCyrillic("123qwe!") == False
	assert Data.CheckForCyrillic("123йцу!") == True

def test_IsNotAlpha():
	assert Data.IsNotAlpha("123!@") == True
	assert Data.IsNotAlpha("123q!@") == False

def test_MergeDictionaries():
	assert Data.MergeDictionaries(
		{"1": 1, "3": 3},
		{"2": 2}
	) == {"1": 1, "2": 2, "3": 3}
	assert Data.MergeDictionaries(
		{"1": 1, "2": 2, "3": 3},
		{"2": 4},
		overwrite = True
	) == {"1": 1, "2": 4, "3": 3}

def test_ReplaceDictionaryKey():
	assert Data.ReplaceDictionaryKey(
		{"1": 1, "2": 2},
		"2",
		"3"
	) == {"1": 1, "3": 2}
	assert tuple(Data.ReplaceDictionaryKey(
		{"1": 1, "2": 2, "3": 3},
		"2",
		"4"
	).keys()) == ("1", "4", "3")