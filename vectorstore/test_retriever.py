from core.embeddings import get_embeddings
from langchain_chroma import Chroma


def test_query(query: str):
    embeddings = get_embeddings()

    # открываем существующую коллекцию с embedding-функцией
    db = Chroma(persist_directory="chroma_store", embedding_function=embeddings)

    print("COLLECTION COUNT:", db._collection.count())

    retriever = db.as_retriever(search_type="mmr", search_kwargs={"k": 5})
    docs = retriever.invoke(query)

    for d in docs:
        print("\n---")
        print(d.metadata)
        print(d.page_content[:500])


if __name__ == "__main__":
    test_query("""Геодезическая основа сгущается до плотности, необходимой и достаточной для
выполнения инженерных изысканий, установкой на местности геодезических пунктов
временного, долговременного или постоянного закрепления. Тип закрепления, плотность
пунктов (реперов, точек) и их внешнее оформление обосновываются в программе в
зависимости от целей и задач изысканий, условий местности, используемых средств
измерений""")
