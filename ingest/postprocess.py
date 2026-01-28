import re
from typing import List

from ingest.parser import SnipParagraph


VALID_PARAGRAPH = re.compile(r"^\d+\.\d+(\.\d+)*$")


def is_valid_paragraph(p: SnipParagraph) -> bool:
    return bool(VALID_PARAGRAPH.match(p.paragraph))


def remove_tables(text: str) -> str:
    triggers = ["Таблица", "Рисунок", "Приложение"]
    for t in triggers:
        idx = text.find(t)
        if idx != -1:
            return text[:idx].strip()
    return text


def fix_hyphenation(text: str) -> str:
    # убираем переносы типа "тех­ нический"
    text = re.sub(r"(\w)-\s+(\w)", r"\1\2", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def postprocess(paragraphs: List[SnipParagraph]) -> List[SnipParagraph]:
    cleaned = []

    for p in paragraphs:
        if not is_valid_paragraph(p):
            continue

        text = remove_tables(p.text)
        text = fix_hyphenation(text)

        p.text = text
        cleaned.append(p)

    return cleaned
