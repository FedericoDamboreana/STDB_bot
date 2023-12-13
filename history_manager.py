import requests

class ChatHistoryManager:
    def __init__(self):
        self.chat_history = []
        self.last_message = ""
        self.headers = {
            "Authorization": "Bearer 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"
        }
    
    def add_ai_message(self, message):
        self.chat_history.append({"sender": "User", "message": self.last_message})
        self.last_message = ""
        self.chat_history.append({"sender": "AI", "message": message})
        
    
    def add_user_message(self, message):
        self.last_message = message
    
    def get_history(self):
        history_str = "\n".join([f"{m['sender']}: {m['message']}" for m in self.chat_history])
        return history_str
    
    def save_history_to_disk(self, filename):
        # a implementar
        pass
    
    def load_history_from_disk(self, filename):
        # a implementar
        pass
    
    def clear_history(self):
        self.chat_history = []
    
    def get_optimized_history(self):
        payload = {
            "inputs": "Given this conversation: \n" + self.get_history() + "\n\nSummary: " ,
        }

        response = requests.post(
            "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct",
            headers=self.headers,
            json=payload
        )
        if response.status_code == 200:
            summary = response.json()
            return summary[0]["generated_text"].split("Summary:")[-1].strip()
        else:
            return f"An error occurred: {response.text}"
        
    def generate_query(self, summary):
        prompt = "\n\nWhat does the user wants to know?\nWhat the user wants to know is:"
        payload = {
            "inputs": "This is the summary of a conversation of a user and a AI: " + summary + "\n\nThis is the user's last question: " + self.last_message + prompt,
        }
        print("=====================================================================")
        print("\nINPUT\n")
        print(payload["inputs"])

        response = requests.post(
            "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct",
            headers=self.headers,
            json=payload
        )
        if response.status_code == 200:
            summary = response.json()
            return summary[0]["generated_text"].split("What the user wants to know is:")[-1].strip()
        else:
            return "Error: " + response.text



chat1 = ChatHistoryManager()
chat1.add_user_message("I'm planning a vacation. Any suggestions?")
chat1.add_ai_message("That sounds exciting! What kind of places do you like?")
chat1.add_user_message("I love beaches and sunny weather.")
chat1.add_ai_message("You might enjoy visiting the Caribbean islands then. They have beautiful beaches.")
chat1.add_user_message("That's a great idea! How's the weather there around this time?")

chat2 = ChatHistoryManager()
chat2.add_user_message("I'm trying to decide what to cook for dinner.")
chat2.add_ai_message("What kind of cuisine do you enjoy?")
chat2.add_user_message("I really like Italian food.")
chat2.add_ai_message("How about making spaghetti carbonara? It's a classic Italian dish.")
chat2.add_user_message("Good suggestion! Do you have a recipe?")

chat3 = ChatHistoryManager()
chat3.add_user_message("I'm looking to buy a new laptop. Any advice?")
chat3.add_ai_message("Sure, what will you be using it for mostly?")
chat3.add_user_message("Mostly for software development.")
chat3.add_ai_message("You might want a laptop with a powerful CPU, plenty of RAM, and a solid-state drive for faster performance.")
chat3.add_user_message("Do you have any specific models in mind?")

chat4 = ChatHistoryManager()
chat4.add_user_message("I want to watch a movie tonight. Any recommendations?")
chat4.add_ai_message("What genre do you prefer?")
chat4.add_user_message("I love science fiction.")
chat4.add_ai_message("Have you seen 'Interstellar'? It's a great sci-fi movie.")
chat4.add_user_message("Yes, I loved it! Anything similar?")

chat5 = ChatHistoryManager()
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
