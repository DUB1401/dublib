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

def test_CheckForCyrillic():
	assert data.CheckForCyrillic("123qwe!") is False
	assert data.CheckForCyrillic("123йцу!") is True

def test_СontainsAlpha():
	assert data.СontainsAlpha("123!@") is False
	assert data.СontainsAlpha("123q!@") is True

def test_MultipleReplace():
	assert data.MultipleReplace("123_456_789", ("456", "789"), "0") == "123_0_0"

def test_RemoveRecurringSubstrings():
	assert data.RemoveRecurringSubstrings("12123412", "12") == "123412"

def test_StripAlpha():
	assert data.StripAlpha("123qwe!") == "qwe"

def test_InsertDictionaryAfterKey():
	FirstDict = {"1": 1, "2": 2, "3": 3}
	SecondDict = {"3": 33, "4": 4}

	Result = data.InsertDictionaryAfterKey(FirstDict, SecondDict, "1")
	assert tuple(Result.keys())[1] == "3"
	assert tuple(Result.values())[1] == 3
	Result = data.InsertDictionaryAfterKey(FirstDict, SecondDict, "1", overwrite = True)
	assert tuple(Result.values())[1] == 33

def test_LowerDictionaryKeys():
	assert data.LowerDictionaryKeys({"AbC": 1, 34: "ACb"}) == {"abc": 1, 34: "ACb"}

def test_MergeDictionaries():
	assert data.MergeDictionaries(
		{"1": 1, "3": 3},
		{"2": 2}
	) == {"1": 1, "2": 2, "3": 3}
	assert data.MergeDictionaries(
		{"1": 1, "2": 2, "3": 3},
		{"2": 4},
		overwrite = True
	) == {"1": 1, "2": 4, "3": 3}

def test_ReplaceDictionaryKey():
	assert data.ReplaceDictionaryKey(
		{"1": 1, "2": 2},
		"2",
		"3"
	) == {"1": 1, "3": 2}
	assert tuple(data.ReplaceDictionaryKey(
		{"1": 1, "2": 2, "3": 3},
		"2",
		"4"
	).keys()) == ("1", "4", "3")