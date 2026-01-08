
from pydrive4 import GoogleDrive
drive = GoogleDrive()
files = drive.list_files()
print(files)
