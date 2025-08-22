import re


def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)

    text = re.sub(r"[^\w\s\.\-]", "", text)

    text = re.sub(r"\.{2,}", ".", text)

    return text.lower().strip()
