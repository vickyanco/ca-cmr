import pydicom
import matplotlib.pyplot as plt
import os
import matplotlib

# Ensure an interactive backend
matplotlib.use('TkAgg')

# Define the folder path containing the DICOMDIR files
folder_path = "C:/Users/USUARIO/Desktop/51"

# Path to the DICOMDIR file
dicomdir_path = os.path.join(folder_path, 'DICOMDIR')

# Read the DICOMDIR file
dicomdir = pydicom.dcmread(dicomdir_path)
        
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
                        # Get the pixel data (image data)
                        image_data = dicom_dataset.pixel_array

                        # Display the image
                        plt.figure()  # Create a new figure for each image
                        plt.imshow(image_data, cmap=plt.cm.gray)
                        plt.title(f"File: {dicom_file_path}")
                        plt.axis('off')  # Hide the axis
                        plt.show(block=False)  # Ensure the call does not block execution
                        plt.pause(1)  # Pause briefly to ensure the plot is rendered
                        plt.close()  # Close the figure after displaying
                    except Exception as e:
                        print(f"Error processing file {dicom_file_path}: {e}")
                else:
                    print(f"No pixel data found in file: {dicom_file_path}")

print("Finished processing files.")