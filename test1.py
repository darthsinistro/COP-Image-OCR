import cv2
import urllib.request
import numpy as np
import random
import easyocr
import csv
import pandas as pd

reader = easyocr.Reader(['en'], gpu=False)

def download_image(url):
    req = urllib.request.urlopen(url)
    image_data = np.asarray(bytearray(req.read()), dtype=np.uint8)
    image = cv2.imdecode(image_data, -1)
    return image

def display_images(url_list):
    global reader
    random.seed(42)
    random.shuffle(url_list)

    current_image_index = 0
    total_images = len(url_list)
    
    while True:
        # Download and display the current image
        current_url = url_list[current_image_index]
        current_image = download_image(current_url)
        print(reader.readtext(current_image, detail=0))
        resized_image = cv2.resize(current_image, None, fx=0.2, fy=0.2)
        cv2.imshow('Image Viewer', resized_image)
        
        key = cv2.waitKey(0)
        
        if key == ord('d'):  # Move to the next image
            current_image_index = (current_image_index + 1) % total_images
        elif key == ord('a'):  # Move to the previous image
            current_image_index = (current_image_index - 1) % total_images
        elif key == ord('q'):  # Exit the program
            break
    
    cv2.destroyAllWindows()

def read_csv_column(csv_file, column_name):
    values = []

    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            value = row.get(column_name)
            if value:
                values.append(value)

    return values

# Example usage
csv_file = 'drone_images.csv'  # Replace with the path to your CSV file
column_name = 'Img URL'

# url_list = read_csv_column(csv_file, column_name)

# Call the display_images function
# display_images(url_list)

def readtext_from_images(csv_path, img_col, new_col):
    df = pd.read_csv(csv_path)
    image_values = df[img_col].tolist()
    text_values = []

    for img_path in image_values:
        try:
            image = download_image(img_path)
            text = reader.readtext(image, detail=0)
            conc_text = ' '.join(text)
            text_values.append(conc_text)
        except Exception as e:
            print(f"Error processing image {img_path}: {str(e)}")
            text_values.append("")

    df[new_col] = text_values
    df.to_csv(csv_path, index=False)


# Example usage
csv_path = 'drone_images.csv'  # Replace with the path to your CSV file
img_col = 'Img URL'  # Replace with the name of the column containing image paths
new_col = 'Text'  # Replace with the desired name for the new column

readtext_from_images(csv_path, img_col, new_col)