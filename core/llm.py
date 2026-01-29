from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOllama


def get_llm(cfg):
    provider = cfg["llm"]["provider"]

    if provider == "openai":
        return ChatOpenAI(
            model=cfg["llm"]["model"],
            temperature=cfg["llm"]["temperature"],
        )

    if provider == "ollama":
        return ChatOllama(
            model=cfg["llm"]["model"],
            temperature=cfg["llm"]["temperature"],
        )

    raise ValueError("Unknown LLM provider")
