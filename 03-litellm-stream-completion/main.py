import os
from litellm import completion
from dotenv import load_dotenv

# Load .env file
load_dotenv()

response = completion(
    model=f"openai/{os.environ.get('MODEL_ID')}", 
    api_key="tada",
    api_base=os.environ.get('MODEL_BASE_URL'),
    temperature=0.7,

    messages=[
        {
            "role": "system", 
            "content": "You are an expert of Pizza."
        },
        {
            "role": "user", 
            "content": "What is the best pizza in the world?"
        }
    ],
    stream=True,
)

# Stream the answer
for chunk in response:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end='', flush=True)

"""
🤚 Show the inspect request feature in Docker Desktop
"""