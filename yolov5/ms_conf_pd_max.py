import os
import argparse
import pandas as pd
from tqdm import tqdm

def ms_answersheet(date):
    folder_path = f"R:/seatbelt/ms_daily_testdata/detect/ms_{date}/labels" 
    csv_file_path = f"C:/Users/Gnt_Safe_Port_DT/Desktop/ms_{date}_answersheet_max.csv"

    # Get all the files in the folder
    all_files = os.listdir(folder_path)

    # Create a dictionary to store unique labels for each desired filename
    desired_filenames = {}

    # Iterate over all the files
    for file_name in tqdm(all_files):
        # Extract the desired filename using .split('_')[1] + .split('_')[2]
        desired_filename = file_name.split('_')[1] + '_' + file_name.split('_')[2]
        
        # Check if the desired filename already exists in the dictionary
        if desired_filename in desired_filenames:
            # Retrieve the existing dictionary for the desired filename
            file_info = desired_filenames[desired_filename]
            unique_labels = file_info['unique_labels']
            label_conf_map = file_info['label_conf_map']
        else:
            # Initialize a new set for unique labels and a dictionary for label-conf mapping
            unique_labels = set()
            label_conf_map = {}
        
        # Construct the full file path
        file_path = os.path.join(folder_path, file_name)
        
        # Read and process the file
        with open(file_path, 'r') as file:
            for line in file:
                label = int(line.split()[0])
                conf = float(line.split()[5])  # Convert confidence to float
                if label >= 3 and label <= 14:
                    # If label exists in label_conf_map, update the confidence if current conf is higher
                    if label in label_conf_map:
                        label_conf_map[label] = max(label_conf_map[label], conf)
                    else:
                        label_conf_map[label] = conf
                    unique_labels.add(label)

        # Update the dictionary with the new set of unique labels and label-conf mapping
        desired_filenames[desired_filename] = {'unique_labels': unique_labels, 'label_conf_map': label_conf_map}

    # Create a list of dictionaries to store data for DataFrame
    data = []
    
    for desired_filename, file_info in desired_filenames.items():
        unique_labels = file_info['unique_labels']
        label_conf_map = file_info['label_conf_map']
        
        seat_list = [''] * 12
        seat_conf_list = [''] * 12

        for label in unique_labels:
            seat_index = label - 3
            seat_list[seat_index] = 'O'
            seat_conf_list[seat_index] = label_conf_map[label]

        data.append({
            'filename': desired_filename,
            'seated': len(unique_labels),
            **{f'seat{i+1}': seat_list[i] for i in range(12)},
            **{f'seat{i+1}_conf': seat_conf_list[i] for i in range(12)}
        })

    # Create a DataFrame
    df = pd.DataFrame(data)
    
    # Reorder columns
    column_order = ['filename', 'seated']
    for i in range(1, 13):
        column_order.extend([f'seat{i}', f'seat{i}_conf'])

    # Reindex DataFrame with the new column order
    df = df[column_order]

    # Write the DataFrame to a CSV file
    df.to_csv(csv_file_path, index=False)

    print("CSV file completed")

# Create an argument parser
parser = argparse.ArgumentParser(description='Process MS answer sheets for a specific date')

# Add an argument for the date
parser.add_argument('-d', '--date', type=str, help='Date for processing MS answer sheets')

# Parse the command-line arguments
args = parser.parse_args()

# Call the function with the provided date argument
ms_answersheet(args.date)
