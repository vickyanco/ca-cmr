import os
import csv

# Definir las rutas de las carpetas
base_dirs = {
    "posTrain": "D:/CA EN CMR/input/Train/PosTrain",
    "negTrain": "D:/CA EN CMR/input/Train/NegTrain",
    "posVal": "D:/CA EN CMR/input/Validation/PosVal",
    "negVal": "D:/CA EN CMR/input/Validation/NegVal",
    "posTest": "D:/CA EN CMR/input/Test/PosTest",
    "negTest": "D:/CA EN CMR/input/Test/NegTest"
}

# Nombre del archivo CSV de salida
output_csv = "dicom_files.csv"

# Abrir el archivo CSV para escritura
with open(output_csv, mode='w', newline='') as file:
    writer = csv.writer(file)
    
    # Escribir la cabecera del CSV
    writer.writerow(["filepath", "label", "set"])

    # Recorrer cada carpeta
    for label, base_dir in base_dirs.items():
        set_type = base_dir.split('/')[-1]  # train, val o test
        
        for root, _, files in os.walk(base_dir):
            for filename in files:
                if filename.endswith(".dcm"):  # Solo procesar archivos DICOM
                    filepath = os.path.join(root, filename)
                    
                    # Escribir la información en el CSV
                    writer.writerow([filepath, "positive" if "pos" in label else "negative", set_type])

print("CSV generado con éxito:", output_csv)


