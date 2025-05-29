from langchain.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.schema import Document
import os
from dotenv import load_dotenv
load_dotenv()

class VectorStore:
    def __init__(self, api_key=None):
        # Use env var if not passed
        if api_key is None:
            api_key = os.getenv("GEMINI_API_KEY")
        self.embeddings = GoogleGenerativeAIEmbeddings(
            google_api_key=api_key,
            model="models/embedding-001"
        )
        self.vector_store = None

    def create_vector_store(self, docs):
        # docs: list of dicts with 'content' and 'meta'
        langchain_docs = [
            Document(page_content=doc['content'], metadata=doc.get('meta', {}))
            for doc in docs
        ]
        self.vector_store = FAISS.from_documents(langchain_docs, self.embeddings)
        return self.vector_store

    def retrieve_info(self, query, k=3):
        if not self.vector_store:
            raise ValueError("Vector store not initialized. Call create_vector_store first.")
        return self.vector_store.similarity_search(query, k=k)
