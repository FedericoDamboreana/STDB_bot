from managers.history_manager import HistoryManager
from managers.state_manager import StateManager
import re

chat1 = HistoryManager()
chat1.add_user_message("Hi, I am Hernan")
chat1.add_ai_message("Hi Hernan!")
chat1.add_user_message("How are you?")

chat2 = HistoryManager()
chat2.add_user_message("Hi, I am Hernan")

chat3 = HistoryManager()
chat3.add_user_message("I'm looking to buy a new laptop. Any advice?")
chat3.add_ai_message("Sure, what will you be using it for mostly?")
chat3.add_user_message("Mostly for software development.")
chat3.add_ai_message("You might want a laptop with a powerful CPU, plenty of RAM, and a solid-state drive for faster performance.")
chat3.add_user_message("Do you have any specific models in mind?")

chat4 = HistoryManager()
chat4.add_user_message("I want to watch a movie tonight. Any recommendations?")
chat4.add_ai_message("What genre do you prefer?")
chat4.add_user_message("I love science fiction.")
chat4.add_ai_message("Have you seen 'Interstellar'? It's a great sci-fi movie.")
chat4.add_user_message("Yes, I loved it! Anything similar?")


chats = [chat1, chat2, chat3, chat4]

state_manager = StateManager()

for chat in chats:
    full_history = chat.get_full_history()

    state = state_manager.get_state(full_history)

    print("\n\n")
    print(state)
#    print(state.split("The state that better match the conversation is ")[-1].rstrip('.'))
    print("\n=====================================================================")
