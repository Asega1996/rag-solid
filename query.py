from dotenv import load_dotenv
load_dotenv()

import os
from vectorstore_factory import get_vectorstore
from llm_factory import get_chat_llm
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

vectorstore = get_vectorstore()
k = int(os.getenv("RETRIEVER_K", "6"))
retriever = vectorstore.as_retriever(search_kwargs={"k": k})

llm = get_chat_llm()

prompt = ChatPromptTemplate.from_template("""You are an expert assistant in SOLID principles and software best practices.
Use ONLY the following context to answer. Do not use any prior knowledge.
If the context is missing information needed to fully answer, explicitly say what's missing instead of guessing.
Include a short source list at the end of your answer, using the provided source file names.

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