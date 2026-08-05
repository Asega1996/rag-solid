from dotenv import load_dotenv
load_dotenv()

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import MarkdownHeaderTextSplitter
from vectorstore_factory import get_vectorstore

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

vectorstore = get_vectorstore()
vectorstore.add_documents(chunks)

print("Indexing completed.")