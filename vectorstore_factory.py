import os
from llm_factory import get_embeddings

def get_vectorstore(persist_directory: str = "./chroma_db"):
    backend = os.getenv("VECTOR_BACKEND", "chroma")
    embeddings = get_embeddings()

    if backend == "chroma":
        from langchain_chroma import Chroma
        return Chroma(
            persist_directory=persist_directory,
            embedding_function=embeddings,
            collection_name="solid_principles",
        )

    if backend == "pgvector":
        from langchain_postgres import PGVector
        connection = os.getenv("PGVECTOR_CONNECTION")
        return PGVector(
            embeddings=embeddings,
            collection_name="solid_principles",
            connection=connection,
            use_jsonb=True,
        )

    if backend == "qdrant":
        from langchain_qdrant import QdrantVectorStore
        return QdrantVectorStore.from_existing_collection(
            embedding=embeddings,
            collection_name="solid_principles",
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY"),
        )

    raise ValueError(f"Unknown VECTOR_BACKEND: {backend}")