# file: Converting.py
# description: Converting dicom to png.
# author: María Victoria Anconetani
# date: 23/09/2024

import cv2
import os
import pydicom

inputdir = 'D:/CA EN CMR/raw'
outdir = 'D:/CA EN CMR/convertidas'

for root, dirs, files in os.walk(inputdir):
    relative_path = os.path.relpath(root, inputdir)
    output_dir = os.path.join(outdir, relative_path)
    os.makedirs(output_dir, exist_ok=True)
    
    for file in files:
        file_path = os.path.join(root, file)
        print(f'Processing file: {file_path}') 
        ds = pydicom.dcmread(file_path)  
        img = ds.pixel_array  
        output_file = os.path.join(output_dir, file.replace('.dcm', '.png')) 
        cv2.imwrite(output_file, img)
        print(f'Saved: {output_file}')
