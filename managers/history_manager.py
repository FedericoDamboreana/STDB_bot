import requests

class HistoryManager:
    def __init__(self):
        self.chat_history = []

    def add_ai_message(self, message):
        self.chat_history.append({"sender": "AI", "message": message})
        
    def add_user_message(self, message):
        self.chat_history.append({"sender": "User", "message": message})
    
    def get_history(self):
        history_str = "\n".join([f"{m['sender']}: {m['message']}" for m in self.chat_history])
        return history_str
    
    def get_full_history(self):
        return self.chat_history
    
    def clear_history(self):
        self.chat_history = []
    
