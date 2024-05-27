#!/usr/bin/env python
# coding: utf-8

# In[77]:


import os
import argparse
import pandas as pd

def main():
    """ 
    Title: Accesment_Automation(ver2.0)
    Platform: os, pandas 
    Version: 0.2.0
    Created by srl(SeungRyul Lee), 2023.04.12
    Description: It is a program that uses detection result form YOLOv5 and access by the given condition.
    Warning: It only compares each of three right and left images, so it does not consider the case of both sides (person_05_seatbelt, person_06).
    """
    
    # Create argument parser
    parser = argparse.ArgumentParser(description='Accesment Automation', epilog='Note: Additional information about the usage of this code can be found in the README file.')
    parser.add_argument('--f', dest='folder_path', type=str, help='Folder path for input files')
    parser.add_argument('--s', dest='set_num', type=str, help='Test set number')
    
    # Parse command-line arguments
    args = parser.parse_args()
    
    # Access folder path from command-line argument
    folder_path = args.folder_path
    
    # Access set number from command-line argument
    set_num = args.set_num
    
    # Call function to sort files in folder by first number
    sort_files_by_first_number(folder_path)

    # Call function to create group answer sheet
    create_group_answer_sheet(folder_path, set_num)

    # Call function to generate answer sheet
    generate_answer_sheet(folder_path, set_num)

    # Call function to extract and modify data
    extract_and_modify_data(folder_path, set_num)
    
# In[78]:


def sort_files_by_first_number(folder_path):
    """
    Sorts all .txt files in a given folder by the first number in each line.
    If a file contains a line that doesn't start with a number, prints a ValueError and skips the file.
    """
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            file_path = os.path.join(folder_path, file_name)

            # Read the lines from the file
            with open(file_path, "r") as f:
                lines = f.readlines()

            try:
                # Sort the lines based on the first number in each line
                lines = sorted(lines, key=lambda x: int(x.split()[0]))
            except ValueError:
                # If there's aw ValueError, print the file name and continue with the next file
                print(f"ValueError in file {file_name}")
                continue

            # Write the sorted lines back to the file
            with open(file_path, "w") as f:
                for line in lines:
                    f.write(line.strip() + "\n")


# In[79]:


def create_group_answer_sheet(folder_path, set_num):
    
    output_path = folder_path + '/' + 'set_' + set_num + '_class_set' + '.csv'
    
    # Create an empty dataframe to store the results
    columns = ['filename', '_01_', '_04_', '_05_06_']
    df = pd.DataFrame(columns=columns)

    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            try:
                # Extract the file information
                file_data = {}
                with open(os.path.join(folder_path, filename), 'r') as file:
                    for line in file:
                        values = line.split()
                        class_number = int(values[0])
                        confidence = float(values[5])
                        file_data[class_number] = (confidence, values[1])

                # Get the class with the highest confidence value for each group
                group1_values = [(file_data.get(c, (0, None))[0], c) for c in [2, 3, 8]]
                group2_values = [(file_data.get(c, (0, None))[0], c) for c in [4, 5, 9]]
                group3_values = [(file_data.get(c, (0, None))[0], c) for c in [6, 7, 11]]
                max_group1 = max(group1_values)[1] if max(group1_values)[0] != 0 else ''
                max_group2 = max(group2_values)[1] if max(group2_values)[0] != 0 else ''
                max_group3 = max(group3_values)[1] if max(group3_values)[0] != 0 else ''

                # Create a row for the dataframe
                row = [filename, max_group1, max_group2, max_group3]
                df = df.append(pd.DataFrame([row], columns=columns), ignore_index=True)

            except PermissionError:
                print(f"Permission denied: {filename}")

    # Replace values in the dataframe
    replace_map = {2: 'X', 3: 'O', 4: 'X', 5: 'O', 6: 'X',7: 'O', 8: '', 9: '', 11:'p6'}
    df.replace(replace_map, inplace=True)

    # Save the dataframe to a CSV file
    df.to_csv(output_path, index=False)


# In[80]:


import pandas as pd

def generate_answer_sheet(folder_path, set_num):
    
    output_path = folder_path + '/' + 'set_' + set_num + '_group_answersheet_set'+ '.csv'
    
    # Open the CSV file and create a dataframe
    df = pd.read_csv(folder_path + '/' + 'set_' + set_num + '_class_set' + '.csv')

    # Create empty columns for the answers
    df['answer1'] = ''
    df['answer2'] = ''
    df['answer3'] = ''

    # Loop through the dataframe in groups of three rows
    for i in range(0, len(df), 3):
        # Get the values from each row in the group
        row1 = df.iloc[i]
        row2 = df.iloc[i+1]
        row3 = df.iloc[i+2]

        # Determine the most common value in each group and update the answer columns(group1)
        for j, group in enumerate(['_01_']):
            values = [row1[group]]
            df.at[i, 'answer1'] = values[0]

        
        # Determine the most common value in each group and update the answer columns(group2)
        for j, group in enumerate(['_04_']):
            values = [row2[group], row3[group]]
            o_count = values.count('O')
            x_count = values.count('X')
            if o_count == 0 and x_count == 0:
                df.at[i, 'answer2'] = ''
            elif o_count >= x_count:
                df.at[i, 'answer2'] = 'O'
            else:
                df.at[i, 'answer2'] = 'X'
                

        # Determine the most common value in each group and update the answer columns(group3)
        for j, group in enumerate(['_05_06_']):
            values = [row2[group], row3[group]]
            if 'p6' in values:
                df.at[i, 'answer3'] = ''
            else:
                o_count = values.count('O')
                x_count = values.count('X')
                if o_count == 0 and x_count == 0:
                    df.at[i, 'answer3'] = ''
                elif o_count >= x_count:
                    df.at[i, 'answer3'] = 'O'
                else:
                    df.at[i, 'answer3'] = 'X'
                    

    # Save the updated dataframe to a new CSV file
    df.to_csv(output_path, index=False)


# In[81]:


import pandas as pd

def extract_and_modify_data(folder_path, set_num):
    
    output_path = folder_path + '/' 'set_' + set_num + '_final_answersheet_set'+ '.csv'
    
    # Read the original dataframe from the CSV file
    df = pd.read_csv(folder_path + '/' + 'set_' + set_num + '_group_answersheet_set'+ '.csv')

    # Create a new dataframe to store the extracted values
    new_df = pd.DataFrame(columns=['filename', 'left1', 'left2', 'right1', 'right2'])

    # Loop through the original dataframe in groups of 6 rows
    for i in range(0, len(df), 6):
        # Get the values from each row in the group
        row1 = df.iloc[i]
        row2 = df.iloc[i+1]
        row3 = df.iloc[i+2]
        row4 = df.iloc[i+3]
        row5 = df.iloc[i+4]
        row6 = df.iloc[i+5]

        # Extract the values to the new dataframe
        new_row1 = {
            'filename': '',
            'left1': '',
            'left2': '',
            'right1': row4['answer1'],
            'right2': row4['answer2']
        }
        new_row2 = {
            'filename': '',
            'left1': '',
            'left2': row1['answer3'],
            'right1': '',
            'right2': row4['answer3']
        }
        new_row3 = {
            'filename': '',
            'left1': row1['answer1'],
            'left2': row1['answer2'],
            'right1': '',
            'right2': ''
        }

        new_df = new_df.append([new_row1, new_row2, new_row3], ignore_index=True)

        # Update the 'answer1', 'answer2', and 'answer3' values at specific row and column positions
        new_df.at[i/2+2, 'filename'] = row4['filename'].split('_')[1]
        new_df.at[i/2+2, 'left1'] = row1['answer1']
        new_df.at[i/2+2, 'left2'] = row1['answer2']
        new_df.at[i/2+1, 'left2'] = row1['answer3']
        new_df.at[i/2, 'right1'] = row4['answer1']
        new_df.at[i/2, 'right2'] = row4['answer2']
        new_df.at[i/2+1,'right2'] = row4['answer3']

    # Save the updated original dataframe to a new CSV file
    new_df.to_csv(output_path , index=False)




if __name__ == "__main__":
    main()


# In[ ]:




