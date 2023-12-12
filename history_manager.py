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


chat_manager = ChatHistoryManager()
chat_manager.add_user_message("Hi, I'm looking for advice on how to improve my AI application's performance.")
chat_manager.add_ai_message("Hello! Sure, I can help with that. Could you tell me which programming language your application is written in and what kind of tasks it performs?")
chat_manager.add_user_message("It's written in Python and uses neural networks for image processing.")
chat_manager.add_ai_message("Got it. Have you considered implementing optimization techniques like neural network pruning or quantization to reduce your model's size and speed up inference?")
chat_manager.add_user_message("I'm not very familiar with those techniques. Can you explain more about them?")
chat_manager.add_ai_message("Certainly. Neural network pruning involves removing redundant or less important neural connections, reducing model complexity without significantly impacting accuracy. Quantization, on the other hand, reduces the precision of the numbers used in calculations, which can also speed up inference and reduce model size.")
chat_manager.add_user_message("That sounds useful. How can I implement these techniques in my code?")
chat_manager.add_ai_message("There are Python libraries like TensorFlow Model Optimization or PyTorch that offer tools for pruning and quantization. I can show you some code examples if you're interested.")
chat_manager.add_user_message("which of those is better?")
print(chat_manager.get_history())
optimized_history = chat_manager.get_optimized_history()
print("\n\n"+optimized_history[0]["summary_text"])
