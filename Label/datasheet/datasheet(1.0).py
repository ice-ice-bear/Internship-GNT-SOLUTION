#!/usr/bin/env python
# coding: utf-8

# In[39]:


import os
import pandas as pd
import argparse


def main():
    """ 
    Title: Accesment_Datasheet(ver2.0)
    Platform: os, pandas, argparse 
    Version: 0.2.0
    Created by srl(SeungRyul Lee), 2023.04.17
    Description: It is a program that uses detection result form YOLOv5 and access by the given condition.
    """
    
    # Create argument parser
    parser = argparse.ArgumentParser(description='Accesment Datasheet', epilog='Note: Additional information about the usage of this code can be found in the README file.')
    parser.add_argument('--source', dest='folder_path', type=str, help='Folder path for input files')
    parser.add_argument('--name', dest='folder_name', type=str,default = 'jj', help='forder name(ex. jj, dw)')
    parser.add_argument('--weights', dest='weight', type=str,default = 'weight', help='model weight')
    
    # Parse command-line arguments
    args = parser.parse_args()
    
    # Access folder path from command-line argument
    folder_path = args.folder_path
    
    # Access folder name from command-line argument
    folder_name = args.folder_name
    
    # Access weight from command-line argument
    weight = args.weight
    
    label_list(folder_path)
    
    image_list(folder_path)
    
    make_empty_file(folder_path)

    assesment_datasheet(folder_path, folder_name, weight)


def label_list(folder_path):
    
    #label_path
    label_path = folder_path + '/labels'
    
    # Get a list of all files in the folder
    label_names = os.listdir(label_path)

    # Save the list of file names to a text file in the same folder
    with open(os.path.join(folder_path, "label_list.txt"), "w") as file:
        for name in label_names:
            file.write(name + "\n")

def image_list(folder_path):
    
    # Get a list of all files in the folder
    image_names = os.listdir(folder_path)

    # Replace '.jpg' with '.txt' for image file names
    image_names = [name.replace('.jpg', '.txt') for name in image_names]

    # Save the list of file names to a text file in the same folder
    with open(os.path.join(folder_path, "image_list.txt"), "w") as file:
        for name in image_names:
            file.write(name + "\n")

def make_empty_file(folder_path):
    file1_path = os.path.join(folder_path, 'label_list.txt')
    file2_path = os.path.join(folder_path, 'image_list.txt')
    output_folder = os.path.join(folder_path, 'labels_blank')
    label_path = os.path.join(folder_path, 'labels')

    # Create 'labels_blank' subfolder, if not exists
    os.makedirs(output_folder, exist_ok=True)

    banned_words = ['.csv', 'image', 'labels', 'label']  # List of banned words

    # Read file1
    with open(file1_path, 'r') as file1:
        file1_lines = set(line.strip() for line in file1)

    # Read file2
    with open(file2_path, 'r') as file2:
        file2_lines = set(line.strip() for line in file2)

    # Find differences
    differences = file1_lines.symmetric_difference(file2_lines)

    # Create empty text file with differences, if not found
    if differences:
        print("Differences found:")
        for line in differences:
            # Skip creating empty text file for lines that contain banned words
            if any(word in line for word in banned_words):
                continue
            print(line)

            # Create empty text file with the line as filename in the output folder, if not found
            filename_output = os.path.join(output_folder, line)
            if not os.path.exists(filename_output):
                open(filename_output, 'w').close()

            # Create empty text file with the line as filename in the label path, if not found and not already exists
            filename_label = os.path.join(label_path, line)
            if not os.path.exists(filename_label):
                open(filename_label, 'w').close()
            else:
                print(f"File '{line}' already exists in the label path.")
        print("Total number of different lines: {}".format(len(differences)))
    else:
        print("No differences found.")

def assesment_datasheet(folder_path, folder_name, weight):

    label_path = folder_path + '/labels'

    # Create an empty dataframe to store the results
    columns = ['filename', '_01', '_01_conf', '_04', '_04_conf', '_05', '_05_conf']
    df = pd.DataFrame(columns=columns)

    for filename in os.listdir(label_path):
        if filename.endswith('.txt'):
            try:
                # Extract the file information
                file_data = {}
                with open(os.path.join(label_path, filename), 'r') as file:
                    for line in file:
                        values = line.split()
                        class_number = int(values[0])
                        confidence = float(values[5])
                        file_data[class_number] = (confidence, )

                # Get the class with the highest confidence value for each group
                _01_values = [(file_data.get(c, (0, None))[0], c) for c in [2, 3, 8]]
                _04_values = [(file_data.get(c, (0, None))[0], c) for c in [4, 5, 9]]
                _05_values = [(file_data.get(c, (0, None))[0], c) for c in [6, 7, 11]]

                max_01 = max(_01_values)[1] if max(_01_values)[0] != 0 else ''
                max_04 = max(_04_values)[1] if max(_04_values)[0] != 0 else ''
                max_05 = max(_05_values)[1] if max(_05_values)[0] != 0 else ''

                max_01_conf = max(_01_values)[0] if max(_01_values)[0] != 0 else ''
                max_04_conf = max(_04_values)[0] if max(_04_values)[0] != 0 else ''
                max_05_conf = max(_05_values)[0] if max(_05_values)[0] != 0 else ''

                # Create a row for the dataframe
                row = [filename, max_01, max_01_conf, max_04, max_04_conf, max_05, max_05_conf]
                df = df.append(pd.DataFrame([row], columns=columns), ignore_index=True)


            except PermissionError:
                print(f"Permission denied: {filename}")


        # Replace values in the dataframe
        replace_map = {2: 'X', 3: 'O', 4: 'X', 5: 'O', 6: 'X',7: 'O', 8: 'emp', 9: 'emp', 11:'emp'}
        df.replace(replace_map, inplace=True)

    # Define the column names for the new dataframe
    columns = ['filename',
            '1_conf', '1', '3', '3_conf', 
            '4_conf', '4', '6', '6_conf', 
            '5_l_conf', '5_l', '5_r', '5_r_conf'
            ] 

    # Create an empty dataframe with the defined columns
    df_lr = pd.DataFrame(columns = columns)

    # Loop through the original dataframe in increments of 6 rows
    for i in range(0, len(df), 6):
        # Get the rows for each body part from the original dataframe
        row1 = df.iloc[i]
        row2 = df.iloc[i+1]
        row3 = df.iloc[i+2]
        row4 = df.iloc[i+3]
        row5 = df.iloc[i+4]
        row6 = df.iloc[i+5]

        # Create a dictionary for the first row of the new dataframe
        df_lr_row1 = {
            'filename' : row1['filename'].split('_')[1] + '_' + row1['filename'].split('_')[2],
            '1' : row1['_01'],
            '1_conf' : row1['_01_conf'],
            '3' : row4['_01'],
            '3_conf' : row4['_01_conf'],
            '4' : row1['_04'],
            '4_conf' : row1['_04_conf'],
            '6' : row4['_04'],
            '6_conf' : row4['_04_conf'],
            '5_l' : row1['_05'],
            '5_l_conf' : row1['_05_conf'],
            '5_r' : row4['_05'],
            '5_r_conf' : row4['_05_conf']
        }

        # Create a dictionary for the second row of the new dataframe
        df_lr_row2 = {
            '1' : row2['_01'],
            '1_conf' : row2['_01_conf'],
            '3' : row5['_01'],
            '3_conf' : row5['_01_conf'],
            '4' : row2['_04'],
            '4_conf' : row2['_04_conf'],
            '6' : row5['_04'],
            '6_conf' : row5['_04_conf'],
            '5_l' : row2['_05'],
            '5_l_conf' : row2['_05_conf'],
            '5_r' : row5['_05'],
            '5_r_conf' : row5['_05_conf']
        }

        # Create a dictionary for the third row of the new dataframe
        df_lr_row3 = {
            '1' : row3['_01'],
            '1_conf' : row3['_01_conf'],
            '3' : row6['_01'],
            '3_conf' : row6['_01_conf'],
            '4' : row3['_04'],
            '4_conf' : row3['_04_conf'],
            '6' : row6['_04'],
            '6_conf' : row6['_04_conf'],
            '5_l' : row3['_05'],
            '5_l_conf' : row3['_05_conf'],
            '5_r' : row6['_05'],
            '5_r_conf' : row6['_05_conf']
        }

        # Append the three new rows to the new dataframe
        df_lr = df_lr.append([df_lr_row1, df_lr_row2, df_lr_row3], ignore_index=True)

        df_lr['left'] = ''
        df_lr['mid'] = ''
        df_lr['right'] = ''

        for i in range(0, len(df_lr), 3):
            row1 = df_lr.iloc[i]
            row2 = df_lr.iloc[i+1]
            row3 = df_lr.iloc[i+2]

            for j, k in enumerate(['1']):
                values = [row1[k]]
                df_lr.at[i+1, 'left'] = values[0]

            for j, k in enumerate(['3']):
                values = [row1[k]]
                df_lr.at[i+1, 'right'] = values[0]

            for j, k in enumerate(['4']):
                values = [row2[k], row3[k]]
                o_count = values.count('O')
                x_count = values.count('X')
                emp_count = values.count('emp')
                if o_count == 0 and x_count == 0:
                    df_lr.at[i+2, 'left'] = ''
                elif emp_count == 2:
                    df_lr.at[i+2, 'left'] = ''
                elif o_count >= x_count:
                    df_lr.at[i+2, 'left'] = 'O'
                else:
                    df_lr.at[i+2, 'left'] = 'X'


            for j, k in enumerate(['6']):
                values = [row2[k], row3[k]]
                o_count = values.count('O')
                x_count = values.count('X')
                emp_count = values.count('emp')
                if o_count == 0 and x_count == 0:
                    df_lr.at[i+2, 'right'] = ''
                elif emp_count == 2:
                    df_lr.at[i+2, 'right'] = ''
                elif o_count >= x_count:
                    df_lr.at[i+2, 'right'] = 'O'
                else:
                    df_lr.at[i+2, 'right'] = 'X'


            for j, k in enumerate(['5_l', '5_r']):
                values_l = [row2['5_l'], row3['5_l']]
                values_r = [row2['5_r'], row3['5_r']]
                o_count_l = values_l.count('O') 
                x_count_l = values_l.count('X')
                emp_count_l = values_l.count('emp')
                o_count_r = values_r.count('O') 
                x_count_r = values_r.count('X')
                emp_count_r = values_r.count('emp')

                if o_count_l == 0 and x_count_l == 0:
                    l_count = ''
                elif emp_count_l >= 1:
                    l_count = ''
                else:
                    if o_count_l >= 1:
                        l_count = 'O'
                    else:
                        l_count = 'X'

                if o_count_r == 0 and  x_count_r == 0:
                    r_count = ''
                elif emp_count_r >= 1:
                    r_count = ''
                else:
                    if o_count_r >= 1:
                        r_count = 'O'
                    else:
                        r_count = 'X'

                if l_count == '' or r_count == '':
                    df_lr.at[i+2, 'mid'] = ''
                else:
                    if l_count == r_count:
                        df_lr.at[i+2, 'mid'] = l_count
                    elif l_count == 'O' and r_count == 'X':
                        df_lr.at[i+2, 'mid'] = 'O'
                    elif l_count == 'X' and r_count == 'O':
                        df_lr.at[i+2, 'mid'] = 'O'
                    else:
                        df_lr.at[i+2, 'mid'] = 'X'

        replace_map = {'emp' : ''}
        df_lr['left'].replace(replace_map, inplace=True)
        df_lr['mid'].replace(replace_map, inplace=True)
        df_lr['right'].replace(replace_map, inplace=True)

        df_lr.to_csv(folder_path + '/' + weight + '_' + folder_name + '_' + 'assesment_datasheet.csv', index=False)


if __name__ == "__main__":
    main()

