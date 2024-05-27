import os
import glob
import numpy as np

def convert_labels_to_yolo_format(folder_path, img_width, img_height):
    # Loop over all the label files in the folder
    for file_path in glob.glob(os.path.join(folder_path, "*.txt")):
        # Read the anchor boxes from the label file
        with open(file_path, "r") as f:
            anchor_boxes = [list(map(float, line.strip().split())) for line in f]

        # Convert the anchor boxes to YOLO format
        yolo_boxes = []
        for anchor_box in anchor_boxes:
            scale_factor, x1, y1, x2, y2, x3, y3, x4, y4 = anchor_box

            # Calculate the center coordinates and dimensions
            center_x = (x1 + x3) / 2
            center_y = (y1 + y3) / 2
            box_width = x3 - x1
            box_height = y3 - y1

            # Scale the center coordinates and dimensions to be relative to the image size
            center_x /= img_width
            center_y /= img_height
            box_width /= img_width
            box_height /= img_height

            # Find the class index based on the scale factor
            class_index = int(scale_factor)

            # Concatenate the YOLO-format box
            yolo_box = [class_index, center_x, center_y, box_width, box_height]
            yolo_boxes.append(yolo_box)

        # Write the YOLO-format boxes to a new label file
        yolo_file_path = os.path.splitext(file_path)[0] + "_yolo.txt"
        with open(yolo_file_path, "w") as f:
            for yolo_box in yolo_boxes:
                f.write(" ".join(str(x) for x in yolo_box) + "\n")



convert_labels_to_yolo_format("S:/98.기타/승렬학생/dacon/convert_test_sample", 1920, 1040)
