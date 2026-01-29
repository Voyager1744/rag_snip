# rag/rerank.py
from sentence_transformers import CrossEncoder

model = CrossEncoder("BAAI/bge-reranker-base")


def rerank(query: str, docs: list, top_k: int = 5):
    pairs = [(query, d.page_content) for d in docs]
    scores = model.predict(pairs)

    ranked = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)
    return [d for d, _ in ranked[:top_k]]
