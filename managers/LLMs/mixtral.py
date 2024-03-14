import requests

class Mixtral:
    def __init__(self) -> None:
        self.headers = {
        "Authorization": "Bearer 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"
        }
    def get_model_name(self):
        return 'mixtral'
    
    def run(self, prompt):
        print(">>> prompt: ", prompt)
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 4000
            }
        }
        response = requests.post(
            "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1",
            headers=self.headers,
            json=payload
        )
        if response.status_code == 200:
            result = response.json()
            if "Answer: </s>" in result[0]["generated_text"]: 
                result = result[0]["generated_text"].split("Answer: </s>")[-1].strip()
            else:
                result = result[0]["generated_text"].split("Your response (brief and to the point):")[-1].strip()
        else:
            return "error"
        return result