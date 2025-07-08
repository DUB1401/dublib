from dublib.Polyglot import HTML, Markdown

def test_HTML():
	TestData = "<b><i class=\"dev\">test</i></b><b>123</b>"
	Object = HTML(TestData)

	assert Object.plain_text == "test123"
	assert Object.text == TestData

	assert str(Object) == TestData
	assert Object.has_tag("b") == 2
	assert Object.has_tag("u") == 0
	assert Object.remove_tags("i") == "<b>test</b><b>123</b>"
	assert Object.replace_tag("b", "span") == "<span>test</span><span>123</span>"
	
	TestData = "&copy;"
	Object = HTML(TestData)
	assert Object.unescape() == "©"

	TestData = "<b><i>test</b></i>"
	Object = HTML(TestData)
	assert Object.validate() == ("Bad tags order: expected </i>, found </b>.", "Bad tags order: expected </b>, found </i>.")

	TestData = "<b>test"
	Object = HTML(TestData)
	assert Object.validate() == ("Opening tag <b> not closed.",)

	TestData = "test</b>"
	Object = HTML(TestData)
	assert Object.validate() == ("Closing tag </b> not opened.",)

def test_Markdown():
	TestData = "**Hello**, [world](https://site.com)!"
	EscapedData = "\\*\\*Hello\\*\\*, \\[world\\]\\(https://site\\.com\\)\\!"
	Object = Markdown(TestData)

	assert Object.text == TestData
	assert Object.escaped_text == EscapedData

	assert str(Object) == TestData
	assert Object.escape() == EscapedData
	assert Object.text == EscapedData