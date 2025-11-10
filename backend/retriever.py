from langchain_community.vectorstores import FAISS
from langchain_openai.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv
from drive_loader import download_missing_files, get_local_txt_files, download_faiss_index_from_drive, upload_faiss_index_to_drive
from langchain_community.document_loaders import TextLoader
from loader import load_and_chunk_documents
from tqdm import tqdm
from pathlib import Path
import os

load_dotenv()

def load_documents_from_drive():
    download_missing_files()
    paths = get_local_txt_files()
    docs = []
    for path in paths:
        loader = TextLoader(str(path), encoding="utf-8")
        docs.extend(loader.load())
    return docs


def build_retriever():
    """
    Builds or loads a persisted FAISS retriever using OpenAI embeddings.
    Priority: 1) Local cache, 2) Google Drive, 3) Generate new
    """

    embeddings = OpenAIEmbeddings(model='text-embedding-3-small', chunk_size=100)

    FAISS_PATH = Path("faiss_index")

    # Try to load from local cache first
    if FAISS_PATH.exists() and (FAISS_PATH / "index.faiss").exists():
        print("[FAISS] Loading index from local cache...")
        vector = FAISS.load_local(str(FAISS_PATH), embeddings, allow_dangerous_deserialization=True)
    else:
        # Try to download from Google Drive
        print("[FAISS] No local index found. Checking Google Drive...")
        drive_success = download_faiss_index_from_drive(FAISS_PATH)
        
        if drive_success:
            print("[FAISS] Loading index downloaded from Google Drive...")
            vector = FAISS.load_local(str(FAISS_PATH), embeddings, allow_dangerous_deserialization=True)
        else:
            # Generate new index
            print("[FAISS] No index in Drive. Generating new FAISS index...")
            print("[FAISS] Remember to manually upload the generated index to Google Drive!")
            chunks = load_and_chunk_documents()
            batch_size = 1000
            all_vectors = None
            for i in tqdm(range(0, len(chunks), batch_size)):
                batch = chunks[i:i+batch_size]
                batch_vector = FAISS.from_documents(batch, embeddings)
                if all_vectors is None:
                    all_vectors = batch_vector
                else:
                    all_vectors.merge_from(batch_vector)
            
            # Save locally
            all_vectors.save_local(str(FAISS_PATH))
            vector = all_vectors
            print(f"[FAISS] Index saved to {FAISS_PATH}")
            print(f"[FAISS] Upload these files to Google Drive (faiss_index folder):")
            print(f"   - {FAISS_PATH}/index.faiss")
            print(f"   - {FAISS_PATH}/index.pkl")

    return vector.as_retriever(search_kwargs={"k": 4})