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
            "inputs": "<s> [INST]Summarize the last message question and relevant context from this chat history: \n" + self.get_history() + " [/INST] </s>" ,
        }
        print(">>> input: ", payload["inputs"])
        response = requests.post(
            "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1",
            headers=self.headers,
            json=payload
        )
        if response.status_code == 200:
            summary = response.json()
            return summary[0]["generated_text"].split("</s>")[-1].strip()
        else:
            return f"An error occurred: {response.text}"
        
    def generate_query(self, history):
        API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"
        headers = {"Authorization": "Bearer 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"}

        question = "What question do i need to research to answer the last message? \n"
        context = "Conversation summary:\n" + history
        
        input = question + context
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
chat_manager.add_user_message("I'm planning a vacation. Any suggestions?")
chat_manager.add_ai_message("That sounds exciting! What kind of places do you like?")
chat_manager.add_user_message("I love beaches and sunny weather.")
chat_manager.add_ai_message("You might enjoy visiting the Caribbean islands then. They have beautiful beaches.")
chat_manager.add_user_message("That's a great idea! How's the weather there around this time?")

optimized_history = chat_manager.get_optimized_history()
print("\n\n>>> optimized history: " + optimized_history)


answer = chat_manager.generate_query(optimized_history)
print("\n\n >>> answer: ", answer)
