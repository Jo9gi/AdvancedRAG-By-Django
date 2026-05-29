import numpy as np

from turbovec import TurboQuantIndex


# =====================================================
# IMPORTS
# =====================================================

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
# CREATE TURBOVEC INDEX
# =====================================================

def create_turbovec_index(chunks,bit_width=4):

    """
    Create TurboVec index.
    """

    # CREATE EMBEDDINGS
    embeddings = create_embeddings(chunks)

    embeddings = np.array(embeddings,dtype="float32")

    # GET DIMENSION
    dimension = embeddings.shape[1]

    print(f"\nEmbedding Dimension: {dimension}")

    print(f"\nBit Width: {bit_width}")


    # CREATE INDEX
    index = TurboQuantIndex( dim=dimension, bit_width=bit_width)


    # ADD VECTORS
    index.add(embeddings)

    return index, embeddings


# =====================================================
# SEARCH QUERY
# =====================================================

def search_query(query, index, chunks, top_k=3):

    """
    Search using TurboVec.
    """
    # QUERY EMBEDDING
    query_embedding = create_embeddings([query])

    query_embedding = np.array(query_embedding,dtype="float32")

    # SEARCH
    scores, indices = index.search(query_embedding,k=top_k)

    results = []


    # BUILD RESULTS
    for idx, score in zip(indices[0],scores[0]):
        if idx < len(chunks):
            results.append({
                "chunk": chunks[idx],
                "score": round(float(score), 4)
            })

    return results


# =====================================================
# DISPLAY RESULTS
# =====================================================

def display_results(results):

    print("\n" + "=" * 60)

    print("TOP RETRIEVED CHUNKS")

    print("=" * 60)


    for i, result in enumerate(
        results,
        start=1
    ):

        print(f"\nRESULT #{i}")

        print("-" * 60)

        print(f"\nSIMILARITY SCORE: {result['score']}")

        print(f"\nCHUNK:\n")

        print(result["chunk"])


# =====================================================
# MAIN
# =====================================================
from services.llm import generate_response
if __name__ == "__main__":

    print("\n" + "=" * 60)

    print("LOADING DOCUMENT")

    print("=" * 60)


    # LOAD DOCUMENT
    document = load_document("rag/documents/test.pdf")

    print("\nDOCUMENT LOADED SUCCESSFULLY\n")


    # =================================================
    # CHUNKING
    # =================================================

    print("=" * 60)

    print("CREATING CHUNKS")

    print("=" * 60)


    chunks = recursive_chunking(

        document,

        chunk_size=500
    )

    print(f"\nTOTAL CHUNKS: {len(chunks)}")


    # =================================================
    # CREATE INDEX
    # =================================================

    print("\n" + "=" * 60)

    print("CREATING TURBOVEC INDEX")

    print("=" * 60)


    index, embeddings = create_turbovec_index(
        chunks
    )

    print("\nTURBOVEC INDEX CREATED\n")

    print(f"\nEmbedding Shape: {embeddings.shape}")


    # =================================================
    # INTERACTIVE SEARCH
    # =================================================

    print("\n" + "=" * 60)

    print("TURBOVEC RAG READY")

    print("Type 'exit' to quit.")

    print("=" * 60)


    while True:

        query = input("\nAsk Question: ")


        if query.lower().strip() == "exit":

            print("\nExiting...\n")

            break


        # SEARCH
        results = search_query(

            query=query,

            index=index,

            chunks=chunks,

            top_k=3
        )


        # DISPLAY
        display_results(results)
        print("\n" + "=" * 60)
        print("GENERATING FINAL RESPONSE")
        print("=" * 60)

        answer = generate_response(
    query=query,
    retrieved_chunks=results
)

        print(answer)