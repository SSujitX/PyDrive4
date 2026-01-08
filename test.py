"""
PyDrive4 Test Script

Authentication options:
1. Run: gcloud auth application-default login
2. Place client_secrets.json or service_account.json in this directory
3. Set GOOGLE_APPLICATION_CREDENTIALS environment variable
"""

from pydrive4 import GoogleAuth, GoogleDrive

auth = GoogleAuth()
auth.authenticate()

drive = GoogleDrive(auth=auth)

files = drive.list_files()
print(files)
