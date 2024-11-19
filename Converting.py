# file: Converting.py
# description: Converting dicom to png.
# author: María Victoria Anconetani
# date: 23/09/2024

import cv2
import os
import pydicom
import numpy as np

# Input and output directories
inputdir = 'D:/CA EN CMR/raw'
outdir = 'D:/CA EN CMR/convertidas'

for root, dirs, files in os.walk(inputdir):
    relative_path = os.path.relpath(root, inputdir)
    output_dir = os.path.join(outdir, relative_path)
    os.makedirs(output_dir, exist_ok=True)
    
    for file in files:
        file_path = os.path.join(root, file)
        print(f'Processing file: {file_path}') 
        
        try:
            ds = pydicom.dcmread(file_path)  # Read the DICOM file

            # Check if the file contains pixel data
            if hasattr(ds, 'PixelData'):
                img = ds.pixel_array.astype(float)

                # Apply DICOM windowing if available
                intercept = ds.RescaleIntercept if hasattr(ds, 'RescaleIntercept') else 0.0
                slope = ds.RescaleSlope if hasattr(ds, 'RescaleSlope') else 1.0
                img = img * slope + intercept  # Adjust pixel values
                
                if hasattr(ds, 'WindowCenter') and hasattr(ds, 'WindowWidth'):
                    center = ds.WindowCenter if isinstance(ds.WindowCenter, (int, float)) else ds.WindowCenter[0]
                    width = ds.WindowWidth if isinstance(ds.WindowWidth, (int, float)) else ds.WindowWidth[0]
                    img_min = center - width / 2
                    img_max = center + width / 2
                    img = np.clip(img, img_min, img_max)  # Clip to window range
                else:
                    # Normalize to the full range if no windowing is provided
                    img_min, img_max = np.min(img), np.max(img)
                
                # Normalize to 0-255
                img = (img - img_min) / (img_max - img_min) * 255.0
                img = img.astype(np.uint8)  # Convert to 8-bit for saving

                # Save the image as PNG
                output_file = os.path.join(output_dir, file + '.png')
                cv2.imwrite(output_file, img)
                print(f'Saved: {output_file}')
            else:
                print(f'No image data found in DICOM file: {file_path}')
        except Exception as e:
            print(f'Error processing {file_path}: {e}')