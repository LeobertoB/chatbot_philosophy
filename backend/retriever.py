from langchain_community.vectorstores import FAISS
from langchain_openai.embeddings import OpenAIEmbeddings
from loader import load_and_chunk_document
from dotenv import load_dotenv

load_dotenv()

def build_retriever():
    """
    Loads chunked documents and builds a FAISS retriever with OpenAI embeddings.

    Returns:
        retriever: A retriever object to be used in a LangChain chain.
    """
    file_path = 'DostoevskyF-Grand-Inquisitor-excerpt.txt'
    
    chunks = load_and_chunk_document()

    embeddings = OpenAIEmbeddings(model='text-embedding-3-small', chunk_size=1000)

    vector = FAISS.from_documents(chunks, embeddings)

    return vector.as_retriever()
