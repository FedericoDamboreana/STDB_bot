from managers.context_manager import ContextManager
from managers.history_manager import HistoryManager
from managers.state_manager import StateManager
from langchain.llms import GPT4All
import time
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from managers.llm_manager import LLM

class MainController:
    def __init__(self) -> None:
        self.primer = "You are an AI assistant having a conversation with a user. Answer the user question briefly and using context provided to get information"
        self.model = "gpt-3.5-turbo"
        self.api_key = "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"
        self.llm = LLM(self.model, self.primer, self.api_key)
    
        self.start_time = time.time()

        self.history_manager = HistoryManager()
        history_manager_time = time.time()
        print(">>> history manager")
        self.state_manager = StateManager()
        print(">>> state manager")
        self.context_manager = ContextManager("./store")
        context_manager_time = time.time()
        print(">>> context manager")

        # self.llm = GPT4All(model="./models/gpt4all-falcon-q4_0.gguf", callbacks=[StreamingStdOutCallbackHandler()], verbose=True, n_threads=6)
        # llm_time = time.time()
        # print(">>> LLM model")
        


        self.context_manager.load_db()
        load_db_time = time.time()

        total_time = time.time()

        print(f"Tiempo para inicializar HistoryManager: {history_manager_time - self.start_time:.2f} segundos")
        print(f"Tiempo para inicializar ContextManager: {context_manager_time - history_manager_time:.2f} segundos")
        #print(f"Tiempo para inicializar GPT4All: {llm_time - context_manager_time:.2f} segundos")
        #print(f"Tiempo para cargar la base de datos: {load_db_time - llm_time:.2f} segundos")
        print(f"Tiempo total para inicializar MainController: {total_time - self.start_time:.2f} segundos")

    def get_prompt_no_related(self, history):
        prompt = f"""
You are an AI assistant. Your only task is to respond briefly to the user's message. Do not initiate or continue a conversation beyond the greeting. 
Conversation history: "{history}"
Your response (brief and to the point):"""
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

    def run(self):
        while True:
            user_message = input("User: ")
            if user_message.lower() == 'salir':
                break
            self.start_time = time.time()
            self.history_manager.add_user_message(user_message)

            summary = self.history_manager.get_optimized_history()
            print("\n")
            print("optimized history")
            print(summary)

            input_optimizated = self.history_manager.generate_query(summary)
            print("\n")
            print("input optimizated")
            print(input_optimizated)

            context_optimizated = self.context_manager.get_optimized_context(input_optimizated)
            print("\n")
            print("context optimizated")
            print(context_optimizated)

            state = self.state_manager.get_state(context_optimizated, input_optimizated)
            print("\n")
            print("state")
            print(state)

            history = self.history_manager.get_full_history()
            print("\n")
            print("history")
            print(history)

            if state == "no related":
                prompt = self.get_prompt_no_related(history)
            else:
                prompt = self.get_prompt(history, context_optimizated, input_optimizated)

            last_message = self.history_manager.last_message
            response = self.llm.run([{"role": "user", "content": last_message}], prompt)

            print("AI: " + response)

            self.history_manager.add_ai_message(response)
            end_time = time.time()


#"Is there a way to create a custom study area in Business Analyst without using rings or drive times?"


controller = MainController()

controller.run()