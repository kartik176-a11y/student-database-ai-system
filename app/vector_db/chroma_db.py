import chromadb


client = chromadb.PersistentClient(
    path="./chroma_data"
)


collection = client.get_or_create_collection(
    name="student_information"
)


def add_document(
    document_id: str,
    document: str,
    metadata: dict | None = None
):
    collection.upsert(
        ids=[document_id],
        documents=[document],
        metadatas=[metadata] if metadata else None
    )


def search_documents(
    query: str,
    n_results: int = 5
):
    return collection.query(
        query_texts=[query],
        n_results=n_results
    )


def get_document_count():
    return collection.count()