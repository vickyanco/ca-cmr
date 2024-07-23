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

# Counter for patient numbers
patient_number = 1

# Iterate over the patient records in the DICOMDIR
for patient_record in dicomdir.patient_records:
    current_patient_number = patient_number
    print(f"Processing Patient {current_patient_number}")

    # Check patient name or ID to ensure we're iterating correctly
    print(f"Patient Record: {patient_record.PatientID if 'PatientID' in patient_record else 'Unknown ID'}")

    # Iterate over the studies for each patient
    for study_record in patient_record.children:
        # Check study details
        print(f"  Study: {study_record.StudyID if 'StudyID' in study_record else 'Unknown Study ID'}")

        # Iterate over the series for each study
        for series_record in study_record.children:
            # Check series details
            print(f"    Series: {series_record.SeriesNumber if 'SeriesNumber' in series_record else 'Unknown Series Number'}")

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
                    print(f"      File not found: {dicom_file_path}")
                    continue

                # Read the DICOM file
                try:
                    dicom_dataset = pydicom.dcmread(dicom_file_path)
                except Exception as e:
                    print(f"      Error reading file {dicom_file_path}: {e}")
                    continue

                # Check if pixel data exists
                if hasattr(dicom_dataset, 'pixel_array'):
                    try:
                        # Get the image size
                        rows = dicom_dataset.Rows
                        columns = dicom_dataset.Columns
                        data.append({
                            'Patient Number': current_patient_number,
                            'File ID': relative_path,
                            'Rows': rows,
                            'Columns': columns
                        })
                        print(f"      Added image {relative_path} with size ({rows}x{columns})")
                    except Exception as e:
                        print(f"      Error processing pixel data in file {dicom_file_path}: {e}")
                else:
                    print(f"      No pixel data found in file: {dicom_file_path}")

    patient_number += 1

# Create a DataFrame
df = pd.DataFrame(data)

# Group by patient number
grouped = df.groupby('Patient Number')

# Save the DataFrame to an Excel file
output_file_path = os.path.join(folder_path, 'dicom_image_sizes_grouped_by_patient.xlsx')
with pd.ExcelWriter(output_file_path, engine='openpyxl') as writer:
    for patient_number, group in grouped:
        sheet_name = f"Patient_{patient_number}"
        group.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"Excel file created at: {output_file_path}")
print("Finished processing files.")