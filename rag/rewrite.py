import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:7b"

PROMPT = """
Перепиши пользовательский вопрос в форму, удобную для поиска по нормативным документам.
Добавь ключевые термины и формулировки.

Вопрос: {q}

Переписанный поисковый запрос:
"""


def rewrite_query(q: str) -> str:
    r = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": PROMPT.format(q=q),
            "stream": False,
        },
        timeout=60,
    )
    return r.json()["response"].strip()
