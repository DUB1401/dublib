from dublib.functions import data

def test_insert_after_ley():
	FirstDict = {"1": 1, "2": 2, "3": 3}
	SecondDict = {"3": 33, "4": 4}

	Result = data.dictionary.insert_after_ley(FirstDict, SecondDict, "1")
	assert tuple(Result.keys())[1] == "3"
	assert tuple(Result.values())[1] == 3
	Result = data.dictionary.insert_after_ley(FirstDict, SecondDict, "1", overwrite = True)
	assert tuple(Result.values())[1] == 33

def test_lower_keys():
	assert data.dictionary.lower_keys({"AbC": 1, 34: "ACb"}) == {"abc": 1, 34: "ACb"}

def test_replace_key():
	assert data.dictionary.replace_key(
		{"1": 1, "2": 2},
		"2",
		"3"
	) == {"1": 1, "3": 2}
	assert tuple(data.dictionary.replace_key(
		{"1": 1, "2": 2, "3": 3},
		"2",
		"4"
	).keys()) == ("1", "4", "3")