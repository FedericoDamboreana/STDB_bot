import requests

class HistoryManager:
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
    
    def get_full_history(self):
        history = self.get_history()
        history += "\n" + 'user: ' + self.last_message
        return history
    
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
            "inputs": "Given this conversation between a user and an AI: \n" + self.get_history() + "\n\nSummary: The user" ,
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
        prompt = "\n\nWhat does the user wants to know?\nThe user wants to"
        payload = {
            "inputs": "This is the summary of a conversation of a user and a AI: " + summary + "\n\nThis is the user's last question: " + self.last_message + prompt,
        }

        response = requests.post(
            "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct",
            headers=self.headers,
            json=payload
        )
        if response.status_code == 200:
            summary = response.json()
            return summary[0]["generated_text"].split("What does the user wants to know?")[-1].strip()
        else:
            return "Error: " + response.text
