import openai


class GPT:
    def __init__(self) -> None:
        self.primer = ""


    def get_model_name(self):
        return 'gpt'
    
    def run(self, prompt):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self.primer},
                    {"role": "user", "content": prompt}
                ]
            )

            return response['choices'][0]['message']['content']
        except:
            return "error"
