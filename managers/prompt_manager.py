
class PromptMangaer:
  def __init__(self) -> None:
    pass

  def greeting_prompt(self):
    return """
You are an AI assistant. Your only task is to respond briefly to the user's message. Do not initiate or continue a conversation beyond the message.

User's message: {message}

Your response (brief and to the point): """

  def mixtral_prompt(self):
    return """
<s>
[INST]
You are an assistant having a conversation with a user.
Answer the user question briefly and using context provided to get information.

This is a summary of the conversation: {history}

This is some information to help you answer the user's question: {context}

This is the user's question: {message}
[/INST]

Answer: </s>"""

  def falcon_prompt(self):
    return """
You are an assistant having a conversation with a user.
Answer the user question briefly and using context provided to get information.

This is a summary of the conversation: {history}

This is some information to help you answer the user's question: {context}

This is the user's question: {message}

Answer:"""

  def get_prompt(self, state, model, history, context, message):
    if "greeting" in state:
      return self.greeting_prompt().format(message=message)
    
    if model == "mixtral":
      return self.mixtral_prompt().format(history=history, context=context, message=message)
    return self.falcon_prompt().format(history=history, context=context, message=message)