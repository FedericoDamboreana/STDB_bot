
class PromptMangaer:
  def __init__(self) -> None:
    self.related = False
    pass



  def gemini_prompt(self, history, context, message):
    prompt = """
You are an assistant having a conversation with a user.
Answer the user question briefly and using context provided to get information.
"""
    if len(history) > 0:
      prompt += "\n\n\nThis is a summary of the conversation: "
      for h in history:
        prompt += f"\n\n-{h['message']}"
    
    if self.related:
      prompt += f"\n\n\n This is some information to help you answer the user's question: {context} \n\n Do not explicity mention the information provided, since it is not visible for the user."

    prompt += f"""
This is the user's question: {message}
"""

    return prompt



  def mixtral_prompt(self, history, context, message):
    prompt = """
<s>
[INST]
You are an assistant having a conversation with a user.
Answer the user question briefly and using context provided to get information.
"""
    if len(history) > 0:
      prompt += "\n\n\nThis is a summary of the conversation: "
      for h in history:
        prompt += f"\n\n-{h['message']}"
    
    if self.related:
      prompt += f"\n\n\n This is some information to help you answer the user's question: {context} \n\n Do not explicity mention the information provided, since it is not visible for the user."



    prompt += f"""
This is the user's question: {message}
[/INST]

Answer: </s>"""

    return prompt



  def gpt_prompt(self, history, context, message):
    primer = """
You are an assistant having a conversation with a user.
Answer the user question briefly and using context provided to get information.
"""

    if self.related:
      primer += f"""
This is some information to help you answer the user's question: {context}"""

    prompt = {
      'primer': primer,
      'history': history,
      'message': message
    }

    return prompt



  def get_prompt(self, state, model, history, context, message):
    self.related = state == "related"
    
    if model == "gemini":
      print(">>> writing prompt for ", model)
      return self.gemini_prompt(history.get_full_history(), context, message)
    
    if model == "mixtral":
      return self.mixtral_prompt(history.get_full_history(), context, message)
    
    if model == "gpt":
      return self.gpt_prompt(history.get_full_history(), context, message)
