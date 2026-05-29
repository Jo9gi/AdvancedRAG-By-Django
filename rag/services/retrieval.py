def retrieve_chunks(
query, vector_store, top_k=3):

    retriever = vector_store.as_retriever(

        search_type="similarity",

        search_kwargs={

            "k": top_k
        }
    )

    results = retriever.invoke(query)

    return results