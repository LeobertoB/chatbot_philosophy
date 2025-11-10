from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from drive_loader import CACHE_DIR
from pathlib import Path

# Load and split
def load_and_chunk_documents():
    """
    Loads all .txt files from CACHE_DIR, adds metadata, splits into chunks.

    Returns:
        List of Document objects: Chunked text pieces with metadata.
    """

    print("Loading manually from:", CACHE_DIR)

    docs = []
    for file in Path(CACHE_DIR).glob("*.txt"):
        loader = TextLoader(str(file), encoding="utf-8")
        raw_docs = loader.load()

        # Metadata
        for doc in raw_docs:
            doc.metadata["source"] = file.name
            doc.metadata["author"] = "Dostoevsky"

        docs.extend(raw_docs)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000, 
        chunk_overlap = 200
    )

    return text_splitter.split_documents(docs)