from managers.context_manager import ContextManager
from managers.history_manager import HistoryManager
from langchain.llms import GPT4All
import time
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

class MainController:
    def __init__(self) -> None:
        self.start_time = time.time()

        self.history_manager = HistoryManager()
        history_manager_time = time.time()

        self.context_manager = ContextManager("./store")
        context_manager_time = time.time()
        
        self.llm = GPT4All(model="./models/gpt4all-falcon-q4_0.gguf", callbacks=[StreamingStdOutCallbackHandler()], verbose=True, n_threads=10)
        llm_time = time.time()
        
        self.context_manager.load_db()
        load_db_time = time.time()

        total_time = time.time()

        print(f"Tiempo para inicializar HistoryManager: {history_manager_time - self.start_time:.2f} segundos")
        print(f"Tiempo para inicializar ContextManager: {context_manager_time - history_manager_time:.2f} segundos")
        print(f"Tiempo para inicializar GPT4All: {llm_time - context_manager_time:.2f} segundos")
        print(f"Tiempo para cargar la base de datos: {load_db_time - llm_time:.2f} segundos")
        print(f"Tiempo total para inicializar MainController: {total_time - self.start_time:.2f} segundos")

    def get_prompt(self, history):
        prompt = """
You are an assistant having a conversation with a user. Be kind.
This is a summary of the conversation:
{history}

Answer:"""
        return prompt.format(history=history)

    def get_prompt(self, history, context, query):
        prompt = """
                You are an assistant having a conversation with a user.
                Answer the user question briefly and using context provided to get information.
                This is a summary of the conversation: {history}
                This is some information to help you answer the user's question: {context}
                This is the user's question: {query}

                Answer:"""
        
        return prompt.format(history=history, context=context, query=query)
    
    #greeting
    def greeting_answer(self, history):
        prompt = self.get_prompt(history)
        response = self.llm(prompt)

        print("\n\nAI:", response)
        self.history_manager.add_ai_message(response)
        pass

    #qa
    def qa_answer(self, history):
        query = self.history_manager.generate_query(history)

        context = self.context_manager.get_optimized_context(query)

        prompt = self.get_prompt(history, context, query)

        response = self.llm(prompt)

        print("\n\nAI:", response)
        self.history_manager.add_ai_message(response)
        pass

    def run(self):
        while True:
            user_message = input("User: ")
            if user_message.lower() == 'salir':
                break
            self.start_time = time.time()

            self.history_manager.add_user_message(user_message)

            history = self.history_manager.get_full_history()
            history_time = time.time()

            state = self.state_manager.get_state(history)

            if state == "greeting":
                self.greeting_answer(history)
            else:
                history = self.history_manager.get_optimized_history()
                history_time = time.time()
                self.qa_answer(history)

            end_time = time.time()


#"Is there a way to create a custom study area in Business Analyst without using rings or drive times?"


controller = MainController()

controller.run()