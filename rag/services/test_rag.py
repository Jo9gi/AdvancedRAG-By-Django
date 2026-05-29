from .document_loader import load_document

from .chunking import recursive_chunking

from .vectordb import create_vector_store

from .retrieval import retrieve_chunks

from .llm import generate_response


# =====================================================
# LOAD PDF
# =====================================================

documents = load_document(

    "rag/documents/test.pdf"
)


# =====================================================
# CHUNKING
# =====================================================

chunks = recursive_chunking(
    documents
)

print(f"\nTOTAL CHUNKS: {len(chunks)}")


# =====================================================
# VECTOR DATABASE
# =====================================================

vector_store = create_vector_store(
    chunks
)

print("\nMILVUS VECTOR STORE CREATED")


# =====================================================
# CHAT LOOP
# =====================================================

while True:

    query = input("\nAsk Question: ")


    if query.lower() == "exit":

        break


    retrieved_docs = retrieve_chunks(

        query=query,

        vector_store=vector_store
    )


    print("\nRETRIEVED CHUNKS:\n")


    for doc in retrieved_docs:

        print(doc.page_content)
        print("\n" + "=" * 50)

    answer = generate_response(query=query, retrieved_docs=retrieved_docs)

    print("\nFINAL ANSWER:\n")

    print(answer)