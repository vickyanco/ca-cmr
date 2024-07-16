import pydicom
import matplotlib.pyplot as plt
import numpy as np
import os

# DICOM folder path
dicom_folder_path = 'Users/USUARIO/Desktop/51'

# read the DICOM file
dicom = pydicom.dcmread(dicom_folder_path)
for filename in os.listdir(dicom_folder_path):
    if filename.endswith('.dcm'):  
        file_path = os.path.join(dicom_folder_path, filename)
        dicom_data = pydicom.dcmread(file_path)