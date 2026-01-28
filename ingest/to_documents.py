from langchain_core.documents import Document
from ingest.parser import SnipParagraph


def to_documents(paragraphs: list[SnipParagraph]) -> list[Document]:
    docs = []
    for p in paragraphs:
        docs.append(
            Document(
                page_content=p.text,
                metadata={
                    "paragraph_id": p.paragraph,
                    "section": p.section,
                    "source": p.source,
                    "page": p.page,
                },
            )
        )
    return docs
