from managers.prompt_manager import PromptMangaer
from managers.LLMs.mixtral import Mixtral
from managers.LLMs.gemini import Gemini
from managers.LLMs.gpt import GPT

class LLMManager:
  def __init__(self) -> None:
    self.prompt_manager = PromptMangaer()
    self.llms = [Gemini(), Mixtral(), GPT()]
    self.error = 0

  def run(self, state, history='', context='', message=''):
    prompt = self.prompt_manager.get_prompt(state, self.llm.get_model_name(), history, context, message)
    answer = self.llm[self.error].run(prompt)

    if answer == "error":
      if self.error < 2:
        self.error += 1
        answer = self.run(state, history=history, context=context, message=message)
      else:
        self.error = 0
    
    return answer