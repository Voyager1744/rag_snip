from pathlib import Path
from core.embeddings import get_embeddings
from langchain_chroma import Chroma

from ingest.parser import parse_snip
from ingest.postprocess import postprocess
from ingest.to_documents import to_documents

from dotenv import load_dotenv

load_dotenv()


def build_store(pdf_path: Path):
    print("building store...")
    paragraphs = parse_snip(pdf_path)
    paragraphs = postprocess(paragraphs)

    docs = to_documents(paragraphs)
    embeddings = get_embeddings()

    db = Chroma.from_documents(
        docs, embedding=embeddings, persist_directory="chroma_store"
    )

    print("store built successfully")


if __name__ == "__main__":
    path_pdf: Path = (Path(__file__).parent.parent / "SP-47-13330-2016.pdf").resolve()
    build_store(path_pdf)
