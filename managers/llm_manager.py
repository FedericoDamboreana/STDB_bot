from managers.prompt_manager import PromptMangaer
from managers.LLMs.mixtral import Mixtral
from managers.LLMs.gemini import Gemini
from managers.LLMs.gpt import GPT

class LLMManager:
  def __init__(self) -> None:
    self.prompt_manager = PromptMangaer()
    self.llms = [Gemini(), Mixtral(), GPT()]
    self.error = 0

  def run(self, is_related, history='', context='', message=''):
    prompt = self.prompt_manager.get_prompt(is_related, self.llms[self.error].get_model_name(), history, context, message)
    answer = self.llms[self.error].run(prompt)

    if answer == "error":
      print(">>> error in llm manager - error count: ", self.error)
      if self.error < 2:
        self.error += 1
        answer = self.run(is_related, history=history, context=context, message=message)
      else:
        self.error = 0
    
    return answer