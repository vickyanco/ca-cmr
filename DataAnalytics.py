# file: DataAnalytics.py
# description: This script performs data analytics on CMR images, including loading DICOM files, extracting image data, calculating areas of regions of interest, and visualizing images.
# author: María Victoria Anconetani
# date: 21
# 21/11/2024

import os
import numpy as np
import pydicom
import matplotlib.pyplot as plt
from scipy.ndimage import measurements

def load_dicom_files(directory):
    """
    Load all DICOM files from a given directory.
    """
    dicom_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.dcm'):
                dicom_files.append(os.path.join(root, file))
    return dicom_files

def extract_image_data(dicom_files):
    """
    Extract pixel data and metadata from DICOM files.
    """
    images = []
    metadata = []
    for dicom_file in dicom_files:
        dicom = pydicom.dcmread(dicom_file)
        images.append(dicom.pixel_array)
        metadata.append(dicom)
    return images, metadata

def calculate_areas(images, pixel_spacing):
    """
    Calculate the area of regions of interest in the images.
    """
    areas = []
    for img in images:
        binary_mask = img > np.percentile(img, 90)  # Thresholding (adjust as needed)
        area = np.sum(binary_mask) * (pixel_spacing[0] * pixel_spacing[1])
        areas.append(area)
    return areas

def visualize_images(images, num_images=5):
    """
    Visualize a subset of the images.
    """
    plt.figure(figsize=(10, 10))
    for i, img in enumerate(images[:num_images]):
        plt.subplot(1, num_images, i + 1)
        plt.imshow(img, cmap='gray')
        plt.axis('off')
    plt.show()

def main(cmr_directory):
    """
    Main function to perform data analytics on CMR images.
    """
    # Load DICOM files
    dicom_files = load_dicom_files(cmr_directory)
    if not dicom_files:
        print("No DICOM files found in the specified directory.")
        return

    # Extract image data and metadata
    images, metadata = extract_image_data(dicom_files)

    # Check pixel spacing for area calculations
    pixel_spacing = metadata[0].PixelSpacing if hasattr(metadata[0], 'PixelSpacing') else [1.0, 1.0]

    # Visualize a subset of images
    visualize_images(images)

    # Calculate areas of regions of interest
    areas = calculate_areas(images, pixel_spacing)
    for i, area in enumerate(areas[:5]):  # Show first 5 results
        print(f"Image {i + 1}: Calculated area = {area:.2f} mm²")

if __name__ == "__main__":
    # Replace with the directory containing your DICOM files
    cmr_directory = "path/to/cmr/dicom/files"
    main(cmr_directory)
