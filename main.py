from managers.context_manager import ContextManager
from managers.history_manager import HistoryManager
from managers.state_manager import StateManager
from langchain.llms import GPT4All
import time
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

class MainController:
    def __init__(self) -> None:
        self.start_time = time.time()

        self.history_manager = HistoryManager()
        history_manager_time = time.time()

        self.state_manager = StateManager()

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

    def get_greeting_prompt(self, user_message):
        return f"""
You are an AI assistant. Your only task is to respond briefly to the user's message. Do not initiate or continue a conversation beyond the message.

User's message: {user_message}

Your response (brief and to the point):"""

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
        print("==================================================================")
        print("GREETING FLOW\n\n")
        prompt = self.get_greeting_prompt(history)
        print("PROMPT")
        print(prompt)
        print("\n\nAI RESPONSE")
        response = self.llm(prompt, 
                            max_tokens=30,
                            temp=0.1,
                            top_k=10, 
                            top_p=0.2,)

        self.history_manager.add_ai_message(response)
        pass

    #qa
    def qa_answer(self, history):
        print("==================================================================")
        print("QA FLOW\n\n")
        query = self.history_manager.generate_query(history)

        context = self.context_manager.get_optimized_context(query)

        prompt = self.get_prompt(history, context, query)
        print("PROMPT")
        print(prompt)
        print("\n\nAI RESPONSE")
        response = self.llm(prompt)

        self.history_manager.add_ai_message(response)
        pass

    def run(self):
        while True:
            user_message = input("\n\nUser: ")
            if user_message.lower() == 'salir':
                break
            self.start_time = time.time()

            self.history_manager.add_user_message(user_message)

            history = self.history_manager.get_full_history()

            state = self.state_manager.get_state(history)
            
            if "question answering" in state:
                history = self.history_manager.get_optimized_history()
                self.qa_answer(history)
            else:
                self.greeting_answer(history)


#"Is there a way to create a custom study area in Business Analyst without using rings or drive times?"


controller = MainController()

controller.run()