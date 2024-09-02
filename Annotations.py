# file: create-annotations.py
# description: Creats a CSV file with all the paths.
# author: María Victoria Anconetani
# date: 20/07/2024

import pandas as pd
import os
import pydicom

# Define the base directories
base_dirs = ["D:/CA EN CMR/input/Train/PosTrain", 
             "D:/CA EN CMR/input/Train/NegTrain",
             "D:/CA EN CMR/input/Validation/PosVal", 
             "D:/CA EN CMR/input/Validation/NegVal",
             "D:/CA EN CMR/input/Test/PosTest", 
             "D:/CA EN CMR/input/Test/NegTest"]

data = []

for base_dir in base_dirs:
    set_type = os.path.basename(base_dir)  # Extracts PosTrain, NegTrain, etc.
    print(f"Processing base directory: {base_dir}")
    for root, dirs, files in os.walk(base_dir):
        for filename in files:
            if filename != "DICOMDIR":  # Exclude files named 'DICOMDIR'
                filepath = os.path.join(root, filename)
                try:
                    # Attempt to read the DICOM file
                    dicom_file = pydicom.dcmread(filepath)

                    # Check if the DICOM file contains pixel data
                    if hasattr(dicom_file, 'PixelData'):
                        label = "positive" if "Pos" in set_type else "negative"
                        data.append([filepath, label, set_type])
                        print(f"Added: {filepath}, {label}, {set_type}")
                    else:
                        print(f"No pixel data found in {filepath}")

                except Exception as e:
                    print(f"Could not read DICOM file {filepath}: {e}")

# Save to CSV
df = pd.DataFrame(data, columns=["filepath", "label", "set"])
df.to_csv('valid_dicom_files.csv', index=False)
print("CSV file has been created successfully!")