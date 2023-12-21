import requests
from managers.context_manager import ContextManager

class StateManager:
    def __init__(self):
        self.state = ""
        self.headers = {
            "Authorization": "Bearer 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"
        }

    def get_state(self, context, input):
        payload = {"inputs": "Given this input: " + input + " \nand this context: " + context + "\n\nThey both are related? Answer YES or NO, Don't give an explanation in your answer: "}
        response = requests.post(
            "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1",
            headers=self.headers,
            json=payload
        )
        if response.status_code == 200:
            summary = response.json()
            response = "related"
            print("===STATE EN FUNCION===")
            print(summary[0]["generated_text"])
            if summary[0]["generated_text"].split("Don't give an explanation in your answer: ")[-1].lower().find("no") != -1:
                response = "no related"
            return response
        else:
            return f"An error occurred: {response.text}"