import pandas as pd
import numpy as np
import pydicom
import os
import matplotlib.pyplot as plt
from skimage.transform import resize

# Read the CSV file
csv_path = 'valid_dicom_files.csv'
df = pd.read_csv(csv_path)

# Define the path to your CSV and the output directory
output_dir = 'resized_images'

# Desired size for resizing
new_size = (256, 256)

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Iterate through the paths and resize images
for idx, row in df.iterrows():
    img_path = row['filepath']
    
    # Read the DICOM file
    dicom_file = pydicom.dcmread(img_path)
    image = dicom_file.pixel_array
    
    # Normalize the image if needed
    image = (image - np.min(image)) / (np.max(image) - np.min(image))
    
    # Resize the image
    resized_image = resize(image, new_size, anti_aliasing=True)
    
    # Save the resized image as a .npy file
    output_file = os.path.join(output_dir, f"resized_image_{idx}.npy")
    np.save(output_file, resized_image)
    
    print(f"Saved resized image to {output_file}")

print("All images have been resized and saved.")