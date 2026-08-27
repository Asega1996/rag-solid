from dotenv import load_dotenv
load_dotenv()

import os
from vectorstore_factory import get_vectorstore
from llm_factory import get_chat_llm, get_embeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

vectorstore = get_vectorstore()
# Number of docs to retrieve initially
k = int(os.getenv("RETRIEVER_K", "6"))
base_retriever = vectorstore.as_retriever(search_kwargs={"k": k})

llm = get_chat_llm()
embeddings = get_embeddings()


class RerankingRetriever:
    """Wraps a LangChain retriever and re-ranks results using embedding cosine similarity."""

    def __init__(self, retriever, embeddings, rerank_top_n: int | None = None):
        self.retriever = retriever
        self.embeddings = embeddings
        self.rerank_top_n = rerank_top_n

    def invoke(self, query: str):
        docs = self.retriever.invoke(query)

        try:
            # Compute embeddings for query and documents
            query_emb = self.embeddings.embed_documents([query])[0]
            texts = [d.page_content for d in docs]
            docs_embs = self.embeddings.embed_documents(texts)

            # cosine similarity
            def cosine(a, b):
                import math

                dot = sum(x * y for x, y in zip(a, b))
                na = math.sqrt(sum(x * x for x in a))
                nb = math.sqrt(sum(y * y for y in b))
                return dot / (na * nb) if na and nb else 0.0

            scored = list(zip(docs, [cosine(query_emb, e) for e in docs_embs]))
            scored.sort(key=lambda t: t[1], reverse=True)

            if self.rerank_top_n:
                scored = scored[: self.rerank_top_n]

            return [s[0] for s in scored]
        except Exception:
            # Fallback to original order on any failure
            return docs

    def __or__(self, other):
        """Allow LCEL-style composition: (retriever | fn) where fn accepts docs.

        Returns a runnable-like object with an `invoke` method that accepts the
        original input (question) and applies the function to the retrieved docs.
        """

        parent = self

        class ComposedRunnable:
            def __init__(self, parent, fn):
                self.parent = parent
                self.fn = fn

            def invoke(self, input):
                docs = self.parent.invoke(input)
                return self.fn(docs)

            def __call__(self, input):
                return self.invoke(input)

        return ComposedRunnable(parent, other)


# Create a retriever that re-ranks results using embeddings
rerank_n = os.getenv("RERANK_N")
rerank_n = int(rerank_n) if rerank_n else None
retriever = RerankingRetriever(base_retriever, embeddings, rerank_top_n=rerank_n)

prompt = ChatPromptTemplate.from_template("""You are an expert assistant in SOLID principles and software best practices.
Use ONLY the following context to answer. Do not use any prior knowledge.
If the context is missing information needed to fully answer, explicitly say what's missing instead of guessing.
Be conservative: if the context does not contain the information necessary to answer confidently, respond with "I don't know; the provided context is insufficient." Do NOT hallucinate.
Always cite the sources used, listing the filenames at the end under a "Sources:" section.

Context:
{context}

Question: {question}

Answer:""")

def format_docs(docs):
    return "\n\n".join(
        f"[source: {doc.metadata.get('source', 'unknown')}\n{doc.page_content}"
        for doc in docs
    )

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

if __name__ == "__main__":
    while True:
        question = input("\nQuestion (or 'exit'): ")
        if question.lower() == "exit":
            break

        retrieved_docs = retriever.invoke(question)
        print("\n--- Retrieved sources ---")
        for doc in retrieved_docs:
            print(f"- {doc.metadata.get('source', 'unknown')}")

        answer = rag_chain.invoke(question)
        print("\n--- Answer ---")
        print(answer)