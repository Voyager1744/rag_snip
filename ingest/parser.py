import re
import pdfplumber
from pathlib import Path

from pydantic import BaseModel


PARAGRAPH_PATTERN = re.compile(
    r"^(\d+\.\d+(?:\.\d+)*)\s+[А-ЯA-Z]"
)  # 4.2.1, 5.1.3.2 и т.д.


class SnipParagraph(BaseModel):
    text: str
    paragraph: str
    section: str
    source: str
    page: int


def clean_line(line: str) -> str:
    """Убираем мусор: двойные пробелы, переносы, номера страниц."""
    line = line.strip()
    if not line:
        return ""
    if re.match(r"^\d+$", line):  # номер страницы
        return ""
    line = re.sub(r"\s+", " ", line)
    # убираем переносы \xad
    line = re.sub(r"\xad +", "", line)

    return line


def extract_lines_from_pdf(pdf_path: Path) -> list[tuple[str, int]]:
    lines = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            for row_line in text.split("\n"):
                if row_line:
                    line = clean_line(row_line)
                    lines.append((line, page_num))
    return lines


def is_paragraph_start(line: str) -> bool:
    return bool(PARAGRAPH_PATTERN.match(line))


def extract_paragraph_number(line: str) -> str:
    return PARAGRAPH_PATTERN.match(line).group(1)


def get_section_from_paragraph(paragraph: str) -> str:
    parts = paragraph.split(".")
    return ".".join(parts[:2])  # 4.2 из 4.2.1


def parse_snip(pdf_path: Path) -> list[SnipParagraph]:
    lines = extract_lines_from_pdf(pdf_path)

    paragraphs: list[SnipParagraph] = []

    current_paragraph_number = None
    current_text = []
    current_page = None

    for line, page in lines:
        if is_paragraph_start(line):
            # Сохраняем предыдущий пункт
            if current_paragraph_number:
                paragraphs.append(
                    SnipParagraph(
                        text=" ".join(current_text).strip(),
                        paragraph=current_paragraph_number,
                        section=get_section_from_paragraph(current_paragraph_number),
                        source=pdf_path.name,
                        page=current_page,
                    )
                )

            # Начинаем новый
            current_paragraph_number = extract_paragraph_number(line)
            current_text = [line]
            current_page = page
        else:
            if current_paragraph_number:
                current_text.append(line)

    # Добавляем последний
    if current_paragraph_number:
        paragraphs.append(
            SnipParagraph(
                text=" ".join(current_text).strip() if current_text else "",
                paragraph=current_paragraph_number,
                section=get_section_from_paragraph(current_paragraph_number),
                source=pdf_path.name,
                page=current_page,
            )
        )

    return paragraphs
