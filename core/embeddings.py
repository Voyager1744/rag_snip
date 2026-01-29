from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings


def get_embeddings(cfg):
    provider = cfg["embeddings"]["provider"]

    if provider == "huggingface":
        return HuggingFaceEmbeddings(model_name=cfg["embeddings"]["model"])

    if provider == "openai":
        return OpenAIEmbeddings()

    raise ValueError("Unknown embeddings provider")
