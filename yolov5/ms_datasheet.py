import os
import csv
import argparse
from tqdm import tqdm

def ms_answersheet(date):
    folder_path = f"/mnt/r/seatbelt/ms_daily_testdata/detect/ms_{date}/labels" 
    csv_file_path = f"/mnt/r/seatbelt/ms_daily_testdata/detect/ms_{date}/ms_{date}_answersheet.csv"

    # Get all the files in the folder
    all_files = os.listdir(folder_path)

    # Create a dictionary to store unique labels for each desired filename
    desired_filenames = {}

    # Iterate over all the files with tqdm
    for file_name in tqdm(all_files, desc='Processing files', unit='file'):
        # Extract the desired filename using .split('_')[1] + .split('_')[2]
        desired_filename = file_name.split('_')[1] + '_' + file_name.split('_')[2]
        
        # Check if the desired filename already exists in the dictionary
        if desired_filename in desired_filenames:
            # Retrieve the existing set of unique labels
            unique_labels = desired_filenames[desired_filename]
        else:
            # Initialize a new set for unique labels
            unique_labels = set()
        
        # Construct the full file path
        file_path = os.path.join(folder_path, file_name)
        
        # Read and process the file
        with open(file_path, 'r') as file:
            for line in file:
                label = line.split()[0]
                label = int(label)
                if label >= 3 and label <= 14:
                    unique_labels.add(label)

        # Update the dictionary with the new set of unique labels
        desired_filenames[desired_filename] = unique_labels

    # Write the results to a CSV file
    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['filename', 'seated', 'seat1', 'seat2', 'seat3', 'seat4', 
                         'seat5', 'seat6', 'seat7', 'seat8', 'seat9','seat10', 'seat11', 'seat12'])
        
        for desired_filename, unique_labels in desired_filenames.items():
            # Initialize lists to store seat and confidence values
            seat_list = [''] * 12

            # Populate seat and confidence lists based on unique_labels
            for label in unique_labels:
                seat_index = label - 3
                seat_list[seat_index] = 'O'

            # Write the row to the CSV file
            writer.writerow([desired_filename, len(unique_labels)] + seat_list)
        
        print("CSV file completed")

# Create an argument parser
parser = argparse.ArgumentParser(description='Process MS answer sheets for a specific date')

# Add an argument for the date
parser.add_argument('-d', '--date', type=str, help='Date for processing MS answer sheets')

# Parse the command-line arguments
args = parser.parse_args()

# Call the function with the provided date argument
ms_answersheet(args.date)
