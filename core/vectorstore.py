from langchain_chroma import Chroma


def get_vectorstore(cfg, embeddings):
    vs_type = cfg["vectorstore"]["type"]

    if vs_type == "chroma":
        return Chroma(
            collection_name=cfg["vectorstore"]["collection_name"],
            persist_directory=cfg["project"]["persist_dir"],
            embedding_function=embeddings,
        )

    raise ValueError("Unknown vectorstore")
