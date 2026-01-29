from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from core.embeddings import get_embeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()

PROMPT = """
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


def ask(question: str) -> str:
    db = Chroma(
        persist_directory="chroma_store",
        embedding_function=get_embeddings(),
    )

    retriever = db.as_retriever(search_type="mmr", search_kwargs={"k": 8})
    docs = retriever.invoke(question)

    context = "\n\n".join(
        f"[п.{d.metadata['paragraph_id']} стр.{d.metadata['page']}]\n{d.page_content}"
        for d in docs
    )

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    prompt = ChatPromptTemplate.from_template(PROMPT)
    chain = prompt | llm

    result = chain.invoke({"context": context, "question": question})

    print(result.content)
