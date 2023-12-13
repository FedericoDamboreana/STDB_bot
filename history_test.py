from managers.history_manager import HistoryManager

chat1 = HistoryManager()
chat1.add_user_message("I'm planning a vacation. Any suggestions?")
chat1.add_ai_message("That sounds exciting! What kind of places do you like?")
chat1.add_user_message("I love beaches and sunny weather.")
chat1.add_ai_message("You might enjoy visiting the Caribbean islands then. They have beautiful beaches.")
chat1.add_user_message("That's a great idea! How's the weather there around this time?")

chat2 = HistoryManager()
chat2.add_user_message("I'm trying to decide what to cook for dinner.")
chat2.add_ai_message("What kind of cuisine do you enjoy?")
chat2.add_user_message("I really like Italian food.")
chat2.add_ai_message("How about making spaghetti carbonara? It's a classic Italian dish.")
chat2.add_user_message("Good suggestion! Do you have a recipe?")

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

chat5 = HistoryManager()
chat5.add_user_message("I'm thinking of taking up a new sport. What do you suggest?")
chat5.add_ai_message("That's a great idea! Are you looking for something indoors or outdoors?")
chat5.add_user_message("Preferably outdoors.")
chat5.add_ai_message("How about tennis? It's a fun outdoor sport and a great way to stay fit.")
chat5.add_user_message("Hmm, I've never played tennis. What do I need to start?")


chats = [chat1, chat2, chat3, chat4, chat5]

for chat in chats:
    optimized_history = chat.get_optimized_history()

    answer = chat.generate_query(optimized_history)
    print("\n\n")
    print("\nGENERATED QUERY\n")
    print(answer)
    print("\n=====================================================================")
