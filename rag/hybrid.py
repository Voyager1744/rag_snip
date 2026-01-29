from rank_bm25 import BM25Okapi


def bm25_search(query: str, docs: list, k: int = 20):
    tokenized = [d.page_content.split() for d in docs]
    bm25 = BM25Okapi(tokenized)
    scores = bm25.get_scores(query.split())

    ranked = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)
    return [d for d, _ in ranked[:k]]
