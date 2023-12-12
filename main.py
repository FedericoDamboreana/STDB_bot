from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import GPT4All
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
import numpy as np
import docx

embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

callbacks = [StreamingStdOutCallbackHandler()]
llm = GPT4All(model="./gpt4all-falcon-q4_0.gguf", callbacks=callbacks, verbose=True)

doc = docx.Document('dataset_1.docx')


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
chroma_db  = Chroma.from_documents(docs, embedding_function)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm, 
    retriever=chroma_db.as_retriever(search_kwargs={"k": 3}),
    memory=memory
)
print(">>> chain")
result = qa_chain({"question": "How do I access Infographics inside Business Analyst?"})
print(result['answer'])