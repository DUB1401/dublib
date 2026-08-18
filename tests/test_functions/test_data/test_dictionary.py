from dublib.functions import data

def test_InsertAfterKey():
	FirstDict = {"1": 1, "2": 2, "3": 3}
	SecondDict = {"3": 33, "4": 4}

	Result = data.dictionary.InsertAfterKey(FirstDict, SecondDict, "1")
	assert tuple(Result.keys())[1] == "3"
	assert tuple(Result.values())[1] == 3
	Result = data.dictionary.InsertAfterKey(FirstDict, SecondDict, "1", overwrite = True)
	assert tuple(Result.values())[1] == 33

def test_LowerDictionaryKeys():
	assert data.dictionary.LowerKeys({"AbC": 1, 34: "ACb"}) == {"abc": 1, 34: "ACb"}

def test_MergeDictionaries():
	assert data.dictionary.Merge(
		{"1": 1, "3": 3},
		{"2": 2}
	) == {"1": 1, "2": 2, "3": 3}
	assert data.dictionary.Merge(
		{"1": 1, "2": 2, "3": 3},
		{"2": 4},
		overwrite = True
	) == {"1": 1, "2": 4, "3": 3}

def test_ReplaceDictionaryKey():
	assert data.dictionary.ReplaceKey(
		{"1": 1, "2": 2},
		"2",
		"3"
	) == {"1": 1, "3": 2}
	assert tuple(data.dictionary.ReplaceKey(
		{"1": 1, "2": 2, "3": 3},
		"2",
		"4"
	).keys()) == ("1", "4", "3")