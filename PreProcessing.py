# file: PreProcessing.py
# description: Process DICOM files to feed the CNN
# author: María Victoria Anconetani
# date: 01/08/2024

import pandas as pd
import numpy as np
import pydicom
import tensorflow as tf

def preprocess_from_csv(csv_file, subset, img_height=256, img_width=256):
    # Load the CSV file
    df = pd.read_csv(csv_file)

    # Filter the dataframe based on the 'set' column
    df_subset = df[df['set'] == subset]

    # Initialize lists to hold the processed images and labels
    images = []
    labels = []

    # Loop through each row in the DataFrame
    for _, row in df_subset.iterrows():
        img_path = row['filepath']
        label = 1 if row['label'] == 'positive' else 0

        # Read and preprocess the DICOM image
        dicom_file = pydicom.dcmread(img_path)
        image = dicom_file.pixel_array

        # Check if the image is multi-frame (i.e., has more than 2 dimensions)
        if image.ndim == 3:
            # Select the first frame
            image = image[0]
            print(f"Multi-frame image detected. Using the first frame: {image.shape}")

        # Normalize the image
        image = (image - tf.reduce_min(image)) / (tf.reduce_max(image) - tf.reduce_min(image))

        # Add a channel dimension
        image = tf.expand_dims(image, axis=-1)

        # Resize the image
        image = tf.image.resize(image, [img_height, img_width])

        # Ensure consistent shape
        print(f"Processed image shape: {image.shape}")

        # Append the processed image and label to the lists
        images.append(image.numpy()) # Convert TensorFlow tensor to NumPy array
        labels.append(label)

    # Convert the list of images to a stacked tensor or array
    images_np = np.stack(images, axis=0)  # Ensures all images are combined correctly
    labels_np = np.array(labels)

    return images_np, labels_np