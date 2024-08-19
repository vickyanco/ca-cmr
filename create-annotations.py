import pandas as pd
import os

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
            if filename.endswith(".dcm"):
                filepath = os.path.join(root, filename)
                label = "positive" if "Pos" in set_type else "negative"
                data.append([filepath, label, set_type])
                print(f"Added: {filepath}, {label}, {set_type}")

# Save to CSV
df = pd.DataFrame(data, columns=["filepath", "label", "set"])
df.to_csv('dicom_files.csv', index=False)
print("CSV file has been created successfully!")