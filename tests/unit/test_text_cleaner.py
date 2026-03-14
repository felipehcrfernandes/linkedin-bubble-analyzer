from backend.processing.text_cleaner import clean_text, clean_post


def test_clean_text_removes_urls():
    text = "Check out https://example.com for more info"
    result = clean_text(text)
    assert "https://example.com" not in result
    assert "check out" in result


def test_clean_text_strips_html():
    text = "<b>hello</b> <a href='#'>world</a>"
    result = clean_text(text)
    assert "<b>" not in result
    assert "<a" not in result
    assert "hello" in result
    assert "world" in result


def test_clean_text_normalizes_whitespace():
    text = "hello   world\t\tfoo   bar"
    result = clean_text(text)
    assert result == "hello world foo bar"


def test_clean_text_lowercases():
    text = "HELLO World"
    result = clean_text(text)
    assert result == "hello world"


def test_clean_post_adds_cleaned_text_field():
    post = {"content": "Visit https://example.com NOW!", "author": "Alice"}
    result = clean_post(post)
    assert "cleaned_text" in result
    assert "https://example.com" not in result["cleaned_text"]
    assert result["author"] == "Alice"


def test_clean_text_empty_string():
    assert clean_text("") == ""
