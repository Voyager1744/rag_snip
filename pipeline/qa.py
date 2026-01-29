from core.embeddings import get_embeddings
from core.vectorstore import get_vectorstore
from core.llm import get_llm
from core.prompts import get_prompt


def ask(cfg, question: str):
    embeddings = get_embeddings(cfg)
    db = get_vectorstore(cfg, embeddings)

    retriever = db.as_retriever(
        search_type=cfg["retriever"]["search_type"],
        search_kwargs={"k": cfg["retriever"]["k"]},
    )

    docs = retriever.invoke(question)
    context = "\n\n".join(d.page_content for d in docs)

    llm = get_llm(cfg)
    prompt = get_prompt(cfg["prompt"]["template"])

    chain = prompt | llm
    return chain.invoke({"context": context, "question": question})
