import openai


class GPT:
    def __init__(self) -> None:
        pass


    def get_model_name(self):
        return 'gpt'
    
    def get_sender(self, sender):
        if sender == "AI":
            return "assistant"
        return "user"
    
    def get_messages(self, prompt):
        formated_history = [{"role": "system", "content": prompt["primer"]}]
        for m in prompt["history"]:
            e = {"role": self.get_sender(m["sender"]), "content": m["message"]}
            formated_history.append(e)
        formated_history.append({"role": "user", "content": prompt})
        return formated_history
    
    def run(self, prompt):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=self.get_messages(prompt)
            )

            return response['choices'][0]['message']['content']
        except:
            return "error"
