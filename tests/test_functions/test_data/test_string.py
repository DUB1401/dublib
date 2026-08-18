from dublib.functions import data

def test_CheckForCyrillic():
	assert data.string.CheckForCyrillic("123qwe!") is False
	assert data.string.CheckForCyrillic("123йцу!") is True

def test_СontainsAlpha():
	assert data.string.СontainsAlpha("123!@") is False
	assert data.string.СontainsAlpha("123q!@") is True

def test_MultipleReplace():
	assert data.string.MultipleReplace("123_456_789", ("456", "789"), "0") == "123_0_0"

def test_RemoveRecurringSubstrings():
	assert data.string.RemoveRecurringSubstrings("12123412", "12") == "123412"

def test_StripAlpha():
	assert data.string.StripAlpha("123qwe!") == "qwe"