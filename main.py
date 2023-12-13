from managers.context_manager import ContextManager
from managers.history_manager import HistoryManager

class MainController:
    def __init__(self) -> None:
        self.history_manager = HistoryManager()
        self.context_manager = ContextManager("./store")
        self.context_manager.load_db()
        pass

    def run(self):
        self.history_manager.add_user_message("Is there a way to create a custom study area in Business Analyst without using rings or drive times?")
        self.history_manager.add_ai_message("Yes, you can use the drawing tools to create a custom polygon. Would you like a guide on how to do that?")
        self.history_manager.add_user_message("Absolutely, how do I draw a custom polygon?")

        optimized_history = self.history_manager.get_optimized_history()
        print("=====================================================================")
        print("\nHISTORY\n")
        print(optimized_history)    

        query = self.history_manager.generate_query(optimized_history)
        print("=====================================================================")
        print("\nQUERY\n")
        print(query)

        context = self.context_manager.get_optimized_context(query)
        print("=====================================================================")
        print("\nCONTEXT\n")
        print(context)

controller = MainController()

controller.run()