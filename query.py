from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

embeddings = OllamaEmbeddings(model="nomic-embed-text")
vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 6})

llm = ChatOllama(model="llama3.1:8b", temperature=0.1)

prompt = ChatPromptTemplate.from_template("""You are an expert assistant in SOLID principles and software best practices.
Use ONLY the following context to answer. Do not use any prior knowledge.
If the context is missing information needed to fully answer, explicitly say what's missing instead of guessing.

Context:
{context}

Question: {question}

Answer:""")

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

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

        # Show retrieved sources
        retrieved_docs = retriever.invoke(question)
        print("\n--- Retrieved sources ---")
        for doc in retrieved_docs:
            print(f"- {doc.metadata.get('source', 'unknown')}")

        # Generate answer
        answer = rag_chain.invoke(question)
        print("\n--- Answer ---")
        print(answer)