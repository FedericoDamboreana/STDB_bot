import requests

class StateManager:
    def __init__(self):
        self.state = ""
        self.headers = {
            "Authorization": "Bearer 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"
        }

    def get_state(self, history):
        payload = {"inputs": """Classify the following conversation in just one of those states: "greeting" or "question answering". \nDon't give any extra information.\n\n {history} \n\n The state that better match the conversation is"""}
        payload["inputs"] = payload["inputs"].format(history=history)
        print("prompt: ", payload["inputs"])
        response = requests.post(
            "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1",
            headers=self.headers,
            json=payload
        )
        if response.status_code == 200:
            summary = response.json()
            return summary[0]["generated_text"].split("Summary:")[-1].strip().split("The state that better match the conversation is ")[-1].rstrip('.')
        else:
            return f"An error occurred: {response.text}"