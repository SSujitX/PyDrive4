# PyDrive4

A simplified Google Drive API v3 wrapper library for Python.

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

PyDrive4 makes it easy to interact with Google Drive from Python. It wraps the `google-api-python-client` to provide a clean, intuitive API for common file and folder operations.

## Features

- 🔐 **Multiple Auth Methods** - ADC, OAuth2, Service Account with auto-detection
- 📁 **File Management** - Upload, download, list, search files
- 📂 **Folder Operations** - Create, list, search folders
- 🔄 **Folder Upload** - Upload entire directories recursively
- 🗑️ **Delete Operations** - Trash or permanently delete items
- 📄 **Google Drive API v3** - Uses the latest API version
- ✨ **Clean Error Messages** - User-friendly one-line errors

## Installation

```bash
pip install pydrive4
```

Or with UV (recommended):

```bash
uv add pydrive4
```

---

## Quick Start

```python
from pydrive4 import GoogleDrive

# Auto-authenticate (uses best available method)
client = GoogleDrive()

# List files
files = client.list_files()
print(f"Found {files['count']} files")
```

---

## Authentication Methods

PyDrive4 supports multiple authentication methods, ordered by recommendation:

| Method | Best For | Setup Required |
|--------|----------|----------------|
| **1. Application Default Credentials** | Local dev, Google Cloud | `gcloud` CLI |
| **2. Service Account** | Servers, automation, bots | JSON key file |
| **3. OAuth2 Client** | Personal scripts, desktop apps | JSON + browser auth |

---

### Method 1: Application Default Credentials (Recommended)

The **easiest** method for local development. No JSON files to manage!

#### Setup (One-time)

1. Install [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)

2. Login with your Google account:
```bash
gcloud auth application-default login
```

3. That's it! Now just use:
```python
from pydrive4 import GoogleDrive

client = GoogleDrive()  # Works automatically!
files = client.list_files()
```

#### How it Works

ADC (Application Default Credentials) checks these locations in order:
1. `GOOGLE_APPLICATION_CREDENTIALS` environment variable
2. `gcloud auth application-default login` credentials
3. Google Cloud metadata service (on GCE, Cloud Run, etc.)

---

### Method 2: Service Account (For Automation)

Best for servers, bots, and CI/CD pipelines. **No user interaction needed.**

#### Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create project → Enable **Google Drive API**
3. Go to **IAM & Admin** → **Service Accounts**
4. Create Service Account → Go to **Keys** → **Add Key** → **JSON**
5. Download and save as `service_account.json`

#### Usage

```python
from pydrive4 import GoogleDrive

# Auto-detect (if file is named service_account.json in current dir)
client = GoogleDrive()

# Or explicit
client = GoogleDrive(
    credentials_name="service_account.json",
    service_account=True
)
```

#### What is `service_account=True`?

| Aspect | OAuth2 | Service Account |
|--------|--------|-----------------|
| Browser needed | Yes (first time) | No |
| Whose Drive? | Your personal Drive | Service account's own Drive |
| Best for | Personal scripts | Servers, automation |
| Access | All your files | Only files shared with it |

> **Important**: Service accounts have their own empty Drive. To access your files, share folders with the service account email (e.g., `name@project.iam.gserviceaccount.com`).

---

### Method 3: OAuth2 Client Credentials

For desktop apps where a user authorizes access to their Drive.

#### Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create project → Enable **Google Drive API**
3. Go to **APIs & Services** → **Credentials**
4. **Create Credentials** → **OAuth client ID** → **Desktop app**
5. Download JSON as `client_secrets.json`

#### Usage

```python
from pydrive4 import GoogleDrive

# Auto-detect (if file is in current directory)
client = GoogleDrive()

# Or explicit
client = GoogleDrive(credentials_name="client_secrets.json")
```

On first run, a browser opens for authorization. The token is cached in `token.json`.

---

### Environment Variable

You can also set `GOOGLE_APPLICATION_CREDENTIALS`:

```bash
# Linux/macOS
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/credentials.json"

# Windows PowerShell
$env:GOOGLE_APPLICATION_CREDENTIALS="C:\path\to\credentials.json"

# Windows CMD
set GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\credentials.json
```

Then:
```python
client = GoogleDrive()  # Automatically uses the env variable
```

---

### Auto-Detection Priority

When you call `GoogleDrive()` without arguments, it tries:

1. **Application Default Credentials** (gcloud login or env variable)
2. **Service account files** in current directory:
   - `service_account.json`
   - `service_account_key.json`
3. **OAuth2 files** in current directory:
   - `client_secrets.json`
   - `credentials.json`

---

## API Reference

### GoogleDrive

```python
GoogleDrive(
    credentials_name: str = None,      # Path to credentials JSON
    service_account: bool = None,      # True/False/None (auto-detect)
    token_file: str = "token.json",    # Where to cache OAuth tokens
    readonly: bool = False             # Request read-only access
)
```

### Methods

| Method | Description | Returns |
|--------|-------------|---------|
| `list_files(folder_id, trashed)` | List files in a folder | `{"success": bool, "files": list, "count": int}` |
| `list_folders(parent_id, trashed)` | List folders | `{"success": bool, "folders": list, "count": int}` |
| `search_files(query, folder_id)` | Search files by name | `{"success": bool, "files": list, "count": int}` |
| `search_folders(query, parent_id)` | Search folders by name | `{"success": bool, "folders": list, "count": int}` |
| `get_folder(name, parent_id)` | Get folder by exact name | `{"success": bool, "folder": dict, "found": bool}` |
| `create_folder(name, parent_id)` | Create a folder | `{"success": bool, "folder": dict, "id": str}` |
| `upload_file(path, folder_id, overwrite)` | Upload a file | `{"success": bool, "file": dict, "id": str}` |
| `download_file(file_id, output_path)` | Download a file | `{"success": bool, "path": str, "size": int}` |
| `upload_folder(path, parent_id)` | Upload folder recursively | `{"success": bool, "files_uploaded": int}` |
| `delete_item(item_id, permanently)` | Delete/trash an item | `{"success": bool}` |

---

## Usage Examples

### List Files and Folders

```python
from pydrive4 import GoogleDrive

client = GoogleDrive()

# List files in root
files = client.list_files()
for f in files["files"]:
    print(f"📄 {f['name']}")

# List folders
folders = client.list_folders()

# List in specific folder
files = client.list_files(folder_id="folder_id_here")
```

### Search

```python
# Search files by name
results = client.search_files("report")
print(f"Found {results['count']} files")

# Search folders
folders = client.search_folders("Projects")
```

### Create Folders

```python
# Create in root
folder = client.create_folder("My Folder")
print(f"Created: {folder['id']}")

# Create nested
parent = client.create_folder("Parent")
child = client.create_folder("Child", parent_id=parent["id"])
```

### Upload Files

```python
# Upload to root
result = client.upload_file("document.pdf")

# Upload to folder
result = client.upload_file("report.pdf", folder_id="folder_id")

# Overwrite existing
result = client.upload_file("report.pdf", folder_id="folder_id", overwrite=True)
```

### Download Files

```python
# Download with custom path
result = client.download_file("file_id", "local.pdf")

# Download with original name
result = client.download_file("file_id")
```

### Upload Folder

```python
result = client.upload_folder("./my_project")
print(f"Uploaded {result['files_uploaded']} files")
```

### Delete

```python
# Move to trash
client.delete_item("item_id")

# Delete permanently
client.delete_item("item_id", permanently=True)
```

---

## Advanced: GoogleAuth

For more control over authentication:

```python
from pydrive4 import GoogleAuth, GoogleDrive

# Manual auth
auth = GoogleAuth(credentials_file="creds.json")
auth.authenticate()

# Pass to client
client = GoogleDrive(auth=auth)

# Check status
print(f"Authenticated: {auth.is_authenticated}")
print(f"Using ADC: {auth.is_adc}")
print(f"Using Service Account: {auth.is_service_account}")
```

Or use the convenience function:

```python
from pydrive4 import authenticate

auth = authenticate()  # Auto-detect and authenticate
drive = auth.get_drive_service()  # Get raw Drive API service
```

---

## Error Handling

All methods return a dict with `success` key:

```python
result = client.upload_file("document.pdf")

if result["success"]:
    print(f"Uploaded: {result['id']}")
else:
    print(f"Error: {result['error']}")
```

Clean error messages:
```
❌ InvalidCredentialsError: No credentials available. Options:
  1. Run: gcloud auth application-default login
  2. Place 'client_secrets.json' in current directory
  3. Set GOOGLE_APPLICATION_CREDENTIALS environment variable
```

---

## Requirements

- Python 3.10+
- google-api-python-client >= 2.100.0
- google-auth >= 2.15.0
- google-auth-oauthlib >= 1.0.0
- google-auth-httplib2 >= 0.2.0

---

## License

MIT License

---

## Contributing

Contributions are welcome! Please submit a Pull Request.

---

## Acknowledgments

Inspired by [PyDrive2](https://github.com/iterative/PyDrive2), updated for Google Drive API v3.
