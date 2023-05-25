import cv2
import urllib.request
import numpy as np
import easyocr
import pandas as pd
import time

reader = easyocr.Reader(['en'], gpu=False)

def download_image(url):
    req = urllib.request.urlopen(url)
    image_data = np.asarray(bytearray(req.read()), dtype=np.uint8)
    image = cv2.imdecode(image_data, -1)
    return image

def readtext_from_images(csv_path, img_col):
    df = pd.read_csv(csv_path)
    final_df = pd.DataFrame(columns=['id','URL','text','confidence'])

    for index, row in df.iterrows():
        if index >=100:
            break
        start_time = time.time()
        img_path = row[img_col]
        try:
            image = download_image(img_path)
            reader_op = reader.readtext(image)
            reader_text = [op[1] for op in reader_op]
            reader_conf = [op[2] for op in reader_op]
            temp_df = pd.DataFrame({'id':index,'URL':img_path, 'text':reader_text,'confidence':reader_conf})
            final_df = pd.concat([final_df,temp_df], ignore_index=True)
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Completed row {index} in {elapsed_time:.2f} seconds")
        except Exception as e:
            print(f"Error processing image {index}: {str(e)}")
    final_df.to_csv("final_df.csv", index=False)


csv_path = 'drone_images.csv'  # Replace with the path to your CSV file
img_col = 'Img URL'  # Replace with the name of the column containing image paths

readtext_from_images(csv_path, img_col)