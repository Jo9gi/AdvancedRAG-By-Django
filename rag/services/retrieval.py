import faiss
import numpy as np

try:
    from .document_loader import load_document
    from .chunking import recursive_chunking
    from .embedding import create_embeddings

except ImportError:

    import sys
    import os

    pkg_root = os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )

    if pkg_root not in sys.path:
        sys.path.insert(0, pkg_root)

    from services.document_loader import load_document
    from services.chunking import recursive_chunking
    from services.embedding import create_embeddings


# =====================================================
# CREATE VECTOR STORE
# =====================================================

def create_vector_store(chunks):

    embeddings = create_embeddings(chunks)

    # Convert to float32
    embeddings = np.array(
        embeddings,
        dtype="float32"
    )

    # Get embedding dimensions
    dimension = embeddings.shape[1]

    # Create FAISS index
    index = faiss.IndexFlatIP(dimension)

    # Add embeddings to index
    index.add(embeddings)

    return index, embeddings


# =====================================================
# SEARCH FUNCTION
# =====================================================

def search_query(
    query,
    index,
    chunks,
    top_k=3
):

    query_embedding = create_embeddings(
        [query]
    )

    query_embedding = np.array(
        query_embedding,
        dtype="float32"
    )

    # SEARCH
    scores, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for idx, score in zip(
        indices[0],
        scores[0]
    ):

        results.append({

            "chunk": chunks[idx],
            "score": float(score)

        })

    return results


# =====================================================
# TESTING
# =====================================================

if __name__ == "__main__":

    # LOAD DOCUMENT
    document = load_document()

    # CREATE CHUNKS
    chunks = recursive_chunking(
        document,
        chunk_size=100
    )

    print("\nTOTAL CHUNKS:\n")

    print(len(chunks))


    # CREATE VECTOR STORE
    index, embeddings = create_vector_store(
        chunks
    )

    print("\nFAISS INDEX CREATED\n")


    # TEST QUERY
    query = "What is Django?"

    print(f"\nQUERY:\n{query}\n")


    # SEARCH
    results = search_query(
        query,
        index,
        chunks
    )

    print("\nTOP RESULTS:\n")


    for result in results:

        print(result)

        print("\n")