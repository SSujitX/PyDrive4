"""
PyDrive4 Basic Usage Example

This example demonstrates the core functionality of PyDrive4 library.
Before running, make sure you have:
1. Created a Google Cloud project
2. Enabled the Google Drive API
3. Created OAuth2 credentials (client_secrets.json) or a service account key
"""

from pydrive4 import GoogleDrive


def main():
    """Main example function demonstrating PyDrive4 usage."""
    
    # ==========================================================================
    # AUTHENTICATION
    # ==========================================================================
    
    # Option 1: OAuth2 with client secrets (interactive browser auth)
    # This will open a browser for you to authorize the application
    client = GoogleDrive(credentials_name="client_secrets.json")
    
    # Option 2: Service Account (no user interaction needed)
    # client = GoogleDrive(
    #     credentials_name="service_account.json",
    #     service_account=True
    # )
    
    print("✓ Authentication successful!")
    
    # ==========================================================================
    # LIST FILES AND FOLDERS
    # ==========================================================================
    
    # List all files in root
    print("\n--- Listing Files in Root ---")
    files_result = client.list_files()
    if files_result["success"]:
        print(f"Found {files_result['count']} files:")
        for f in files_result["files"][:5]:  # Show first 5
            print(f"  - {f['name']} (ID: {f['id']})")
    
    # List all folders in root
    print("\n--- Listing Folders in Root ---")
    folders_result = client.list_folders()
    if folders_result["success"]:
        print(f"Found {folders_result['count']} folders:")
        for f in folders_result["folders"][:5]:  # Show first 5
            print(f"  - {f['name']} (ID: {f['id']})")
    
    # ==========================================================================
    # SEARCH
    # ==========================================================================
    
    # Search for files containing "report" in name
    print("\n--- Searching Files ---")
    search_result = client.search_files("report")
    if search_result["success"]:
        print(f"Found {search_result['count']} files matching 'report'")
    
    # Search for folders containing "project" in name
    print("\n--- Searching Folders ---")
    folder_search = client.search_folders("project")
    if folder_search["success"]:
        print(f"Found {folder_search['count']} folders matching 'project'")
    
    # ==========================================================================
    # CREATE FOLDER
    # ==========================================================================
    
    print("\n--- Creating Folder ---")
    folder_result = client.create_folder("PyDrive4 Test Folder")
    if folder_result["success"]:
        test_folder_id = folder_result["id"]
        print(f"Created folder: {folder_result['folder']['name']}")
        print(f"Folder ID: {test_folder_id}")
    
    # ==========================================================================
    # UPLOAD FILE
    # ==========================================================================
    
    # Create a test file to upload
    test_file_path = "test_upload.txt"
    with open(test_file_path, "w") as f:
        f.write("Hello from PyDrive4!\nThis is a test file.")
    
    print("\n--- Uploading File ---")
    upload_result = client.upload_file(test_file_path, folder_id=test_folder_id)
    if upload_result["success"]:
        uploaded_file_id = upload_result["id"]
        print(f"Uploaded file: {upload_result['file']['name']}")
        print(f"File ID: {uploaded_file_id}")
    
    # Upload with overwrite
    print("\n--- Uploading File (Overwrite) ---")
    with open(test_file_path, "w") as f:
        f.write("Updated content from PyDrive4!")
    
    overwrite_result = client.upload_file(
        test_file_path, 
        folder_id=test_folder_id, 
        overwrite=True
    )
    if overwrite_result["success"]:
        print(f"File overwritten: {overwrite_result['overwritten']}")
    
    # ==========================================================================
    # DOWNLOAD FILE
    # ==========================================================================
    
    print("\n--- Downloading File ---")
    download_path = "downloaded_test.txt"
    download_result = client.download_file(uploaded_file_id, download_path)
    if download_result["success"]:
        print(f"Downloaded to: {download_result['path']}")
        print(f"Size: {download_result['size']} bytes")
        
        # Read and print content
        with open(download_path, "r") as f:
            print(f"Content: {f.read()}")
    
    # ==========================================================================
    # GET FOLDER BY NAME
    # ==========================================================================
    
    print("\n--- Getting Folder by Name ---")
    get_result = client.get_folder("PyDrive4 Test Folder")
    if get_result["success"] and get_result["found"]:
        print(f"Found folder: {get_result['folder']['name']}")
    
    # ==========================================================================
    # DELETE (TRASH)
    # ==========================================================================
    
    print("\n--- Moving File to Trash ---")
    delete_result = client.delete_item(uploaded_file_id)
    if delete_result["success"]:
        print("File moved to trash successfully")
    
    # Delete folder permanently
    print("\n--- Deleting Folder Permanently ---")
    perm_delete = client.delete_item(test_folder_id, permanently=True)
    if perm_delete["success"]:
        print("Folder deleted permanently")
    
    # ==========================================================================
    # CLEANUP
    # ==========================================================================
    
    import os
    os.remove(test_file_path)
    os.remove(download_path)
    
    print("\n✓ All operations completed successfully!")


if __name__ == "__main__":
    main()
