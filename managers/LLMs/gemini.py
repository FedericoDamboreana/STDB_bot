import google.generativeai as genai

class Gemini:
    def __init__(self) -> None:
        genai.configure(api_key="AIzaSyB0Xf7u8MZ65MOaYdrlk0_SNzK2zwU5qT8")
        self.model = genai.GenerativeModel('gemini-pro')


    def get_model_name(self):
        return 'gemini'
    
    def run(self, prompt):
        response = self.model.generate_content(prompt)
        try:
            return response.text
        except:
            return "error"