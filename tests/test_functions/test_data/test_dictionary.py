from dublib.functions.data import dictionary

def test_insert_item():
	base_dict = {"1": 1, "2": 2, "3": 3}
	result = dictionary.insert_item(base_dict, "2", ("4", 4))

	assert tuple(result.keys())[2] == "4"
	assert tuple(result.values())[2] == 4

def test_insert_dictionary_after_key():
	first_dict = {"1": 1, "2": 2, "3": 3}
	second_dict = {"3": 33, "4": 4}
	result = dictionary.insert_dictionary_after_key(first_dict, second_dict, "1")

	assert tuple(result.keys())[1] == "3"
	assert tuple(result.values())[1] == 3

	result = dictionary.insert_dictionary_after_key(first_dict, second_dict, "1", overwrite = True)

	assert tuple(result.values())[1] == 33

def test_lower_keys():
	assert dictionary.lower_keys({"AbC": 1, 34: "ACb"}) == {"abc": 1, 34: "ACb"}

def test_replace_key():
	assert dictionary.replace_key(
		{"1": 1, "2": 2},
		"2",
		"3"
	) == {"1": 1, "3": 2}
	assert tuple(dictionary.replace_key(
		{"1": 1, "2": 2, "3": 3},
		"2",
		"4"
	).keys()) == ("1", "4", "3")