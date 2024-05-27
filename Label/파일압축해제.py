#unzip the whole file
import zipfile

folder_path = "path/to/folder"

# Open the zip file
with zipfile.ZipFile(folder_path + "/filename.zip", "r") as zip_ref:

    for file in zip_ref.namelist():
        zip_ref.extract(file, folder_path + "/foldername")