import argparse
import pandas as pd
import re
import os

def update_file(road, month, date, number):

    txt_path = f'R:/seatbelt/highway_send_data/{road}/{month}/{date}_base64/{date}_plate/{date}_plate_{number}.txt'
    updated_txt_path = f'R:/seatbelt/highway_send_data/{road}/{month}/{date}_base64/{date}_plate/updated_{date}_plate_{number}.txt'
    # os.makedirs(updated_txt_path, exist_ok=True)       
    updated_lines = []
    pattern = r'pg_(\d{6}_\d{6})_c_0.txt'
    
    with open(txt_path, 'r') as file:
        for line in file:
            line = line.strip()
            match = re.match(pattern, line)
            if match:
                extracted_text = match.group(1)
                updated_lines.append(extracted_text + '\n')

    with open(updated_txt_path, 'w') as updated:
        for text in updated_lines:
            updated.write(text + '\n')


def extract_excel_data(road, month, date, number):
    
    updated_txt_path = f'R:/seatbelt/highway_send_data/{road}/{month}/{date}_base64/{date}_plate/updated_{date}_plate_{number}.txt'

    excel_path = r'R:\seatbelt\highway_send_data\seatbelt.xlsx'

    # Read the text file with the list of filenames
    with open(updated_txt_path, 'r') as file:
        filenames = [line.strip() for line in file]

    # Read the Excel file
    excel_data = pd.read_excel(excel_path, sheet_name=f'dp_{date}')

    # Filter rows based on matching filenames
    matching_rows = excel_data[excel_data['filename'].isin(filenames)]
    # Extract the desired columns
    extracted_data = matching_rows[['filename', 'seated']]

    # Save the extracted data to a CSV file
    csv_filename = f'R:/seatbelt/highway_send_data/{road}_0~7/{number}_{date}.csv'
    extracted_data.to_csv(csv_filename, index=False)
    print(f"Extraction completed. The data has been saved to {csv_filename}")

def main():
    parser = argparse.ArgumentParser(description='Extract Excel data based on a specified date.')
    parser.add_argument('-r','--road', type=str, default= 'dp', help='The road to extract the data from (e.g., dp)')
    parser.add_argument('-m','--month', type=str,default='2306', help='The month to extract the data from (e.g., 2306)')
    parser.add_argument('-d','--date', type=int, help='The date to extract the data from (e.g., 230502)')
    parser.add_argument('-n', '--number', type=str, default='0to6', help="The number of the car plate (e,g., 0to6)")
    args = parser.parse_args()

    update_file(args.road, args.month, args.date, args.number)
    extract_excel_data(args.road, args.month, args.date, args.number)

if __name__ == "__main__":
    main()