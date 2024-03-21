from managers.context_manager import ContextManager
from managers.history_manager import HistoryManager
from managers.llm_manager import LLMManager
from managers.flow_helper import FlowHelper
from managers.cache_manager import CacheManager
from managers.fix_prompt_manager import FixPromptManager

class MainController:
    def __init__(self) -> None:
        self.helper = FlowHelper()
        self.cache = CacheManager('./cache')
        self.history_manager = HistoryManager()
        self.context_manager = ContextManager("./store")
        self.llm = LLMManager()
        self.prompt_fixer = FixPromptManager()
    

    def fix_chained_question(self, message):
        return self.prompt_fixer.fix_prompt(self.history_manager.get_history(), message)
    
    def process_user_message(self, message, retries=0):
        user_message = message
        is_related = self.helper.is_related(user_message)["is_related"]
        is_chained = self.helper.is_chained(user_message)["is_chained"]
        if is_chained and retries < 3:
            print(">>> fixing chained question. Try number ", retries)
            retries += 1
            user_message = self.fix_chained_question(user_message)
            user_message, is_related, is_chained = self.process_user_message(user_message, retries)

        return (user_message, is_related, is_chained)
    
    def end_process(self, question, response):
        self.history_manager.add_user_message(question)
        self.history_manager.add_ai_message(response)
        print("\n\n====================================\n\n")
        print(self.history_manager.get_history())

    def run(self):
        while True:
            response = ''
            is_related = False
            raw_message = input("\n\nUser: ") # mensaje original
            if raw_message.lower() == 'salir':
                break
            user_message, is_related, is_chained = self.process_user_message(raw_message)

            print(">>> user message: ", user_message) # nuevo mensaje (si es que se cambio)
            print(">>> related: ", is_related)
            print(">>> chained: ", is_chained)
            
            cached_response = self.cache.get_match(user_message)

            if cached_response != None:
                response = cached_response
                self.end_process(raw_message, response)
                continue

            if is_related:
                context = self.context_manager.get_matches(user_message)
                print(">>> context retrieved")
                response = self.llm.run(is_related, self.history_manager, context, raw_message)
            else:
                response = self.llm.run(is_related, self.history_manager, None, raw_message)
            
            if not is_chained: 
                self.cache.add(user_message, response)
            self.end_process(raw_message, response)


#Is there a way to create a custom study area in Business Analyst without using rings or drive times?


controller = MainController()

controller.run()