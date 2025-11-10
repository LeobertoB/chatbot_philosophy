import os
import json
from pathlib import Path
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from dotenv import load_dotenv
import io

load_dotenv()

CACHE_DIR = Path(__file__).resolve().parent / "data"
CACHE_DIR.mkdir(exist_ok=True)

GOOGLE_DRIVE_FOLDER_ID = os.environ.get("GOOGLE_DRIVE_FOLDER_ID")

# Credentials
def load_credentials_from_env():
    json_str = os.environ.get("GOOGLE_CREDENTIALS_JSON")
    if not json_str:
        raise EnvironmentError("Variable not defined.")

    credentials_dict = json.loads(json_str)
    creds = Credentials.from_service_account_info(
        credentials_dict,
        scopes=["https://www.googleapis.com/auth/drive"] 
    )
    return creds

# Connecting Google Drive to Credentials
def get_drive_service():
    creds = load_credentials_from_env()
    return build("drive", "v3", credentials=creds)

# Listing files from shared folder
def list_text_files(service):
    results = service.files().list(
        q=f"'{GOOGLE_DRIVE_FOLDER_ID}' in parents and mimeType='text/plain' and trashed = false",
        fields="files(id, name)"
    ).execute()
    return results.get("files", [])

# Download files that are not local
def download_missing_files():
    service = get_drive_service()
    files = list_text_files(service)

    for file in files:
        local_path = CACHE_DIR / file["name"]
        if local_path.exists():
            print(f"[CACHE] Skipping {file['name']} (already exists)")
            continue

        print(f"[DOWNLOAD] Downloading {file['name']}...")
        request = service.files().get_media(fileId=file["id"])
        fh = io.FileIO(local_path, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
        print(f"[SUCCESS] {file['name']} saved on {local_path}")

def get_local_txt_files():
    return [f for f in CACHE_DIR.glob("*.txt")]


def download_file_by_name(filename: str, output_path: Path):
    service = get_drive_service()
    results = service.files().list(
        q=f"'{GOOGLE_DRIVE_FOLDER_ID}' in parents and name='{filename}' and trashed=false",
        fields="files(id, name)"
    ).execute()
    files = results.get("files", [])

    if not files:
        print(f"[DRIVE] File '{filename}' not found in Google Drive.")
        return False

    file_id = files[0]['id']
    request = service.files().get_media(fileId=file_id)
    with open(output_path, 'wb') as f:
        downloader = MediaIoBaseDownload(f, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
    print(f"[DRIVE] Downloaded '{filename}' to '{output_path}'")
    return True

def download_faiss_index_from_drive(local_index_dir: Path):
    """
    Download FAISS index files (index.faiss and index.pkl) from Google Drive
    Looks for them in a 'faiss_index' subfolder within the main folder
    """
    service = get_drive_service()
    
    # First, find the faiss_index subfolder
    results = service.files().list(
        q=f"'{GOOGLE_DRIVE_FOLDER_ID}' in parents and name='faiss_index' and mimeType='application/vnd.google-apps.folder' and trashed=false",
        fields="files(id, name)"
    ).execute()
    folders = results.get("files", [])
    
    if not folders:
        print("[DRIVE] faiss_index folder not found in Google Drive")
        return False
    
    faiss_folder_id = folders[0]['id']
    print(f"[DRIVE] Found faiss_index folder with ID: {faiss_folder_id}")
    
    local_index_dir.mkdir(exist_ok=True, parents=True)
    
    index_faiss = local_index_dir / "index.faiss"
    index_pkl = local_index_dir / "index.pkl"
    
    # Download from the subfolder
    success_faiss = download_file_from_folder(faiss_folder_id, "index.faiss", index_faiss)
    success_pkl = download_file_from_folder(faiss_folder_id, "index.pkl", index_pkl)
    
    if success_faiss and success_pkl:
        print("[DRIVE] FAISS index downloaded successfully from Google Drive")
        return True
    else:
        print("[DRIVE] FAISS index files not found in Google Drive")
        return False

def download_file_from_folder(folder_id: str, filename: str, output_path: Path):
    """
    Download a specific file from a specific folder
    """
    service = get_drive_service()
    results = service.files().list(
        q=f"'{folder_id}' in parents and name='{filename}' and trashed=false",
        fields="files(id, name)"
    ).execute()
    files = results.get("files", [])

    if not files:
        print(f"[DRIVE] File '{filename}' not found in folder")
        return False

    file_id = files[0]['id']
    request = service.files().get_media(fileId=file_id)
    with open(output_path, 'wb') as f:
        downloader = MediaIoBaseDownload(f, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
    print(f"[DRIVE] Downloaded '{filename}' to '{output_path}'")
    return True

def upload_file_to_drive(local_path: Path, drive_filename: str = None):
    """
    Upload a file to Google Drive folder
    """
    from googleapiclient.http import MediaFileUpload
    
    if not local_path.exists():
        print(f"[DRIVE] Local file '{local_path}' does not exist")
        return False
    
    if drive_filename is None:
        drive_filename = local_path.name
    
    service = get_drive_service()
    
    # Check if file already exists
    results = service.files().list(
        q=f"'{GOOGLE_DRIVE_FOLDER_ID}' in parents and name='{drive_filename}' and trashed=false",
        fields="files(id, name)"
    ).execute()
    existing_files = results.get("files", [])
    
    file_metadata = {
        'name': drive_filename,
        'parents': [GOOGLE_DRIVE_FOLDER_ID]
    }
    media = MediaFileUpload(str(local_path), resumable=True)
    
    if existing_files:
        # Update existing file
        file_id = existing_files[0]['id']
        service.files().update(
            fileId=file_id,
            media_body=media
        ).execute()
        print(f"[DRIVE] Updated '{drive_filename}' in Google Drive")
    else:
        # Create new file
        service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        print(f"[DRIVE] Uploaded '{drive_filename}' to Google Drive")
    
    return True

def upload_faiss_index_to_drive(local_index_dir: Path):
    """
    Upload FAISS index files (index.faiss and index.pkl) to Google Drive
    """
    index_faiss = local_index_dir / "index.faiss"
    index_pkl = local_index_dir / "index.pkl"
    
    if not index_faiss.exists() or not index_pkl.exists():
        print("[DRIVE] FAISS index files not found locally")
        return False
    
    success_faiss = upload_file_to_drive(index_faiss, "index.faiss")
    success_pkl = upload_file_to_drive(index_pkl, "index.pkl")
    
    if success_faiss and success_pkl:
        print("[DRIVE] FAISS index uploaded successfully to Google Drive")
        return True
    else:
        print("[DRIVE] Failed to upload FAISS index")
        return False
