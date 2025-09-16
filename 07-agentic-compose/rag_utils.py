import os
import glob
import numpy as np
from typing import List, Dict, Any
from dataclasses import dataclass
from litellm import embedding
import re


@dataclass
class DocumentChunk:
    """Represents a chunk of text with metadata"""
    content: str
    source: str
    chunk_id: int
    embedding: np.ndarray = None


class InMemoryVectorStore:
    """Simple in-memory vector store for similarity search"""

    def __init__(self):
        self.chunks: List[DocumentChunk] = []
        self.embeddings_matrix: np.ndarray = None

    def add_chunks(self, chunks: List[DocumentChunk]):
        """Add chunks to the vector store"""
        self.chunks.extend(chunks)
        # Create embeddings matrix for efficient similarity search
        if self.chunks:
            embeddings = [chunk.embedding for chunk in self.chunks]
            self.embeddings_matrix = np.array(embeddings)

    def similarity_search(self, query_embedding: np.ndarray, k: int = 3) -> List[tuple]:
        """Find k most similar chunks to the query"""
        if self.embeddings_matrix is None or len(self.chunks) == 0:
            return []

        # Calculate cosine similarity
        similarities = np.dot(self.embeddings_matrix, query_embedding) / (
            np.linalg.norm(self.embeddings_matrix, axis=1) * np.linalg.norm(query_embedding)
        )

        # Get top k indices
        top_k_indices = np.argsort(similarities)[-k:][::-1]

        return [(self.chunks[i], similarities[i]) for i in top_k_indices]


def chunk_text(text: str, chunk_size: int = 300, overlap: int = 50) -> List[str]:
    """Split text into overlapping chunks"""
    # Remove extra whitespace and normalize
    text = re.sub(r'\s+', ' ', text.strip())

    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size - overlap):
        chunk_words = words[i:i + chunk_size]
        chunk_text = ' '.join(chunk_words)
        chunks.append(chunk_text)

        # Break if we've reached the end
        if i + chunk_size >= len(words):
            break

    return chunks


def get_embedding(text: str) -> np.ndarray:
    """Get embedding for text using LiteLLM"""
    try:
        response = embedding(
            model=f"openai/{os.environ.get('EMBEDDING_MODEL', 'ai/granite-embedding-multilingual:latest')}",
            input=[text],
            api_key="tada",
            api_base=os.environ.get('MODEL_BASE_URL')
        )

        # Handle different response formats
        if hasattr(response, 'data') and response.data:
            if hasattr(response.data[0], 'embedding'):
                return np.array(response.data[0].embedding)
            elif isinstance(response.data[0], dict) and 'embedding' in response.data[0]:
                return np.array(response.data[0]['embedding'])
        elif isinstance(response, list) and len(response) > 0:
            return np.array(response[0])
        elif isinstance(response, dict):
            if 'data' in response and response['data']:
                return np.array(response['data'][0]['embedding'])
            elif 'embedding' in response:
                return np.array(response['embedding'])

        # If we can't parse the response, return dummy embedding
        print(f"⚠️  Unexpected embedding response format: {type(response)}")
        return np.random.random(384)

    except Exception as e:
        print(f"❌ Error getting embedding: {e}")
        # Return a dummy embedding in case of error
        return np.random.random(384)  # Typical embedding dimension


def load_and_process_documents() -> InMemoryVectorStore:
    """Load documents, chunk them, and create embeddings"""
    print("📚 Loading and processing documents...")

    vector_store = InMemoryVectorStore()
    data_dir = "data"

    if not os.path.exists(data_dir):
        print("⚠️  Data directory not found")
        return vector_store

    # Get all .md files in data directory
    md_files = glob.glob(os.path.join(data_dir, "*.md"))

    if not md_files:
        print("⚠️  No .md files found in data directory")
        return vector_store

    all_chunks = []
    chunk_id = 0

    for file_path in sorted(md_files):
        try:
            print(f"   Processing {os.path.basename(file_path)}...")

            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read().strip()

            # Chunk the document
            text_chunks = chunk_text(content)

            for chunk_content in text_chunks:
                # Get embedding for the chunk
                embedding_vector = get_embedding(chunk_content)

                # Create document chunk
                chunk = DocumentChunk(
                    content=chunk_content,
                    source=os.path.basename(file_path),
                    chunk_id=chunk_id,
                    embedding=embedding_vector
                )

                all_chunks.append(chunk)
                chunk_id += 1

        except Exception as e:
            print(f"⚠️  Could not process {file_path}: {e}")

    # Add all chunks to vector store
    vector_store.add_chunks(all_chunks)

    print(f"✅ Processed {len(all_chunks)} chunks from {len(md_files)} documents")
    return vector_store


def load_system_instructions():
    """Load system instructions from system-instructions.md file."""
    try:
        with open("system-instructions.md", "r", encoding="utf-8") as file:
            return file.read().strip()
    except FileNotFoundError:
        print("⚠️  system-instructions.md not found, using default instructions")
        return "You are a helpful AI assistant."


def create_rag_context(relevant_chunks: List[tuple]) -> str:
    """Create context from relevant chunks for the LLM"""
    if not relevant_chunks:
        return ""

    context = "\n\n# RELEVANT CONTEXT FROM KNOWLEDGE BASE:\n"

    for i, (chunk, similarity) in enumerate(relevant_chunks, 1):
        context += f"\n## Context {i} (from {chunk.source}):\n{chunk.content}\n"

    return context