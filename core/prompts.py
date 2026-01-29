from langchain_core.prompts import PromptTemplate

SNIP_QA_PROMPT = """
Ты инженер-геодезист. Отвечай строго на основании предоставленных фрагментов СП/СНИП.

Правила ответа:
- Не придумывай ничего вне контекста
- Обязательно указывай номера пунктов
- Если ответа в контексте нет — так и скажи

Контекст:
{context}

Вопрос:
{question}
"""


def get_prompt(name: str):
    if name == "snip_qa":
        return PromptTemplate.from_template(SNIP_QA_PROMPT)

    raise ValueError("Unknown prompt")
