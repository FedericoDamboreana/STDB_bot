import requests

def fix_chained_question():
    API_URL = "https://api-inference.huggingface.co/models/MBZUAI/LaMini-Flan-T5-248M"
    headers = {"Authorization": "Bearer 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"}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()
    
    prompt = """
user: What's the best time of year to visit Japan?
assistant: Spring is generally considered the best time.
user: And what festivals occur during that period?

What does the user want to know?
"""

    output = query({
        "inputs": prompt,
    })
    return output[0]["generated_text"].split("The user wants to know ", 1)[1]


print(fix_chained_question())

history = """
assistant: Hello! How can I help you?
user: Hi! How tall is a dog?
assistant: About a meter tall.
user: And what about a cat?

What does the user want to know?
"""

"What does the user want to know?"

history = """
user: Hi! What is the best CPU?
assistant: The core i9.
user: How many cores doest it have?
"""

history = """
user: What's the best time of year to visit Japan?
assistant: Spring is generally considered the best time.
user: And what festivals occur during that period?

"""