from drive_loader import download_missing_files, get_local_txt_files

if __name__ == "__main__":
    print("Initializing test")
    download_missing_files()
    print("\n Files downloaded: ")
    for file in get_local_txt_files():
        print(f"{file.name}")