from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
import requests
import docx

class ContextManager:
    def __init__(self, store_path):
        self.store_path = store_path
        self.embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        self.chroma_db = None
        self.load_db()
        print(">>> context manager - init")
    
    
    def is_title(self, paragraph):
        return paragraph.style.name == 'Heading 2' or paragraph.style.name == 'Heading 1'

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
        matches_str = "\n\n\n".join([f"{m.page_content}" for m in matches])
        return matches_str