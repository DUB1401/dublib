from dublib.functions import data

def test_is_contains_cyrillic():
	assert data.string.is_contains_cyrillic("123qwe!") is False
	assert data.string.is_contains_cyrillic("123йцу!") is True

def test_is_contains_alpha():
	assert data.string.is_contains_alpha("123!@") is False
	assert data.string.is_contains_alpha("123q!@") is True

def test_multiple_replace():
	assert data.string.multiple_replace("123_456_789", ("456", "789"), "0") == "123_0_0"

def test_emove_recurring_substrings():
	assert data.string.remove_recurring_substrings("12123412", "12") == "123412"

def test_strip_non_alpha():
	assert data.string.strip_non_alpha("123qwe!") == "qwe"