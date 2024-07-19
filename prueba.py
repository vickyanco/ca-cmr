import pydicom
import matplotlib.pyplot as plt
import os
import matplotlib

# Ensure an interactive backend
matplotlib.use('TkAgg')

# Define the folder path containing the DICOM files
folder_path = "C:/Users/USUARIO/Desktop/51"

# Ensure the folder path is correct
print(f"Checking folder: {folder_path}")

# List all files in the folder to verify the folder path
files_in_folder = os.listdir(folder_path)
print(f"Files in folder: {files_in_folder}")

# List to store the DICOM datasets
dicom_datasets = []
        
# Iterate over all files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".dcm"):  # Check if the file is a DICOM file
        file_path = os.path.join(folder_path, filename)
        print(f"Reading file: {file_path}")
        # Read the DICOM file
        dicom_dataset = pydicom.dcmread(file_path)

        # Add it to the list
        dicom_datasets.append(dicom_dataset)
        
        # Get the pixel data (image data)
        image_data = dicom_dataset.pixel_array
        
        print(f"Displaying file: {filename}")

        # Display the image
        plt.figure()
        plt.imshow(image_data, cmap=plt.cm.gray)
        plt.title(f"File: {filename}")
        plt.axis('off')  # Hide the axis
        plt.show(block=False)  # Ensure the call does not block execution
        