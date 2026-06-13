import os
import re

def load_documents(docs_folder="docs"):
    documents = []
    for filename in os.listdir(docs_folder):
        if filename.endswith(".txt"):
            filepath = os.path.join(docs_folder, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
            documents.append({
                "filename": filename,
                "text": text
            })
    print(f"Loaded {len(documents)} documents")
    return documents

def clean_text(text):
    lines = text.splitlines()
    cleaned_lines = [line.strip() for line in lines if line.strip()]
    return "\n".join(cleaned_lines)

def chunk_text(text):
    # Split by "Review #" to keep each review as one complete chunk
    chunks = re.split(r'(?=Review #\d+)', text)
    chunks = [c.strip() for c in chunks if c.strip()]
    return chunks

def process_documents(docs_folder="docs"):
    documents = load_documents(docs_folder)
    all_chunks = []
    for doc in documents:
        cleaned = clean_text(doc["text"])
        chunks = chunk_text(cleaned)
        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "source": doc["filename"],
                "chunk_index": i,
                "text": chunk
            })
    print(f"Total chunks created: {len(all_chunks)}")
    return all_chunks

if __name__ == "__main__":
    chunks = process_documents()
    print("\n--- Sample Chunks ---")
    for chunk in chunks[:5]:
        print(f"\nSource: {chunk['source']}")
        print(f"Chunk {chunk['chunk_index']}: {chunk['text']}")
        print("-" * 40)