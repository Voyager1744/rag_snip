from ingest.parser import parse_snip
from ingest.postprocess import postprocess
from ingest.to_documents import to_documents

from core.embeddings import get_embeddings
from core.vectorstore import get_vectorstore


def build_store(cfg, pdf_path):
    paragraphs = parse_snip(pdf_path)
    paragraphs = postprocess(paragraphs)
    docs = to_documents(paragraphs)

    embeddings = get_embeddings(cfg)
    db = get_vectorstore(cfg, embeddings)

    db.add_documents(docs)
