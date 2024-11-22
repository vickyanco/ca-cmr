# file: metadata.py
# description: This script reads a DICOM file, extracts its metadata, and saves it to a text file.
# author: María Victoria Anconetani
# date: 22/11/2024

import pydicom
import os
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

ds = pydicom.dcmread('D:/CA EN CMR/1444')

# Specify the folder and file name
output_folder = 'D:/CA EN CMR/'
output_file = os.path.join(output_folder, 'dicom_metadata.txt')

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Print the DICOM metadata to a text file
with open(output_file, 'w') as file:
    print(ds, file=file)