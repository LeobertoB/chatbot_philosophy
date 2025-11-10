"""
Script to upload FAISS index to Google Drive
Run this once after generating the index locally
"""
from pathlib import Path
from drive_loader import upload_faiss_index_to_drive

if __name__ == "__main__":
    FAISS_PATH = Path("faiss_index")
    
    if not FAISS_PATH.exists():
        print("Error: No local FAISS index found. Generate it first by running the server.")
        exit(1)
    
    print("Uploading FAISS index to Google Drive...")
    success = upload_faiss_index_to_drive(FAISS_PATH)
    
    if success:
        print("✅ FAISS index uploaded successfully!")
        print("Your Railway deployment will now download it automatically.")
    else:
        print("❌ Failed to upload FAISS index")
