import requests

def generate_query(history):
    API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"
    headers = {"Authorization": "Bearer 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"}

    question = "What do i need to research to answer the last message? \n"
    context = "Conversation summary:\n" + history
    
    input = question + context
    payload = {
        "inputs": input,
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        answer = response.json().get('answer')  # Changed 'generated_text' to 'answer'
        return answer
    else:
        return "Error: " + response.text

# Example of use
history = ["Hello, how are you?", "Good, thanks. How about you?", "I would like to know more about chatbots.", "a chatbot is an AI that can have a conversation."]
last_message = "are there other types of AI?"
query = generate_query(history, last_message)
print(query)