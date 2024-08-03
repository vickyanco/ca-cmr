import os
import pydicom
import pandas as pd

# Define the folder path containing the DICOMDIR files
folder_path = "C:/Users/USUARIO/Desktop/51"

# Path to the DICOMDIR file
dicomdir_path = os.path.join(folder_path, 'DICOMDIR')

# Read the DICOMDIR file
dicomdir = pydicom.dcmread(dicomdir_path)

# List to store image data
data = []

# Function to read DICOM files and extract pixel data
def read_dicom_files(dicomdir):
    for root, dirs, files in os.walk(dicomdir):
        for file in files:
            if file.endswith(".dcm"):
                dicom_file_path = os.path.join(root, file)
                try:
                    dicom_dataset = pydicom.dcmread(dicom_file_path)
                    print(f"Reading file: {dicom_file_path}")
                    if hasattr(dicom_dataset, 'pixel_array'):
                        image_data = dicom_dataset.pixel_array
                        rows = dicom_dataset.Rows
                        columns = dicom_dataset.Columns
                        data.append({
                            'File ID': dicom_file_path,
                            'Rows': rows,
                            'Columns': columns
                        })
                        print(f"Added data for file: {dicom_file_path}")
                    else:
                        print(f"No pixel data found in file: {dicom_file_path}")
                except Exception as e:
                    print(f"Error reading file {dicom_file_path}: {e}")

# Read DICOM files and extract image data
read_dicom_files(folder_path)

# Create a DataFrame from the collected data
df = pd.DataFrame(data)

# Save the DataFrame to an Excel file
output_excel_path = "C:/Users/USUARIO/Desktop/resul/dicom_image_data.xlsx"
df.to_excel(output_excel_path, index=False)

print(f"Extracted data saved to {output_excel_path}")