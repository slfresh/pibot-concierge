import chromadb
import os

# Initialize ChromaDB client
client = chromadb.PersistentClient(path="./data/chroma_db")
collection_name = "hotel_knowledge"

try:
    collection = client.get_collection(name=collection_name)
except Exception:
    collection = client.create_collection(name=collection_name)

def init_db():
    if collection.count() > 0:
        return # already initialized

    try:
        with open("data/hotel_info.txt", "r") as f:
            content = f.read()
    except FileNotFoundError:
        print("data/hotel_info.txt not found.")
        return

    # Split into paragraphs as simple chunks
    chunks = [chunk.strip() for chunk in content.split("\n\n") if chunk.strip()]

    if not chunks:
        return

    # Add to chromadb
    collection.add(
        documents=chunks,
        ids=[f"doc_{i}" for i in range(len(chunks))]
    )
    print(f"Added {len(chunks)} documents to ChromaDB.")

def retrieve(query: str, n_results: int = 2) -> str:
    if collection.count() == 0:
        return ""

    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    if not results['documents'] or not results['documents'][0]:
        return ""

    # Join top results
    documents = results['documents'][0]
    return "\n\n".join(documents)

# Auto-initialize on import
init_db()
