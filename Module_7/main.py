import sys
import os
from utils import (
    extract_text_from_pdf,
    chunk_text,
    get_embeddings,
    build_and_save_index,
    load_index,
    retrieve,
    generate_answer
)

def ingest(pdf_path: str):
    print("1. Extracting text from PDF...", flush=True)
    text = extract_text_from_pdf(pdf_path)
    
    print("2. Creating chunks...", flush=True)
    chunks = chunk_text(text)
    print(f"   → Created {len(chunks)} chunks")
    
    print("3. Generating embeddings (this may take a while)...", flush=True)
    embeddings = get_embeddings(chunks)
    
    print("4. Building and saving FAISS index...", flush=True)
    build_and_save_index(embeddings)
    
    # Save chunks for later use
    with open("index/chunks.txt", "w", encoding="utf-8") as f:
        f.write("\n<CHUNK_SEPARATOR>\n".join(chunks))
    
    print("\nIngestion completed! You can now ask questions.\n")


def ask_question(question: str):
    if not os.path.exists("index/faiss_index.index"):
        print("No index found. Please run ingestion first:")
        print("   python main.py ingest your_document.pdf\n")
        return
    
    print("Loading index and chunks...", flush=True)
    index = load_index()
    
    with open("index/chunks.txt", "r", encoding="utf-8") as f:
        chunks = f.read().split("\n<CHUNK_SEPARATOR>\n")
    
    print("Searching for relevant chunks...", flush=True)
    results = retrieve(question, index, chunks)
    
    print("\nTop matches found:")
    for i, (text, dist) in enumerate(results, 1):
        preview = text.replace("\n", " ")[:90].strip() + "..." if len(text) > 90 else text
        print(f"{i}.  distance: {dist:>6.4f}  |  {preview}")
    
    print("\nGenerating answer...", flush=True)
    answer = generate_answer(question, results)
    
    print("\n" + "═" * 70)
    print("ANSWER:")
    print(answer)
    print("═" * 70)


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Ingest PDF:     python main.py ingest your_document.pdf")
        print("  Ask question:   python main.py ask \"Your question here\"")
        print()
        return
    
    command = sys.argv[1].lower()
    
    if command == "ingest":
        if len(sys.argv) < 3:
            print("Please provide path to PDF file")
            return
        pdf_path = sys.argv[2]
        if not os.path.exists(pdf_path):
            print(f"File not found: {pdf_path}")
            return
        ingest(pdf_path)
        
    elif command == "ask":
        if len(sys.argv) < 3:
            print("Please provide your question")
            return
        question = " ".join(sys.argv[2:])
        ask_question(question)
        
    else:
        print(f"Unknown command: {command}")
        print("Use 'ingest' or 'ask'")


if __name__ == "__main__":
    main()