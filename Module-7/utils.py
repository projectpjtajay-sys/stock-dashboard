import os
import numpy as np
import faiss
from pypdf import PdfReader
import ollama

#Config
EMBEDDING_MODEL = "nomic-embed-text"
GENERATION_MODEL = "llama3.2:3b"    
CHUNK_SIZE = 700
CHUNK_OVERLAP = 140

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file"""
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text() or ""
        text += page_text + "\n"
    return text.strip()


def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """Simple overlapping chunking"""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if len(chunk.strip()) > 60:
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


def get_embedding(text: str) -> np.ndarray:
    """Get embedding using Ollama"""
    response = ollama.embeddings(
        model=EMBEDDING_MODEL,
        prompt=text
    )
    return np.array(response['embedding'], dtype=np.float32)


def get_embeddings(texts: list[str]) -> np.ndarray:
    """Batch embedding (Ollama processes one at a time but we keep API similar)"""
    embeddings = []
    for text in texts:
        emb = get_embedding(text)
        embeddings.append(emb)
    return np.array(embeddings)


def build_and_save_index(embeddings: np.ndarray, index_path="index/faiss_index.index"):
    """Create and save FAISS index"""
    os.makedirs(os.path.dirname(index_path), exist_ok=True)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)  # Simple L2 distance
    index.add(embeddings)
    faiss.write_index(index, index_path)
    return index


def load_index(index_path="index/faiss_index.index"):
    """Load existing FAISS index"""
    return faiss.read_index(index_path)


def retrieve(query: str, index, chunks: list[str], top_k=4):
    """Find top-k most relevant chunks"""
    query_embedding = get_embedding(query).reshape(1, -1)
    distances, indices = index.search(query_embedding, top_k)
    
    results = []
    for idx, dist in zip(indices[0], distances[0]):
        if idx != -1 and idx < len(chunks):
            results.append((chunks[idx], float(dist)))
    return results


def generate_answer(query: str, context_chunks: list[tuple[str, float]]) -> str:
    """Generate answer using retrieved context with Ollama"""
    context = "\n\n".join([chunk for chunk, _ in context_chunks])
    
    prompt = f"""You are a helpful assistant that answers questions based ONLY on the provided context.
If the information is not in the context, say "I don't have enough information to answer this."

Context:
{context}

Question: {query}

Answer:"""

    response = ollama.chat(
        model=GENERATION_MODEL,
        messages=[{"role": "user", "content": prompt}],
        options={
            "temperature": 0.2,
            "num_predict": 600,
        }
    )
    
    return response['message']['content'].strip()