import os
from litellm import completion
from dotenv import load_dotenv
from rag_utils import (
    DocumentChunk, InMemoryVectorStore, chunk_text,
    get_embedding, load_and_process_documents,
    load_system_instructions, create_rag_context
)

# Load .env file
load_dotenv()

def chat_bot():
    """Interactive RAG chat bot using LiteLLM with vector search"""
    print("🤖 RAG Chat Bot - ['quit', 'exit' or '/bye' to exit]")
    print("🔍 Initializing vector store...")
    
    # Initialize vector store
    vector_store = load_and_process_documents()
    
    # Load system instructions
    system_instructions = load_system_instructions()
    
    print("\n✅ Ready to chat!\n")
    
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
        
        try:
            # Get embedding for user query
            query_embedding = get_embedding(user_input)
            
            # Search for relevant chunks
            relevant_chunks = vector_store.similarity_search(query_embedding, k=3)
            
            #   The k parameter in the similarity_search method specifies the number of most similar
            #   chunks to retrieve from the vector store.
            #   In this case, k=3 means the system will return the 3 most similar document chunks
            #   based on the query embedding's similarity to the stored embeddings.

            # Display relevant chunks with similarity ratios
            print("\nRelevant chunks:")
            for i, (chunk, similarity) in enumerate(relevant_chunks, 1):
                print(f"\nChunk {i} (similarity: {similarity:.4f}):")
                print(f"Content: {chunk.content[:200]}...")
            
            print("\n\nGenerating response...\n\n")


            # Create context from relevant chunks
            rag_context = create_rag_context(relevant_chunks)
            
            # Combine system instructions with RAG context
            full_system_content = system_instructions + rag_context
            
            # Prepare messages
            messages = [
                {
                    "role": "system",
                    "content": full_system_content
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ]
            
            # Get streaming response from the model
            response = completion(
                model=f"openai/{os.environ.get('MODEL_ID')}", 
                api_key="tada",
                api_base=os.environ.get('MODEL_BASE_URL'),
                messages=messages,
                temperature=0.0,
                stream=True,
            )
            
            print("Bot: ", end='', flush=True)
            
            # Stream the response
            for chunk in response:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    print(content, end='', flush=True)
            
            print("\n")  # New line after response
            
        except KeyboardInterrupt:
            print("\n\nBye! 👋")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")

if __name__ == "__main__":
    chat_bot()