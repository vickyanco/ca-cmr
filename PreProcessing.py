# file: PreProcessing.py
# description: Process DICOM files to feed the CNN
# author: María Victoria Anconetani
# date: 01/08/2024

import pandas as pd
import numpy as np
import pydicom
import torch
import tensorflow as tf
from skimage.transform import resize
from torch.utils.data import Dataset, DataLoader

def preprocess_from_csv(csv_file, img_height=256, img_width=256):
    df = pd.read_csv(csv_file)

    # Initialize lists to hold the processed images and labels
    images = []
    labels = []

    # Loop through each row in the DataFrame
    for index, row in df.iterrows():
        img_path = row['filepath']
        label = row['label']

        # Convert label to 0 or 1
        label = 1 if label.lower() == 'positive' else 0

        # Read and preprocess the DICOM image
        dicom_file = pydicom.dcmread(img_path)
        image = dicom_file.pixel_array

        # Normalize the image
        image = (image - np.min(image)) / (np.max(image) - np.min(image))

        # Resize the image
        image = tf.image.resize(image, [img_height, img_width])

        # Add a channel dimension
        image = tf.expand_dims(image, axis=-1)

        # Append the processed image and label to the lists
        images.append(image)
        labels.append(label)

    return images, labels