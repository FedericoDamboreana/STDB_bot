from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.docstore.document import Document
from langchain.vectorstores import Chroma

class CacheManager:
    def __init__(self, store_path):
        self.store_path = store_path
        self.embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        self.chroma_db = None
        self.load_db()
    
    def create(self):
        docs = [
            Document(
                page_content="I like bread",
                metadata={
                    "answer": "Me too!"
                }
            )
        ]
        self.chroma_db = Chroma.from_documents(docs, self.embedding_function, persist_directory=self.store_path)
        print(">>> cache manager - db created: ", self.chroma_db)
    
    def load_db(self):
        self.chroma_db = Chroma(persist_directory=self.store_path, embedding_function=self.embedding_function)
        print(">>> cache manager - db loaded: ", self.chroma_db)
    
    def add(self, question, answer):
        docs = [
            Document(
                page_content=question,
                metadata={
                    "answer": answer
                }
            )
        ]
        self.chroma_db.add_documents(docs)


    def get_match(self, query):
        result = None
        match = self.chroma_db.similarity_search_with_score(query, k=1)
        if match and len(match) > 0 and match[0][1] < 0.2:
            print(">>> cache manager - top result: ", match[0])
            result = match[0][0].metadata['answer']
        else:
            print(">>> cache manager - no coincidences")

        return result