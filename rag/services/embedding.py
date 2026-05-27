
try:
    from .document_loader import load_document
    from .chunking import recursive_chunking
except Exception:
    import sys, os
    pkg_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if pkg_root not in sys.path:
        sys.path.insert(0, pkg_root)
    from services.document_loader import load_document
    from services.chunking import recursive_chunking

# Lazy-load embedding model to avoid heavy work on import
embedding_model = None

def create_embeddings(chunks):
    global embedding_model
    if embedding_model is None:
        from sentence_transformers import SentenceTransformer
        embedding_model = SentenceTransformer("BAAI/bge-base-en-v1.5")
    embeddings = embedding_model.encode(chunks, normalize_embeddings=True)
    return embeddings

# Testing
if __name__ == "__main__":
    document = load_document()
    print("\n Documnent is loaded Successfully\n")
    chunks = recursive_chunking(document,chunk_size= 100)
    print(f"\nTotal Chunks:{len(chunks)}\n")

    embeddings = create_embeddings(chunks)
    print("\nEmbedding Created Successfully\n")

    # shape
    print(f"Embedding Shape:\n {embeddings.shape} \n")

    print(f"\n First Chunk:\n {chunks[0]} \n")

    # FIRST VECTOR
    print("\nFIRST VECTOR (FIRST 10 VALUES):\n")

    print(embeddings[0][:10])