from langchain_classic.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import os

# Load and split
def load_and_chunk_document():
    """
    Loads the text file and splits it into chunks suitable for embeddings.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        List of Document objects: Chunked text pieces, ready for embedding.
    """

    file_path = os.path.join(os.path.dirname(__file__), "DostoevskyF-Grand-Inquisitor-excerpt.txt")

    print("Loading manually from:", file_path)

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Wrap the text in a Document (LangChain expects this)
    documents = [Document(page_content=text)]

    loader = TextLoader(
        file_path=file_path, 
        encoding='utf-8'
    )

    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 200
    )

    return text_splitter.split_documents(documents)