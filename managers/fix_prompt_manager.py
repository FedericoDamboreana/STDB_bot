import requests

class FixPromptManager: 
  def __init__(self):
    self.API_URL = "https://api-inference.huggingface.co/models/MBZUAI/LaMini-T5-738M"
    self.headers = {"Authorization": "Bearer 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"}
    pass

  def fix_prompt(self, history, message):
    def query(payload):
      response = requests.post(self.API_URL, headers=self.headers, json=payload)
      return response.json()
    
    prompt = f"""
{history}
User: {message}

What does the user wants to know about in the last question?
"""

    output = query({
        "inputs": prompt,
    })
    print(">>> output: ", output)
    if output[0]:
      return output[0]["generated_text"]
    return "error"
