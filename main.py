from managers.context_manager import ContextManager
from managers.history_manager import HistoryManager
from managers.state_manager import StateManager
from managers.llm_manager import LLMManager
import time

class MainController:
    def __init__(self) -> None:
        self.start_time = time.time()

        self.history_manager = HistoryManager()
        history_manager_time = time.time()

        self.state_manager = StateManager()

        self.context_manager = ContextManager("./store")
        context_manager_time = time.time()
        self.llm = LLMManager()
        llm_time = time.time()
        
        self.context_manager.load_db()
        load_db_time = time.time()

        total_time = time.time()

        print(f"Tiempo para inicializar HistoryManager: {history_manager_time - self.start_time:.2f} segundos")
        print(f"Tiempo para inicializar ContextManager: {context_manager_time - history_manager_time:.2f} segundos")
        print(f"Tiempo para inicializar GPT4All: {llm_time - context_manager_time:.2f} segundos")
        print(f"Tiempo para cargar la base de datos: {load_db_time - llm_time:.2f} segundos")
        print(f"Tiempo total para inicializar MainController: {total_time - self.start_time:.2f} segundos")
    
    #greeting
    def greeting_answer(self, message):
        print("==================================================================")
        print("GREETING FLOW\n\n")
        print("\n\nAI RESPONSE")
        response = self.llm.run('greeting', message=message)
        return response

    #qa
    def qa_answer(self, history, user_message):
        print("==================================================================")
        print("QA FLOW\n\n")
        query = self.history_manager.generate_query(history)
        context = self.context_manager.get_matches(query)
        response = self.llm.run('question answering', history, context, user_message)

        return response

    def run(self):
        while True:
            response = ''
            user_message = input("\n\nUser: ")
            if user_message.lower() == 'salir':
                break

            self.start_time = time.time()

            self.history_manager.add_user_message(user_message)

            history = self.history_manager.get_full_history()

            state = self.state_manager.get_state(user_message)
            print(">>> state: ", state)
            if "question answering" in state:
                history = self.history_manager.get_full_history()
                response = self.qa_answer(history, user_message)
            else:
                response = self.greeting_answer(user_message)

            self.history_manager.add_ai_message(response)
            
            print("\n\n====================================\n\n")
            print(self.history_manager.get_history())


#"Is there a way to create a custom study area in Business Analyst without using rings or drive times?"


controller = MainController()

controller.run()