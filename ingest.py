from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

loader = DirectoryLoader("data/", glob="*.md", loader_cls=TextLoader)
docs = loader.load()
headers_to_split_on = [("##", "section")]
splitter = MarkdownHeaderTextSplitter(headers_to_split_on)

chunks = []
for doc in docs:
    splits = splitter.split_text(doc.page_content)
    for s in splits:
        s.metadata["source"] = doc.metadata["source"]
    chunks.extend(splits)
print(f"Generated chunks: {len(chunks)}")

embeddings = OllamaEmbeddings(model="nomic-embed-text")
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

print("Indexing completed.")