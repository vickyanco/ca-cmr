import pydicom
import matplotlib.pyplot as plt
import os

# Define the folder path containing the DICOM files
folder_path = 'C:/Users/USUARIO/Desktop/51'

# List to store the DICOM datasets
dicom_datasets = []
        
# Iterate over all files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".dcm"):  # Check if the file is a DICOM file
        file_path = os.path.join(folder_path, filename)
        # Read the DICOM file
        dicom_dataset = pydicom.dcmread(file_path)

        # Add it to the list
        dicom_datasets.append(dicom_dataset)
        
        # Get the pixel data (image data)
        image_data = dicom_dataset.pixel_array
        
        # Display the image
        plt.imshow(image_data, cmap=plt.cm.gray)
        plt.title(f"File: {filename}")
        plt.show()