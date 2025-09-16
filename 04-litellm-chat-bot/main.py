import os
from litellm import completion
from dotenv import load_dotenv

# Load .env file
load_dotenv()

def chat_bot():
    """Interactive chat bot using LiteLLM with streaming responses."""
    print("🤖 >  ['quit', 'exit' or '/bye' to exit]\n")
    
    messages = [
        {
            "role": "system",
            "content": """
            You are a Hawaiian pizza expert. Your name is Bob.
            Provide accurate, enthusiastic information about Hawaiian pizza's history 
            (invented in Canada in 1962 by Sam Panopoulos), 
            ingredients (ham, pineapple, cheese on tomato sauce), preparation methods, and cultural impact.
            Use a friendly tone with occasional pizza puns. 
            Defend pineapple on pizza good-naturedly while respecting differing opinions. 
            If asked about other pizzas, briefly answer but return focus to Hawaiian pizza. 
            Emphasize the sweet-savory flavor combination that makes Hawaiian pizza special.
            USE ONLY THE INFORMATION PROVIDED IN THE KNOWLEDGE BASE.
            """
        }
    ]
    
    while True:
        # Get user input
        user_input = input("🤖: > ").strip()
        
        # Check for exit commands
        if user_input.lower() in ['quit', 'exit', 'q', '/bye']:
            print("\nBye! 👋")
            break
            
        # Skip empty inputs
        if not user_input:
            continue
            
        # Add user message to conversation history
        messages.append({
            "role": "user",
            "content": user_input
        })
        
        try:
            # Get streaming response from the model
            response = completion(
                model=f"openai/{os.environ.get('MODEL_ID')}", 
                api_key="tada",
                api_base=os.environ.get('MODEL_BASE_URL'),
                messages=messages,
                stream=True,
            )
            
            print("Bot: ", end='', flush=True)
            assistant_response = ""
            
            # Stream the response
            for chunk in response:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    print(content, end='', flush=True)
                    assistant_response += content
            
            print("\n")  # New line after response
            
            # Add assistant response to conversation history
            messages.append({
                "role": "assistant",
                "content": assistant_response
            })
            
        except KeyboardInterrupt:
            print("\n\nBye! 👋")
            break
        except Exception as e:
            print(f"\n❌ Erreur: {e}\n")

if __name__ == "__main__":
    chat_bot()