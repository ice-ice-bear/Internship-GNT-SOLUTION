import argparse
import os
import shutil
import base64
import cv2
from tqdm import tqdm

def copy_images(date, source_folder, destination_folder):
    """Copies images from a certain folder to another folder.
    Args:
        source_folder: The path to the source folder.
        destination_folder: The path to the destination folder.
    """
    file_list = []
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            if "_c_0" in file:
                file_list.append(os.path.join(root, file))

    # Use tqdm to display progress
    with tqdm(total=len(file_list), desc="Copying Images", unit="image") as pbar:
        for file in file_list:
            shutil.copy(file, destination_folder)
            pbar.update(1)

def make_folder(destination_dir, date):
    """Creates a folder in the destination folder."""
    folder_nm = date + "_target"
    os.makedirs(os.path.join(destination_dir, folder_nm), exist_ok=True)

def convert_to_base64(destination_dir, destination_folder, date):
    """Converts all images in the specified directory to base64 format.
    Args:
        date: The date of the images to convert.
    Returns:
        None.
    """
    # Get the path to the directory containing the images.
    file_path = destination_folder

    # Get a list of all the images in the directory.
    file_list = os.listdir(file_path)

    # Create a new directory to store the base64 files.
    path2 = os.path.join(destination_dir, date + '_base64')
    os.makedirs(path2, exist_ok=True)

    # Use tqdm to display progress
    with tqdm(total=len(file_list), desc="Converting to Base64", unit="image") as pbar:
        # Iterate over the images and convert them to base64 format.
        for i in file_list:
            with open(file_path + "/" + i, "rb") as img:
                base64_str = base64.b64encode(img.read())
                f = open(path2 + "/" + i[:-4] + ".txt", "w+")
                f.write(str(base64_str, "utf-8"))
                f.close()
            pbar.update(1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--date", type=str, default="230528", help="The date of the images.")
    parser.add_argument("-s", "--source_dir", type=str, default="S:/04.seatbelt/01.수집데이터/[R2022-02]죽전휴게소_수집데이터/죽전수집데이터", help="The path to the source folder.")
    parser.add_argument("-t", "--destination_dir", type=str, default="R:/seatbelt/highway_send_data/jj", help="The path to the destination folder.")

    args = parser.parse_args()

    date = args.date
    source_folder = args.source_dir
    destination_dir = args.destination_dir

    source_folder = os.path.join(source_folder, date)
    destination_folder = os.path.join(destination_dir, date + "_target")

    make_folder(destination_dir, date)
    copy_images(date, source_folder, destination_folder)
    convert_to_base64(destination_dir, destination_folder, date)

if __name__ == "__main__":
    main()