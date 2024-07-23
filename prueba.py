import os
import pydicom
import pandas as pd

# Define the folder path containing the DICOMDIR files
folder_path = "C:/Users/USUARIO/Desktop/51"

# Path to the DICOMDIR file
dicomdir_path = os.path.join(folder_path, 'DICOMDIR')

# Read the DICOMDIR file
dicomdir = pydicom.dcmread(dicomdir_path)

# List to store image dimensions
data = []
        
# Iterate over the patient records in the DICOMDIR
for patient_record in dicomdir.patient_records:
    # Iterate over the studies for each patient
    for study_record in patient_record.children:
        # Iterate over the series for each study
        for series_record in study_record.children:
            # Iterate over the images for each series
            for image_record in series_record.children:
                # Get the relative path to the DICOM file
                relative_path = image_record.ReferencedFileID
                # Handle MultiValue by joining the components
                if isinstance(relative_path, pydicom.multival.MultiValue):
                    relative_path = os.path.join(*relative_path)
                else:
                    relative_path = str(relative_path)

                dicom_file_path = os.path.join(folder_path, relative_path)

                # Ensure the path exists
                if not os.path.exists(dicom_file_path):
                    print(f"File not found: {dicom_file_path}")
                    continue

                # Read the DICOM file
                dicom_dataset = pydicom.dcmread(dicom_file_path)

               # Check if pixel data exists
                if hasattr(dicom_dataset, 'pixel_array'):
                    try:
                        # Get the image size
                        rows = dicom_dataset.Rows
                        columns = dicom_dataset.Columns
                        data.append({
                            'File ID': relative_path,
                            'Rows': rows,
                            'Columns': columns
                        })
                    except Exception as e:
                        print(f"Error processing file {dicom_file_path}: {e}")
                else:
                    print(f"No pixel data found in file: {dicom_file_path}")

# Create a DataFrame
df = pd.DataFrame(data)

# Save the DataFrame to an Excel file
output_file_path = os.path.join(folder_path, 'dicom_image_sizes.xlsx')
df.to_excel(output_file_path, index=False)

print(f"Excel file created at: {output_file_path}")
print("Finished processing files.")