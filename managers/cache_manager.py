from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
import requests
import docx

class ContextManager:
    def __init__(self, store_path):
        self.store_path = store_path
        self.embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        self.chroma_db = None
        self.headers = {
            "Authorization": "Bearer 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"
        }
        print(">>> context manager - init")
    
    def load_db(self):
        self.chroma_db = Chroma(persist_directory=self.store_path, embedding_function=self.embedding_function)
        print(">>> context manager - db loaded: ", self.chroma_db)

    def get_matches(self, query):
        match = self.chroma_db.similarity_search_with_score(query, k=1)
        return match

    def get_optimized_context(self, query):
        matches = self.get_matches(query)
        payload = {
            "inputs": matches,
        }
        response = requests.post(
            "https://api-inference.huggingface.co/models/facebook/bart-large-cnn",
            headers=self.headers,
            json=payload
        )
        if response.status_code == 200:
            summary = response.json()
            return summary[0]["summary_text"]
        else:
            return f"An error occurred: {response.text}"
        pass