import zipfile
from tqdm import tqdm
import argparse
import shutil
import os

def main():
  # Import the argparse module
  import argparse

  # Create the parser
  parser = argparse.ArgumentParser()

  # Add the arguments
  parser.add_argument("-f", "--folder_path", type=str, default="S:/04.seatbelt/01.수집데이터/daewangpangyo/[R2022-02]대왕판교_수집데이터/daewangpangyo", help="The path to the directory where the files are located.")
  parser.add_argument("-n", "--folder_name", type=str, required=True, help="The name of the directory containing the files.")
  parser.add_argument("-c", "--copy_path", type=str, default="R:/seatbelt/dp_daily_testdata", help="The path to the directory where the files will be copied to.")

  # Parse the arguments
  args = parser.parse_args()
  
  # # Unzip the file
  # unzip(args.folder_path, args.folder_name)
  
  # Copy the files
  copy_files(args.folder_path, args.folder_name, args.copy_path)


def unzip(folder_path, folder_name):
  """Unzips a zip file to the specified folder.

  Args:
    folder_path: The path to the zip file.
    folder_name: The name of the folder to unzip the files to.

  """

  # Open the zip file
  with zipfile.ZipFile(folder_path + '/' + folder_name + '.zip', "r") as zip_ref:

    # Extract all the files to the directory "/my/new/directory"
    for file in tqdm(zip_ref.namelist(), desc = 'Unzip file', unit = 'file'):
      zip_ref.extract(file, folder_path + "/" + folder_name)


def copy_files(folder_path, folder_name, copy_path):
  """Copies all the files in the specified directory to the specified directory.

  Args:
    folder_path: The path to the directory where the files are located.
    folder_name: The name of the directory containing the files.
    copy_path: The path to the directory where the files will be copied to.

  """
    
  # Set the source directory and the copy directory
  src_dir = folder_path + "/" + folder_name # source directory
  copy_dir = copy_path + "/" + folder_name # copy directory

  # Make the directory if it does not exist
  os.makedirs(copy_dir, exist_ok=True)

  # Reset the total number of files and make a empty file list
  total_files = 0
  file_list = []

  # Check through all the file from the source directory and the subdirectory
  for root, dirs, files in os.walk(src_dir):
    for filename in files:
          # Check if file extension is ".jpg", ".jpeg", or ".png" and if the filename contains "right1" or "left1" and "_yolo" is not in the filename
          if filename.lower().endswith((".jpg", ".jpeg", ".png")) and ("_r_" in filename.lower() or "_l_" in filename.lower()) and "_yolo" not in filename.lower():
              total_files += 1
              file_list.append((root, filename))
              
  # Use tqdm to see the process
  with tqdm(total=total_files, desc="Copying Files", unit="file") as pbar:
      for root, filename in file_list:
          src_path = os.path.join(root, filename)
          copy_file_path = os.path.join(copy_dir, filename)
          shutil.copy(src_path, copy_file_path)
          pbar.update(1)

if __name__ == "__main__":
  main()

