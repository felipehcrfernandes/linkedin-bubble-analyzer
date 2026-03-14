import re


def clean_text(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = text.lower()
    text = re.sub(r"\s+", " ", text).strip()
    return text


def clean_post(post: dict) -> dict:
    cleaned = dict(post)
    cleaned["cleaned_text"] = clean_text(post.get("content", ""))
    return cleaned
