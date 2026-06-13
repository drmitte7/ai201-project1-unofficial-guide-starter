import chromadb
from sentence_transformers import SentenceTransformer
from ingest import process_documents

def embed_and_store(docs_folder="docs"):
    # Load and chunk documents
    chunks = process_documents(docs_folder)
    
    # Load embedding model
    print("Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    
    # Set up ChromaDB
    client = chromadb.PersistentClient(path="chroma_db")
    
    # Delete collection if it already exists
    try:
        client.delete_collection("professor_reviews")
    except:
        pass
    
    collection = client.create_collection("professor_reviews")
    
    # Embed and store each chunk
    print("Embedding chunks...")
    for i, chunk in enumerate(chunks):
        embedding = model.encode(chunk["text"]).tolist()
        collection.add(
            ids=[f"chunk_{i}"],
            embeddings=[embedding],
            documents=[chunk["text"]],
            metadatas=[{
                "source": chunk["source"],
                "chunk_index": chunk["chunk_index"]
            }]
        )
    
    print(f"Stored {len(chunks)} chunks in ChromaDB")
    return collection

def retrieve(query, top_k=5):
    # Load embedding model
    model = SentenceTransformer("all-MiniLM-L6-v2")
    
    # Connect to existing ChromaDB
    client = chromadb.PersistentClient(path="chroma_db")
    collection = client.get_collection("professor_reviews")
    
    # Embed the query and search
    query_embedding = model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    
    return results

if __name__ == "__main__":
    # Embed and store all chunks
    embed_and_store()
    
    # Test retrieval with 3 queries
    test_queries = [
        "What do students say about Prof. Cheikhna's exams?",
        "Is attendance mandatory in Prof. Ethan Atkin's class?",
        "Do students recommend Prof. Cheikhna for Calc 1?"
    ]
    
    print("\n--- Retrieval Tests ---")
    for query in test_queries:
        print(f"\nQuery: {query}")
        results = retrieve(query)
        for j, (doc, meta) in enumerate(zip(results["documents"][0], results["metadatas"][0])):
            print(f"\n  Result {j+1} (source: {meta['source']}):")
            print(f"  {doc[:150]}...")
        print("-" * 40)