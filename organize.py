# file: organize.py
# description: Errasing unnecessary files.
# author: María Victoria Anconetani
# date: 19/11/2024

import os
import shutil

# Define the root directory and the desired folder names
root_dir = 'D:/CA EN CMR/convertidas'
desired_folders = {'casos', 'controles'}

for folder in desired_folders:
    folder_path = os.path.join(root_dir, folder)
    
    # Skip files or folders not in the desired list
    if not os.path.isdir(folder_path) or folder not in desired_folders:
        continue
    
    # Process only 'casos' and 'controles'
    for patient_folder in os.listdir(folder_path):
        patient_path = os.path.join(folder_path, patient_folder)
        
        # Ensure this is a patient folder
        if not os.path.isdir(patient_path):
            continue
        
        # Traverse through subfolders in the patient folder
        for root, dirs, files in os.walk(patient_path, topdown=False):
            # Move files to the patient folder
            for file in files:
                file_path = os.path.join(root, file)
                target_path = os.path.join(patient_path, file)  # Move to the patient folder
                shutil.move(file_path, target_path)
                print(f'Moved: {file_path} -> {target_path}')
            
            # Remove empty subfolders
            for sub_dir in dirs:
                sub_dir_path = os.path.join(root, sub_dir)
                try:
                    os.rmdir(sub_dir_path)
                    print(f'Removed empty folder: {sub_dir_path}')
                except OSError:
                    print(f'Could not remove folder (not empty): {sub_dir_path}')
