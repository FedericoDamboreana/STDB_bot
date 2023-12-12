import requests

class ChatHistoryManager:
    def __init__(self):
        self.chat_history = []
        self.headers = {
            "Authorization": "Bearer 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"
        }
    
    def add_ai_message(self, message):
        self.chat_history.append({"sender": "AI", "message": message})
    
    def add_user_message(self, message):
        self.chat_history.append({"sender": "User", "message": message})
    
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
            "inputs":"Summarize the following chat history: " + self.get_history(),
        }
        response = requests.post(
            "https://api-inference.huggingface.co/models/facebook/bart-large-cnn",
            headers=self.headers,
            json=payload
        )
        if response.status_code == 200:
            summary = response.json()
            return summary
        else:
            return f"An error occurred: {response.text}"
        
    def generate_query(self, history):
        API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"
        headers = {"Authorization": "Bearer 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"}

        question = "What question do i need to research to answer the last message? \n"
        context = "Conversation summary:\n" + history
        
        input = question + context
        print(">>> input: ", input)
        payload = {
            "inputs": input,
        }

        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            answer = response.json()[0]["generated_text"]  # Changed 'generated_text' to 'answer'
            return answer
        else:
            return "Error: " + response.text


chat_manager = ChatHistoryManager()
chat_manager.add_user_message("Hi, how are you?")
chat_manager.add_ai_message("Hello! I'm fine! how about you?")
chat_manager.add_user_message("I'm fine too, i'd like yo know what is a chatbot!")
chat_manager.add_ai_message("a chatbot is a kind of AI that can have conversations.")
chat_manager.add_user_message("Wow! How do they work?")

print(chat_manager.get_history())
optimized_history = chat_manager.get_optimized_history()
optimized_history = optimized_history[0]["summary_text"]
print("\n\n"+optimized_history)


answer = chat_manager.generate_query(optimized_history)
print("\n\n >>> answer: ", answer)
