import re
try:
    from .document_loader import load_document
except Exception:
    import sys, os
    pkg_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if pkg_root not in sys.path:
        sys.path.insert(0, pkg_root)
    from services.document_loader import load_document

#fixed Chunking
def fixed_chunking(text, chunk_size = 100):
    chunks = []
    for i in range(0,len(text), chunk_size):
        chunk = text[i:i+chunk_size]
        chunks.append(chunk)
    return chunks

#Recursive Chunking
def recursive_chunking(text,
                       chunk_size = 100,
                       separators = ["\n\n","\n","","."," "]):
    chunks = []
    def split_text(text,separator_index=0):

        # stop recursion
        if len(text)<=chunk_size:
            chunks.append(text.strip())
            return
        #Last separator fallback
        if separator_index >= len(separators):
            chunks.append(text[:chunk_size].strip())
            remaining = text[chunk_size:]

            if remaining:
                split_text(remaining,separator_index)
            return 
        

        separator = separators[separator_index]

        # Character-level fallback
        if separator == "":
            parts = [
                text[i:i + chunk_size]
                for i in range(0, len(text), chunk_size)
            ]

        else:
            parts = text.split(separator)

        current_chunk = ""

        for part in parts:

            # Restore separator except for empty separator
            piece = (
                part + separator
                if separator != ""
                else part
            )

            if len(current_chunk) + len(piece) <= chunk_size:

                current_chunk += piece

            else:

                if current_chunk:
                    split_text(
                        current_chunk,
                        separator_index + 1
                    )

                current_chunk = piece

        if current_chunk:
            split_text(
                current_chunk,
                separator_index + 1
            )

    split_text(text)

    return chunks


#Sentence Chunking
def sentence_chunking(text,sentence_per_chunk=2):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    for i in range(0,len(sentences),sentence_per_chunk):
        chunk = " ".join(sentences[i:i+sentence_per_chunk])
        chunks.append(chunk)
    return chunks

# Token Chunking
def token_chunking(text, max_tokens=20):

    # Naive whitespace tokenizer
    tokens = text.split()

    chunks = []

    for i in range(0, len(tokens), max_tokens):

        chunk = " ".join(
            tokens[i:i + max_tokens]
        )

        chunks.append(chunk)

    return chunks

# 5. SEMANTIC CHUNKING (SIMPLIFIED)

def semantic_chunking(text):

    """
    Simplified semantic chunking.

    Groups paragraphs based on meaning boundaries.
    Here we use paragraph separation.
    """

    paragraphs = text.split("\n\n")

    chunks = []

    for para in paragraphs:

        cleaned = para.strip()

        if cleaned:
            chunks.append(cleaned)

    return chunks


if __name__ == "__main__":

    document = load_document()

    print("\n========== FIXED ==========\n")

    fixed_chunks = fixed_chunking(document)

    for idx, chunk in enumerate(fixed_chunks):

        print(f"\nChunk {idx+1}:\n{chunk}")


    print("\n========== RECURSIVE ==========\n")

    recursive_chunks = recursive_chunking(document)

    for idx, chunk in enumerate(recursive_chunks):

        print(f"\nChunk {idx+1}:\n{chunk}")


    print("\n========== SENTENCE ==========\n")

    sentence_chunks = sentence_chunking(document)

    for idx, chunk in enumerate(sentence_chunks):

        print(f"\nChunk {idx+1}:\n{chunk}")


    print("\n========== TOKEN ==========\n")

    token_chunks = token_chunking(document)

    for idx, chunk in enumerate(token_chunks):

        print(f"\nChunk {idx+1}:\n{chunk}")


    print("\n========== SEMANTIC ==========\n")

    semantic_chunks = semantic_chunking(document)

    for idx, chunk in enumerate(semantic_chunks):

        print(f"\nChunk {idx+1}:\n{chunk}")