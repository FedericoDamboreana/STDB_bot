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
        self.headers = {
            "Authorization": "Bearer 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"
        }
        print(">>> context manager - init")
    
    
    def is_title(self, paragraph):
        return paragraph.style.name == 'Heading 2' or paragraph.style.name == 'Heading 1'

    def create_test(self, file_name):
        doc = docx.Document(self.store_path + "/" + file_name)
        db_elements = []
        current_element = {'title': '', 'content': ''}

        for para in doc.paragraphs:
            if self.is_title(para):
                if current_element['title']:
                    content = current_element['content'].strip()
                    db_elements.append(current_element['title'] + "\n" + content)
                    current_element = {'title': '', 'content': ''}
                current_element['title'] = para.text
            else:
                current_element['content'] += para.text + "\n"

        if current_element['title']:
            content = current_element['content'].strip()
            db_elements.append(current_element['title'] + "\n" + content)
        

        for e in db_elements:
            print("\n\n=======================\n\n")
            print(e)

        document_text = "\n\n\n".join([e for e in db_elements if e.strip() != ''])
        text_splitter = CharacterTextSplitter(
            separator="\n\n\n",
            chunk_size=400,
            chunk_overlap=0,
            length_function=len,
            is_separator_regex=False
        )
        documents = text_splitter.create_documents([document_text])
        docs = text_splitter.split_documents(documents)
        self.chroma_db = Chroma.from_documents(docs, self.embedding_function, persist_directory="./store")
        

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