import os
import shutil

def copy_images(date, source_folder, destination_folder):
  """Copies images from a certain folder to another folder.

  Args:
    source_folder: The path to the source folder.
    destination_folder: The path to the destination folder.

  """
  for root, dirs, files in os.walk(source_folder):
    for file in files:
      if "_c_0" in file:
        shutil.copy(os.path.join(root, file), destination_folder)

def make_folder(destination_dir, date):
  """Creates a folder in the destination folder."""
  folder_nm = date + "_target"
  os.makedirs(os.path.join(destination_dir, folder_nm), exist_ok=True)

if __name__ == "__main__":
  
  date = "230528"
  source_dir = "S:/04.seatbelt/01.수집데이터/[R2022-02]대왕판교_수집데이터/daewangpangyo"
  destination_dir = "R:/seatbelt/highway_send_data"

  source_folder = os.path.join(source_dir, date)
  destination_folder = os.path.join(destination_dir, date + "_target")

  make_folder(destination_dir, date)
  copy_images(date,source_folder, destination_folder)
