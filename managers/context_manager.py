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

    def create(self, file_name):
        doc = docx.Document(self.store_path + "/" + file_name)
        document_text = "\n".join([para.text for para in doc.paragraphs if para.text.strip() != ''])
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=100,
            chunk_overlap=0,
            length_function=len,
            is_separator_regex=False
        )
        documents = text_splitter.create_documents([document_text])
        docs = text_splitter.split_documents(documents)
        self.chroma_db = Chroma.from_documents(docs, self.embedding_function, persist_directory="./store")
        print(">>> context manager - db created")
    
    def load_db(self):
        self.chroma_db = Chroma(persist_directory=self.store_path, embedding_function=self.embedding_function)
        print(">>> context manager - db loaded: ", self.chroma_db)

    def get_matches(self, query):
        matches = self.chroma_db.similarity_search(query, k=3)
        matches_str = "\n".join([f"{m.page_content}" for m in matches])
        return matches_str

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
