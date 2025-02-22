import os
import pandas as pd

# Directory dove sono salvati gli appunti in formato TXT
APPUNTI_DIR = "./appunti"
OUTPUT_FILE = "dataset_appunti.csv"

def leggi_appunti(directory):
    data = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            filepath = os.path.join(directory, filename)
            with open(filepath, "r", encoding="utf-8") as file:
                contenuto = file.read()
                data.append({
                    "ID": len(data) + 1,
                    "Titolo": filename.replace(".txt", ""),
                    "Contenuto": contenuto,
                    "Data": os.path.getmtime(filepath)
                })
    return data

def salva_dataset(data, output_file):
    df = pd.DataFrame(data)
    df["Data"] = pd.to_datetime(df["Data"], unit='s')
    df.to_csv(output_file, index=False, encoding="utf-8")
    print(f"Dataset salvato in {output_file}")

if __name__ == "__main__":
    appunti_data = leggi_appunti(APPUNTI_DIR)
    salva_dataset(appunti_data, OUTPUT_FILE)
