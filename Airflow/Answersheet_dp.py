from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.sensors.filesystem import FileSensor
from airflow.utils.task_group import TaskGroup

import datetime
import pendulum
import pandas as pd
import zipfile
import os
import base64
import requests
import re

# Augment for answersheet(Volatile)
road = "dp"

# Augment for answersheet(Stationary)
copy_path = f"/mnt/r/seatbelt/{road}_daily_testdata"
weight = '230412_seatbelt_traingset06.pt'

# Augment for car number plate(Stationary)
highway_dir = f"/mnt/r/seatbelt/highway_send_data/{road}"

def _set_variable(**kwargs):
    # today = datetime.date.today()

    # today = datetime.date.today()

    # days_before = today - datetime.timedelta(days=13)

    # year = days_before.year

    # month = days_before.month

    # day = days_before.day

    # # Check if the month is less than 10
    # if month < 10:
    #     # Pad the month with a leading zero
    #     month = "0" + str(month)

    # # Check if the date is less than 10
    # if day < 10:
    #     # Pad the date with a leading zero
    #     day = "0" + str(day)

    # date = str(year)[2:4] + str(month) + str(day)

    date = "230821"

    folder_path = f'/mnt/s/04.seatbelt/01.수집데이터/daewangpangyo/[R2022-02]대왕판교_수집데이터/daewangpangyo'
    folder_name = road + "_" + date
    extract_path = os.path.join(folder_path, date)
    project_path = os.path.join(copy_path, "detect")
    detected_folder_path = os.path.join(project_path, folder_name)
    month = date[:4]

    kwargs['ti'].xcom_push(key='date', value=date)
    kwargs['ti'].xcom_push(key='folder_path', value=folder_path)
    kwargs['ti'].xcom_push(key='extract_path', value=extract_path)
    kwargs['ti'].xcom_push(key='folder_name', value=folder_name)
    kwargs['ti'].xcom_push(key='project_path', value=project_path)
    kwargs['ti'].xcom_push(key='detected_folder_path', value=detected_folder_path)
    kwargs['ti'].xcom_push(key='month', value=month)

def _unzip_files(extract_path):
    
    zip_file_path = os.path.join(extract_path + '.zip')
    
    with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
        zip_ref.extractall(extract_path)


def _copy_side_image(extract_path, date, copy_path):

    copy_dir = os.path.join(copy_path, date)
    os.makedirs(copy_dir, exist_ok=True)

    file_list = []

    for root, dirs, files in os.walk(extract_path):
        for filename in files:
            if filename.lower().endswith((".jpg", ".jpeg", ".png")) and ("_r_" in filename.lower() or "_l_" in filename.lower()) and "_yolo" not in filename.lower():
                file_list.append((root, filename))
  
    for root, filename in file_list:
        source_file_path = os.path.join(root, filename)
        copy_file_path = os.path.join(copy_dir, filename)
        os.system(f'sudo cp {source_file_path} {copy_file_path}')

    return copy_dir
    

def _copy_center_image(date, extract_path, highway_dir):

    folder_nm = f"{date}_target"
    highway_folder = os.path.join(highway_dir, folder_nm)

    os.makedirs(highway_folder, exist_ok=True)
    
    file_list = []

    for root, dirs, files in os.walk(extract_path):
        for filename in files:
            if filename.lower().endswith((".jpg", ".jpeg", ".png")) and ("_c_" in filename.lower()) and "_yolo" not in filename.lower():
                file_list.append((root, filename))

    for root, filename in file_list:
        source_file_path = os.path.join(root, filename)
        copy_file_path = os.path.join(highway_folder, filename)
        os.system(f'sudo cp {source_file_path} {copy_file_path}')

    return highway_folder


def _convert_to_base64(highway_dir, highway_folder, date):
    file_path = highway_folder

    folder_nm = date + "_target"
    os.makedirs(os.path.join(highway_dir, folder_nm), exist_ok=True)

    # Get a list of all the images in the directory.
    file_list = os.listdir(file_path)

    # Create a new directory to store the base64 files.
    base_path = os.path.join(highway_dir, date + '_base64')
    os.makedirs(base_path, exist_ok=True)

    # Iterate over the images and convert them to base64 format.
    for i in file_list:
        with open(file_path + "/" + i, "rb") as img:
            base64_str = base64.b64encode(img.read())
            f = open(base_path + "/" + i[:-4] + ".txt", "w+")
            f.write(str(base64_str, "utf-8"))
            f.close()

def _make_image_list(detected_folder_path):

    # Get a list of all files in the folder
    image_names = os.listdir(detected_folder_path)

    # Replace '.jpg' with '.txt' for image file names
    image_names = [name.replace('.jpg', '.txt') for name in image_names]

    # Save the list of file names to a text file in the same folder
    with open(os.path.join(detected_folder_path, "image_list.txt"), "w") as file:
        for name in image_names:
            file.write(name + "\n")

def _make_label_list(detected_folder_path):
    
    #label_path
    label_path = os.path.join(detected_folder_path, "labels")
    
    # Get a list of all files in the folder
    label_names = os.listdir(label_path)

    # Save the list of file names to a text file in the same folder
    with open(os.path.join(detected_folder_path, "label_list.txt"), "w") as file:
        for name in label_names:
            file.write(name + "\n")


def _make_empty_file(detected_folder_path):
    file1_path = os.path.join(detected_folder_path, 'label_list.txt')
    file2_path = os.path.join(detected_folder_path, 'image_list.txt')
    label_path = os.path.join(detected_folder_path, 'labels')

    banned_words = ['.csv', '.xlsx', '.db', 'image', 'labels', 'label']  # List of banned words

    # Read file1
    with open(file1_path, 'r') as file1:
        file1_lines = set(line.strip() for line in file1)

    # Read file2
    with open(file2_path, 'r') as file2:
        file2_lines = set(line.strip() for line in file2)

    # Find differences
    differences = file1_lines.symmetric_difference(file2_lines)

    # Remove lines that contain banned words
    differences = [line for line in differences if not any(word in line for word in banned_words)]

    # Create empty text file with differences, if not found
    if differences:
        print("Empty text file detected.")        
        for line in differences:
            # Create empty text file with the line as filename in the label path, if not found and not already exists
            filename_label = os.path.join(label_path, line)
            if not os.path.exists(filename_label):
                open(filename_label, 'w').close()
            else:
                print(f"File '{line}' already exists in the label path.")
    
        print("Total number of different lines: {}".format(len(differences)))
    else:
        print("All files are remining.")

    return label_path

def _check_6_pairs(label_path):
    files = os.listdir(label_path)

    expected_files = ['_r_0', '_r_1', '_r_2', '_l_0', '_l_1', '_l_2']
    missing_files = []

    name_counts = {}
    for file in files:
        road = file.split("_")[0]
        date = file.split("_")[1]
        third_name = file.split("_")[2]
        name_counts[third_name] = name_counts.get(third_name, 0) + 1

    for third_name in name_counts:
        if name_counts[third_name] < 6:
            for expected_file in expected_files:
                missing_file = f"{road}_{date}_{third_name}{expected_file}.txt"
                if missing_file not in files:
                    missing_files.append(missing_file)

    for missing_file in missing_files:
        open(os.path.join(label_path, missing_file), 'w').close()
        print(f"The file '{missing_file}' has been created.")

    if len(missing_files) == 0:
        print("No missing files found.")
            
def _update_file_0to6(road, month, date):

    txt_path = f'/mnt/r/seatbelt/highway_send_data/{road}/{month}/{date}_base64/{date}_plate/{date}_plate_0to6.txt'
    updated_txt_path = f'/mnt/r/seatbelt/highway_send_data/{road}/{month}/{date}_base64/{date}_plate/updated_{date}_plate_0to6.txt'
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

def _update_file_7(road, month, date):

    txt_path = f'/mnt/r/seatbelt/highway_send_data/{road}/{month}/{date}_base64/{date}_plate/{date}_plate_7.txt'
    updated_txt_path = f'/mnt/r/seatbelt/highway_send_data/{road}/{month}/{date}_base64/{date}_plate/updated_{date}_plate_7.txt'
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

def _make_answersheet_filepath(detected_folder_path, date, weight):

    csv_path = detected_folder_path + '/' + date + '_' + weight + '_' + 'assesment_datasheet.csv'
    return csv_path


def _extract_csv_data_0to6(road, month, date, csv_path):

    number = "0to6"

    updated_txt_path = f'/mnt/r/seatbelt/highway_send_data/{road}/{month}/{date}_base64/{date}_plate/updated_{date}_plate_{number}.txt'

    # Read the text file with the list of filenames
    with open(updated_txt_path, 'r') as file:
        filenames = [line.strip() for line in file]

    # Read the CSV file
    csv_data = pd.read_csv(csv_path)

    # Filter rows based on matching filenames
    matching_rows = csv_data[csv_data['filename'].isin(filenames)]
    # Extract the desired columns
    extracted_data = matching_rows[['filename', 'seated']]

    # Save the extracted data to a CSV file
    csv_filename = f'/mnt/r/seatbelt/highway_send_data/{road}_0~7/{number}_{date}.csv'
    extracted_data.to_csv(csv_filename, index=False)
    print(f"Extraction completed. The data has been saved to {csv_filename}")

def _extract_csv_data_7(road, month, date, csv_path):

    number = "7"

    updated_txt_path = f'/mnt/r/seatbelt/highway_send_data/{road}/{month}/{date}_base64/{date}_plate/updated_{date}_plate_{number}.txt'

    # Read the text file with the list of filenames
    with open(updated_txt_path, 'r') as file:
        filenames = [line.strip() for line in file]

    # Read the CSV file
    csv_data = pd.read_csv(csv_path)

    # Filter rows based on matching filenames
    matching_rows = csv_data[csv_data['filename'].isin(filenames)]
    # Extract the desired columns
    extracted_data = matching_rows[['filename', 'seated']]

    # Save the extracted data to a CSV file
    csv_filename = f'/mnt/r/seatbelt/highway_send_data/{road}_0~7/{number}_{date}.csv'
    extracted_data.to_csv(csv_filename, index=False)
    print(f"Extraction completed. The data has been saved to {csv_filename}")

with DAG(f'answersheet_{road}',
         description="make answersheet",
         tags = ["yolov5"],
         start_date=pendulum.datetime(2022, 1, 1 ,tz="Asia/Seoul"),
         schedule_interval = None,
         catchup=False) as dag:
    
    set_variable = PythonOperator(
        task_id="set_variable",
        python_callable=_set_variable
    )
    
    unzip_files = PythonOperator(
        task_id="unzip_files",
        python_callable=_unzip_files,
        op_kwargs={'extract_path' :"{{ti.xcom_pull(task_ids='set_variable', key = 'extract_path')}}",
                   }
    )
    
    copy_side_image = PythonOperator(
        task_id="copy_side_image",
        python_callable=_copy_side_image,
        op_kwargs={'extract_path':"{{ti.xcom_pull(task_ids='set_variable', key = 'extract_path')}}",
                    'date': "{{ti.xcom_pull(task_ids='set_variable', key = 'date')}}",
                    'copy_path': copy_path
                    }
                    )
    
    run_object_detection = BashOperator(
        task_id="run_object_detection",
        bash_command="""
        cd ~
        source yolov5_env/bin/activate
        cd /home/gnt/yolov5
        python3 detect.py --weights {{ params.weight }} --source {{ ti.xcom_pull(task_ids='copy_side_image') }} --project {{ ti.xcom_pull(task_ids='set_variable', key = 'project_path') }} --save-txt --save-conf --conf 0.55  --name {{ ti.xcom_pull(task_ids='set_variable', key = 'folder_name') }} --save-txt --save-conf --conf 0.55
        """,
        params={
            'weight': weight
            }
            )
    
    make_image_list = PythonOperator(
        task_id="make_image_list",
        python_callable=_make_image_list,
        op_kwargs={
            'detected_folder_path': "{{ ti.xcom_pull(task_ids='set_variable', key = 'detected_folder_path') }}"
            }
            )

    make_label_list = PythonOperator(
        task_id="make_label_list",
        python_callable=_make_label_list,
        op_kwargs={
            'detected_folder_path': "{{ ti.xcom_pull(task_ids='set_variable', key = 'detected_folder_path') }}"
            }
            )

    make_empty_file = PythonOperator(
        task_id="make_empty_file",
        python_callable=_make_empty_file,
        op_kwargs={
            'detected_folder_path': "{{ ti.xcom_pull(task_ids='set_variable', key = 'detected_folder_path') }}"
            }
            )

    check_6_pairs = PythonOperator(
        task_id="check_6_pairs",
        python_callable=_check_6_pairs,
        op_kwargs={
            'label_path': "{{ ti.xcom_pull(task_ids='make_empty_file') }}"
            }
            )
    
    make_datasheet = BashOperator(
        task_id="make_datasheet",
        bash_command="""
        cd /home/gnt/yolov5
        python3 datasheet.py --source {{ ti.xcom_pull(task_ids='set_variable', key = 'detected_folder_path') }} --name {{ ti.xcom_pull(task_ids='set_variable', key = 'date') }} --weight {{params.weight}}
        """,
        params={
            'weight': weight
            }
            )
            
    # copy_center_image = PythonOperator(
    #     task_id="copy_center_image",
    #     python_callable=_copy_center_image,
    #     op_kwargs={'date': date,
    #                 'extract_path': "{{ ti.xcom_pull(task_ids='unzip_files') }}",
    #                 'highway_dir' : highway_dir
    #                 }
    #                 )
    
    # convert_to_base64 = PythonOperator(
    #     task_id="convert_to_base64",
    #     python_callable=_convert_to_base64,
    #     op_kwargs={'highway_dir': highway_dir,
    #                 'highway_folder': "{{ti.xcom_pull(task_ids='copy_center_image')}}",
    #                 'date' : date
    #                 }
    #                 )
    
    # LPR_request = BashOperator(
    #     task_id="LPR_request",
    #     bash_command="""
    #     cd /home/gnt/yolov5
    #     sudo python3 request_data.py --date {{ params.date }} --road {{ params.road }}
    #     """,
    #     params={
    #         'date': date,
    #         'road' : road
    #         }
    #         )

    # move_to_subfolder = BashOperator(
    #     task_id="mover_to_subfolder",
    #     bash_command="""
    #     sudo mv /mnt/r/seatbelt/highway_send_data/dp/{{params.date}}_base64 /mnt/r/seatbelt/highway_send_data/dp/{{params.month}}
    #     sudo mv /mnt/r/seatbelt/highway_send_data/dp/{{params.date}}_target /mnt/r/seatbelt/highway_send_data/dp/{{params.month}}
    #     """,
    #     params={
    #         'date': date,
    #         'month' : month
    #         }
    #         )
    
    # update_file_0to6 = PythonOperator(
    #     task_id = "update_file_0to6",
    #     python_callable = _update_file_0to6,
    #     op_kwargs= {
    #         'road' : road,
    #         'month' : month,
    #         'date' : date
    #         }
    #         )

    # update_file_7 = PythonOperator(
    #     task_id = "update_file_7",
    #     python_callable= _update_file_7,
    #     op_kwargs= {
    #         'road' : road,
    #         'month' : month,
    #         'date' : date
    #         }
    #         )
    
    # copy_center_image >> convert_to_base64 >> LPR_request >> move_to_subfolder 
    # move_to_subfolder >> [update_file_0to6, update_file_7]
        
    # make_answersheet_filepath = PythonOperator(
    #     task_id = "make_answersheet_filepath",
    #     python_callable = _make_answersheet_filepath,
    #     op_kwargs= {'detected_folder_path': "{{ ti.xcom_pull(task_ids='make_image_list') }}",
    #                 'date' : date,
    #                 'weight' : weight
    #                 }
    # )

    # answersheet_filesensor = FileSensor(
    #     task_id = "answersheet_filesensor",
    #     filepath=make_answersheet_filepath.output
    # )

    # extract_csv_data_0to6 = PythonOperator(
    #     task_id = "extract_csv_data_0to6",
    #     python_callable = _extract_csv_data_0to6,
    #     op_kwargs= { 'road' : road,
    #                 'month' : month,
    #                 'date' : date,
    #                 'csv_path': "{{ ti.xcom_pull(task_ids='make_answersheet_filepath') }}"
    #                 }
    # )

    # extract_csv_data_7 = PythonOperator(
    #     task_id = "extract_csv_data_7",
    #     python_callable = _extract_csv_data_7,
    #     op_kwargs= { 'road' : road,
    #                 'month' : month,
    #                 'date' : date,
    #                 'csv_path': "{{ ti.xcom_pull(task_ids='make_answersheet_filepath') }}"
    #                 }
    # )
    
    # unzip_files >> [copy_center_image, copy_side_image]
    set_variable >> unzip_files >> copy_side_image >> run_object_detection >>[make_image_list, make_label_list] >> make_empty_file >> check_6_pairs >> make_datasheet
    # copy_center_image >> convert_to_base64 >> LPR_request >> move_to_subfolder >> [update_file_0to6, update_file_7]
    # [update_file_0to6, update_file_7, make_datasheet]>> make_answersheet_filepath >> answersheet_filesensor
    # answersheet_filesensor >> [extract_csv_data_0to6, extract_csv_data_7]
    
