import requests

def generate_query(history, last_message):
    API_URL = "https://api-inference.huggingface.co/models/bert-large-uncased-whole-word-masking-finetuned-squad"
    # Ensure your API token is handled securely in production
    headers = {"Authorization": "Bearer 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"}

    context = "Conversation summary:\n" + "\n".join(history) + "\nLast message: " + last_message
    question = "What do i need to research to answer the last message?"
    inputs = {
        "question": question,
        "context": context
    }
    print(inputs)

    payload = {
        "inputs": inputs,
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