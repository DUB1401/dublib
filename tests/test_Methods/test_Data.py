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
	assert Data.StringToBool("0") is False
	assert Data.StringToBool("fAlsE") is False
	assert Data.StringToBool("1") is True
	assert Data.StringToBool("") is False


def test_ToSequence():
	assert Data.ToSequence("test") == ("test",)
	assert Data.ToSequence(["test"]) == ("test",)
	assert Data.ToSequence("test", target_type = list) == ["test"]

def test_Zerotify():
	assert Data.Zerotify(0) is None
	assert Data.Zerotify("") is None
	assert Data.Zerotify(-1) == -1
	assert Data.Zerotify("1") == "1"

def test_CheckForCyrillic():
	assert Data.CheckForCyrillic("123qwe!") is False
	assert Data.CheckForCyrillic("123йцу!") is True

def test_СontainsAlpha():
	assert Data.СontainsAlpha("123!@") is False
	assert Data.СontainsAlpha("123q!@") is True

def test_MultipleReplace():
	assert Data.MultipleReplace("123_456_789", ("456", "789"), "0") == "123_0_0"

def test_RemoveRecurringSubstrings():
	assert Data.RemoveRecurringSubstrings("12123412", "12") == "123412"

def test_StripAlpha():
	assert Data.StripAlpha("123qwe!") == "qwe"

def test_InsertDictionaryAfterKey():
	FirstDict = {"1": 1, "2": 2, "3": 3}
	SecondDict = {"3": 33, "4": 4}

	Result = Data.InsertDictionaryAfterKey(FirstDict, SecondDict, "1")
	assert tuple(Result.keys())[1] == "3"
	assert tuple(Result.values())[1] == 3
	Result = Data.InsertDictionaryAfterKey(FirstDict, SecondDict, "1", overwrite = True)
	assert tuple(Result.values())[1] == 33

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