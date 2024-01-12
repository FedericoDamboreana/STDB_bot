import requests
from langchain.llms import GPT4All
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from managers.prompt_manager import PromptMangaer

class LLMManager:
  def __init__(self) -> None:
    self.prompt_manager = PromptMangaer()
    # self.llm = GPT4All(model="./model/gpt4all-falcon-q4_0.gguf", callbacks=[StreamingStdOutCallbackHandler()], verbose=True, n_threads=10)
    self.model = 'mixtral'
    self.headers = {
        "Authorization": "Bearer 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"
    }

  def mixtral_query(self, prompt):
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

  # def falcon_query(self, prompt):
  #   response = self.llm(prompt)
  #   return response

  def run(self, state, history='', context='', message=''):
    prompt = self.prompt_manager.get_prompt(state, 'mixtral', history, context, message)
    answer = self.mixtral_query(prompt)

    # if answer == "error":
    #   prompt = self.prompt_manager.get_prompt(state, 'falcon', history, context, message)
    #   answer = self.falcon_query(prompt)
    return answer