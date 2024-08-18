import csv
import os

# Define the base directories
base_dirs = {
    "Train": ["D:/CA EN CMR/input/Train/PosTrain", "D:/CA EN CMR/input/Train/NegTrain"],
    "Val": ["D:/CA EN CMR/input/Val/PosVal", "D:/CA EN CMR/input/Val/NegVal"],
    "Test": ["D:/CA EN CMR/input/Test/PosTest", "D:/CA EN CMR/input/Test/NegTest"]
}

# Create a CSV file to document the paths
with open('dicom_paths.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["filepath", "label", "set"])

    # Iterate over each base directory
    for set_type, paths in base_dirs.items():
        for base_dir in paths:
            label = "positive" if "Pos" in base_dir else "negative"
            # Walk through the directory tree
            for root, dirs, files in os.walk(base_dir):
                for filename in files:
                    if filename.endswith(".dcm"):
                        filepath = os.path.join(root, filename)
                        writer.writerow([filepath, label, set_type])
print("CSV file successfully created.")
