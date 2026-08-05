import os

def get_chat_llm():
    provider = os.getenv("LLM_PROVIDER", "ollama")

    if provider == "ollama":
        from langchain_ollama import ChatOllama
        model = os.getenv("OLLAMA_CHAT_MODEL", "llama3.1:8b")
        return ChatOllama(model=model, temperature=0.1)

    if provider == "openai":
        from langchain_openai import ChatOpenAI
        model = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")
        return ChatOpenAI(model=model, temperature=0.1)

    if provider == "anthropic":
        from langchain_anthropic import ChatAnthropic
        model = os.getenv("ANTHROPIC_CHAT_MODEL", "claude-sonnet-4-6")
        return ChatAnthropic(model=model, temperature=0.1)

    raise ValueError(f"Unknown LLM_PROVIDER: {provider}")


def get_embeddings():
    provider = os.getenv("EMBEDDINGS_PROVIDER", "ollama")

    if provider == "ollama":
        from langchain_ollama import OllamaEmbeddings
        model = os.getenv("OLLAMA_EMBEDDING_MODEL", "nomic-embed-text")
        return OllamaEmbeddings(model=model)

    if provider == "openai":
        from langchain_openai import OpenAIEmbeddings
        model = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
        return OpenAIEmbeddings(model=model)

    raise ValueError(f"Unknown EMBEDDINGS_PROVIDER: {provider}")