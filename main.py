from managers.context_manager import ContextManager
from managers.history_manager import HistoryManager
from managers.llm_manager import LLMManager
from managers.flow_helper import FlowHelper

class MainController:
    def __init__(self) -> None:
        self.helper = FlowHelper()
        self.history_manager = HistoryManager()
        self.context_manager = ContextManager("./store")
        self.llm = LLMManager()
        
        self.context_manager.load_db()
    
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

            print(self.helper.is_related("hi!"))

            #history = self.history_manager.get_full_history()

            #state = self.state_manager.get_state(user_message)
            #if "question answering" in state:
            #    history = self.history_manager.get_full_history()
            #    response = self.qa_answer(history, user_message)
            #else:
            #    response = self.greeting_answer(user_message)

            #self.history_manager.add_user_message(user_message)
            #self.history_manager.add_ai_message(response)
            
            #print("\n\n====================================\n\n")
            #print(self.history_manager.get_history())


#"Is there a way to create a custom study area in Business Analyst without using rings or drive times?"


controller = MainController()

controller.run()